import speech_recognition as sr # Bu kütüphane mikrofondan alınan ses verisini metne çevirmek için kullanılır.
import pyttsx3 #Metin tabanlı sesli geri bildirim sağlamak için kullanılan bir metin-okuma kütüphanesidir.
import webbrowser #Web tarayıcısını açmak veya belirli bir URL'yi ziyaret etmek için kullanılan bir modüldür
import requests #HTTP üzerinden web servislerine istek göndermek ve yanıtları almak için kullanılan bir kütüphanedir.OpenWeatherMap API'den hava durumu

# Bu nesne, ses verisini metne çevirme işlevselliğini sağlar.
r = sr.Recognizer()

# Metin-okuma motoru (text-to-speech engine) başlatıyor. 
engine = pyttsx3.init()

def get_weather():
    try:
        # Determine the user's location
        with sr.Microphone() as source: # Mikrofonu kullanarak kullanıcının konumunu belirlemek için bir ses kaynağı oluşturulur.
            print("Specify your location...")
            engine.say("Specify your location.")
            engine.runAndWait() # Konuşmayı başlat ve tamamlanmasını bekle
            location_audio = r.listen(source) #Kullanıcının konumunu sesli dinleyip ses verisini elde eder.

        # Convert the user's location to text
        location = r.recognize_google(location_audio, language="en-US")  # Google konuşma tanıma servisi kullanılarak ses verisi metne çevrilir ve konum belirlenir.
        print("Location: " + location)

        # Get weather information using the OpenWeatherMap API
        weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid=ee7da628a3e511b55a233e7d0832e476&lang=en"
        response = requests.get(weather_url) #Hava durumu bilgilerini almak için kullanıcının belirttiği konumu içeren OpenWeatherMap API'ye bir istek yapılır
        weather_data = response.json() #API yanıtı JSON formatındadır ve bu bilgiler weather_data değişkenine atanır.

        
        if "weather" in weather_data: #API yanıtında "weather" anahtarı var mı diye kontrol edilir.
            description = weather_data["weather"][0]["description"] #API yanıtından hava durumu açıklaması (örneğin, "parçalı bulutlu", "yağmurlu" gibi) çekilir.
            temperature = weather_data["main"]["temp"] # API yanıtından sıcaklık bilgisi çekilir.

            # Provide audio feedback
            temperature_celsius = temperature - 273.15 #Kelvin cinsinden alınan sıcaklık değeri Celsius'a çevrilir.
            engine.say(f"Weather in {location}: {description}, temperature: {temperature_celsius:.2f} degrees")
            print(f"Weather in {location}: {description.upper()}, Temperature: {temperature_celsius:.2f} Degrees")
            engine.runAndWait() # Sesli mesajın çalınmasını ve tamamlanmasını bekler

        else:
            print("Weather information could not be obtained.")
            engine.say("Weather information could not be obtained.")
            engine.runAndWait()

    except sr.UnknownValueError:
        print("Location not understood.")
        engine.say("Location not understood.")
        engine.runAndWait()

    except sr.RequestError as e:
        print("Unable to retrieve location information; {0}".format(e))
        engine.say("Unable to retrieve location information.")
        engine.runAndWait()


with sr.Microphone() as source: #Bu, kullanıcının gerçek zamanlı olarak konuşmasını kaydetmek için mikrofonu kullanmayı sağlar.
    print("Speak...")
    engine.say("Speak")
    engine.runAndWait()
    audio = r.listen(source) #kullanıcının konuşmasını kaydederek bir ses verisi elde etmeyi sağlar.

try:
    # Convert audio data to text
    recognized_text = r.recognize_google(audio, language="en-US")  # speech_recognition kütüphanesinin recognize_google fonksiyonu kullanılarak kaydedilen ses verisi metne çevrilir. language parametresi, tanıma işleminin hangi dilde gerçekleştirileceğini belirler.
    print("Speech Recognition Result: " + recognized_text)

    # Perform actions based on specific commands
    if "open google" in recognized_text.lower():
        webbrowser.open("http://www.google.com")
    if "open youtube" in recognized_text.lower():
        webbrowser.open("https://www.youtube.com")
    if "weather" in recognized_text.lower():
        # Call the weather function
        get_weather()

   
    engine.say(recognized_text)
    engine.runAndWait()

except sr.UnknownValueError:
    print("Speech not understood.")
    engine.say("Speech not understood.")
    engine.runAndWait()

except sr.RequestError as e:
    print("Unable to access the speech recognition service; {0}".format(e))
    engine.say("Unable to access the speech recognition service.")
    engine.runAndWait()