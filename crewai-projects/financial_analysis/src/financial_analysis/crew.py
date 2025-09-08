from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task 
from crewai_tools import ScrapeWebsiteTool, SerperDevTool
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
import os
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class FinancialAnalysis():
    """FinancialAnalysis crew"""

    agents: List[BaseAgent]
    tasks: List[Task]
    search_tool: SerperDevTool = SerperDevTool()
    web_scrape_tool: ScrapeWebsiteTool = ScrapeWebsiteTool()
    llm = LLM(model=os.getenv("MODEL",""), api_base=os.getenv("API_BASE"))

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def data_analyst_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['data_analyst_agent'], # type: ignore[index]
            verbose=True,
            allow_delegation=True, 
            tools=[self.search_tool, self.web_scrape_tool],
            llm=self.llm
        )

    @agent
    def trading_strategy_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['trading_strategy_agent'], # type: ignore[index]
            verbose=True,
            tools=[self.search_tool, self.web_scrape_tool],
            allow_delegation=True,
            llm=self.llm
        )
    
    @agent 
    def execution_planning_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['execution_planning_agent'], # type: ignore[index]
            verbose=True,
            tools=[self.search_tool, self.web_scrape_tool],
            allow_delegation=True,
            llm=self.llm
        )

    @agent
    def risk_assesment_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['risk_assesment_agent'], # type: ignore[index]
            verbose=True,
            tools=[self.search_tool, self.web_scrape_tool],
            allow_delegation=True,
            llm=self.llm
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def data_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['data_analysis_task'], # type: ignore[index]
        )
    
    @task
    def trading_strategy_task(self) -> Task:
        return Task(
            config=self.tasks_config['trading_strategy_task'], # type: ignore[index]
        )

    @task 
    def execution_planning_task(self) -> Task:
        return Task(
            config=self.tasks_config['execution_planning_task'], # type: ignore[index]
        )

    @task 
    def risk_assessment_task(self) -> Task:
        return Task(
            config=self.tasks_config['risk_assessment_task'], # type: ignore[index]
        )


    @crew
    def crew(self) -> Crew:
        """Creates the FinancialAnalysis crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.hierarchical,
            manager_llm=self.llm,
            verbose=True,
            memory=True,
            embedder={
                'provider': 'ollama',
                "config": {
                    "model" : "mxbai-embed-large",
                    "api_base": "http://localhost:11434/api/embed"
                }
            }
        )
