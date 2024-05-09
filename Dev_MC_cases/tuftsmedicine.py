import asyncio
from playwright.async_api import async_playwright

async def main():
    url = 'https://www.tuftsmedicine.org/find-a-doctor?yext_retrieveFacets=true&yext_sortBys=%5B%7B%22type%22%3A%22RELEVANCE%22%7D%5D&yext_input=Melrose+Wakefield+Hospital&yext_offset=0&yext_limit=16&yext_facetFilters=%7B%7D'

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url)

        try:
            # Evaluate JavaScript to access the shadow root
            root1 = await page.evaluate('''() => {
                const parentElement = document.querySelector('tufts-yext');
                return parentElement.shadowRoot;
            }''')

            print(root1)

            """# Evaluate JavaScript to access the nested shadow DOM
            root2 = await page.evaluate('''(root1) => {
                return root1.querySelector('tufts-container:nth-child(2)');
            }''', root1)

            nested_shadow_root = await page.evaluate('(element) => element.shadowRoot', root2)

            print(nested_shadow_root)"""

        except Exception as e:
            print("An error occurred:", e)
        finally:
            await browser.close()

def run_main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

run_main()
