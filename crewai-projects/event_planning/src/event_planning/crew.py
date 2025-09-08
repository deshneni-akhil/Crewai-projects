from crewai import Agent, Crew, Process, Task, LLM
from crewai_tools import ScrapeWebsiteTool, SerperDevTool
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from src.event_planning.validators.model_validators import VenueDetails
import os

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class EventPlanning():
    """EventPlanning crew"""

    agents: List[BaseAgent]
    tasks: List[Task]
    search_tool: SerperDevTool = SerperDevTool()
    scrape_tool: ScrapeWebsiteTool = ScrapeWebsiteTool()
    
    llm = LLM(model=os.getenv("MODEL",""), base_url=os.getenv("API_BASE"))

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def venue_coordinator(self) -> Agent:
        return Agent(
            config=self.agents_config['venue_coordinator'], # type: ignore[index]
            verbose=True,
            tools=[self.search_tool, self.scrape_tool]
        )

    @agent
    def logistics_manager(self) -> Agent:
        return Agent(
            config=self.agents_config['logistics_manager'], # type: ignore[index]
            verbose=True,
            tools=[self.scrape_tool, self.search_tool]
        )

    @agent 
    def marketing_communications_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['marketing_communications_agent'], # type: ignore[index]
            verbose=True,
            tools=[self.search_tool, self.scrape_tool]
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def venue_task(self) -> Task:
        return Task(
            config=self.tasks_config['venue_task'], # type: ignore[index]
            human_input=True,
            output_json=VenueDetails,
            output_file='venue_details.json'
        )

    @task
    def logistics_task(self) -> Task:
        return Task(
            config=self.tasks_config['logistics_task'], # type: ignore[index]
            human_input=True,
            async_execution=True
        )

    @task
    def marketing_task(self) -> Task:
        return Task(
            config=self.tasks_config['marketing_task'], # type: ignore[index]
            output_file='marketing_report.md',
            async_execution=False
        )

    @crew
    def crew(self) -> Crew:
        """Creates the EventPlanning crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            manager_llm=self.llm
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
