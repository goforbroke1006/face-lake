import sys
import urllib2

import os
import unicodecsv as csv
import vk_api
import face_detector

access_token = sys.argv[1]
user_id = sys.argv[2]

with open('face-lake.csv', 'w') as csv_file:
    writer = csv.writer(csv_file, encoding='utf-8')
    writer.writerow(['id', 'shape'])

    friends = vk_api.get_friends(access_token, user_id)
    for friend in friends:
        photo_url = friend['photo_max_orig']

        if "https://vk.com/images/" in photo_url:
            continue

        tmp_image_path = photo_url.replace("https://pp.userapi.com/", "tmp/")

        if not os.path.isfile(tmp_image_path):
            tmp_dir = tmp_image_path.split("/")
            tmp_dir = "/".join(tmp_dir[:-1])
            if not os.path.isdir(tmp_dir):
                os.makedirs(tmp_dir)

            print "Download: " + photo_url

            request = urllib2.Request(photo_url)
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
            photo_url
        )
