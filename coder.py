from openai import OpenAI
from dotenv import load_dotenv
import os

"""Make a call to OpenAI API to generate code based on the requirement"""
def generate_tool_code(requirement: str)->str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"));

