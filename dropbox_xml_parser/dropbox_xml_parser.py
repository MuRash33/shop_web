from requests import exceptions

import dropbox
from lxml import etree

from sw_app import config


def main():
    dbx = dropbox.Dropbox(config.DROPBOX_KEY)
    xml_file = get_xml_file(dbx, config.FILEPATH)
    xml_parser(xml_file)
    

def get_xml_file(dbx, filepath):
    try:
        metadata, file_content = dbx.files_download(filepath)
    except (dropbox.exceptions.ApiError, dropbox.exceptions.BadInputError, exceptions.ConnectionError):
        print('Connection Error, incorrect filepath or bad access token')
        return False 
    xml_data = file_content.content
    return xml_data


def xml_parser(xml_file):
    if xml_file:
        root = etree.fromstring(xml_file)
        for appt in root.getchildren():
            for element in appt.getchildren():
                if not element.text:
                    text = "None"
                else:
                    text = element.text
                
                print(element.tag + " => " + text)
            print()


if __name__ == '__main__':
    main()