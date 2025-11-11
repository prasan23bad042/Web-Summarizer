import httpx
from bs4 import BeautifulSoup
from typing import Optional

async def fetch_webpage_content(url: str) -> str:
    """
    Fetch and extract main content from a webpage.
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, follow_redirects=True, timeout=10.0)
            response.raise_for_status()
            
            # Use BeautifulSoup to extract main content
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "footer", "header"]):
                script.decompose()
                
            # Get text and clean it up
            text = soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            return '\n'.join(chunk for chunk in chunks if chunk)
            
    except Exception as e:
        raise Exception(f"Failed to fetch or parse webpage: {str(e)}")
