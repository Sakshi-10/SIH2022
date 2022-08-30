import speech_recognition as sr

def speech_to_text():
    global text
    r = sr.Recognizer()
    file_audio = sr.AudioFile('audio.wav')
    with file_audio as source:
        audio_text = r.record(source)
    text=r.recognize_google(audio_text)
    return text
    
def No_of_words():
    global text
    words=list(text.split(" "))
    items=len(words) 
    return items

def WPM(duration):
    count=No_of_words()
    WPS=count/duration
    WPM=WPS*60
    return int(WPM)

def get_tips(wpm):
    if wpm<120:
        tip = "\n1. Your speed of speech is lower than the average speaking speed. A speed around 140 to 160 WPM is considered to be good for the speaker and listener to understand the context completely.\n\n2. Too slow speeds may give the listener the perception of slow thinking, incompetence,and being uneducated. If you think your speaking rate might be affecting your intelligibility, we recommend that you speak just slightly slower than the average English speaker (about 150 words per minute).\n\n3. You can try increasing your speaking speed slowly along with balancing your facial emotions and voice confidence so that the listener grasps the whole content and builds a connection with you."

    elif wpm<140:
        tip = "\n1. Your speed of speech is near to the average speaking speed. A speed around 140 to 160 WPM is considered to be good for the speaker and listener to understand the context completely.\n\n2. We highly recommend incorporating shadowing practice into your daily pronunciation and practice. Shadowing is the action of imitating a speech sample as closely and as quickly as possible. With or without a transcript, you follow just behind a recording.\n\n3. If you feel this is your natural speaking speed, and listeners are able to grasp fully out of it, then you may not need to increase your speaking speed."
               
    elif wpm<=160:
        tip = "\n1. Your speed of speech is in the perfect range of speaking speed. A speed around 140 to 160 WPM is considered to be good for the speaker and listener to understand the context completely.\n\n2. If you're giving a speech or presentation, the concept of a flexibility plays a major role, it is the ability of the speaker to mix and match pace appropriately with speech content and the audience's ability to comprehend it.\n\n3. You can maintain this speech rate at 140 to 160 Words Per Minute to give your presentation effectively."

    elif wpm<180:
        tip = "\n1. Your speed of speech is near to the average speaking speed. A speed around 140 to 160 WPM is considered to be good for the speaker and listener to understand the context completely.\n\n2. We highly recommend incorporating shadowing practice into your daily pronunciation and practice. Shadowing is the action of imitating a speech sample as closely and as quickly as possible. With or without a transcript, you follow just behind a recording.\n\n3. If you feel this is your natural speaking speed, and listeners are able to grasp fully out of it, then you may not need to increase your speaking speed."

    else:
        tip = "\n1. Your speed of speech is higher than the average speaking speed. A speed around 140 to 160 WPM is considered to be good for the speaker and listener to understand the context completely.\n\n2.  A rate higher than 160 words per minute can be difficult for the listener to absorb the and may confuse them to understand the content.\n\n3. You can try decreasing your speaking speed gradually along with balancing your facial emotions and voice confidence so that the listener grasps the whole content and builds a connection with you."
    
    return tip

def common_tips():

        tip = "\n\n4. You can adjust your speech rate according to type of Speech:\n\tPresentations : 100 - 150 WPM\n\tConversation  : 120 - 150 WPM\n\tShow Anchors  : 160 - 170 WPM\n\tCommentators  : 250 - 400 WPM"
        return tip