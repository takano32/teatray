# Copyright 2014 Oktay Sancak
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import cgi
import json

import requests

from slacker.utils import get_item_id_by_name


API_BASE_URL = 'https://slack.com/api/{api}'


__all__ = ['Error', 'Response', 'BaseAPI', 'API', 'Auth', 'Users', 'Groups',
           'Channels', 'Chat', 'IM', 'Search', 'Files', 'Stars', 'Emoji',
           'Presence', 'RTM', 'Team', 'OAuth', 'Slacker']


class Error(Exception):
    pass


class Response(object):
    def __init__(self, body):
        self.raw = body
        self.body = json.loads(body)
        self.successful = self.body['ok']
        self.error = self.body.get('error')


class BaseAPI(object):
    def __init__(self, token=None):
        self.token = token

    def _request(self, method, api, **kwargs):
        if self.token:
            kwargs.setdefault('params', {})['token'] = self.token

        response = method(API_BASE_URL.format(api=api),
                          **kwargs)

        assert response.status_code == 200

        response = Response(response.text)
        if not response.successful:
            raise Error(response.error)

        return response

    def get(self, api, **kwargs):
        return self._request(requests.get, api, **kwargs)

    def post(self, api, **kwargs):
        return self._request(requests.post, api, **kwargs)


class API(BaseAPI):
    def test(self, error=None, **kwargs):
        if error:
            kwargs['error'] = error

        return self.get('api.test', params=kwargs)


class Auth(BaseAPI):
    def test(self):
        return self.get('auth.test')


class Users(BaseAPI):
    def info(self, user):
        return self.get('users.info', params={'user': user})

    def list(self):
        return self.get('users.list')

    def set_active(self):
        return self.post('users.setActive')

    def get_presence(self, user):
        return self.get('users.getPresence', params={'user': user})

    def set_presence(self, presence):
        assert presence in Presence.TYPES, 'Invalid presence type'
        return self.post('users.setPresence', params={'presence': presence})

    def get_user_id(self, user_name):
        members = self.list().body['members']
        return get_item_id_by_name(members, user_name)


class Groups(BaseAPI):
    def create(self, name):
        return self.post('groups.create', params={'name': name})

    def create_child(self, channel):
        return self.post('groups.createChild', params={'channel': channel})

    def list(self, exclude_archived=None):
        return self.get('groups.list',
                        params={'exclude_archived': exclude_archived})

    def history(self, channel, latest=None, oldest=None, count=None):
        return self.get('groups.history',
                        params={
                            'channel': channel,
                            'latest': latest,
                            'oldest': oldest,
                            'count': count
                        })

    def invite(self, channel, user):
        return self.post('groups.invite',
                         params={'channel': channel, 'user': user})

    def kick(self, channel, user):
        return self.post('groups.kick',
                         params={'channel': channel, 'user': user})

    def leave(self, channel):
        return self.post('groups.leave', params={'channel': channel})

    def mark(self, channel, ts):
        return self.post('groups.mark', params={'channel': channel, 'ts': ts})

    def rename(self, channel, name):
        return self.post('groups.rename',
                         params={'channel': channel, 'name': name})

    def archive(self, channel):
        return self.post('groups.archive', params={'channel': channel})

    def unarchive(self, channel):
        return self.post('groups.unarchive', params={'channel': channel})

    def open(self, channel):
        return self.post('groups.open', params={'channel': channel})

    def close(self, channel):
        return self.post('groups.close', params={'channel': channel})

    def set_purpose(self, channel, purpose):
        return self.post('groups.setPurpose',
                         params={'channel': channel, 'purpose': purpose})

    def set_topic(self, channel, topic):
        return self.post('groups.setTopic',
                         params={'channel': channel, 'topic': topic})


class Channels(BaseAPI):
    def create(self, name):
        return self.post('channels.create', params={'name': name})

    def info(self, channel):
        return self.get('channels.info', params={'channel': channel})

    def list(self, exclude_archived=None):
        return self.get('channels.list',
                        params={'exclude_archived': exclude_archived})

    def history(self, channel, latest=None, oldest=None, count=None):
        return self.get('channels.history',
                        params={
                            'channel': channel,
                            'latest': latest,
                            'oldest': oldest,
                            'count': count
                        })

    def mark(self, channel, ts):
        return self.post('channels.mark',
                         params={'channel': channel, 'ts': ts})

    def join(self, name):
        return self.post('channels.join', params={'name': name})

    def leave(self, channel):
        return self.post('channels.leave', params={'channel': channel})

    def invite(self, channel, user):
        return self.post('channels.invite',
                         params={'channel': channel, 'user': user})

    def kick(self, channel, user):
        return self.post('channels.kick',
                         params={'channel': channel, 'user': user})

    def rename(self, channel, name):
        return self.post('channels.rename',
                         params={'channel': channel, 'name': name})

    def archive(self, channel):
        return self.post('channels.archive', params={'channel': channel})

    def unarchive(self, channel):
        return self.post('channels.unarchive', params={'channel': channel})

    def set_purpose(self, channel, purpose):
        return self.post('channels.setPurpose',
                         params={'channel': channel, 'purpose': purpose})

    def set_topic(self, channel, topic):
        return self.post('channels.setTopic',
                         params={'channel': channel, 'topic': topic})

    def get_channel_id(self, channel_name):
        channels = self.list().body['channels']
        return get_item_id_by_name(channels, channel_name)


