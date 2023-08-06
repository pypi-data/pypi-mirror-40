# -*- coding: utf-8 -*-

"""
pywebcopy.workers
~~~~~~~~~~~~~~~~~

Provides different services to several modules in pywebcopy.

"""
import re
from threading import Thread, Lock

from six.moves import queue
from six.moves.urllib.parse import urljoin

from .configs import config
from .webpage import WebPage
from .core import zip_project


class EXIT:
    pass


DEBUG = True
EXIT_FLAG = EXIT()
D_QUEUE = queue.Queue()
LOCK = Lock()
ALL = []


class OffLoader(Thread):
    """Simple run or wait type process.
    """

    def run(self):
        """
        Downloads the objects filled in the queue or wait until killed explicitly.
        """
        while True:

            task = D_QUEUE.get(block=True)
            if isinstance(task, EXIT):

                D_QUEUE.task_done()

                if DEBUG:
                    print("Downloader Exiting...")
                break
            else:
                task.start()
                D_QUEUE.task_done()

        if DEBUG:
            print("Downloader Exited.")


class _Crawler(WebPage, Thread):
    _current_level = 0  # level of this crawler
    scan_level = 2

    def __init__(self, url):
        self.url = url
        Thread.__init__(self)
        WebPage.__init__(self, url)

    def run(self):
        """
        Crawl the current url and create a several new crawler
        objects from the urls found and add them to the queue.
        """

        if self._current_level > self.scan_level:
            return

        self.save_complete()

        links = self.bs4.find_all('a', href=True)
        matcher = re.compile(self.url + r'/?(?:.*?)')

        for link in links:

            url = link.get('href', '')  # type: str
            url = url.split('#')[0]
            url = urljoin(self.url, url)

            match = matcher.match(url)

            if match is not None and url not in ALL:
                ALL.append(url)

                new_task = _Crawler(url)
                new_task._current_level += 1

                LOCK.acquire()
                D_QUEUE.put(new_task)
                LOCK.release()


class Crawler(_Crawler):
    """Crawls a specific url and saves any internal pages found. """

    def __init__(self, base_page_url, scan_level=2):

        self.base_page_url = base_page_url
        self.scan_level = scan_level
        self._offloader = OffLoader()
        self._current_level = 0
        _Crawler.__init__(self, self.base_page_url)

    def run(self):
        if DEBUG:
            print("Downloader Starting..")

        self._offloader.start()     # start the downloader

        if DEBUG:
            print("Crawler Starting..")

        super(Crawler, self).run()   # start off at the base_url

        if DEBUG:
            print("Adding EXIT_FLAG")

        D_QUEUE.put(EXIT_FLAG)     # Put a kill switch at end of queue

        print("Waiting for tasks to complete..")
        D_QUEUE.join()              # Wait for the download queue to be emptied

        if DEBUG:
            print("Ended..")

    def crawl(self):
        """Run Threaded:  Scans pages for links to other pages to save in COPY_WHOLE_WEBSITE mode.

        fetches the first page and scans for links to
        other pages which are under your given _url
        """

        self.start()


def save_website(url, project_folder, project_name=None, **kwargs):
    """Saves the complete website with one function."""

    config.setup_config(url, project_folder, project_name, **kwargs)
    crawler = Crawler(url)
    crawler.run()
    zip_project()
