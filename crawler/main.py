from .get_vhome import VhomeCrawler 
import time


if __name__=='__main__':
    crawler = VhomeCrawler()
    crawler.open()
    crawler.action()
    crawler.close()
