import csv
import shutil

from WordFetch import Word_Fetcher
DECK_NAME='deck.csv'
SAMPLE_TXT_NAME = 'sample.txt'
RECORD_FOLDER = 'recording'
IMAGE_FOLDER = 'images'
RECORD_DESTINATION=''
IMAGE_DESTINATION=''
SRC = "cs"
DEST = "en"
USER_AGENT = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive',
}

if __name__ == '__main__':
    wf = Word_Fetcher(record_folder=RECORD_FOLDER, image_folder=IMAGE_FOLDER, file_name=SAMPLE_TXT_NAME, src=SRC,
                      dest=DEST, usr_agent=USER_AGENT)
    anki_data = wf.get_data()
    with open(DECK_NAME, 'w', newline='') as file:
        writer = csv.writer(file)
        for i in range(len(anki_data[0])):
            writer.writerow([anki_data[0][i],"[sound:{}.mp3]".format(anki_data[0][i]),anki_data[1][i],'<img src=\'{}.jpg\'>'.format(anki_data[0][i])])
            print(anki_data[2][i])
            shutil.copy2("./{}".format(anki_data[2][i]), '/home/mikoaj/.local/share/Anki2/User 1/collection.media/')
            shutil.copy2("./{}".format(anki_data[3][i]), '/home/mikoaj/.local/share/Anki2/User 1/collection.media/')
    shutil.copy2(DECK_NAME,'/home/mikoaj/Desktop')

