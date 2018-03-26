from pprint import pprint

import requests
from urllib.parse import urlencode

# https://UlvacMoscow.github.io/
#
# Права:
#
# Создание счётчиков, изменение параметров своих и доверенных счётчиков
#
# Получение статистики, чтение параметров своих и доверенных счётчиков
#
# ID: e95478f3c0b84ac38835491d5af6dd1d
# Пароль: f2f90796f1d24ec182b0239381e832c7
# Callback URL: https://oauth.yandex.ru/verification_code

# APP_ID = 'e95478f3c0b84ac38835491d5af6dd1d'
# AUTH_URL = 'https://oauth.yandex.ru/authorize'
#
# auth_data = {
#     'response_type' : 'token',
#     'client_id' : APP_ID,
# }
#
# print('?'.join((AUTH_URL, urlencode(auth_data))))
#
TOKEN = 'AQAAAAAHPqQEAATpni9X1Yz75kDUtVIvdVxhrlE'
#
#
#
#
# params = {
#     'id' : counter_id,
#     'pretty' : 1,
#     'metrics' : 'ym:s:visits'
# }
#
# params = {
#     'oauth_token': TOKEN,
#     'pretty': 1,
# }
#
#
# response = requests.get('https://api-metrika.yandex.ru/stat/v1/data', params, headers=headers)
# pprint(response.json())
#
#


class YaBAse:
    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return  {
            'Authorization': 'OAuth {}'.format(self.token)
        }


class YaMetrikaUser(YaBAse):

    # def __init__(self,token):
    #     self.token = token

    def get_counters(self):
        headers = self.get_headers()
        response = requests.get('https://api-metrika.yandex.ru/management/v1/counters',
                                headers=headers)
        return [c['id'] for c in response.json()['counters']]
        # counter_id = response.json()['counters'][0]['id']


class Counter(YaBAse):

    def __init__(self, counter_id, token):
        self.counter_id = counter_id
        super().__init__(token)
        # self.token = token

    @property
    def visits(self):
        headers = self.get_headers()
        params = {
            'id' : self.counter_id,
            'metrics' : 'ym:s:visits'
        }
        response = requests.get('https://api-metrika.yandex.ru/stat/v1/data',
                                params, headers=headers)
        try:
            return response.json()['data'][0]['metrics'][0]
        except IndexError as e:
            return e


first_user = YaMetrikaUser(TOKEN)
counters = first_user.get_counters()
pprint(counters)
for counter_id in counters:
    counter = Counter(counter_id, first_user.token)
    visits = counter.visits
    print(visits)