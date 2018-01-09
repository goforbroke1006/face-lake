import time

__author__ = 'GoForBroke'

import json
import urllib2

vk_api_url = 'https://api.vk.com/method/'
version = '5.45'


def get_photos_tags_with_user(access_token, user_id, count=10):
    user_photos = get_user_photos(access_token, user_id, offset=0, count=count)
    if not user_photos:
        return []
    user_photo_tags_infos = []
    for photo in user_photos:
        time.sleep(0.25)
        tags = get_photo_tags(access_token, photo['owner_id'], photo['id'])
        for t in tags:
            if t["user_id"] == user_id:
                user_photo_tags_infos.append({
                    "src": get_biggest_photo_url(photo),
                    "x": t["x"],
                    "y": t["y"],
                    "x2": t["x2"],
                    "y2": t["y2"],
                })
                break
    return user_photo_tags_infos


def get_photo_tags(access_token, owner_id, photo_id):
    list = send(access_token, "photos.getTags", {"owner_id": owner_id, "photo_id": photo_id, })
    return list


def get_user_photos(access_token, user_id, offset=0, count=20, extended=False):
    result = send(access_token, "photos.getUserPhotos", {
        'user_id': user_id,
        'offset': offset,
        'count': count,
        'extended': int(extended),
    })
    if not result.has_key('items'):
        return False

    # urls = []
    # for photo in result['items']:
    #     urls.append(get_biggest_photo_url(photo))

    return result['items']


def get_avatars_list(access_token, owner_id, reverse_order=True):
    params = {
        'owner_id': owner_id,
        'album_id': 'profile',
        'rev': int(reverse_order),
    }
    res = send(access_token, 'photos.get', params)
    if not res.has_key('items'):
        return False
    urls = []
    for it in res['items']:
        urls.append(get_biggest_photo_url(it))

    return urls


def get_current_avatar_url(access_token, user_id):
    params = {'user_ids': user_id, 'fields': 'photo_max_orig'}
    response = send(access_token, 'users.get', params)
    return response[0]['photo_max_orig']


def get_friends(access_token, user_id):
    params = {'user_id': user_id, 'fields': 'photo_max_orig'}
    response = send(access_token, 'friends.get', params)
    return response['items']


def get_biggest_photo_url(photo_info):
    for ifn in ['photo_2560', 'photo_1280', 'photo_807', 'photo_604', 'photo_130', ]:
        if photo_info.has_key(ifn):
            return photo_info[ifn]


def send(access_token, method_name, params=()):
    params_list = []
    for k, v in params.iteritems():
        params_list.append("%s=%s" % (k, v))

    request_url = \
        vk_api_url + method_name \
        + '?v=%s&media_type=photo&access_token=%s' % (version, access_token) \
        + "&" \
        + "&".join(params_list)

    res = urllib2.urlopen(request_url)
    raw_response = res.read().decode('utf-8')

    json_data = json.loads(raw_response)
    if not json_data.has_key('response'):
        return dict()

    api_response = json_data['response']
    return api_response
