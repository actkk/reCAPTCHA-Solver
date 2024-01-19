import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from pydub import AudioSegment
import speech_recognition as sr

class TestSolver():
    def setup_method(self, method):
        self.driver = webdriver.Firefox()
        self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()

    def test_usersignup(self):
        self.driver.get("https://www.google.com/recaptcha/api2/demo")
        DOWNLOADS_FOLDER = "Your path"

        time.sleep(5)

        iframe = self.driver.find_element(By.CSS_SELECTOR, "iframe[src*='recaptcha']")

    
        self.driver.switch_to.frame(iframe)

        checkbox = self.driver.find_element(By.CSS_SELECTOR, ".recaptcha-checkbox-border")
        checkbox.click()


        self.driver.switch_to.default_content()

        time.sleep(1)
        iframe_locator = (By.CSS_SELECTOR, "iframe[title='recaptcha challenge expires in two minutes']")
        iframe = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(iframe_locator))

        self.driver.switch_to.frame(iframe)
        time.sleep(1)
        checkbox = self.driver.find_element(By.ID, "recaptcha-audio-button")
        checkbox.click()
        time.sleep(1)

        
        audio_link = self.driver.find_element(By.CLASS_NAME, "rc-audiochallenge-tdownload-link")
        audio_link_url = audio_link.get_attribute("href")
        time.sleep(1)

        mp3_file_path = DOWNLOADS_FOLDER+"/audio.mp3"
        wav_file_path = DOWNLOADS_FOLDER+"/ses.wav"

        file_name = f'audio.mp3'
        file_path = os.path.abspath(os.path.join(DOWNLOADS_FOLDER, file_name))
        os.makedirs(DOWNLOADS_FOLDER, exist_ok=True)

        response = requests.get(audio_link_url)
        open(file_path, 'wb').write(response.content)
        audio = AudioSegment.from_mp3(mp3_file_path)
        audio.export(wav_file_path, format='wav')
        print("Conversion to WAV successful")

        # Recognize speech using Sphinx
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_file_path) as source:
            audio_data = recognizer.record(source)

        text = recognizer.recognize_sphinx(audio_data, language="en-US")
        print("Transcription: ", text)
        os.remove(wav_file_path)
        os.remove(mp3_file_path)


        self.driver.find_element(By.ID, "audio-response").send_keys(text)
        checkbox = self.driver.find_element(By.ID, "recaptcha-verify-button")
        checkbox.click()
        self.driver.switch_to.default_content()

        time.sleep(5)
