import pyaudio
import keyboard
import numpy as np
from scipy.io import wavfile
from os import path, remove
import speech_recognition as sr
import pyttsx3


class Recorder():
    def __init__(self, filename):
        self.audio_format = pyaudio.paInt16
        self.channels = 1
        self.sample_rate = 44100
        self.chunk = int(0.03*self.sample_rate)
        self.filename = filename
        self.START_KEY = 's'
        self.STOP_KEY = 'q'
        self.lang_codename = 'en'


    def record(self):
        recorded_data = []
        p = pyaudio.PyAudio()

        stream = p.open(format=self.audio_format, channels=self.channels,
                        rate=self.sample_rate, input=True,
                        frames_per_buffer=self.chunk)
        while(True):
            data = stream.read(self.chunk)
            recorded_data.append(data)
            if keyboard.is_pressed(self.STOP_KEY):
                print("\nStop recording")
                # stop and close the stream
                stream.stop_stream()
                stream.close()
                p.terminate()
                #convert recorded data to numpy array
                recorded_data = [np.frombuffer(frame, dtype=np.int16) for frame in recorded_data]
                wav = np.concatenate(recorded_data, axis=0)
                wavfile.write(self.filename, self.sample_rate, wav)
                break


    def listen(self):
        print(f"Press `{self.START_KEY}` to start and `{self.STOP_KEY}` to quit!")
        while True:
            if keyboard.is_pressed(self.START_KEY):
                print('\nrecord started')
                self.record()
                break


    def language(self):
        while True:
            try:
                print('''English	(en)
Korean	(ko)
Russian	(ru)
Chinese	(zh-CN)
Spanish	(es)
Vietnamese	(vi)''')
                ans = input("Choose language you want (en, vi,...): ")
                ans = ans.lower()
                if ans == 'english' or ans == 'en':
                    lang_codename = 'en'
                elif ans == 'vietnam' or ans == 'việt nam' or ans == 'vi' or ans == 'vn':
                    lang_codename = 'vi'
                elif ans == 'korean' or ans == '한국어' or ans == 'kr':
                    lang_codename = 'ko'
                elif ans == 'russian' or ans == 'Русский язык' or ans == 'ru':
                    lang_codename = 'ru'
                elif ans == 'chinese' or ans == '汉语' or ans == '漢語' or ans == 'zh-CN':
                    lang_codename = 'zh-CN'
                elif ans == 'spanish' or ans == 'español' or ans == 'es':
                    lang_codename = 'es'
                elif ans == '' or ans != '':
                    print('Invalid input or language not supported')
                return lang_codename
            except:
                print('Invalid input!')

    #ask to redo
def redo():
    while True:
        try:
            decide = input('Do you want to try again?(y/n): ')
            decide = decide.lower()
            if decide == 'y':
                break
            elif decide == 'n':
                input('See you again!')
                return False
            else:
                print('Invalid input!')
                redo()
        except:
            print('Invalid input!')
            redo()
    return True



#main code
while True:
    recorder = Recorder("mic.wav") #name of output file
    lan = recorder.language()
    recorder.listen()



    AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "mic.wav")
    # AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "french.aiff")
    # AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "chinese.flac")

    # use the audio file as the audio source
    r = sr.Recognizer()
    with sr.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source)  # read the entire audio file



    # recognize speech using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        print("you just said " + r.recognize_google(audio, language = lan))
    except sr.UnknownValueError:
        print("Speech Recognition could not understand what you said")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))


        #text_to_speech
    try:
        input_text = r.recognize_google(audio, language = lan )
    except:
        input_text = "I did not quite catch that"


    engine = pyttsx3.init()
    #change active voice
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)

    #change reading speed
    engine.setProperty('rate', 125)
    engine.say("You was saying: " + input_text)
    engine.runAndWait()
    remove('mic.wav')
    
    re = redo()
    if re == True:
        continue
    elif re == False:
        break


