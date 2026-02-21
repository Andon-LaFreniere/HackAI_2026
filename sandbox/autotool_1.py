# depends: requests
# depends: beautifulsoup4
from fastmcp import FastMCP
import requests
from bs4 import BeautifulSoup

mcp = FastMCP("HTMLContentFetcher")

@mcp.tool()
def fetch_html_content(url: str, data_type: str) -> str:
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        if data_type == "title":
            return soup.title.string if soup.title else "No title found"
        elif data_type == "headlines":
            headlines = [headline.get_text() for headline in soup.find_all(['h1', 'h2', 'h3'])]
            return "\n".join(headlines) if headlines else "No headlines found"
        else:
            return "Unsupported data type requested"
    except requests.exceptions.RequestException as e:
        return f"Request error: {e}"
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    mcp.run()