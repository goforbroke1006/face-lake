__author__ = 'GoForBroke'

import json
import urllib2

vk_api_url = 'https://api.vk.com/method/'
version = '5.45'


def get_current_avatar_url(access_token, user_id):
    params = {'user_ids': user_id, 'fields': 'photo_max_orig'}
    response = send(access_token, 'users.get', params)
    return response[0]['photo_max_orig']


def get_friends(access_token, user_id):
    params = {'user_ids': user_id, 'fields': 'photo_max_orig'}
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
    api_response = json.loads(raw_response)['response']
    return api_response
