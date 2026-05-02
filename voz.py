import speech_recognition as sr
import pyaudio


def escuchar():
    r = sr.Recognizer()
    text = ""
    try:
        with sr.Microphone() as source:
            print("Di algo...")
            audio = r.listen(source)

        text = r.recognize_google(audio, language="es-ES").upper()
        print("Has dicho: " + text)
    except sr.UnknownValueError:
        print("No se pudo entender el audio")
    except sr.RequestError as e:
        print("Error al solicitar resultados; {0}".format(e))


    return text




