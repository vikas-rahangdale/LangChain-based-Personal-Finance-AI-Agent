import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from tools import calculator, emi_calculator, sip_calculator, budget_planner

def create_personal_agent():
    # Load environment variables
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")

    # Initialize LLM
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.0,
        api_key=api_key
    )

    # Register finance tools
    tools = [
        calculator,
        emi_calculator,
        sip_calculator,
        budget_planner
    ]

    # Create agent with custom system prompt
    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt="""
        You are a Smart Personal Finance Assistant.

        Rules:
        - Use Calculator tool for general math (percentages, ratios).
        - Use EMI Calculator tool for loan EMI queries.
        - Use SIP Calculator tool for investment return queries.
        - Use Budget Planner tool for income allocation queries.
        - Always respond clearly, concisely, and with structured output.
        - don't make up numbers; if unsure, ask for clarification.
        - don't show meta data or tool names in your responses.
        - Keep answers user-friendly and avoid unnecessary jargon.
        """
    )

    return agent
