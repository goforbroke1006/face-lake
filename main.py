import sys
import os

import urllib2

import time
import unicodecsv as csv
from PIL import Image

import vk_api
import face_detector

access_token = sys.argv[1]
user_id = sys.argv[2]


def save_image(url):
    tmp_image_path = url.replace("https://pp.userapi.com/", "tmp/")

    if not os.path.isfile(tmp_image_path):
        tmp_dir = tmp_image_path.split("/")
        tmp_dir = "/".join(tmp_dir[:-1])
        if not os.path.isdir(tmp_dir):
            os.makedirs(tmp_dir)

        # print "Download: " + url

        request = urllib2.Request(url)
        try:
            img = urllib2.urlopen(request).read()
        except urllib2.HTTPError as e:
            return False
        except urllib2.URLError:
            time.sleep(4)
            img = urllib2.urlopen(request).read()

        f = open(tmp_image_path, 'w')
        f.write(img)
        f.close()

        return tmp_image_path


with open('face-lake-%s.csv' % user_id, 'w') as csv_file:
    writer = csv.writer(csv_file, encoding='utf-8')
    writer.writerow(['id', 'shape'])

    friends = vk_api.get_friends(access_token, user_id)
    for friend in friends:
        # avatars = vk_api.get_avatars_list(access_token, friend['id'])
        # if not avatars:
        #     time.sleep(4)
        #     avatars = vk_api.get_avatars_list(access_token, friend['id'])
        #
        # for ava_url in avatars:
        #     if "https://vk.com/images/" in ava_url:
        #         continue
        #
        #     tmp_image_path = save_image(ava_url)
        #     if not tmp_image_path:
        #         continue
        #
        #     faces = face_detector.get_faces(tmp_image_path)
        #     if len(faces) == 0 or len(faces) > 1:
        #         continue
        #
        #     writer.writerow([
        #         friend['id'],
        #         ",".join(str(x) for x in faces[0]),
        #     ])
        #
        #     print "%d %s %s %s" % (
        #         friend['id'],
        #         friend['last_name'], friend['first_name'],
        #         ava_url
        #     )

        photos_tags = vk_api.get_photos_tags_with_user(access_token, friend['id'])
        for pt in photos_tags:
            tmp_image_path = save_image(pt['src'])
            if not tmp_image_path:
                continue
            img = Image.open(tmp_image_path)
            w, h = img.size
            img.crop((
                pt["x"] * w,
                pt["y"] * h,
                (pt["x2"] - pt["x"]) / 100 * w,
                (pt["y2"] - pt["y"]) / 100 * h
            )).save(tmp_image_path)
