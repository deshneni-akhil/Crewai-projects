from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task, before_kickoff
from crewai_tools import ScrapeWebsiteTool
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
import os
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators


@before_kickoff
def before_crew_start(inputs: dict):
    print("Crew is starting with inputs:", inputs)


@CrewBase
class CustomerSupport:
    """CustomterSupport crew"""
    agents: List[BaseAgent]
    tasks: List[Task]
    llm = LLM(
        model=os.getenv("MODEL", "ollama/llama3.1:latest"),
        temperature=0.7,
        base_url=os.getenv("API_BASE", "http://localhost:11434"),
    )
    print(f"Using LLM model: {llm.model} from {llm.base_url}")

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended

    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def support_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["support_agent"],  # type: ignore[index]
            allow_delegation=False,
            verbose=True,
            llm=self.llm,
        )

    @agent
    def support_quality_assurance_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["support_quality_assurance_agent"],  # type: ignore[index]
            allow_delegation=True,
            verbose=True,
            llm=self.llm,
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def support_agent_task(self) -> Task:
        docs_scrape_tool = ScrapeWebsiteTool(
            website_url="https://docs.crewai.com/how-to/Creating-a-Crew-and-kick-it-off/"
        )
        return Task(
            config=self.tasks_config["support_task"],  # type: ignore[index]
            tools=[docs_scrape_tool],
        )

    @task
    def support_quality_assurance_agent_task(self) -> Task:
        return Task(
            config=self.tasks_config["support_quality_assurance_task"],  # type: ignore[index]
            output_file="report.md",
        )

    @crew
    def crew(self) -> Crew:
        """Creates the CustomerSupport crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # right now, memory implementation is tricky with ollama
            # memory=True,
            # embedder={
            #     'provider': 'ollama',
            #     'config': {
            #         'model': 'embeddinggemma:latest',
            #         'api_base': os.getenv("API_BASE", "http://localhost:11434")
            #     }
            # },
            planning_llm=self.llm,
            cache=True,
        )
