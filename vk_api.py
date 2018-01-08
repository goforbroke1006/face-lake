__author__ = 'GoForBroke'

ORDER_ASC = 0
ORDER_DESC = 1

IMAGES_FIELD_NAMES = ['photo_2560', 'photo_1280', 'photo_807', 'photo_604', ]

import json
import urllib2

vk_api_url = 'https://api.vk.com/method/'
version = '5.45'


def get_avatars_list(access_token, owner_id):
    params = {'owner_id': owner_id, 'album_id': 'profile', 'rev': ORDER_DESC}
    res = send(access_token, 'photos.get', params)
    if not res.has_key('items'):
        return False
    items = res['items']
    urls = []
    for it in items:
        for ifn in IMAGES_FIELD_NAMES:
            if it.has_key(ifn):
                max_size_img_url = it[ifn]
                urls.append(max_size_img_url)
                break

    return urls


def get_current_avatar_url(access_token, user_id):
    params = {'user_ids': user_id, 'fields': 'photo_max_orig'}
    response = send(access_token, 'users.get', params)
    return response[0]['photo_max_orig']


def get_friends(access_token, user_id):
    params = {'user_id': user_id, 'fields': 'photo_max_orig'}
    response = send(access_token, 'friends.get', params)
    return response['items']


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
