Scrapy middleware to handle javascript pages using seleniumbase driver.

Based on [scrapy-selenium](https://github.com/clemfromspace/scrapy-selenium) library, scrapy-seleniumbase was made for those who want to  make use of Seleniumbase Driver convenient features.

## Installation

```
pip install git+https://github.com/Quartz-Core/scrapy-seleniumbase
```


## Configuration
1.  Provide keyword arguments for Driver in dict. For example:

    ```python
    SELENIUMBASE_DRIVER_KWARGS = {
    "browser": "chrome",
    "uc": True,
    "headless": True,
    "block_images": True,
    }
    ```

2. Add the `SeleniumBaseMiddleware` to the downloader middlewares:
    ```python
    DOWNLOADER_MIDDLEWARES = {
        'scrapy_seleniumbase.SeleniumBaseMiddleware': 800
    }
    ```
## Usage
Use the `scrapy_seleniumbase.SeleniumBaseRequest` instead of the scrapy built-in `Request` like below:
```python
from scrapy_seleniumbase import SeleniumBaseRequest

yield SeleniumBaseRequest(url=url, callback=self.parse_result)
```
The request will be handled by seleniumbase, and the request will have an additional `meta` key, named `driver` containing the seleniumbase driver with the request processed.
```python
def parse_result(self, response):
    print(response.request.meta['driver'].title)
```
For more information about the available driver methods and attributes, refer to the [selenium python documentation](http://selenium-python.readthedocs.io/api.html#module-selenium.webdriver.remote.webdriver) (all vanilla selenium driver methods are available) and [seleniumbase documentation](https://seleniumbase.io/help_docs/method_summary/#seleniumbase-methods-api-reference) (look for "driver" specific methods, located at the end of the page).

The `selector` response attribute work as usual (but contains the html processed by the selenium driver).
```python
def parse_result(self, response):
    print(response.selector.xpath('//title/@text'))
```

### Additional arguments
The `scrapy_selenium.SeleniumBaseRequest` accept 5 additional arguments:

#### `wait_time` / `wait_until`

When used, webdriver will perform an [Explicit wait](http://selenium-python.readthedocs.io/waits.html#explicit-waits) before returning the response to the spider.
```python
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

yield SeleniumBaseRequest(
    url=url,
    callback=self.parse_result,
    wait_time=10,
    wait_until=EC.element_to_be_clickable((By.ID, 'someid'))
)
```

#### `screenshot`
When used, webdriver will take a screenshot of the page and the binary data of the .png captured will be added to the response `meta`:
```python
yield SeleniumBaseRequest(
    url=url,
    callback=self.parse_result,
    screenshot=True
)

def parse_result(self, response):
    with open('image.png', 'wb') as image_file:
        image_file.write(response.meta['screenshot'])
```

#### `script`
When used, webdriver will execute custom JavaScript code.
```python
yield SeleniumBaseRequest(
    url=url,
    callback=self.parse_result,
    script='window.scrollTo(0, document.body.scrollHeight);',
)
```

#### `driver_methods`
When used, seleniumbase webdriver will execute methods, provided as strings in a list, before returning page's html.
```python
def start_requests(self):
    for url in self.start_urls:
        yield SeleniumRequest(
                        url=url,
                        driver_methods=['''.find_element("xpath","some_xpath").click()'''])
)
```