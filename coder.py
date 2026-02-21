# import gpt and environment and operating system controls
from openai import OpenAI
from dotenv import load_dotenv
import os
from prompts import CODER_SYSTEM_PROMPT

# Load variables from .env
load_dotenv()

def generate_tool_code(requirement: str) -> str:
    # Attempt to load API key
    api_key = os.getenv("OPENAI_API_KEY")

    # Create OpenAI client
    client = OpenAI(api_key=api_key)
    
    # Try to send the requirement to the model
    try:
        response = client.chat.completions.create(
            model="gpt-4o", 
            messages=[
                {"role": "system", "content": CODER_SYSTEM_PROMPT},
                {"role": "user", "content": f"Task: {requirement}"}
            ],
            temperature=0.2,
        )
    
        code = response.choices[0].message.content

        # Clean up markdown artifacts if the LLM ignores the 'no markdown' instruction
        if "```python" in code:
            code = code.split("```python")[1].split("```")[0]
        
        return code.strip()

    except Exception as e:
        print("API call failed.")
        print("Error:", e)
        return ""