class Chat(BaseAPI):
    def post_message(self, channel, text, username=None, as_user=None, parse=None,
                     link_names=None, attachments=None, unfurl_links=None,
                     icon_url=None, icon_emoji=None):
        return self.post('chat.postMessage',
                         params={
                             'channel': channel,
                             'text': cgi.escape(text),
                             'username': username,
                             'as_user': as_user,
                             'parse': parse,
                             'link_names': link_names,
                             'attachments': attachments,
                             'unfurl_links': unfurl_links,
                             'icon_url': icon_url,
                             'icon_emoji': icon_emoji
                         })

    def update(self, channel, ts, text):
        self.post('chat.update',
                  params={'channel': channel, 'ts': ts, 'text': cgi.escape(text)})

    def delete(self, channel, ts):
        self.post('chat.delete', params={'channel': channel, 'ts': ts})


class IM(BaseAPI):
    def list(self):
        return self.get('im.list')

    def history(self, channel, latest=None, oldest=None, count=None):
        return self.get('im.history',
                        params={
                            'channel': channel,
                            'latest': latest,
                            'oldest': oldest,
                            'count': count
                        })

    def mark(self, channel, ts):
        return self.post('im.mark', params={'channel': channel, 'ts': ts})

    def open(self, user):
        return self.post('im.open', params={'user': user})

    def close(self, channel):
        return self.post('im.close', params={'channel': channel})


class Search(BaseAPI):
    def all(self, query, sort=None, sort_dir=None, highlight=None, count=None,
            page=None):
        return self.get('search.all',
                        params={
                            'query': query,
                            'sort': sort,
                            'sort_dir': sort_dir,
                            'highlight': highlight,
                            'count': count,
                            'page': page
                        })

    def files(self, query, sort=None, sort_dir=None, highlight=None,
              count=None, page=None):
        return self.get('search.files',
                        params={
                            'query': query,
                            'sort': sort,
                            'sort_dir': sort_dir,
                            'highlight': highlight,
                            'count': count,
                            'page': page
                        })

    def messages(self, query, sort=None, sort_dir=None, highlight=None,
                 count=None, page=None):
        return self.get('search.messages',
                        params={
                            'query': query,
                            'sort': sort,
                            'sort_dir': sort_dir,
                            'highlight': highlight,
                            'count': count,
                            'page': page
                        })


class Files(BaseAPI):
    def list(self, user=None, ts_from=None, ts_to=None, types=None,
             count=None, page=None):
        return self.get('files.list',
                        params={
                            'user': user,
                            'ts_from': ts_from,
                            'ts_to': ts_to,
                            'types': types,
                            'count': count,
                            'page': page
                        })

    def info(self, file_, count=None, page=None):
        return self.get('files.info',
                        params={'file': file_, 'count': count, 'page': page})

    def upload(self, file_, filetype=None, filename=None, title=None,
               initial_comment=None, channels=None):
        with open(unicode(file_, 'utf-8'), 'rb') as f:
            if isinstance(channels, (tuple, list)):
                channels = ','.join(channels)

            return self.post('files.upload',
                             params={
                                 'filetype': filetype,
                                 'filename': filename,
                                 'title': title,
                                 'initial_comment': initial_comment and cgi.escape(initial_comment),
                                 'channels': channels
                             },
                             files={'file': f})

    def delete(self, file_):
        return self.post('files.delete', params={'file': file_})


class Stars(BaseAPI):
    def list(self, user=None, count=None, page=None):
        return self.get('stars.list',
                        params={'user': user, 'count': count, 'page': page})


class Emoji(BaseAPI):
    def list(self):
        return self.get('emoji.list')


class Presence(BaseAPI):
    AWAY = 'away'
    ACTIVE = 'active'
    TYPES = (AWAY, ACTIVE)

    def set(self, presence):
        assert presence in Presence.TYPES, 'Invalid presence type'
        return self.post('presence.set', params={'presence': presence})


class RTM(BaseAPI):
    def start(self):
        return self.get('rtm.start')


class Team(BaseAPI):
    def info(self):
        return self.get('team.info')

    def access_logs(self, count=None, page=None):
        return self.get('team.accessLogs',
                        params={'count': count, 'page': page})


class OAuth(BaseAPI):
    def access(self, client_id, client_secret, code, redirect_uri=None):
        return self.post('oauth.access',
                         params={
                             'client_id': client_id,
                             'client_secret': client_secret,
                             'code': code,
                             'redirect_uri': redirect_uri
                         })


class Slacker(object):
    oauth = OAuth()

    def __init__(self, token):
        self.im = IM(token=token)
        self.api = API(token=token)
        self.rtm = RTM(token=token)
        self.auth = Auth(token=token)
        self.chat = Chat(token=token)
        self.team = Team(token=token)
        self.users = Users(token=token)
        self.files = Files(token=token)
        self.stars = Stars(token=token)
        self.emoji = Emoji(token=token)
        self.search = Search(token=token)
        self.groups = Groups(token=token)
        self.channels = Channels(token=token)
        self.presence = Presence(token=token)
