#!/usr/bin/python3

import winsound
from pynput.keyboard import Key, Listener

from gtts import gTTS
import vlc
import pafy
# import os

modes = {
    0: {
        'name': 'Piánko'
    },
    1: {
        'name': 'Čtení písmen'
    },
    2: {
        'name': 'Čtení vět'
    },
    3: {
        'name': 'Pohádky'
    }
}

current_mode_id = 0
player = None

# 'story': {'name':'', 'url':''}
# 'story': {'name':'', 'url':''}






keys = {
    ';': {'f': 220, 'like': None, 'read_char_as': 'středník'},
    '+': {'f': 233, 'like': None},
    'ě': {'f': 247, 'like': None},
    'š': {'f': 277, 'like':'šibálek',  'story': {'name':'O Šípkové Růžence', 'url':'https://www.youtube.com/watch?v=AEXixpSy1SY'}},
    'č': {'f': 294, 'like':'čistítko', 'story': {'name':'O Červené karkulce', 'url':'https://youtu.be/WWjMRA1s6sg'}},
    'ř': {'f': 311, 'like':'řeřicha',  'story': {'name':'Alenka v říši divů', 'url':'https://youtu.be/k8ekzT85DjY'}},
    'ž': {'f': 330, 'like':'život',    'story': {'name':'Živá voda', 'url':'https://youtu.be/rI4xMJZWUhc'}},
    'ý': {'f': 349, 'like': None},
    'á': {'f': 369, 'like': None},
    'í': {'f': 392, 'like': 'Írán'},
    'é': {'f': 415, 'like': None},
    '=': {'f': 440, 'like': None},
    '´': {'f': 466, 'like': None},

    'q': {'f': 415,  'like': 'kvark',   'story': {'name':'Don Quijote', 'url':'https://www.youtube.com/watch?v=zQFWKxmqx6Q'}},
    'w': {'f': 466,  'like': 'western', 'story': {'name':' Werich: Žil kdys kdes chlap', 'url':'https://youtu.be/k_gDG1gUdmo'}},
    'e': {'f': 554,  'like': 'ego',     'story': {'name':'O makové panence a motýlu Emanueli - O makové panence a Kaňce Čunčové', 'url':'https://www.youtube.com/watch?v=Dq2DXo8q3os'}},
    'r': {'f': 622,  'like': 'rarášek', 'story': {'name':'O rybáři a jeho ženě', 'url':'https://www.youtube.com/watch?v=C9DrsQ_xlPI'}},
    't': {'f': 740,  'like': 'táta',    'story': {'name':'Tři veteráni', 'url':'https://www.youtube.com/watch?v=rkG-FEAYeT8'}},
    'z': {'f': 830,  'like': 'zahrada', 'story': {'name':'Zlatá husa', 'url':'https://youtu.be/G2Tvh47AXMU'}},
    'u': {'f': 932,  'like': 'ulice',   'story': {'name':'Ubrousku, prostři se!', 'url':'https://www.youtube.com/watch?v=e_hLL-el5CI'}},
    'i': {'f': 1108, 'like': 'indián',  'story': {'name':'Indiánské pohádky: Dar totemů', 'url':'https://youtu.be/fdFMZyDpu3k'}},
    'o': {'f': 1245, 'like': 'Ondra',   'story': {'name':'O Pejskovi a Kočičce', 'url':'https://www.youtube.com/watch?v=-PGnB4LTs9E'}},
    'p': {'f': 1480, 'like': 'pejsek',  'story': {'name':'Devatero pohádek, pohádka psí', 'url': 'https://www.youtube.com/watch?v=bxqOqsCoP2s'}},
    'ú': {'f': 1661, 'like': 'úl',      'story': {'name':'Úžasňákovi', 'url':'https://www.youtube.com/watch?v=Apmp8Yvf36g'}},
    ')': {'f': 1865, 'like': None,      'read_char_as': 'konec závorky'},

    'a': {'f':440, 'like': 'auto',   'story': {'name':'Až opadá listí z dubu', 'url':'https://www.youtube.com/watch?v=WoV4g_erido'}},
    's': {'f':494, 'like': 'strom',  'story': {'name':'Sůl nad zlato', 'url':'https://youtu.be/8IdcsbXP__U'}},
    'd': {'f':523, 'like': 'dům',    'story': {'name':'Dlouhý, Široký a Bystrozraký', 'url':'https://youtu.be/VK1X7xHPCkU'}},
    'f': {'f':587, 'like': 'fík',    'story': {'name':'František Nebojsa', 'url':'https://www.youtube.com/watch?v=Ery1iikkMGQ'}},
    'g': {'f':659, 'like': 'gorila', 'story': {'name':'Jak Grinch ukradl Vánoce', 'url':'https://www.youtube.com/watch?v=U1z7rz3Bqgo'}},
    'h': {'f':698, 'like': 'hrášek', 'story': {'name':'Hrnečku vař!', 'url':'https://www.youtube.com/watch?v=H8rY4WJK7ZA'}},
    'j': {'f':784, 'like': 'jablko', 'story': {'name':'Král Ječmínek', 'url':'https://youtu.be/mmJEf3GwkEY'}},
    'k': {'f':880, 'like': 'kočka',  'story': {'name': 'Křemílek a Vochomůrka', 'url': 'https://www.youtube.com/watch?v=aDK_Wj5RzkI'}},
    'l': {'f':988, 'like': 'lev',    'story': {'name':'Líná pohádka', 'url':'https://youtu.be/1DEpccD7-ww'}},
    'ů': {'f':1175,'like': None},
    '§': {'f':1319,'like': None},
    '¨': {'f':1397,'like': None},

    '\\':{'f': 440, 'like': None},
    'y': {'f': 466, 'like': 'Yetti',  'story': {'name':'Yakari a velký orel', 'url':'https://youtu.be/u1Gcu0Ij_w8'}},
    'x': {'f': 494, 'like': 'xilofon','story': {'name':'Bylo nás pět', 'url':'https://youtu.be/EH7LO9GIFns'}},
    'c': {'f': 523, 'like': 'citrón', 'story': {'name':'Chytrá horákyně', 'url':'https://www.youtube.com/watch?v=7lYa5m3i3BA'}},
    'v': {'f': 554, 'like': 'včela',  'story': {'name':'Přátelství vydry', 'url':'https://youtu.be/XaQgL1Rl0kM'}},
    'b': {'f': 587, 'like': 'babička','story': {'name':'Budulínek', 'url':'https://www.youtube.com/watch?v=PzFR5wFUFLw'}},
    'n': {'f': 622, 'like': 'nočník', 'story': {'name':'Neználek', 'url':'https://www.youtube.com/watch?v=YLGNNs6Yh5Y'}},
    'm': {'f': 659, 'like': 'máma',   'story': {'name':'Mach a Šebestová', 'url':'https://www.youtube.com/watch?v=BuPrNST4ofY'}},
    ',': {'f': 698, 'like': None},
    '.': {'f': 740,'like': None},
    '-': {'f': 784,'like': None},
}

