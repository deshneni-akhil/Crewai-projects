#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from help_me_in_finding_job.crew import HelpMeInFindingJob

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    inputs = {
        'job_posting_url': 'https://jobs.careers.microsoft.com/global/en/job/1872630/Software-Engineer',
        'github_url': 'https://github.com/deshneni-akhil',
        'personal_writeup': """Akhil Deshneni is a software engineer and architects 0-to-1 solutions designed for performance and scale. Using Java and Python, I apply strategic design and algorithmic thinking to build cost-efficient, data-intensive systems. I own complex challenges end-to-end, delivering backend services that are robust and reliable at massive scale."""
    }
    
    try:
        HelpMeInFindingJob().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs",
        'current_year': str(datetime.now().year)
    }
    try:
        HelpMeInFindingJob().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        HelpMeInFindingJob().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs",
        "current_year": str(datetime.now().year)
    }
    
    try:
        HelpMeInFindingJob().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
