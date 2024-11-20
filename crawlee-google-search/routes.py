from crawlee.beautifulsoup_crawler import BeautifulSoupCrawlingContext
from crawlee.router import Router

router = Router[BeautifulSoupCrawlingContext]()


@router.default_handler
async def default_handler(context: BeautifulSoupCrawlingContext) -> None:
    """Default request handler."""
    context.log.info(f'Processing {context.request} ...')

    order = context.request.user_data.get("last_order", 1)
    query = context.request.user_data.get("query")
    for item in context.soup.select("div#search div#rso div[data-hveid][lang]"):
        try:
            data = {
                "query": query,
                "order_no": order,
                'title': item.select_one("h3").get_text(),
                "url": item.select_one("a").get("href"),
                "text_widget": item.select_one("div[style*='line']").get_text(),
            }
            await context.push_data(data)
            order += 1
        except AttributeError as e:
            context.log.warning(f'Attribute error for query "{query}": {str(e)}')
        except Exception as e:
            context.log.error(f'Unexpected error for query "{query}": {str(e)}')

        await context.enqueue_links(selector="div[role='navigation'] td[role='heading']:last-of-type > a",
                                    user_data={"last_order": order, "query": query})
