"""This module contains the ``SeleniumBaseRequest`` class"""

from scrapy import Request


class SeleniumBaseRequest(Request):
    """Scrapy ``Request`` subclass providing additional arguments"""

    def __init__(
        self,
        wait_time=None,
        wait_until=None,
        screenshot=False,
        script=None,
        driver_methods=None,
        *args,
        **kwargs
    ):
        """Initialize a new selenium request

        Parameters
        ----------
        wait_time: int
            The number of seconds to wait.
        wait_until: method
            One of the "selenium.webdriver.support.expected_conditions". The response
            will be returned until the given condition is fulfilled.
        screenshot: bool
            If True, a screenshot of the page will be taken and the data of the screenshot
            will be returned in the response "meta" attribute.
        script: str
            JavaScript code to execute.
        driver_methods: list
            List of seleniumbase driver methods as strings to execute. (e.g., [".find_element(...).click()", ...])

        """

        self.wait_time = wait_time
        self.wait_until = wait_until
        self.screenshot = screenshot
        self.script = script
        self.driver_methods = driver_methods
        super().__init__(*args, **kwargs)
