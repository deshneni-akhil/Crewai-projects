from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from playwright.sync_api import sync_playwright

class MyCustomToolInput(BaseModel):
    """Input schema for MyCustomTool."""
    url: str = Field(..., description="The URL of the website to scrape.")

class PWScrapeWebsite(BaseTool):
    name: str = "Playwright Website Scraper"
    description: str = (
        "A tool that uses Playwright to scrape the full text content from a given website URL."
    )
    args_schema: Type[BaseModel] = MyCustomToolInput

    def _run(self, url: str) -> str:
        try:
            text = ""
            with sync_playwright() as pw:
                browser = pw.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto(url)
                page.wait_for_load_state("networkidle")
                text = page.text_content("body")
                browser.close()
            return text # type: ignore
        except Exception as e:
            return f"An error occurred while scraping the website: {e}"
    
