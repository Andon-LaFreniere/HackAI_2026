# depends: requests, beautifulsoup4
from fastmcp import FastMCP
import requests
from bs4 import BeautifulSoup

mcp = FastMCP("GeneratedTool")

@mcp.tool()
def fetch_html_content(url: str) -> str:
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        return f"Error fetching URL: {e}"

@mcp.tool()
def extract_titles_from_html(html_content: str) -> list:
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        titles = [title.get_text() for title in soup.find_all('h1')]
        return titles
    except Exception as e:
        return f"Error parsing HTML: {e}"

if __name__ == "__main__":
    mcp.run()