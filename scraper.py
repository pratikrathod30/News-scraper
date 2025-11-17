
import requests
from bs4 import BeautifulSoup

URL = "https://www.hindustantimes.com/"     
OUTPUT_FILE = "headlines.txt"

def fetch_html(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()  
        return resp.text
    except requests.exceptions.RequestException as e:
        print("Error fetching URL:", e)
        return None

def scrape_headlines(html):
    soup = BeautifulSoup(html, "html.parser")
    headlines = []
    for h2 in soup.find_all("h2"):
        text = h2.get_text(strip=True)
        
        if len(text) >= 8:
            headlines.append(text)
    
    seen = set()
    unique = []
    for t in headlines:
        if t not in seen:
            unique.append(t)
            seen.add(t)
    return unique

def save_to_file(lines, filename=OUTPUT_FILE):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            for line in lines:
                f.write(line + "\n")
        print(f"Saved {len(lines)} headlines to '{filename}'.")
    except Exception as e:
        print("Error writing file:", e)

def main():
    print("Fetching:", URL)
    html = fetch_html(URL)
    if html is None:
        print("Exiting due to fetch error.")
        return
    headlines = scrape_headlines(html)
    if not headlines:
        print("No headlines found on the page.")
        return
    save_to_file(headlines)

if __name__ == "__main__":
    main()
