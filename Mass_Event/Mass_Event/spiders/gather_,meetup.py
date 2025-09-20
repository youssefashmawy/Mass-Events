import scrapy
from ..items import MassEventItem
from scrapy.utils.response import open_in_browser
from scrapy_playwright.page import PageMethod


class MassEvent(scrapy.Spider):
    name = "gather_ticketsmarche"

    def start_requests(self):
        url = "https://www.meetup.com/find/eg--cairo/"
        yield scrapy.Request(
            url,
            meta={
                "playwright": True,
                "playwright_include_page": True,
                "playewright_page_methods": [
                    PageMethod("wait_for_selector", ".hover\:no-underline"),
                    PageMethod(
                        "evaluate", "window.scrollBy(0, document.body.scrollHeight)"
                    ),
                    PageMethod(
                        "wait_for_selector", "div.hover\:no-underline::nth-child(3)"
                    ),
                ],
                "errback": self.errback,
            },
        )

    async def parse(self, response):
        open_in_browser(response)
        page = response.meta["playwright_page"]
        await page.close()
        events = response.css(".pt-ds2-12")
        for event in events:
            item = MassEventItem()
            item["event_name"] = event.css(
                ".text-ds2-text-fill-primary-enabled::text"
            ).extract()
            item["date"] = event.css(
                ".truncate.text-ds2-text-fill-tertiary-enabled::text"
            ).extract()
            item["location"] = event.css(".flex-shrink::text").extract()
            yield item

    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()
