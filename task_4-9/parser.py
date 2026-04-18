from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

import os

load_dotenv()

login = os.getenv("GITHUB_LOGIN")
password = os.getenv("GITHUB_PASSWORD")

def register(page, login, password):
    page.goto("https://github.com/login")
    page.fill("#login_field", login)
    page.fill("#password", password)
    page.click("input[name='commit']")

def parse_repos(page, search_query, page_to_parse):
    results = []

    for pg in range(1, page_to_parse + 1):
            search_url = f"https://github.com/search?q={search_query}&type=repositories&p={pg}"


            page.goto(search_url)
            page.wait_for_selector("div[data-testid='results-list']", timeout=10000)

            items = page.query_selector_all("div[data-testid='results-list'] > div")

            for item in items:
                author_name_elem = item.query_selector("h3 div div a")
                if not author_name_elem:
                    continue
                author, name = author_name_elem.inner_text().split("/")

                desc_elem = item.query_selector(".search-match")
                desc = desc_elem.inner_text() if desc_elem else "No description"

                lang_elem = item.query_selector("span[aria-label$='language']")
                lang = lang_elem.inner_text() if lang_elem else "Not specified"

                stars_elem = item.query_selector("ul li a span")
                stars = stars_elem.inner_text() if stars_elem else "0"

                results.append({
                    "name": name,
                    "author": author,
                    "description": desc,
                    "language": lang,
                    "stars": stars,
                })        
    return results

def run_parser(search_query):
    with sync_playwright() as p:

        browser = p.firefox.launch(
            headless=True,
            args=[
                "--disable-gpu",
                "--no-sandbox"
            ]
        )
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
            viewport={"width": 1920, "height": 1080}
        )
         
        page = context.new_page()
        page.set_default_timeout(60000)  

        register(page, login, password)

        parsed_data = parse_repos(page, search_query, 1)

        browser.close()
    return parsed_data

