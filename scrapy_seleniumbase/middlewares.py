from importlib import import_module

from scrapy import signals
from scrapy.exceptions import NotConfigured
from scrapy.http import HtmlResponse
from selenium.webdriver.support.ui import WebDriverWait

from .request import SeleniumBaseRequest


class SeleniumBaseMiddleware:
    """Scrapy middleware handling the requests using seleniumbase"""

    def __init__(
        self,
        driver_kwargs,
    ):
        """Initialize the selenium webdriver

        Parameters
        ----------
        driver_arguments: dict
            A dictionary of keyword arguments to initialize the driver with.
        """
        seleniumbase_module = import_module("seleniumbase")
        self.driver = getattr(seleniumbase_module, "Driver")
        self.driver = self.driver(**driver_kwargs)

    @classmethod
    def from_crawler(cls, crawler):
        """Initialize the middleware with the crawler settings"""
        driver_kwargs = crawler.settings.get("SELENIUMBASE_DRIVER_KWARGS")

        if not driver_kwargs:
            raise NotConfigured("SELENIUMBASE_DRIVER_KWARGS have to be set")

        middleware = cls(
            driver_kwargs=driver_kwargs,
        )

        crawler.signals.connect(middleware.spider_closed, signals.spider_closed)

        return middleware

    def process_request(self, request, spider):
        """Process a request using the selenium driver if applicable"""

        if not isinstance(request, SeleniumBaseRequest):
            return None

        self.driver.get(request.url)

        for cookie_name, cookie_value in request.cookies.items():
            self.driver.add_cookie({"name": cookie_name, "value": cookie_value})

        if request.wait_until:
            WebDriverWait(self.driver, request.wait_time).until(request.wait_until)

        if request.script:
            self.driver.execute_script(request.script)

        if request.driver_methods:
            driver_commands = [
                "self.driver" + method for method in request.driver_methods
            ]
            for command in driver_commands:
                exec(command)

        if request.screenshot:
            request.meta["screenshot"] = self.driver.get_screenshot_as_png()

        body = str.encode(self.driver.page_source)

        # Expose the driver via the "meta" attribute
        request.meta.update({"driver": self.driver})

        return HtmlResponse(
            self.driver.current_url, body=body, encoding="utf-8", request=request
        )

    def spider_closed(self):
        """Shutdown the driver when spider is closed"""
        self.driver.quit()
