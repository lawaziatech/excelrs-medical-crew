from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from mycrewapp.tools import PractoTool, AskUserTool

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class Mycrewapp():
    """Mycrewapp crew - Health Bot System"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def inquiry_agent(self) -> Agent:
        """Health Inquiry Bot powered by Gemini - asks questions to understand patient concerns"""
        return Agent(
            config=self.agents_config['inquiry_agent'], # type: ignore[index]
            tools=[AskUserTool()],  # Ask the user
            verbose=True,
            allow_delegation=False
        )

    @agent
    def advisor_agent(self) -> Agent:
        """Health Advice Bot powered by GPT-4 - provides advice and coordinates consultations"""
        return Agent(
            config=self.agents_config['advisor_agent'], # type: ignore[index]
            tools=[PractoTool()],  # Can book consultations
            verbose=True,
            allow_delegation=False
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def inquiry_task(self) -> Task:
        """Task for inquiry agent to gather patient information"""
        return Task(
            config=self.tasks_config['inquiry_task'], # type: ignore[index]
        )

    @task
    def advice_task(self) -> Task:
        """Task for advisor agent to provide health advice and coordinate actions"""
        return Task(
            config=self.tasks_config['advice_task'], # type: ignore[index]
            output_file='health_report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Mycrewapp crew - Health Management System"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,  # Sequential: inquiry agent -> advisor agent
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
