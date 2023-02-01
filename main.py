"""-----------------------------------------------Task 1------------------------------------------------"""
import requests
url = 'https://akabab.github.io/superhero-api/api/all.json'

response = requests.get(url)
response = response.json()

hero_intelligence = {}

for i in range(len(response)):
    if response[i]['name'] == 'Hulk' or \
            response[i]['name'] == 'Captain America' or \
                response[i]['name'] == 'Thanos':
        hero_intelligence.update({response[i]['name']: response[i]['powerstats']['intelligence']})

hero_intelligence = {k: hero_intelligence[k] for k in
                     sorted(hero_intelligence, key=hero_intelligence.get, reverse=True)}

print(hero_intelligence)

"""-----------------------------------------------------------------------------------------------------"""


"""-----------------------------------------------Task 2------------------------------------------------"""
import requests
import os

class YaUploader:
    host = 'https://cloud-api.yandex.net/'
    def __init__(self, token: str):
        self.token = token

    def get_headers(self):
        return {'Content-Type': 'application/json', 'Authorization': f'OAuth {self.token}'}

    def get_upload_link(self, path_to_file):
        uri = 'v1/disk/resources/upload'
        url = self.host + uri
        params = {'path': f'/{path_to_file}'}
        response = requests.get(url, headers=self.get_headers(), params=params)
        return response.json()['href']

    def upload(self, file_path: str):
        file_name = self.split_file_name(file_path)
        uplad_link = self.get_upload_link(file_name)
        response = requests.put(uplad_link, headers=self.get_headers(), data=open(file_path, 'rb'))
        print(response.status_code)
        if response.status_code == 201:
            print('Загрузка прошла успешно')

    def split_file_name(self, file_path: str):
        try:
            try:
                return file_path.split('\\')[-1]
            except:
                return file_path.split('/')[-1]
        except:
            return file_path

def check_file():
    while True:
        path_to_file = input('Введите путь к загружаемому файлу:\n')
        if os.path.isfile(path_to_file) == True:
            break
        print(f'Файла - {path_to_file.upper()} не существует!')
    return path_to_file

if __name__ == '__main__':
    path_to_file = check_file()
    token = input('Введите токен:\n')
    uploader = YaUploader(token)
    result = uploader.upload(path_to_file)

"""-----------------------------------------------------------------------------------------------------"""


"""-----------------------------------------------Task 3------------------------------------------------"""
import requests
from datetime import datetime, timedelta
today = datetime.now()

two_day_ago = today.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=2)

today = int(today.timestamp())
two_day_ago = int(two_day_ago.timestamp())

page_number = 1
count = 1
while True:
    url = f'https://api.stackexchange.com/2.3/questions?' \
          f'page={page_number}&' \
          f'pagesize=100&' \
          f'fromdate={two_day_ago}&' \
          f'todate={today}&' \
          f'order=desc&' \
          f'sort=creation&' \
          f'tagged=python&' \
          f'site=stackoverflow'

    headers = {'user-agent': 'my-app/0.0.1'}
    response = requests.get(url, headers=headers)
    response = response.json()
    try:
        for i in response['items']:
            print(datetime.fromtimestamp(i['creation_date']), i['title'], i['link'])
            count += 1
        page_number += 1
        if response['has_more'] == False:
            break
    except:
        break

print(f'Найдено {count} вопросов.')

"""-----------------------------------------------------------------------------------------------------"""