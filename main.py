from googletrans import Translator
import pyttsx3 #artık daha iyi bir ses motoru olan pyttsx3 kullanıyoruz
import speech_recognition as sr

# pyttsx3 motorunu başlat
engine = pyttsx3.init()

# İngilizce ses seçimi (varsayılan İngilizce sesi bulmaya çalışır)
voices = engine.getProperty("voices")
for voice in voices:
  if "en" in voice.id.lower() or "english" in voice.name.lower():
    engine.setProperty("voice", voice.id)
    break


def speak_english(text):
  """Metni bilgisayarın yerel ses motoruyla (pyttsx3) İngilizce seslendirir."""
  print(f"Çeviri (İngilizce): {text}")
  engine.say(text)
  engine.runAndWait()


def listen_and_translate():
  recognizer = sr.Recognizer()
  translator = Translator()

  with sr.Microphone() as source:
    print("\n[+] Ortam gürültüsü ayarlanıyor, lütfen bekleyin...")
    recognizer.adjust_for_ambient_noise(source, duration=1)
    print("[+] Dinliyorum... Konuşabilirsiniz (Türkçe):")
#türkçe cümleyi algılar
    try:
      # Sesi dinle
      audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
      print("[+] Ses algılandı, işleniyor...")

      # Türkçe sesi metne dök
      turkish_text = recognizer.recognize_google(audio, language="tr-TR")
      print(f"Algılanan Metin (Türkçe): {turkish_text}")

      # İngilizceye çevir
      translated = translator.translate(turkish_text, src="tr", dest="en")
      english_text = translated.text

      # İngilizce olarak seslendir
      speak_english(english_text)

    except sr.WaitTimeoutError:
      print("[-] Herhangi bir ses algılanmadı.")
    except sr.UnknownValueError:
      print("[-] Söylediğiniz anlaşılamadı.")
    except sr.RequestError as e:
      print(f"[-] Servis hatası: {e}")
    except Exception as e:
      print(f"[-] Bir hata oluştu: {e}")


if __name__ == "__main__":
  listen_and_translate()
