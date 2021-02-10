import os
import re

import requests
from google_speech import Speech
from googletrans import Translator

# I don't know how to get images from google images, but getting images from Unsplash site was quiet easy
#GOOGLE_IMAGE = 'https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&'
#STOCK_IMAGE='https://unsplash.com/s/photos/' the address is hardcoded into a class

class Word_Fetcher():
    def __init__(self,record_folder,image_folder,file_name,usr_agent,src="auto",dest="en",):
        # Source language, Destination language, name of record, name of image
        self.wordsArray = [[], [],[],[]]
        self.file_name=file_name
        self.src=src
        self.dest=dest
        self.__extract_words()
        self.__translate_words()
        self.__download_records(record_folder)
        self.__download_images(self.__generate_image_links(), image_folder,usr_agent)
        self.wordsArray[2]=["{}/{}.mp3".format(record_folder,x) for x in self.wordsArray[0]]
        self.wordsArray[3]=["{}/{}.jpg".format(image_folder,x) for x in self.wordsArray[0]]

    def __extract_words(self):
        file = open(self.file_name, 'r')
        Lines = file.readlines()
        for line in Lines:
            self.wordsArray[0].append(line.strip())
        file.close()

    def __translate_words(self):
        translator = Translator()
        translations = translator.translate(self.wordsArray[0], src=self.src, dest=self.dest)
        for translation in translations:
            self.wordsArray[1].append(translation.text)

    def __download_records(self, record_folder):
        if not os.path.exists(record_folder):
            os.mkdir(record_folder)
        for word in self.wordsArray[0]:
            speach=Speech(word,self.src)
            print("Recoring for {start} : downloading mp3 and saving it in {folder}/{name}.jpg".format(
                start=word,
                 folder=record_folder, name=word))
            speach.save("{}/{}.mp3".format(record_folder,word))


    def __download_images(self, links, image_folder, usr_agent):
        for i,link in enumerate(links):
            word=self.wordsArray[0][i]
            response = requests.get(link, headers=usr_agent)
            html = response.text
            regex = r"https:\/\/images\.unsplash\.com\/photo-[^;]*"
            matches = re.search(regex, html, re.MULTILINE)
            if matches:
                print("Match was found for {start} : {match} downloading image and saving it in {folder}/{name}.jpg".format(start=word,
                                                                         match=matches.group(),folder=image_folder,name=word))
                response = requests.get(matches.group())
                file = open("{}/{}.jpg".format(image_folder,word), "wb")
                file.write(response.content)
                file.close()

    def __generate_image_links(self):
        links = []
        for word in self.wordsArray[1]:
            # space needs to be replaced by "+" otherwise google searches only part of the phrase in case of Unsplash replace with "-"
            stock_image_url = 'https://unsplash.com/s/photos/'
            searchurl = stock_image_url + word.replace(" ", "-")
            links.append(searchurl)
        return links

    def get_data(self):
        """Function returns 4D array, first are words in source lang, second are words in destination lang, third are locations of mp3 files, fourh are locations of images"""
        return self.wordsArray