import csv
import os

from dotenv import load_dotenv
import dropbox
from lxml import etree
from typing import Optional, List
import requests


def main():
    load_dotenv()
    dbx = dropbox.Dropbox(os.getenv('DROPBOX_KEY'))
    try:
        xml_files_list = get_xml_files_list(dbx, os.getenv('FOLDERNAME'))
    except requests.exceptions.ConnectionError:
        print('Connection problem')
        return False
    if xml_files_list:
        parsed_xml_data = parse_xml_files(dbx, xml_files_list)
        prepared_data = prepare_xml_data_to_save(parsed_xml_data)
        for xml_file in xml_files_list:
            save_data_as_csv(xml_file, prepared_data)


def get_xml_files_list(dbx, foldername: str) -> Optional[List[str]]:
    try:
        xml_folder = dbx.files_list_folder(f'/{foldername}').entries
        xml_files_list = [xml_file.name for xml_file in xml_folder]
    except (dropbox.stone_validators.ValidationError):
        print(f'Foldername did not match pattern')
        return None
    except (dropbox.exceptions.ApiError):
        print('Foldername is incorrect')
        return None
    except (dropbox.exceptions.AuthError):
        print('Failed authorization. Check token')
        return None
    except (dropbox.exceptions.BadInputError):
        print('Bad access token')
        return None
    except FileNotFoundError:
        print('Folder is empty')
        return None
    if not xml_files_list:
        print('Folder is empty')
        return None
    return xml_files_list


def parse_xml_files(dbx, xml_files_list: List[str]) -> Optional[List]:
    if xml_files_list:
        parsed_files_data_list = []
        for xml_file in xml_files_list:
            basedir = os.path.join(os.altsep, f'{os.getenv("FOLDERNAME")}')
            filepath_template = os.path.join(basedir, f'{xml_file}')
            filepath_template = filepath_template.replace(os.sep, os.altsep)
            metadata, file_content = dbx.files_download(filepath_template)
            parsed_files_elements = (metadata, file_content)
            parsed_files_data_list.append(parsed_files_elements)
        return parsed_files_data_list


def prepare_xml_data_to_save(parsed_files_data_list: List) -> Optional[List]:
    if parsed_files_data_list:
        cd_data = []
        for file_data in parsed_files_data_list:
            metadata, file_content = file_data
            try:
                root = etree.fromstring(file_content.content)
                
                for element in root.getchildren():
                    cd_data.append({
                        'title': element.find('TITLE').text,
                        'artist': element.find('ARTIST').text,
                        'country': element.find('COUNTRY').text,
                        'company': element.find('COMPANY').text,
                        'price': element.find('PRICE').text,
                        'year': element.find('YEAR').text,
                        })
            except (etree.XMLSyntaxError):
                print('Bad XML syntax')
                return None
        return cd_data


def save_data_as_csv(xml_file_name: str, prepared_data: List) -> None:
    if prepared_data:
        fields = ['title', 'artist', 'country', 'company', 'price', 'year', ]
        filename, file_extension = os.path.splitext(xml_file_name)
        with open(f'{filename}.csv', 'w', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fields, delimiter=';')
            writer.writeheader()
            for cd in prepared_data:
                writer.writerow(cd)


if __name__ == '__main__':
    main()