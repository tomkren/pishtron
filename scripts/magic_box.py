#!/usr/bin/python3

from pynput.keyboard import Key, Listener
from gtts import gTTS
import vlc
import pafy
import platform
import sys
import string
import re
import time
from os import path

if platform.system() == 'Windows':
    import winsound


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
    },
    4: {
        'name': 'Básničky'
    }
}

# Thanks to https://github.com/fuhton/piano-mp3 (MIT license) for piano mp3s in piano folder!
notes = [
    'A0', 'Bb0', 'B0', 'C1', 'Db1', 'D1', 'Eb1', 'E1', 'F1', 'Gb1', 'G1', 'Ab1',
    'A1', 'Bb1', 'B1', 'C2', 'Db2', 'D2', 'Eb2', 'E2', 'F2', 'Gb2', 'G2', 'Ab2',
    'A2', 'Bb2', 'B2', 'C3', 'Db3', 'D3', 'Eb3', 'E3', 'F3', 'Gb3', 'G3', 'Ab3',
    'A3', 'Bb3', 'B3', 'C4', 'Db4', 'D4', 'Eb4', 'E4', 'F4', 'Gb4', 'G4', 'Ab4',
    'A4', 'Bb4', 'B4', 'C5', 'Db5', 'D5', 'Eb5', 'E5', 'F5', 'Gb5', 'G5', 'Ab5',
    'A5', 'Bb5', 'B5', 'C6', 'Db6', 'D6', 'Eb6', 'E6', 'F6', 'Gb6', 'G6', 'Ab6',
    'A6', 'Bb6', 'B6', 'C7', 'Db7', 'D7', 'Eb7', 'E7', 'F7', 'Gb7', 'G7', 'Ab7',
    'A7', 'Bb7', 'B7', 'C8'
]

print('num notes:', len(notes))
firstNote = 20
isFrequencyMode = False


current_mode_id = 0
player = None
current_word = ''
current_sentence = ''

