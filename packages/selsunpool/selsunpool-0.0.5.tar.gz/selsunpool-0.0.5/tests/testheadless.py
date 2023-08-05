import pytest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from .context import (
    SeleniumPoolExecutor,
    SeleniumPoolException,
    selenium_job,
    WebDriver)

from .testbasic import TEST_URLS, get_url

@pytest.fixture(scope='module')
def workers():
    options = Options()
    options.add_argument('--headless')
    workers = [
        webdriver.Chrome(options=options),
        webdriver.Chrome(options=options),
    ]
    yield workers
    for d in workers:
        try:
            d.close()
        except Exception:
            pass



def test_headless(workers):
    with SeleniumPoolExecutor(workers) as pool:
        pool.map_async(get_url, TEST_URLS)
        job_objects = list(pool)
        assert all(r.result for r in job_objects)
        print()
        print(job_objects, sep='\n')
        for job in job_objects:
            assert job.caller is get_url

        # print([job.caller for job in job_objects])




@selenium_job('driver')
def get_src(url, driver):
    driver.get(url)
    return 'page_source', driver.page_source