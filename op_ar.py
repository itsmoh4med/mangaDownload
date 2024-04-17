import requests
import os
import re
from bs4 import BeautifulSoup
from prompt_toolkit.shortcuts import checkboxlist_dialog
from prompt_toolkit.styles import Style

def get_arabic_chapters(url):
    response = requests.get(url)
    if response.status_code != 200:
        return None
    soup = BeautifulSoup(response.content, 'html.parser')
    pattern = re.compile(r'https://3asq.org/manga/one-piece/\d+/')
    chapters = soup.find_all('a', href=pattern)
    available_chapters = []
    for chapter in chapters:
        chapter_number = chapter.text.lstrip('\n').split()[0]
        available_chapters.append(chapter_number)
    return available_chapters

def download_chapter_ara(chapter_number):
    print(f'The download of chapter {chapter_number} is in progress...')
    save_folder = f'chapter {chapter_number}'
    url = f'https://3asq.org/manga/one-piece/{chapter_number}/'
    response = requests.get(url)
    if response.status_code != 200:
        print('Failed to download the chapter')
    else:
        soup = BeautifulSoup(response.content, 'html.parser')
        img_list = [img['src'] for img in soup.find_all('img', src=True)]
        img_list = [s.lstrip('\t\n') for s in img_list]

        os.makedirs(save_folder, exist_ok=True)

        for idx, image_url in enumerate(img_list, start=1):
            res = requests.get(image_url)
            img_name = os.path.basename(image_url)
            img_path = os.path.join(save_folder, img_name)
            with open(img_path, 'wb') as img_file:
                img_file.write(res.content)
            print(f'Page {idx} downloaded and saved')
        print(f'Chapter {chapter_number} Downloaded successfully')

arabic = 'https://3asq.org/manga/one-piece/'

available_chapters = get_arabic_chapters(arabic)


def show_menu(list_of_options):
    options = [(value, f'Chapter {value}') for value in list_of_options]

    result = checkboxlist_dialog(
        title='Select chapters',
        text='',
        values=options,
        style=Style.from_dict({
            'dialog': 'bg:#004400',
            'button': 'bg:#00ff00',
            'selected-button': 'bg:#004400',
        })
    ).run()

    return result


def main():
    while True:
        choices = show_menu(available_chapters)
        return choices

if __name__ == '__main__':
    chapters = main()
    if chapters is not None:
        for chapter in chapters:
            download_chapter_ara(chapter)