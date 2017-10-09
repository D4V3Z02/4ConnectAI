from enum import Enum
import requests
import logging


class GameStatus(Enum):
    WAITING = 'WAITING'
    PLAYING = 'PLAYING'
    FINISHED = 'FINISHED'


class GameWinner(Enum):
    RED = 'RED'
    YELLOW = 'YELLOW'


class CFMSClient:
    def __init__(self, endpoint):
        logging.info('Initializing master server client')

        self.endpoint = endpoint

    def _call(self, method, resource, params=None, json=None):
        url = self.endpoint + resource

        headers = {
            'User-Agent': 'CFMS Client'
        }

        response = requests.request(method, url, params=params, json=json, headers=headers)

        logging.info('Master server: {} ({} {})'.format(response.status_code, method, resource))

        response.raise_for_status()

        return response.json()

    def get_games(self, version):
        params = {
            'version': version
        }

        return self._call('GET', 'games', params=params)

    def create_game(self, name, version):
        json = {
            'name': name,
            'version': version
        }

        return self._call('POST', 'games', json=json)

    def get_game(self, id):
        return self._call('GET', 'games/{}'.format(id))

    def update_game(self, id, token, status=None, name=None, version=None, winner=None):
        json = {
            'token': token
        }

        if status:
            valid_statuses = [GameStatus.PLAYING, GameStatus.FINISHED]

            if status not in valid_statuses:
                raise ValueError('Invalid status. It can be one of: {}'.format(', '.join([s for s in valid_statuses])))

            json['status'] = status.value

        if name:
            json['name'] = name

        if version:
            json['version'] = version

        if winner:
            if winner not in GameWinner:
                raise ValueError('Invalid winner. It can be one of: {}'.format(', '.join([w for w in GameWinner])))

            json['winner'] = winner.value

        return self._call('PUT', 'games/{}'.format(id), json=json)

    def delete_game(self, id, token):
        json = {
            'token': token
        }

        return self._call('DELETE', 'games/{}'.format(id), json=json)
