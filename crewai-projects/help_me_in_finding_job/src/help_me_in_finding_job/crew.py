from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import FileReadTool, ScrapeWebsiteTool, PDFSearchTool, SerperDevTool
from crewai.agents.agent_builder.base_agent import BaseAgent
from src.help_me_in_finding_job.tools.custom_tool import PWScrapeWebsite
from typing import List
from pathlib import Path
import os

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators


@CrewBase
class HelpMeInFindingJob:
    """HelpMeInFindingJob crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    llm = LLM(model=os.getenv("MODEL", ""), api_base=os.getenv("API_BASE", ""))
    print(f"Using LLM model: {os.getenv('MODEL', '')} with API base: {os.getenv('API_BASE', 'http://localhost:11434')}")
    
    search_tool: SerperDevTool = SerperDevTool()
    scrape_website_tool: ScrapeWebsiteTool = ScrapeWebsiteTool() 
    playwright_scrape_tool: PWScrapeWebsite = PWScrapeWebsite()
    
    RESUME_PDF_ENV = os.getenv("RESUME_PDF", "Akhil_Deshneni_Resume.pdf") 
    BASE_DIR = Path(__file__).resolve().parent 
    resume_path = Path(RESUME_PDF_ENV)

    if not resume_path.is_absolute():
        resume_path = BASE_DIR / resume_path

    print(f"Using resume PDF at: {resume_path}")
    
    if not resume_path.exists():
        raise RuntimeError(
            f"Resume PDF not found at: {resume_path}\n"
            "Place the file there, or set RESUME_PDF to an absolute path, e.g.:\n"
            "export RESUME_PDF=/full/path/to/Akhil_Deshneni_Resume.pdf"
        )
   
    file_read_tool: FileReadTool = FileReadTool(file_path=str(resume_path))
    pdf_search_tool: PDFSearchTool = PDFSearchTool(
        pdf=str(resume_path),
        config=dict(
            llm=dict(
                provider="ollama",
                config=dict(
                    model="gpt-oss:20b",
                    base_url="http://localhost:11434",
                ),
            ),
            embedder = dict(
                provider= "ollama",
                config = dict(
                    model = "mxbai-embed-large"
                )
            )
        ),
    )

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended

    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config["researcher"],  # type: ignore[index]
            verbose=True,
            tools=[self.search_tool, self.scrape_website_tool, self.playwright_scrape_tool],
            llm=self.llm,
        )

    @agent
    def profiler(self) -> Agent:
        return Agent(
            config=self.agents_config["profiler"],  # type: ignore[index]
            verbose=True,
            tools=[
                self.file_read_tool,
                # self.pdf_search_tool,
                self.search_tool,
                self.scrape_website_tool,
                self.playwright_scrape_tool,
            ],
            llm=self.llm,
        )

    @agent
    def resume_strategist(self) -> Agent:
        return Agent(
            config=self.agents_config["resume_strategist"],  # type: ignore[index]
            verbose=True,
            tools=[
                self.file_read_tool,
                # self.pdf_search_tool,
                self.search_tool,
                self.scrape_website_tool,
            ],
            llm=self.llm,
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config["research_task"],  # type: ignore[index]
            async_execution=True,
        )

    @task
    def profile_task(self) -> Task:
        return Task(
            config=self.tasks_config["profile_task"],  # type: ignore[index]
            async_execution=True,
        )

    @task
    def resume_strategy_task(self) -> Task:
        return Task(
            config=self.tasks_config["resume_strategy_task"],  # type: ignore[index]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the HelpMeInFindingJob crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            memory=False,
            embedder={
                'provider': 'ollama',
                "config": {
                    "model" : "mxbai-embed-large",
                    "api_base": "http://localhost:11434/api/embed"
                }
            },
        )
