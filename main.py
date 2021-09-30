from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image_dataset_from_directory
import myparser
import cv2
import pytesseract 
import telebot
import os, time
import requests

#pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
bot = telebot.TeleBot(token="1993230425:AAEqbDCNCDGDcAJ00w1nBmk9loenYbMRcbc")
link = 'https://twitter.com/nd6q4X6qTYcbZCV'
xpath = '//article[@data-testid="tweet"]'
image_path = '/projects/NEYROv3/images/ims/'
dataset_image_path = '/projects/NEYROv3/images/'
driver_path = '/usr/local/bin/geckodriver'
model = load_model("/projects/NEYROv1/crypto_checking_network_vID.h5")
trig = ''

parser = myparser.Parser(link, xpath, image_path, driver_path)

triggers = ['doge', 'shib']
batch_size = 32
image_size = (254, 254)

class Checker():
    def __init__(self, triggers, batch_size, image_size, image_path, dataset_image_path):
        self.triggers = triggers
        self.batch_size = batch_size
        self.image_size = image_size
        self.image_path = image_path
        self.dataset_image_path = dataset_image_path
        self.trig = trig

    def connect(self):
        try:
            parser.connect_driver()
            time.sleep(2)
            parser.start()
        except Exception as e:
            print('_________________________________________________________________________________________________\n')
            print('                              PRECONNECTING ERROR\n')
            print(f'{e}\n')
            print('_________________________________________________________________________________________________\n')

    def start_cycle(self):
        try:
            while True:
                parser.get_tweet()
                time.sleep(0.3)
                if parser.last_time != parser.time_post:
                    parser.driver.implicitly_wait(5)
                    parser.get_image()
                    time.sleep(0.3)
                    self.tweet_text = parser.get_text()
                    if self.check_text():
                        self.message()
                        parser.last_time = parser.time_post
                        continue 
                    time.sleep(0.2)
                    if self.check_image_text():
                        self.message()
                        parser.last_time = parser.time_post
                        continue
                    time.sleep(0.2)
                    if self.check_image():
                        self.message()
                        parser.last_time = parser.time_post
                        continue
                parser.last_time = parser.time_post
                for elem in os.listdir(self.image_path):
                    os.remove(f'{self.image_path}{elem}')
                parser.driver.refresh()
                parser.driver.implicitly_wait(5)
                time.sleep(0.1)
        except Exception as e:
            print('_________________________________________________________________________________________________\n')
            print('                              CYCLE ERROR\n')
            print(f'{e}\n')
            print('_________________________________________________________________________________________________\n')
                

    def check_text(self):
        try:
            for trigger in self.triggers:
                if trigger in self.tweet_text:
                    self.trig = trigger
                    return True
        except Exception as e:
            print('_________________________________________________________________________________________________\n')
            print('                              TEXT CHECKING ERROR\n')
            print(f'{e}\n')
            print('_________________________________________________________________________________________________\n')

    
    def check_image(self):
        try:
            test_dataset = image_dataset_from_directory(self.dataset_image_path,
                                    batch_size=self.batch_size,
                                    image_size=self.image_size)
        except Exception as e:
            print('_________________________________________________________________________________________________\n')
            print('                              DATASET MAKING ERROR\n')
            print(f'{e}\n')
            print('_________________________________________________________________________________________________\n')
        try:
            res = model.predict(test_dataset)
            for pic in res:
                if pic[1] > 0.5:
                    self.trig = 'babydog'
                    return True
                elif pic[4] > 0.5:
                    self.trig = 'doge'
                    return True
                elif pic[8] > 0.5:
                    self.trig = 'shiba'
                    return True
        except Exception as e:
            print('_________________________________________________________________________________________________\n')
            print('                              PREDICTION ERROR\n')
            print(f'{e}\n')
            print('_________________________________________________________________________________________________\n')


    def check_image_text(self):
        try:
            images = os.listdir(self.image_path)
            for img in images:
                img = cv2.imread(f'{self.image_path}{img}')
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                res = pytesseract.image_to_string(img)
                self.res = res.lower()
                print('-------------------------------------------------------------------------------------------------\n')
                print('                              TESSERACT RESULTS\n')
                print('-------------------------------------------------------------------------------------------------\n')
                for trigger in self.triggers:
                    if trigger in self.res:
                        self.trig = trigger
                        return True
                       
        except Exception as e:
            print('text_img_ERROR')
            print(e)
    
    
    def message(self):
        print(f'{self.trig} распознан')
     
        bot.send_message('293125099', f'{self.trig} распознан')
        r = requests.get('http://45.137.64.175:2001/ZldaOUMyTlBiU1hFdWpYRkZUbUFFNjdv/SHIB')
        bot.send_message('488664136', f'{self.trig} распознан')

        
def main():
    checker = Checker(triggers, batch_size, image_size, image_path, dataset_image_path)
    checker.connect()
    checker.start_cycle()
    
if __name__ == "__main__":
    main()
