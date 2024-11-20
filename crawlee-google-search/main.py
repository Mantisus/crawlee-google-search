from crawlee.beautifulsoup_crawler import BeautifulSoupCrawler, BeautifulSoupCrawlingContext
from crawlee.http_clients.curl_impersonate import CurlImpersonateHttpClient
from crawlee import Request, ConcurrencySettings, HttpHeaders

from .routes import router

QUERIES = ["Apify", "Crawlee"]

CRAWL_DEPTH = 2


async def main() -> None:
    """The crawler entry point."""

    concurrency_settings = ConcurrencySettings(max_concurrency=5, max_tasks_per_minute=200)

    http_client = CurlImpersonateHttpClient(impersonate="chrome124",
                                            headers=HttpHeaders({"referer": "https://www.google.com/",
                                                     "accept-language": "en",
                                                     "accept-encoding": "gzip, deflate, br, zstd",
                                                     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
                                            }))
    crawler = BeautifulSoupCrawler(
        request_handler=router,
        max_request_retries=1,
        concurrency_settings=concurrency_settings,
        http_client=http_client,
        max_requests_per_crawl=30,
        max_crawl_depth=CRAWL_DEPTH
    )

    requests_lists = [Request.from_url(f"https://www.google.com/search?q={query}", user_data = {"query": query}) for query in QUERIES]

    await crawler.run(requests_lists)

    await crawler.export_data_csv("google_ranked.csv")
