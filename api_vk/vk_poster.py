import requests
from vk_api import vk_api
from dotenv import load_dotenv
import os
import csv
import httplib2



def main():
    load_dotenv()
    vk_session = vk_api.VkApi(os.getenv('VK_LOGIN'), os.getenv('VK_PASS'))
    vk_session.auth()

    vk = vk_session.get_api()
    with open('simple.csv', 'r', encoding='utf-8') as f:
        fields = ['name', 'price', 'description', 'calories', 'picture', ]
        reader = csv.DictReader(f, fields, delimiter=';')
        for row in reader:
            available = os.path.exists(os.path.join('data', f'{row["name"]}.jpg'))
            if available:
                print('file exists')
                continue
            else:
                save_item_picture_from_web(row['picture'], row['name'])

            picture = set_item_picture(vk, os.path.join('data', f'{row["name"]}.jpg')) 
            vk.market.add(owner_id=f'-{os.getenv("GROUP_ID")}', name=row["name"],
                description=row['description'],
                category_id='1',
                price=float(row['price'].replace('$', '')),
                main_photo_id=picture[0]['id'],
                v='5.95')


def set_item_picture(vk, picture_path):
    photo_server = vk.photos.getMarketUploadServer(group_id=os.getenv('GROUP_ID'),
        main_photo='1')
    files = {'file': open(picture_path, 'rb')}
    response = requests.post(photo_server['upload_url'], files=files)
    multipart_picture = response.json()
    saved_picture = vk.photos.saveMarketPhoto(group_id=os.getenv('GROUP_ID'),
        server=multipart_picture['server'],
        photo=multipart_picture['photo'],
        crop_data=multipart_picture['crop_data'],
        crop_hash=multipart_picture['crop_hash'],
        hash=multipart_picture['hash'])
    return saved_picture


def save_item_picture_from_web(link, item_name):
    h = httplib2.Http('.cache')
    response, content = h.request(link)
    out = open(os.path.join('data', f'{item_name}.jpg'), 'wb')
    out.write(content)
    out.close()


if __name__ == '__main__':
    main()
