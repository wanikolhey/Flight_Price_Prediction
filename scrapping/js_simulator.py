from playwright.sync_api import sync_playwright, TimeoutError

def get_html_after_js(url):
    """
    Fetches the HTML content of a URL after JavaScript has executed,
    while attempting to mimic a real user to avoid bot detection.

    This function launches a non-headless browser, sets a realistic user agent
    and viewport, navigates to the URL, and waits for a specific element
    or a timeout before extracting the page content.

    Args:
        url (str): The URL of the website to scrape.

    Returns:
        str: The HTML content of the page, or None if an error occurs.
    """
    html_content = None
    print("Starting Playwright...")
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)  # Run in non-headless mode to appear more human

            # Create a new context with a common user agent and viewport
            context = browser.new_context(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            )
            page = context.new_page()
            page.goto(url, timeout=60000)
            html_content = page.content()

            browser.close()
            print("Browser closed.")

    except TimeoutError:
        print(f"Navigation to {url} timed out. The website may be actively blocking bots or is very slow.")
    except Exception as e:
        print(f"An error occurred: {e}")

    return html_content


if __name__ == "__main__":
    target_url = "https://www.ixigo.com/search/result/flight?from=PNQ&to=NAG&date=08102025&adults=1&children=0&infants=0&class=e&source=Search+Form&utm_source=Brand_Ggl_Search&utm_medium=paid_search_google"
    dynamic_html = get_html_after_js(target_url)

    if dynamic_html:
        try:
            with open("rendered_page.html", "w", encoding="utf-8") as f:
                f.write(dynamic_html)
            print("\nSuccessfully fetched HTML after JavaScript execution.")
            print("Content saved to 'rendered_page.html'")
        except IOError as e:
            print(f"\nCould not write to file: {e}")
    else:
        print("\nFailed to retrieve HTML content.")

