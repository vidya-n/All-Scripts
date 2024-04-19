import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        # Launch a Chromium browser
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()  # Create a new page instance

        url = 'https://cls.health/providers/'
        await page.goto(url)  # Navigate to the URL

        # Wait for 5 seconds
        await page.wait_for_timeout(5000)

        count = 1
        profiles = []

        while count <= 6:
            page_count = count
            # Find all elements matching the XPath
            data = await page.query_selector_all('//a[contains(@class, "view-profile")]')
            if data:
                for i in data:
                    doc_url = await i.get_attribute('href')
                    print(doc_url)
                    profiles.append(doc_url)
            try:
                print(f"Page {page_count} done.")
                print(len(profiles))
                # Click the next page link
                await page.click('a.nextpostslink')
                # Wait for 5 seconds
                await page.wait_for_timeout(5000)
                count = count + 1
            except Exception as e:
                print("element-click failed:", e)
                break

        print(len(profiles))
        await browser.close()  # Close the browser

# Run the main function
asyncio.run(main())
