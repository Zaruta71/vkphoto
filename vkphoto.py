import requests
import datetime
import json

class VK:
    def __init__(self, token):
        #self.vktoken = '''vk1.a.RN0ySSkUZdM8hXar05BUsNBEpR22RpM2jkl9ENEGCpSnQIZ7helmVF4KtWvawUF14jRHRtCHk_kIh7rvaKr6ZJ_DSROtC47Hz4qa5c
        #                -L8htPrcNrUk96fCg7PMTjot8EMuEbYtjQz-T7jCCSx2e_PAZ20fwvj3KBpmHfmHZJXwZUI98JLQz7nTTCO8s1BvjpCZFWckVfQ-iMb5tUIdAu8g'''
        self.vktoken = token

    def get_photo_data(self, userid):
        url = 'https://api.vk.com/method/photos.get'
        params = {
            'owner_id': userid,
            'album_id': 'profile',
            'extended': '1',
            'access_token': self.vktoken,
            'v': '5.131'
        }
        res = requests.get(url, params=params).json()
        res = res['response']['items']

        data_list = []
        like_check = []

        for item in res:
            temporary_dict = {}
            if item['likes']['count'] in like_check:
                temporary_dict['name'] = f"{datetime.datetime.fromtimestamp(item['date']).strftime('%Y-%m-%d')}.jpg"
            else:
                temporary_dict['name'] = str(f"{item['likes']['count']}.jpg")
            like_check.append(item['likes']['count'])
            for size in item['sizes']:
                if size['type'] == 'z':
                    temporary_dict['photo_url'] = size['url']
                    temporary_dict['size'] = 'z'
            data_list.append(temporary_dict)
        return data_list


class Yandex:
    def __init__(self, token):
        self.token = token
        self.headers = {'Authorization': f'OAuth {self.token}'}

    def create_folder(self, folder_name):
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        params = {'path': folder_name}
        response = requests.put(url, headers=self.headers, params=params)

    def upload_photo(self, url, folder_name, file_name):
        response = requests.get(url)

        upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        params = {
            'path': f'{folder_name}/{file_name}',
            'url': url
        }
        response = requests.post(upload_url, headers=self.headers, params=params)
        print(response)

if __name__ == '__main__':
    #yatoken = 'y0_AgAAAAAmu9C9AAooZQAAAADnYiPSy8UuTf1ITP6fVO0oD1F2YK35UUQ'

    with open('vk_token.txt', 'r') as file:
        vk_token = file.read().strip()

    with open('yandex_token.txt', 'r') as file:
        ya_token = file.read().strip()

    #ya_token = input('Введите yandex токен: ')
    
    vk_id = input('Введите vk id: ')
    

    vk_test = VK(vk_token)
    ya_disk = Yandex(ya_token)

    ya_disk.create_folder('vk_pfp')

    data = vk_test.get_photo_data(vk_id)
    print(data)

    result = []
    for item in data:
        ya_disk.upload_photo(item['photo_url'], 'vk_pfp', item['name'])
        temp_dict = {
            'file_name': item['name'],
            'size': item['size']
            }
        result.append(temp_dict)
    json_result = json.dumps(result, indent=3)

    with open('json_data.json', 'w') as file:
        file.write(json_result)

    print('Программа завершена')
