import functools
import inspect
import logging
import typing
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed, Future
from collections import namedtuple

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.webdriver import WebDriver

from typing import Callable


Config = namedtuple('Config', 'DEFAULT_WEBDRIVER_CLS WEBDRIVER_PARAM_NAME')
config = Config(
    DEFAULT_WEBDRIVER_CLS=webdriver.Chrome,
    WEBDRIVER_PARAM_NAME='__driver'
)


def selenium_job(webdriver_param_name: str):
    """
    Decorator for job functions that are submitted to the executor.

    Example:
        >>> @selenium_job(webdriver_param_name='param_for_webdriver')
        >>> def get_title(url, param_for_webdriver):
        >>>     param_for_webdriver.get(url)
        >>>     return param_for_webdriver.title

    :param webdriver_param_name: The name for the webdriver passed in by the executor.
    :return:
    """
    def decorator(fn):
        @functools.wraps(fn)
        def wrapped(*args, **kwargs):
            passed_name = config.WEBDRIVER_PARAM_NAME
            if passed_name not in kwargs:
                raise SeleniumPoolException(
                    "webdriver object not found in kwargs")
            if passed_name != webdriver_param_name:
                kwargs[webdriver_param_name] = kwargs.pop(config.WEBDRIVER_PARAM_NAME)
            return fn(*args, **kwargs)
        wrapped.is_selenium_job = True
        return wrapped
    return decorator


class SeleniumPoolException(Exception):
    pass


class SeleniumJobResult:
    def __init__(self, caller: Callable, args, kwargs):
        """
        The object returned when the selenium_job has been completed.
        The executor passes in the original caller, args, and kwargs for identification

        Example:
            >>> for result in pool:
            ...     if result is orig_func:
            ...         do_stuff_with(result.result)

        :param caller:
        :param args:
        :param kwargs:
        """
        self._caller = caller
        self._args = args
        self._kwargs = kwargs
        self._result = None

    def __repr__(self) -> str:
        r = bool(self.result)
        c = repr(self.caller)
        a = len(self.args)
        k = len(self.kwargs)
        return (
            f'SeleniumJobResult(result={r}, caller={c}, args={a}, kwargs={k})')

    @property
    def caller(self):
        return self._caller

    @property
    def args(self):
        return self._args

    @property
    def kwargs(self):
        return self._kwargs

    @property
    def result(self):
        return self._result


class SeleniumPoolExecutor:
    """

    """
    def __init__(self,
                 wrap_drivers: typing.Iterable[WebDriver]=None,
                 num_workers: int=2,
                 close_on_exit: bool=False,
                 webdriver_cls: WebDriver=None,
    ):
        """
        :param wrap_drivers: An iterable on instantiated webdrivers.
        :param num_workers: Number of workers to instantiate if no workers are passed
        :param close_on_exit: Closes the webdrivers passed if True. Default is false
        :param webdriver_cls: The webdriver class to instantiate new webdrivers. If None, default is used.
        """

        self.num_workers = num_workers
        if self.num_workers < 1:
            raise ValueError('Wrong count for num_workers')
        self.webdriver_cls = webdriver_cls
        if wrap_drivers is not None:
            for driver in wrap_drivers:
                if not isinstance(driver, WebDriver):
                    raise SeleniumPoolException(
                        'Must pass an active selenium webdriver instance')
            self.drivers = set(wrap_drivers)
        else:
            self.drivers = None
        self._futures = set()
        self._jobs = []
        self._executor = ThreadPoolExecutor(max_workers=num_workers * 2)
        self.close_on_exit = close_on_exit
        if wrap_drivers is None and num_workers > 0:
            self.close_on_exit = True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.shutdown()
        return False

    def __iter__(self):
        yield from self.job_results()

    def _init_pool(self):
        if self.drivers is not None:
            return True
        if self.webdriver_cls is None:
            self.webdriver_cls = config.DEFAULT_WEBDRIVER_CLS
        self.drivers = {self.webdriver_cls()
                        for _ in range(self.num_workers)}
        return len(self.drivers) > 0

    def submit(self, fn: Callable, *args, **kwargs):
        """
        Submits a job to the executor.

        :param fn:
        :param args:
        :param kwargs:
        :return:
        """
        if not hasattr(fn, 'is_selenium_job'):
            params = inspect.signature(fn).parameters
            if config.WEBDRIVER_PARAM_NAME not in params:
                raise SeleniumPoolException(
                    f'Job function does not have a "selenium_job" decorator and '
                    f'"{config.WEBDRIVER_PARAM_NAME}" is not listed as a function param')
        self._jobs.append((fn, args, kwargs))

    def map_async(self, fn: Callable, *iterables) -> None:
        """
        Maps the @selenium_job decorated function to any number of iterables
        as positional args. Jobs are stored in the job-queue.

        Example:
            >>> sites = [
            ...    'https://google.com',
            ...    'https://msn.com']
            >>> pool.map_async(job_func, sites)

        :param fn: @selenium_job decorated function
        :param iterables: Iterables to pass as positional args.
        :return: None
        """
        for args in zip(*iterables):
            self.submit(fn, *args)
        return self.job_results()

    def shutdown(self, wait=True):
        """
        Shuts down the threadpool executor and closes webdrivers if specified.

        :param wait:
        :return:
        """
        thread_pool_down = self._executor.shutdown(wait)
        for future in as_completed(self._futures):
            self.drivers.add(future.driver)
        if self.close_on_exit and self.drivers is not None:
            for driver in self.drivers:
                try:
                    driver.close()
                except WebDriverException as exc:
                    logging.warning(exc)
        return thread_pool_down

    @staticmethod
    def _get_result(future: Future) -> SeleniumJobResult:
        result_object = future.result_object
        result_object._result = future.result()
        return result_object


    def job_results(self):
        if not self._init_pool():
            raise SeleniumPoolException(
                'Could not initialize the webdriver pool')
        for job in self._jobs:
            # unpack job
            fn, args, kwargs = job
            result_object = SeleniumJobResult(fn, args, kwargs)
            # get the first available driver
            if len(self.drivers) > 0:
                driver = self.drivers.pop()
            else:
                future = next(as_completed(self._futures))
                # return driver to free-driver pool
                self.drivers.add(future.driver)
                yield self._get_result(future)
                # abandon future object
                self._futures.remove(future)
                # pop off a driver from the pool
                driver = self.drivers.pop()
            # submit function to the executor and pass driver as kwarg to job fn
            kwargs[config.WEBDRIVER_PARAM_NAME] = driver
            future = self._executor.submit(fn, *args, **kwargs)
            # attach driver to the future object for recall
            future.driver = driver
            # attach results_object to future
            future.result_object = result_object
            # add future to set
            self._futures.add(future)
        # all jobs submitted. Collect remaining futures results
        for future in as_completed(self._futures):
            self.drivers.add(future.driver)
            yield self._get_result(future)
        self._futures.clear()
        self._jobs.clear()