keys = {
    ';': {'f': 220, 'n': 0, 'like': None, 'read_char_as': 'středník'},
    '+': {'f': 233, 'n': 1, 'like': None, 'read_char_as': 'plus'},
    'ě': {'f': 247, 'n': 2, 'like': None},
    'š': {'f': 277, 'n': 3, 'like':'šibálek',  'story': {'name':'O Šípkové Růžence', 'url':'https://www.youtube.com/watch?v=AEXixpSy1SY'}},
    'č': {'f': 294, 'n': 4, 'like':'čistítko', 'story': {'name':'O Červené karkulce', 'url':'https://youtu.be/WWjMRA1s6sg'}},
    'ř': {'f': 311, 'n': 5, 'like':'řeřicha',  'story': {'name':'Alenka v říši divů', 'url':'https://youtu.be/k8ekzT85DjY'}},
    'ž': {'f': 330, 'n': 6, 'like':'život',    'story': {'name':'Živá voda', 'url':'https://youtu.be/rI4xMJZWUhc'}},
    'ý': {'f': 349, 'n': 7, 'like': None},
    'á': {'f': 369, 'n': 8, 'like': None},
    'í': {'f': 392, 'n': 9, 'like': 'Írán'},
    'é': {'f': 415, 'n': 10, 'like': None},
    '=': {'f': 440, 'n': 11, 'like': None, 'read_char_as': 'rovná se'},
    '´': {'f': 466, 'n': 12, 'like': None, 'read_char_as': 'akut'},

    'q': {'f': 415, 'n': 13, 'like': 'kvark',   'story': {'name':'Don Quijote', 'url':'https://www.youtube.com/watch?v=zQFWKxmqx6Q'}},
    'w': {'f': 466, 'n': 14, 'like': 'western', 'story': {'name':' Werich: Žil kdys kdes chlap', 'url':'https://youtu.be/k_gDG1gUdmo'}},
    'e': {'f': 554, 'n': 15, 'like': 'ego',     'story': {'name':'O makové panence a motýlu Emanueli - O makové panence a Kaňce Čunčové', 'url':'https://www.youtube.com/watch?v=Dq2DXo8q3os'}},
    'r': {'f': 622, 'n': 16, 'like': 'rarášek', 'story': {'name':'O rybáři a jeho ženě', 'url':'https://www.youtube.com/watch?v=C9DrsQ_xlPI'}},
    't': {'f': 740, 'n': 17, 'like': 'táta',    'story': {'name':'Tři veteráni', 'url':'https://www.youtube.com/watch?v=rkG-FEAYeT8'}},
    'z': {'f': 830, 'n': 18, 'like': 'zahrada', 'story': {'name':'Zlatá husa', 'url':'https://youtu.be/G2Tvh47AXMU'}},
    'u': {'f': 932, 'n': 19, 'like': 'ulice',   'story': {'name':'Ubrousku, prostři se!', 'url':'https://www.youtube.com/watch?v=e_hLL-el5CI'}},
    'i': {'f': 1108,'n': 20, 'like': 'indián',  'story': {'name':'Indiánské pohádky: Dar totemů', 'url':'https://youtu.be/fdFMZyDpu3k'}},
    'o': {'f': 1245,'n': 21, 'like': 'Ondra',   'story': {'name':'O Pejskovi a Kočičce', 'url':'https://www.youtube.com/watch?v=-PGnB4LTs9E'}},
    'p': {'f': 1480,'n': 22, 'like': 'pejsek',  'story': {'name':'Devatero pohádek, pohádka psí', 'url': 'https://www.youtube.com/watch?v=bxqOqsCoP2s'}},
    'ú': {'f': 1661,'n': 23, 'like': 'úl',      'story': {'name':'Úžasňákovi', 'url':'https://www.youtube.com/watch?v=Apmp8Yvf36g'}},
    ')': {'f': 1865,'n': 24, 'like': None,      'read_char_as': 'konec závorky'},

    'a': {'f':440,  'n': 25, 'like': 'auto',   'story': {'name':'Až opadá listí z dubu', 'url':'https://www.youtube.com/watch?v=WoV4g_erido'}},
    's': {'f':494,  'n': 26, 'like': 'strom',  'story': {'name':'Sůl nad zlato', 'url':'https://youtu.be/8IdcsbXP__U'}},
    'd': {'f':523,  'n': 27, 'like': 'dům',    'story': {'name':'Dlouhý, Široký a Bystrozraký', 'url':'https://youtu.be/VK1X7xHPCkU'}},
    'f': {'f':587,  'n': 28, 'like': 'fík',    'story': {'name':'František Nebojsa', 'url':'https://www.youtube.com/watch?v=Ery1iikkMGQ'}},
    'g': {'f':659,  'n': 29, 'like': 'gorila', 'story': {'name':'Jak Grinch ukradl Vánoce', 'url':'https://www.youtube.com/watch?v=U1z7rz3Bqgo'}},
    'h': {'f':698,  'n': 30, 'like': 'hrášek', 'story': {'name':'Hrnečku vař!', 'url':'https://www.youtube.com/watch?v=H8rY4WJK7ZA'}},
    'j': {'f':784,  'n': 31, 'like': 'jablko', 'story': {'name':'Král Ječmínek', 'url':'https://youtu.be/mmJEf3GwkEY'}},
    'k': {'f':880,  'n': 32, 'like': 'kočka',  'story': {'name': 'Křemílek a Vochomůrka', 'url': 'https://www.youtube.com/watch?v=aDK_Wj5RzkI'}},
    'l': {'f':988,  'n': 33, 'like': 'lev',    'story': {'name':'Líná pohádka', 'url':'https://youtu.be/1DEpccD7-ww'}},
    'ů': {'f':1175, 'n': 34, 'like': None},
    '§': {'f':1319, 'n': 35, 'like': None, 'read_char_as': 'paragraf'},
    '¨': {'f':1397, 'n': 36, 'like': None, 'read_char_as': 'rozlučník'},

    '\\':{'f': 440, 'n': 37, 'like': None, 'read_char_as': 'zpětné lomítko'},
    'y': {'f': 466, 'n': 38, 'like': 'Yetti',  'story': {'name':'Yakari a velký orel', 'url':'https://youtu.be/u1Gcu0Ij_w8'}},
    'x': {'f': 494, 'n': 39, 'like': 'xilofon','story': {'name':'Bylo nás pět', 'url':'https://youtu.be/EH7LO9GIFns'}},
    'c': {'f': 523, 'n': 40, 'like': 'citrón', 'story': {'name':'Chytrá horákyně', 'url':'https://www.youtube.com/watch?v=7lYa5m3i3BA'}},
    'v': {'f': 554, 'n': 41, 'like': 'včela',  'story': {'name':'Přátelství vydry', 'url':'https://youtu.be/XaQgL1Rl0kM'}},
    'b': {'f': 587, 'n': 42, 'like': 'babička','story': {'name':'Budulínek', 'url':'https://www.youtube.com/watch?v=PzFR5wFUFLw'}},
    'n': {'f': 622, 'n': 43, 'like': 'nočník', 'story': {'name':'Neználek', 'url':'https://www.youtube.com/watch?v=YLGNNs6Yh5Y'}},
    'm': {'f': 659, 'n': 44, 'like': 'máma',   'story': {'name':'Mach a Šebestová', 'url':'https://www.youtube.com/watch?v=BuPrNST4ofY'}},
    ',': {'f': 698, 'n': 45, 'like': None, 'read_char_as': 'čárka'},
    '.': {'f': 740, 'n': 46, 'like': None, 'read_char_as': 'tečka'},
    '-': {'f': 784, 'n': 47, 'like': None, 'read_char_as': 'pomlčka'},
}

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

