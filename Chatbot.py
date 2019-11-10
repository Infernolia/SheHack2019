import random
import re
import pygame
import string
from gtts import gTTS
import time
import pyttsx3

import speech_recognition as sr

mic_name = "sysdefault"
sample_rate = 48000
chunk_size = 2048

name = "Xertia"
event = "Shehack"

engine = pyttsx3.init()
pygame.mixer.init()

pygame.init()
footprint = 20.8

start = 0

meal = 0

shop = 0

tree = 0

end = 0

solar = 0

car = 0
car_f = 0

food = ['kitchen', 'zomato', 'swiggy', 'big basket', 'cooking', 'hungry', 'starving', 'food']
cupboard = ['amazon', 'snapdeal', 'flipkart', 'shop', 'myntra', 'clothes']
green = ['planted', 'composting', 'watered']
panel = ['solar', 'panel', 'renewable']
travel = ['cab', 'cycle', 'walk', 'scooter', 'rickshaw', 'flight', 'plane', 'train', 'air', 'travel']
endride = ['end', 'Android']


bot_template = "BOT : {0}"
user_template = "USER : {0}"


rules = {    "hello": ["hey", "hello to you", "good morning"],
  "(.*) name": [
      "my name is {0}".format(name),
      "they call me {0}".format(name),
      "I go by {0}".format(name)
   ],
  "(.*) event": [
      "Today's event is {0}".format(event),
      "it's {0} today".format(event)
    ],
    "I want to go to (.*)": ["We have come to {0}."],
         "I want to order (.*)": ["Carbon footprint for {0} have been calculated."],
             "end ride": ["Your ride has been ended", "Carbon footprint for your ride has been calculated!"],
         "I want to book a (.*)": ["Book an Ola or Uber?"],
             "Ola": ["Okay, your ride has been started"],
             "uber":["Okay, your ride has been started"],
         "order through (.*)": ["Thanks for using our website!"],
         "(.*) hungry": ["Let's redirect you to the kitchen"],
         "(.*) starving": ["Let's redirect you to the kitchen"],
         "I am taking a (.*)": ["Your ride has been started"],
        "(.*) footprint":["Your carbon footprint is " + str(footprint)],
}



# Define variables


# Define a dictionary with the predefined responses




'''def replace_pronouns(message):

    message = message.lower()
    if 'me' in message:
        # Replace 'me' with 'you'
        return re.sub('me','you',message)
    if 'my' in message:
        # Replace 'my' with 'your'
        return re.sub('my','your',message)
    if 'your' in message:
        # Replace 'your' with 'my'
        return re.sub('your','my',message)
    if 'you' in message:
        # Replace 'you' with 'me'
        return re.sub('you', 'me', message)

    return message'''


def match_rule(rules, message):
    response, phrase = "Sorry, couldn't recognise", None

    # Iterate over the rules dictionary
    for pattern, responses in rules.items():
        # Create a match object
        match = re.search(pattern, message)
        if match is not None:
            # Choose a random response
            global start
            global end
            global meal
            global shop
            global tree
            global solar
            global car
            data = match.group(0)
            data = data.split(" ")
            for i in data:
                if i in food:
                    meal += 1
                elif i in cupboard:
                    shop += 1
                elif i in green:
                    tree += 1
                elif i in panel:
                    solar += 3
                elif i in travel:
                    car += 1
                    start=time.time()
                    if i in endride:
                        end=time.time()
                else:
                    meal += 0
                    shop += 0
                    tree += 0
                    solar += 0
                    car += 0
            response = random.choice(responses)
            if '{0}' in response:
                phrase = match.group(1)
    # Return the response and phrase
    return response.format(phrase)


form_question = ["What is your name?",
                 "What car do you use?", ]

ans = []


def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


def form_questions():
    for que in form_question:
        audio = gTTS(que, 'en', False)
        name = randomString(2) + 'mp3'
        audio.save(name)
        pygame.mixer.music.load(name)
        pygame.mixer.music.play(loops=1, start=0.0)
        time.sleep(10)
        pygame.mixer.music.set_volume(10)
        r = sr.Recognizer()
        mic_list = sr.Microphone.list_microphone_names()
        for i, microphone_name in enumerate(mic_list):
            if microphone_name == mic_name:
                device_id = i

        with sr.Microphone(device_index=device_id, sample_rate=sample_rate,
                           chunk_size=chunk_size) as source:
            r.adjust_for_ambient_noise(source)

            print("Say Something")
            audio = r.listen(source)  # listens for the user's input

            try:  # error occurs when google could not understand what was said
                ans = r.recognize_google(audio)
                print("you said: " + ans)

            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")

            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
    global car_f
    if ans[1] is "diesel":
        car_f = 6.99
    elif ans[1] is "petrol":
        car_f = 8.04


#form_questions()

for i in range(0,60):
    r = sr.Recognizer()
    mic_list = sr.Microphone.list_microphone_names()
    for i, microphone_name in enumerate(mic_list):
        if microphone_name == mic_name:
            device_id = i

    with sr.Microphone(device_index=device_id, sample_rate=sample_rate,
                       chunk_size=chunk_size) as source:
        r.adjust_for_ambient_noise(source)

        print("Say Something")
        audio = r.listen(source)  # listens for the user's input

        try:  # error occurs when google could not understand what was said
            text = r.recognize_google(audio)
            print("you said: " + text)

        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")

        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

    if text == "end":
        break

    footprint += 4+((end-start)/3600*car_f)+(meal*2.34)-(solar*2.6)-(tree*0.05)+(shop*2.6)

    bot = match_rule(rules, text)
    audio = gTTS(bot, 'en', False)
    print("BOT:"+ bot)
    name = randomString(3) + 'mp3'
    audio.save(name)
    pygame.mixer.music.load(name)
    pygame.mixer.music.play(loops=1, start=0.0)
    time.sleep(10)
    pygame.mixer.music.set_volume(10)

engine.runAndWait()