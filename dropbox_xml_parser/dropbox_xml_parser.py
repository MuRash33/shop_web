import csv
import os

from dotenv import load_dotenv
import dropbox
from lxml import etree
<<<<<<< HEAD

from sw_app import config
=======
from requests import exceptions
>>>>>>> bd5b5ac9d89c5cda6650c73451c185a739ad9917


def main():
    load_dotenv()
    dbx = dropbox.Dropbox(os.getenv('DROPBOX_KEY'))
    xml_files_list = get_xml_files_list(dbx, os.getenv('FILEPATH'))
    if xml_files_list:
        for xml_file in xml_files_list:
            metadata, file_content = dbx.files_download(f'/{os.getenv("FILEPATH")}/{xml_file}')
            xml_to_csv_parser(xml_file, file_content.content)
    

def get_xml_files_list(dbx, foldername):
    try:
        xml_folder = dbx.files_list_folder(f'/{foldername}').entries
        xml_files_list = [xml_file.name for xml_file in xml_folder]
    except (dropbox.stone_validators.ValidationError):
        print(f'Foldername did not match pattern')
        return False
    except (dropbox.exceptions.ApiError):
        print('Foldername is incorrect')
        return False
    except (exceptions.ConnectionError):
        print('Connection Error')
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


def xml_to_csv_parser(xml_file_name, xml_file_content):
    try:
        root = etree.fromstring(xml_file_content)
        filename, file_extension = os.path.splitext(xml_file_name)
        if file_extension == '.xml':
            with open(f'{filename}.csv', 'w', encoding='utf-8') as f:
                fields = ['title', 'artist', 'country', 'company', 'price', 'year', ]
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