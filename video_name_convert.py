# -*- coding: utf-8 -*-#

# Author:Jiawei Feng
# @software: PyCharm
# @file: video_name_convert.py
# @time: 2021/1/26 15:33
from os import path, rename,system
from json import loads
from tqdm import tqdm
from winsound import Beep


class VideoNameConverter:
    all_count = None
    success_count = 0

    def __init__(self, json_file, video_repo_path):
        with open(json_file) as file:
            file_content = file.read()
        self.video_name_dic: dict = loads(file_content)
        self.video_repo_path = video_repo_path
        self.all_count = len(self.video_name_dic.keys())

    def execute(self):
        for old_video_name in tqdm(self.video_name_dic.keys()):
            try:
                new_video_name = self.video_name_dic.get(old_video_name)
                old_video_path = path.join(self.video_repo_path, old_video_name)
                new_video_path = path.join(self.video_repo_path, new_video_name)
                if path.exists(old_video_path):
                    if path.exists(new_video_path):
                        system("del {}".format(old_video_path))
                        print("{}已存在".format(new_video_name))
                    else:
                        rename(old_video_path, new_video_path)
                        self.success_count += 1
                        print("成功将{}命名为{}".format(old_video_name,new_video_name))
            except:
                pass
        print("json文件中共{}个视频，成功转换{}个".format(self.all_count, self.success_count))
        Beep(1200,1000)


def main():
    v = VideoNameConverter('./oldVideoName_to_newVideoName.json', r'Z:\media\porn\unsorted\repo')
    v.execute()


if __name__ == '__main__':
    main()
