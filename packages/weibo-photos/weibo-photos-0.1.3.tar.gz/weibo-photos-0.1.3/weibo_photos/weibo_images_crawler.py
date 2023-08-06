import requests
import re
import os
import time

class WeiboImageCrawler(object):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        'Referer': 'https://webo.com/'
    }
    pic_url = 'http://photo.weibo.com/photos/get_all?uid=%s&album_id=%s&count=30&page=%d&type=%s&__rnd=%d'
    album_url = 'http://photo.weibo.com/albums/get_all?uid=%s&page=%d&count=20&__rnd=%d'

    def __init__(self, user_id):
        self.user_id = user_id
        self.s = requests.Session()
        self.albums = []
        self.images = []
    
    def init_requests(self):
        self.s.headers = self.headers
        self.s.verify = False
        cookies = {}
        with open('cookies.txt', 'r') as f:
            web_cookies = f.read()
            cookies = WeiboImageCrawler.parse_cookies_from_browser(web_cookies)
        self.s.cookies = requests.utils.cookiejar_from_dict(cookies)
    
    def get_album_info(self):
        i = 1
        while True:
            time_stamp = WeiboImageCrawler.get_timestamp()
            url = self.album_url % (self.user_id, i, time_stamp)
            r = self.s.get(url)
            r.raise_for_status()
            res_dict = r.json()
            if res_dict['code'] != 0:
                raise Exception('Wrong response!')
            album_list = res_dict['data']['album_list']
            if len(album_list) == 0:
                return
            self.albums.extend(album_list)
            i += 1

    def get_images_address(self, album_id, album_type):
        i = 1
        print('正在获取图片地址...')
        while True:
            time_stamp = WeiboImageCrawler.get_timestamp()
            url = self.pic_url % (self.user_id, album_id, i, album_type, time_stamp)
            r = self.s.get(url)
            r.raise_for_status()
            res_dict = r.json()
            if res_dict['code'] != 0:
                raise Exception('Wrong response!')
            photo_list = res_dict['data']['photo_list']
            if len(photo_list) == 0:
                print('获取图片地址完成！总共获取%d张图片！' % len(self.images))
                return
            self.images.extend(photo_list)
            time.sleep(1)
            i += 1

    def get_image_url(self, image):
        host = image['pic_host']
        name = image['pic_name']
        url = '{}/large/{}'.format(host, name)
        return url

    def write_images_address(self, album_id):
        image_file = '{}-{}.txt'.format(self.user_id, album_id)
        with open(image_file, 'w') as f:
            for image in self.images:
                image_url = self.get_image_url(image)
                f.write(image_url)
                f.write('\n')
    
    def save_all_images(self, save_dir):
        if save_dir is not None:
            os.chdir(save_dir)
        for image in self.images:
            image_name = image['pic_name']
            caption = image['caption_render']
            path = '{}/{}'.format(save_dir, image_name)
            if os.path.exists(path):
                print('{}已存在，跳过！'.format(image_name))
                continue
            image_url = self.get_image_url(image)
            cmd = 'curl -O {} -#'.format(image_url)
            print('========', caption, '========')
            os.system(cmd)
    
    def print_albums_info(self):
        for album in self.albums:
            album_id = album['album_id']
            album_caption = album['caption']
            album_type = album['type']
            photos_count = album['count']['photos']
            info = '相册专辑ID：%s, 相册名称: %s, 相册类型: %s, 包含相片数量: %s' % (album_id, album_caption, album_type, photos_count)
            print(info)

    @staticmethod
    def get_timestamp():
        return int(round(time.time() * 1000))

    @staticmethod
    def parse_cookies_from_browser(web_cookies):
        cookies_list = web_cookies.split(';')
        cookies = {}
        for cookie in cookies_list:
            cookie = cookie.strip()
            pair = cookie.split('=')
            try:
                key = pair[0]
                value = pair[1]
                cookies[key] = value
            except:
                raise Exception('cookies is error!')
        return cookies 