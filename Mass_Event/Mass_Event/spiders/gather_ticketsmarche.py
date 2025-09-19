import scrapy
from ..items import MassEventItem
from scrapy.utils.response import open_in_browser
from scrapy_playwright.page import PageMethod


class MassEvent(scrapy.Spider):
    name = "gather_ticketsmarche"

    def start_requests(self):
        url = "https://www.ticketsmarche.com/Event_filter_grid/Eventlist_filter"
        yield scrapy.Request(
            url,
            meta={
                "playwright": True,
                "playwright_include_page": True,
                "playewright_page_methods": [
                    PageMethod("wait_for_selector", "div.quote"),
                    PageMethod(
                        "evaluate", "window.scrollBy(0, document.body.scrollHeight)"
                    ),
                    PageMethod("wait_for_selector", "div.quote::nth-child(11)"),
                ],
                "errback": self.errback,
            },
        )

    async def parse(self, response):
        open_in_browser(response)
        page = response.meta["playwright_page"]
        await page.close()
        events = response.css(".bg-light")
        for event in events:
            item = MassEventItem()
            item["event_name"] = event.css(".event-name::text").extract()
            item["date"] = event.css(".event-date::text").extract()
            item["location"] = event.css(".event-venue::text").extract()
            yield item

    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()
