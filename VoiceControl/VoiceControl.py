import speech_recognition as sr


class VoiceControl:

    def __init__(self):
        self.r = sr.Recognizer()
        self.mic = sr.Microphone()


    def listen(self):
        print("LISTENING...")

        with self.mic as source:
            audio = self.r.listen(source)

            audio = self.r.recognize_google(audio)
            print("AUDIO TYPE IS:", type(audio))
        return audio