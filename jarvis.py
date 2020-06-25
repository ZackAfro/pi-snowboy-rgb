import snowboydecoder
import speech_recognition as sr
import RPi.GPIO as GPIO
import pigpio
import json

with open('colours.json') as json_file:
    data = json.load(json_file) 

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(5,GPIO.OUT)

def listen_command():
    toggle_indicator_light(True)
    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)

    # recognize speech using Google Speech Recognition
    try:
        text = r.recognize_google(audio);
        print("Google Speech Recognition thinks you said " + text)
        action_command(text)
        toggle_indicator_light(False)
    except sr.UnknownValueError:
        toggle_indicator_light(False)
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        toggle_indicator_light(False)
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

def action_command(text):
    if "turn on" in text: 
        toggle_strip(True)
    elif "turn off" in text:
        toggle_strip(False)
    elif "colour" in text:
        set_color(text)

def toggle_indicator_light(val):
    if val:
        GPIO.output(5,GPIO.HIGH)
    else :
        GPIO.output(5,GPIO.LOW)
    
def toggle_strip(val):
    if val:
        setLights(green, 255)
        setLights(red, 255)
        setLights(blue, 255)
    else :
        setLights(green, 0)
        setLights(red, 0)
        setLights(blue, 0)

def setLights(pin, brightness):
	pi.set_PWM_dutycycle(pin, brightness)

def set_color(text):
    print("set colour to :" + text)
    for color in data:
        if color['name'].lower() in text.lower() :
            setLights(red, color['rgb'][0])
            setLights(green, color['rgb'][1])
            setLights(blue, color['rgb'][2])
            break
    

def detected_callback():
    listen_command()

detector = snowboydecoder.HotwordDetector("jarvis.pmdl", sensitivity=0.5, audio_gain=3)

detector.start(detected_callback)

setLights(green, 255)
setLights(red, 0)
setLights(blue, 255)