def switch_mode(new_mode_id):
    global player, current_mode_id

    if player is not None:
        player.stop()

    current_mode_id = new_mode_id
    mode = modes[new_mode_id]

    if 'name' in mode:
        say('Přepínám na ' + mode['name']+'.')


def is_piano_mode():
    return current_mode_id == 0

def is_read_char_mode():
    return current_mode_id == 1

def is_read_sentences_mode():
    return current_mode_id == 2

def is_story_mode():
    return current_mode_id == 3


def say(text, lang='cs', slow=False):
    speech = gTTS(text=text, lang=lang, slow=slow)
    speech.save('text-to-speech.mp3')

    # alternative: os.system("start text-to-speech.mp3")
    p = vlc.MediaPlayer('file:///text-to-speech.mp3')
    p.play()

    print(text)


def say_char(char):

    if char in keys and 'read_char_as' in keys[char]:
        say(keys[char]['read_char_as'])
    else:
        say(char)

    if char in keys and 'like' in keys[char] and keys[char]['like'] is not None:
        say("Jako "+ keys[char]['like'] +".")


def play_story(story):
    say(story['name'])
    play_youtube(story['url'])

def play_youtube(url='https://www.youtube.com/watch?v=Ery1iikkMGQ'):
    video = pafy.new(url)
    best = video.getbest()
    play_url = best.url

    instance = vlc.Instance()
    global player
    if player is None:
        player = instance.media_player_new()
    else:
        player.stop()

    media = instance.media_new(play_url)
    media.get_mrl()
    player.set_media(media)
    player.play()

def on_press(key):
    print('{0} pressed'.format(key))
    if hasattr(key, 'char') and key.char is not None:
        if is_piano_mode() and key.char in keys:
            winsound.Beep(keys[key.char]['f'], 150)
        elif is_read_char_mode() and key.char is not None:
            say_char(key.char)
        elif is_story_mode() and key.char in keys and 'story' in keys[key.char]:
            play_story(keys[key.char]['story'])
    elif hasattr(key, 'vk'):
        num_pad = key.vk - 96
        if 0 <= num_pad <= 9:
            print('=-> new mode:', num_pad)
            if num_pad in modes:
                switch_mode(num_pad)

def on_release(key):
    print('{0} release'.format(key))
    if key == Key.esc:
        # Stop listener
        return False

brambora = """
Koulela se ze dvora, 
takhle velká brambora. 
Neviděla, neslyšela, 
že na ni padá závora.
Kam koukáš ty závoro, 
na tebe ty bramboro. 
Kdyby tudy projel vlak, 
byl by z tebe bramborák!
"""

# say(brambora)

# Collect events until released
with Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()



