# # import requests
# # from bs4 import BeautifulSoup

# # HEADERS = {"User-Agent": "Mozilla/5.0"}

# # def scrape_wikipedia(url: str) -> str:
# #     response = requests.get(url, headers=HEADERS, timeout=10)
# #     response.raise_for_status()

# #     soup = BeautifulSoup(response.text, "html.parser")
# #     paragraphs = soup.select("p")

# #     return " ".join(p.text for p in paragraphs[:10])




# # backend/scraper.py

# import requests
# from bs4 import BeautifulSoup

# HEADERS = {"User-Agent": "Mozilla/5.0"}

# def scrape_wikipedia(url: str) -> str:
#     response = requests.get(url, headers=HEADERS, timeout=10)
#     response.raise_for_status()

#     soup = BeautifulSoup(response.text, "html.parser")
#     paragraphs = soup.select("p")

#     return " ".join(p.text for p in paragraphs[:10])




# backend/scraper.py
import requests
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0"}

def scrape_wikipedia(url: str) -> dict:
    """
    Returns dict:
      {
        "url": url,
        "title": str | None,
        "summary": str | None,
        "sections": [section titles...],
        "content": "big text"  # combined paragraphs used for LLM input
      }
    """
    resp = requests.get(url, headers=HEADERS, timeout=10)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    # title
    title_tag = soup.find("h1", id="firstHeading")
    title = title_tag.get_text(strip=True) if title_tag else None

    # summary = first paragraph(s)
    paragraphs = soup.select("p")
    summary = None
    if paragraphs:
        # pick first non-empty paragraph as summary
        for p in paragraphs:
            text = p.get_text(strip=True)
            if text:
                summary = text
                break

    # sections: collect H2 headings (text only)
    sections = []
    for h2 in soup.select("h2 .mw-headline"):
        s = h2.get_text(strip=True)
        if s:
            sections.append(s)

    # content: join first N paragraphs (for LLM)
    content = " ".join(p.get_text(" ", strip=True) for p in paragraphs[:15])

    return {
        "url": url,
        "title": title,
        "summary": summary,
        "sections": sections,
        "content": content
    }

