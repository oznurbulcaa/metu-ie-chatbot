import requests
from bs4 import BeautifulSoup

# Base URLs to scrape
BASE_URLS = {
    "general_info": "https://sp-ie.metu.edu.tr/en/general-information",
    "steps_follow": "https://sp-ie.metu.edu.tr/en/steps-follow",
    "faq": "https://sp-ie.metu.edu.tr/en/faq"
}

def scrape_page(url):
   
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        return f"Unable to fetch data (status {res.status_code})"

    soup = BeautifulSoup(res.text, "html.parser")

    # Try to find content within specific divs or sections
    content_section = soup.find("div", class_="field-item")  
    if not content_section:
        # If not found, fall back to body content
        content_section = soup.find("body")

    # If content is still not found, return a message
    if content_section is None:
        return "Could not find the content section."

    # Extract all paragraphs, headings, lists, and any other useful sections
    paragraphs = content_section.find_all(["p", "h1", "h2", "h3", "ul", "ol"])

    # Combine text from all found elements
    text_content = "\n".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))
    
    return text_content

# Test the scraper by printing the scraped content
if __name__ == "__main__":
    for key, link in BASE_URLS.items():
        print(f"\n=== {key.upper()} ===\n")
        page_text = scrape_page(link)
        print(page_text[:1000])  # print first 1000 characters to avoid overload
        print("\n-------------------------\n")
