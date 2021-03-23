# -*- coding: utf-8 -*-#

from re import search, sub
from subprocess import call
from time import perf_counter

# Author:Jiawei Feng
# @software: PyCharm
# @file: download.py
# @time: 2021/1/25 18:28
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from tqdm import tqdm


class Downloader:
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    browser = webdriver.Chrome('./chromedriver.exe', chrome_options=chrome_options)
    browser.minimize_window()
    urls = []
    video_name_dic = {}
    no_name_counter = 0

    def __init__(self, url_file, idman_exe, download_repo):
        self.idman_exe = idman_exe
        self.download_repo = download_repo
        self.read_in_urls(url_file)
        self.start_time = perf_counter()

    def read_in_urls(self, url_file_path):
        with open(url_file_path) as file:
            content = file.readlines()
            self.urls = list(filter(lambda x: x, map(lambda x: x.strip(), content)))

    def download(self, url, name):
        call('"{}" /d "{}" /p "{}" /f "{}" /n /a'.format(self.idman_exe, url, self.download_repo, name))
        call([self.idman_exe, '/d', ])

    def format_name(self, name):
        banned_symbols = ['?', '/', r'\\', ':', '*', '"', '<', '>', '|']
        return sub('|'.join(list(map(lambda x: '[{}]'.format(x), banned_symbols))), '', name)

    def main(self):
        for url in tqdm(self.urls):
            try:
                convert_url, name = self.get_video_url_and_name(url)
                self.download(convert_url, self.format_name(name))
            except:
                pass
        self.browser.quit()
        end_time = perf_counter()
        seconds = end_time - self.start_time
        h = int(seconds / 3600)
        m = int((seconds - h * 3600) / 60)
        s = seconds - h * 3600 - m * 60
        print("共运行{}时{}分{}秒".format(h, m, s))

    def get_video_url_and_name(self, url):
        self.browser.get('https://www.tubeoffline.com/download-PornHub-videos.php')
        WebDriverWait(self.browser, 30, 0.2).until(
            lambda x: x.find_element_by_css_selector('input.videoLink') and x.find_element_by_css_selector(
                'input.getVideo'))
        self.browser.find_element_by_css_selector('input.videoLink').send_keys(url)
        self.browser.find_element_by_css_selector('input.getVideo').click()
        # enter new page without alt tabs
        WebDriverWait(self.browser, 30, 0.2).until(lambda x: x.find_element_by_css_selector(
            'div#videoDownload table tbody tr:last-child td:last-child a') and x.find_element_by_css_selector(
            'div#videoContainer'))
        video_url = self.browser.find_element_by_css_selector(
            'div#videoDownload table tbody tr:last-child td:last-child a').get_attribute('href')
        result = search('Title: (.+)', self.browser.find_element_by_css_selector('div#videoContainer').text)
        if result:
            new_video_name = result.group(1)
        else:
            new_video_name = 'NoName{}'.format(self.no_name_counter)
            self.no_name_counter += 1
        new_video_name = '{}.mp4'.format(new_video_name)
        return (video_url, new_video_name)


def main():
    p = Downloader('input.txt', 'C:\\Program Files (x86)\\Internet Download Manager\\IDMan.exe', 'F:\\temp')
    p.main()


if __name__ == '__main__':
    main()
