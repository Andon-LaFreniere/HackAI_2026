from openai import OpenAI

"""Make a call to OpenAI API to generate code based on the requirement"""
def generate_tool_code(requirement: str)->str:
    client = OpenAI();

