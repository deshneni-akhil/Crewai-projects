#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from event_planning.crew import EventPlanning

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
        'event_topic': "Tech Innovation Conference",
        'event_description': "A gathering of tech innovators "
                            "and industry leaders "
                            "to explore future technologies.",
        'event_city': "San Francisco",
        'tentative_date': datetime.now().strftime("%Y-%m-%d"),
        'expected_participants': 500,
        'budget': 20000,
        'venue_type': "Conference Hall"
    }
    
    try:
        EventPlanning().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        'event_topic': "Tech Innovation Conference",
        'event_description': "A gathering of tech innovators "
                            "and industry leaders "
                            "to explore future technologies.",
        'event_city': "San Francisco",
        'tentative_date': "2024-09-15",
        'expected_participants': 500,
        'budget': 20000,
        'venue_type': "Conference Hall"
    }
    try:
        EventPlanning().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        EventPlanning().crew().replay(task_id=sys.argv[1])

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
        EventPlanning().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
