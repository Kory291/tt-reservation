from playwright.sync_api import sync_playwright, Playwright

def run(playwright: Playwright) -> None:
    firefox = playwright.firefox
    browser = firefox.launch(headless=False)
    page = browser.new_page()
    page.goto("")
    anchors = page.locator("a")
    deny_button = anchors.filter(has_text="Accept all")
    deny_button.click()
    browser.close()

def main() -> None:
    with sync_playwright() as playwright:
        run(playwright)


if __name__ == "__main__":
    main()
