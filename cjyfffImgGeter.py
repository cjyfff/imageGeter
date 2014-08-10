#! /usr/bin/env python
#coding=utf-8
#author: cjyfff -- https://github.com/cjyfff

import re
import urllib
import sys
import threading

count = 1
pre_spec_name = 1
MAX_THREADING = 4

message = {
'opt_msg': '''*********************************************************
Enter 1 to input an url, or enter 2 to open a html file: ''',
'url_msg': '''*********************************************************
Enter the url which is contained the images: ''',
'file_dir_msg': '''*********************************************************
Enter the path of the html file: ''',
'reg_msg': '''*********************************************************
Enter the regular to match the images, such like: http://imgsrc\.aaa\.com/forum/w%.*?\.jpg''',
'prefix_msg': '''*********************************************************
Sometime we are visiting a page that is showing the thumbnails, and we want to
download the real images which are relate to these thumbnails, then we need to
enter the prefix of the real url. For example, the thumbnails url is www.aaa.com/thumb/111.jpg',
the real image url is 'www.aaa.com/images/111.jpg', so we need to enter the prefix 'www.abc.com/images/',
this script will download the real image. If the images in the current page is not an thumbnails,
or you just want to download thumbnails, you just need to enter nothing. ''',
'save_dir_msg': '''*********************************************************
Enter the path you want to save the images, enter nothing to save in the current path: ''',
'spec_name_msg': '''*********************************************************
Enter the name you want to named the images.
If you enter 'football', the images will be save as 'football1.jpg', 'football2.jpg'...etc.
Enter nothing to save images with the origin name specified in the url.
''',
}


def get_html_content(url):
    page = urllib.urlopen(url)
    content = page.read()
    return content


def get_file(file):
    fp = open(file)
    content = fp.read()
    fp.close()
    return content


def get_picture_url(content, reg, prefix):
    pic_url_list = []
    img_re = re.compile(reg)
    img_list = re.findall(img_re, content)
    if prefix:
        for item in img_list:
            pic_url_list.append({
                'name': item.split('/')[-1],
                'url': prefix + item.split('/')[-1],
            })
        return pic_url_list

    for item in img_list:
        pic_url_list.append({
            'name': item.split('/')[-1],
            'url': item,
        })

    return pic_url_list


def print_counting():
    global count
    print "%d pictures saved" % count
    count += 1


def save_thread(list, spec_name, save_dir):
    global pre_spec_name

    for item in list:
        try:
            # 'spec_name' stand for specified name of the pictures
            if spec_name:
                urllib.urlretrieve(item['url'], save_dir + '%s.jpg' % spec_name + str(pre_spec_name))
                print_counting()
                pre_spec_name += 1
            else:
                urllib.urlretrieve(item['url'], save_dir + item['name'])
                print_counting()
        except IOError:
            print "You have no permission to save files in the specified path, Choose another path please."
            sys.exit(0)
        except KeyboardInterrupt:
            print "Download abort, existing..."
            sys.exit(0)


def save_picture(pic_url_list, spec_name, save_dir):

    border = len(pic_url_list) / MAX_THREADING

    threads = []
    i = 0
    while i < len(pic_url_list):
        t1 = threading.Thread(target=save_thread, args=(pic_url_list[i:border], spec_name, save_dir))
        threads.append(t1)
        i = border
        border += border

    for t in threads:
        t.start()
    for t in threads:
        t.join()


def main(opt='', url='', reg='', prefix='', file_dir='', spec_name='', save_dir=''):

    if opt == '1':
        content = get_html_content(url)
    else:
        content = get_file(file_dir)
    pic_url_list = get_picture_url(content, reg, prefix)
    save_picture(pic_url_list, spec_name, save_dir)
    print "Completed!"


if __name__ == '__main__':

    try:
        url = ''
        file_dir = ''
        try:
            from settings import *
            print "load setting file successfully."
        except IOError:
            print message['opt_msg']
            opt = raw_input("> ")
            if opt == '1':
                print message['url_msg']
                url = raw_input("> ")
            elif opt == '2':
                print message['file_dir_msg']
                file_dir = raw_input("> ")
            else:
                print "Error input!"
                sys.exit(1)

            if not (url or file_dir):
                print "Error input!"
                sys.exit(1)

            print message['reg_msg']
            reg = r'%s' % raw_input("> ")

            print message['prefix_msg']
            prefix = raw_input("> ")

            print message['save_dir_msg']
            save_dir = raw_input("> ")

            print message['spec_name_msg']
            spec_name = raw_input("> ")

        main(opt=opt, url=url, file_dir=file_dir, prefix=prefix, reg=reg, spec_name=spec_name, save_dir=save_dir)
    except KeyboardInterrupt:
        print "Bye."