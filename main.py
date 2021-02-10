from googletrans import Translator
from google_speech import Speech
import os
import requests
import re
SAMPLE_TXT_NAME= 'sample.txt'
RECORD_FOLDER ='recording'
IMAGE_FOLDER='images'
# I don't know how to get images from google images, but getting images from Unsplash site was quiet easy
GOOGLE_IMAGE = 'https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&'
STOCK_IMAGE='https://unsplash.com/s/photos/'
usr_agent = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive',
}

src="cs"
dest ="en"

def download_records(wordsArray):
    if not os.path.exists(RECORD_FOLDER):
        os.mkdir(RECORD_FOLDER)
    for word in wordsArray[0]:
        speach=Speech(word,src)
        print("Recoring for {start} : downloading mp3 and saving it in {folder}/{name}.jpg".format(
            start=word,
             folder=RECORD_FOLDER, name=word))

        speach.save("{}/{}.mp3".format(RECORD_FOLDER,word))


def download_images(links,wordsArray):
    for i,link in enumerate(links):
        word=wordsArray[0][i]
        response = requests.get(link, headers=usr_agent)
        html = response.text
        regex = r"https:\/\/images\.unsplash\.com\/photo-[^;]*"
        matches = re.search(regex, html, re.MULTILINE)
        if matches:
            print("Match was found for {start} : {match} downloading image and saving it in {folder}/{name}.jpg".format(start=word,
                                                                     match=matches.group(),folder=IMAGE_FOLDER,name=word))
            response = requests.get(matches.group())
            file = open("{}/{}.jpg".format(IMAGE_FOLDER,word), "wb")
            file.write(response.content)
            file.close()


def extract_words(name):
    file = open(name, 'r')
    Lines = file.readlines()
    count = 0
    words=[]
    for line in Lines:
        count += 1
        words.append(line.strip())
    file.close()
    return words


def translate_words(wordsArray):
    translator = Translator()
    translations = translator.translate(wordsArray[0], src=src, dest=dest)
    translated_words=[]
    for translation in translations:
        translated_words.append(translation.text)
    return translated_words


def generate_image_links(wordsArray):
    links = []
    for word in wordsArray[1]:
        # space needs to be replaced by "+" otherwise google searches only part of the phrase in case of Unsplash replace with "-"
        searchurl = STOCK_IMAGE + word.replace(" ", "-")
        links.append(searchurl)
    return links


if __name__ == '__main__':
    wordsArray = [[], []]
    wordsArray[0]=extract_words(SAMPLE_TXT_NAME)
    wordsArray [1]=translate_words(wordsArray)
    download_records(wordsArray)
    download_images(generate_image_links(wordsArray),wordsArray)


