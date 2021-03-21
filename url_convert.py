# -*- coding: utf-8 -*-#

# Author:Jiawei Feng
# @software: PyCharm
# @file: url_convert.py
# @time: 2021/1/25 18:28 
from selenium import webdriver
from time import perf_counter
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from os import system, path
from tqdm import tqdm
from re import search
from json import dumps
from winsound import Beep


class UrlConverter:
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    browser = webdriver.Chrome('./chromedriver.exe',chrome_options=chrome_options)
    browser.minimize_window()
    urls = []
    video_name_dic = {}
    no_name_counter = 0

    def __init__(self, url_file_path, output_file, video_name_json_file):
        self.output_file = output_file
        self.video_name_json_file = video_name_json_file
        self.del_old_file(self.output_file)
        self.read_in_urls(url_file_path)

    def del_old_file(self, file):
        if path.exists(file):
            system('del {}'.format(file))

    def read_in_urls(self, url_file_path):
        with open(url_file_path) as file:
            content = file.readlines()
            self.urls = list(filter(lambda x: x, map(lambda x: x.strip(), content)))

    def execute(self):
        for url in tqdm(self.urls):
            try:
                result = self.get_video_url_and_name(url)
                with open(self.output_file, 'a') as file:
                    file.write(result[0])
                    file.write('\n')
                self.video_name_dic.update(result[1])
                self.del_old_file(self.video_name_json_file)
                with open(self.video_name_json_file, 'w') as file:
                    file.write(dumps(self.video_name_dic, sort_keys=True, indent=4, separators=(',', ': ')))
            except:
                pass

    def get_video_url_and_name(self, url):
        self.browser.get('https://www.tubeoffline.com/download-PornHub-videos.php')
        WebDriverWait(self.browser, 30, 0.2).until(
            lambda x: x.find_element_by_css_selector('input.videoLink') and x.find_element_by_css_selector(
                'input.getVideo'))
        self.browser.find_element_by_css_selector('input.videoLink').send_keys(url)
        self.browser.find_element_by_css_selector('input.getVideo').click()
        # enter new page without alt tabs
        WebDriverWait(self.browser, 30, 0.2).until(lambda x: x.find_element_by_css_selector(
            'div#videoDownload table tbody tr:last-child td:last-child a') and x.find_element_by_css_selector('div#videoContainer'))
        video_url = self.browser.find_element_by_css_selector(
            'div#videoDownload table tbody tr:last-child td:last-child a').get_attribute('href')
        result = search('Title: (.+)', self.browser.find_element_by_css_selector('div#videoContainer').text)
        if result:
            new_video_name = result.group(1)
        else:
            new_video_name = 'NoName{}'.format(self.no_name_counter)
            self.no_name_counter += 1
        new_video_name = '{}.mp4'.format(new_video_name)
        result = search('[^/]+[.]mp4', video_url)
        if result:
            old_video_name = result.group()
            video_name_dic = {old_video_name: new_video_name}
        else:
            video_name_dic = {}
        return (video_url, video_name_dic)
        # return self.browser.find_element_by_css_selector(
        #     'div#videoDownload table tbody tr:last-child td:last-child a').get_attribute('href')

    def close(self):
        self.browser.quit()


def main():
    start_time = perf_counter()
    p = UrlConverter('input.txt', 'output.txt', 'oldVideoName_to_newVideoName.json')
    p.execute()
    p.close()
    end_time = perf_counter()
    seconds = end_time - start_time
    h = int(seconds / 3600)
    m = int((seconds - h * 3600) / 60)
    s = seconds - h * 3600 - m * 60
    print("共运行{}时{}分{}秒".format(h, m, s))
    Beep(600,1000)


if __name__ == '__main__':
    main()
