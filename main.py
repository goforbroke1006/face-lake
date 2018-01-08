import sys
import os

import urllib2

import time
import unicodecsv as csv
import vk_api
import face_detector

access_token = sys.argv[1]
user_ids = sys.argv[2].split(',')

with open('face-lake-%d.csv' % time.time(), 'w') as csv_file:
    writer = csv.writer(csv_file, encoding='utf-8')
    writer.writerow(['id', 'shape'])

    for uid in user_ids:
        friends = vk_api.get_friends(access_token, uid)
        for friend in friends:
            avatars = vk_api.get_avatars_list(access_token, friend['id'])
            if False == avatars:
                time.sleep(4)
                avatars = vk_api.get_avatars_list(access_token, friend['id'])

            for ava_url in avatars:
                if "https://vk.com/images/" in ava_url:
                    continue

                tmp_image_path = ava_url.replace("https://pp.userapi.com/", "tmp/")

                if not os.path.isfile(tmp_image_path):
                    tmp_dir = tmp_image_path.split("/")
                    tmp_dir = "/".join(tmp_dir[:-1])
                    if not os.path.isdir(tmp_dir):
                        os.makedirs(tmp_dir)

                    print "Download: " + ava_url

                    request = urllib2.Request(ava_url)
                    try:
                        img = urllib2.urlopen(request).read()
                    except urllib2.URLError:
                        time.sleep(4)
                        img = urllib2.urlopen(request).read()

                    f = open(tmp_image_path, 'w')
                    f.write(img)
                    f.close()

                faces = face_detector.get_faces(tmp_image_path)
                if len(faces) == 0 or len(faces) > 1:
                    continue

                writer.writerow([
                    friend['id'],
                    ",".join(str(x) for x in faces[0]),
                ])

                print "%d %s %s %s" % (
                    friend['id'],
                    friend['last_name'], friend['first_name'],
                    ava_url
                )
