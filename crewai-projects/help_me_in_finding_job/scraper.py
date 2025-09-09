from playwright.sync_api import sync_playwright

def scrape_with_playwright(url: str) -> str:
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        page.wait_for_load_state("networkidle")
        text = page.text_content("body")
        browser.close()
        return text # type: ignore

if __name__ == "__main__":
    print(scrape_with_playwright("https://jobs.careers.microsoft.com/global/en/job/1872630/Software-Engineer/"))