trans_punctuation_table = str.maketrans('', '', string.punctuation)

def remove_punctuation(s):
    return s.translate(trans_punctuation_table)

def urlify(s):

    # Remove all non-word characters (everything except numbers and letters)
    s = re.sub(r"[^\w\s]", '', s)

    # Replace all runs of whitespace with a single dash
    s = re.sub(r"\s+", '-', s)

    return s

def to_speech_filename(text):
    return '../speech/'+ urlify(remove_punctuation(text.lower()).strip()) + '.mp3'


def switch_mode(new_mode_id):
    global player, current_mode_id

    print(' -> new mode:', new_mode_id)

    if new_mode_id not in modes:
        print('!!! unsupported mode: ', new_mode_id)
        return

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


def is_read_sentence_mode():
    return current_mode_id == 2


def is_story_mode():
    return current_mode_id == 3


def is_poem_mode():
    return current_mode_id == 4


def say(text, lang='cs', slow=False):

    filename = to_speech_filename(text)

    if not path.exists(filename):
        speech = gTTS(text=text, lang=lang, slow=slow)
        speech.save(filename)

    p = vlc.MediaPlayer(filename)

    p.play()

    print(text)


def say_char(char):

    if char in keys and 'read_char_as' in keys[char]:
        say(keys[char]['read_char_as'])
    else:
        say(char)

    if char in keys and 'like' in keys[char] and keys[char]['like'] is not None:
        time.sleep(0.8)
        say("Jako " + keys[char]['like'] + ".")


def process_sentence_key(key):
    global current_word, current_sentence

    if key == Key.space:

        # say(current_word)
        current_sentence += current_word  + ' '
        print(current_sentence)
        current_word = ''

    elif key == Key.tab:

        if current_word.strip() != '':
            say(current_word)

    elif key == Key.enter or key.char == '.' or key.char == '?':

        if key != Key.enter:
            current_word += key.char

        current_sentence += current_word + ' '

        if current_sentence.strip() != '':
            say(current_sentence)

        current_sentence = ''
        current_word = ''

    else:

        current_word += key.char


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


def play_piano_key(key_char):
    if isFrequencyMode and platform.system() == 'Windows':
        freq = keys[key_char]['f']
        winsound.Beep(freq, 150)
    else:
        filename = '../piano/' + notes[(firstNote + keys[key_char]['n']) % len(notes)] + '.mp3'
        # print(filename)
        p = vlc.MediaPlayer(filename)
        p.play()


def on_press(key):
    global isFrequencyMode, firstNote
    try:
        # print('{0} pressed'.format(key))
        if hasattr(key, 'char') and key.char is not None:
            if key.char.isdigit():  # linux
                switch_mode(int(key.char))
            elif is_piano_mode() and key.char in keys:
                play_piano_key(key.char)
            elif is_read_char_mode() and key.char is not None:
                say_char(key.char)
            elif is_read_sentence_mode():
                process_sentence_key(key)
            elif is_story_mode() and key.char in keys and 'story' in keys[key.char]:
                play_story(keys[key.char]['story'])
            elif is_poem_mode():
                say(brambora)
        elif key == Key.space:
            if is_read_sentence_mode():
                process_sentence_key(key)
            elif is_piano_mode():
                firstNote += 1
        elif key == Key.enter:
            if is_read_sentence_mode():
                process_sentence_key(key)
            elif is_piano_mode():
                firstNote -= 1
        elif key == Key.tab:
            if is_read_sentence_mode():
                process_sentence_key(key)
            elif is_piano_mode():
                isFrequencyMode = not isFrequencyMode
        elif hasattr(key, 'vk'):  # windows
            num_pad = key.vk - 96
            if 0 <= num_pad <= 9:
                switch_mode(num_pad)

    except NameError as err:
        print("NameError: {0}".format(err))
    except:
        print("Unexpected error:", sys.exc_info()[0])


def on_release(key):
    # print('{0} release'.format(key))
    if key == Key.esc:
        # Stop listener
        return False


# Collect events until released
with Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()



