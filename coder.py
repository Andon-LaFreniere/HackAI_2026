# import gpt and environment and operating system controls
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load variables from .env
load_dotenv()

def generate_tool_code(requirement: str) -> str:
    # Attempt to load API key
    api_key = os.getenv("OPENAI_API_KEY")

    # Create OpenAI client
    client = OpenAI(api_key=api_key)
    
    # Try to send the requirement to the model
    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=requirement
        )

        return response.output_text

    except Exception as e:
        print("API call failed.")
        print("Error:", e)
        return ""