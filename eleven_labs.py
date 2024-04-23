from elevenlabs import generate, stream, set_api_key, voices, play, save
import time
import os

try:
  set_api_key(os.getenv('ELEVENLABS_API_KEY'))
except TypeError:
  exit("forgot to set ELEVENLABS_API_KEY in your environment")

class ElevenLabsManager:

    def __init__(self):
        all_voices = voices()
        print(f"\nAll ElevenLabs voices: \n{all_voices}\n")

    # Convert text to speech, then save it to file. Returns the file path
    def text_to_audio(self, input_text, voice="INSERT VOICE HERE", save_as_wave=True, subdirectory=""):
        audio_saved = generate(
          text=input_text,
          voice=voice,
          model="eleven_monolingual_v1"
        )
        if save_as_wave:
          file_name = f"___Msg{str(hash(input_text))}.wav"
        else:
          file_name = f"___Msg{str(hash(input_text))}.mp3"
        tts_file = os.path.join(os.path.abspath(os.curdir), subdirectory, file_name)
        save(audio_saved,tts_file)
        return tts_file

    # Convert text to speech, then play it out loud
    def text_to_audio_played(self, input_text, voice="INSERT VOICE HERE"):
        audio = generate(
          text=input_text,
          voice=voice,
          model="eleven_monolingual_v1"
        )
        play(audio)

    # Convert text to speech, then stream it out loud (don't need to wait for full speech to finish)
    def text_to_audio_streamed(self, input_text, voice="INSERT VOICE HERE"):
        audio_stream = generate(
          text=input_text,
          voice=voice,
          model="eleven_monolingual_v1",
          stream=True
        )
        stream(audio_stream)


if __name__ == '__main__':
    elevenlabs_manager = ElevenLabsManager()

    elevenlabs_manager.text_to_audio_streamed("This is a test message, please say something in character", "INSERT VOICE HERE")
    time.sleep(2)
    elevenlabs_manager.text_to_audio_played("helo hello", "INSERT VOICE HERE")
    time.sleep(2)
    file_path = elevenlabs_manager.text_to_audio("idk", "INSERT VOICE HERE")
    print("Finished with all tests")

    time.sleep(30)