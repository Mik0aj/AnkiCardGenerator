from googletrans import Translator
from google_speech import Speech
import os
import requests
import re
src="cs"
dest ="en"
wordsArray = []

RECORD_FOLDER ='recording'
IMAGE_FOLDER='images'
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
def download_records():
    if not os.path.exists(RECORD_FOLDER):
        os.mkdir(RECORD_FOLDER)
    for word in wordsArray:
        speach=Speech(word,src)
        speach.save("{}/{}.mp3".format(RECORD_FOLDER,word))


# https:\/\/images\.unsplash\.com\/photo-[^;]*
def download_images(links):
    for i,link in enumerate(links):
        response = requests.get(link, headers=usr_agent)
        html = response.text
        regex = r"https:\/\/images\.unsplash\.com\/photo-[^;]*"
        matches = re.search(regex, html, re.MULTILINE)
        if matches:
            print("Match was found at {start}-{end}: {match}".format(start=matches.start(), end=matches.end(),
                                                                     match=matches.group()))
            response = requests.get(matches.group())

            file = open("{}/{}.jpg".format(IMAGE_FOLDER,newList[0][i]), "wb")
            file.write(response.content)
            file.close()
            for groupNum in range(0, len(matches.groups())):
                groupNum = groupNum + 1

                print("Group {groupNum} found at {start}-{end}: {group}".format(groupNum=groupNum,
                                                                                start=matches.start(groupNum),
                                                                                end=matches.end(groupNum),
                                                                                group=matches.group(groupNum)))



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    translator = Translator()
    print(translator.translate("word"))
    file1 = open('sample.txt', 'r')
    Lines = file1.readlines()
    count =0
    for line in Lines:
        count += 1
        wordsArray.append(line.strip())
        #print("Line{}: {}".format(count, line.strip()))
    download_records()
    translations = translator.translate(wordsArray, src=src,dest=dest)
    newList=[[],[]]
    links=[]
    for translation in translations:
        newList[0].append(translation.origin)
        newList[1].append(translation.text)
    print(newList)
    for word in newList[1]:
        #space needs to be replaced by + otherwise google searches only part of the phrase
        searchurl = STOCK_IMAGE + word.replace(" ", "-")
        links.append(searchurl)
    download_images(links)


