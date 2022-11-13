from .get_propzy import PropzyCrawler
import time


if __name__=='__main__':
    crawler = PropzyCrawler()
    crawler.open()
    crawler.action()
    crawler.close()
