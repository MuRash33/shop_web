import csv
import os

from dotenv import load_dotenv
import dropbox
from lxml import etree
from typing import Union, List, Any
import requests


def main():
    load_dotenv()
    dbx = dropbox.Dropbox(os.getenv('DROPBOX_KEY'))
    try:
        xml_files_list = get_xml_files_list(dbx, os.getenv('FILEPATH'))
    except (requests.exceptions.ConnectionError):
        print('Connection problem')
        return False
    if xml_files_list:
        for xml_file in xml_files_list:
            xml_tree_template = f'/{os.getenv("FILEPATH")}/{xml_file}'
            metadata, file_content = dbx.files_download(xml_tree_template)
            xml_to_csv_parser(xml_file, file_content.content)


def get_xml_files_list(dbx, foldername: str) -> Union[bool, List[str]]:
    try:
        xml_folder = dbx.files_list_folder(f'/{foldername}').entries
        xml_files_list = [xml_file.name for xml_file in xml_folder]
    except (dropbox.stone_validators.ValidationError):
        print(f'Foldername did not match pattern')
        return False
    except (dropbox.exceptions.ApiError):
        print('Foldername is incorrect')
        return False
    except (dropbox.exceptions.AuthError):
        print('Failed authorization. Check token')
        return False
    except (dropbox.exceptions.BadInputError):
        print('Bad access token')
        return False
    except FileNotFoundError:
        print('Folder is empty')
        return False
    if not xml_files_list:
        print('Folder is empty')
        return False
    return xml_files_list


def xml_to_csv_parser(xml_file_name: str, xml_file_content: bytes) -> Any:
    try:
        root = etree.fromstring(xml_file_content)
        filename, file_extension = os.path.splitext(xml_file_name)
        fields = ['title', 'artist', 'country', 'company', 'price', 'year', ]
        if file_extension == '.xml':
            with open(f'{filename}.csv', 'w', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fields, delimiter=';')
                writer.writeheader()

                cd_data = []
                for element in root.getchildren():
                    cd_data.append({
                        'title': element.find('TITLE').text,
                        'artist': element.find('ARTIST').text,
                        'country': element.find('COUNTRY').text,
                        'company': element.find('COMPANY').text,
                        'price': element.find('PRICE').text,
                        'year': element.find('YEAR').text,
                        })
                for cd in cd_data:
                    writer.writerow(cd)
            print('File parsed')
        else:
            print('This file isn\'t XML')
    except (etree.XMLSyntaxError):
        print('Bad XML syntax')
        return False


if __name__ == '__main__':
    main()
