import time
import keyboard
from rich import print
from azure_STT import SpeechToTextManager
from openai_chat import OpenAiManager
from eleven_labs import ElevenLabsManager
from audio_player import AudioManager

ELEVENLABS_VOICE = "Daniel" 

BACKUP_FILE = "ChatHistoryBackup.txt"

elevenlabs_manager = ElevenLabsManager()
speechtotext_manager = SpeechToTextManager()
openai_manager = OpenAiManager()
audio_manager = AudioManager()

FIRST_SYSTEM_MESSAGE = {"role": "system", "content": '''
You are the AI narrator in a gripping interactive mystery story set in a sprawling, atmospheric manor where a notorious theft has taken place. 
Your role is to assist the user, who plays the detective, in navigating the complexities of the case. Here’s how you should operate:

1) Speak in a formal and articulate manner, reminiscent of classic detective literature, to enhance the immersive experience.
2) Keep track of clues and suspects that the detective encounters, and provide summaries when requested.
3) Offer hints and suggest directions based on the detective’s inquiries, but never solve the puzzles directly. Let the detective make the final connections.
4) Occasionally remind the detective of unresolved threads and inconsistencies in suspects' statements to encourage thorough investigation.
5) Maintain an impartial tone, presenting facts without leading the detective to conclusions.
6) Describe settings and atmospheres vividly to set the mood for each scene or interaction.
7) Adapt your responses to the detective's style of investigation, whether they prefer a methodical approach or intuitive leaps.
8) Your primary goal is to support the detective by being a knowledgeable and reliable resource, helping them to piece together the story and solve the mystery using their own skills and reasoning.
9) Introduce the mystery the detective in a literary manner, that is to say set the scene, and tell the detective why they know about the case
Okay, let the conversation begin!
'''}
openai_manager.chat_history.append(FIRST_SYSTEM_MESSAGE)

print("[green]Starting the loop, press F4 to begin")
while True:
    # Wait until user presses "f4" key
    if keyboard.read_key() != "f4":
        time.sleep(0.1)
        continue

    print("[green]User pressed F4 key! Now listening to your microphone:")

    # Get question from mic
    mic_result = speechtotext_manager.speechtotext_from_mic_continuous()
    
    if mic_result == '':
        print("[red]Did not receive any input from your microphone!")
        continue

    # Send question to OpenAi
    openai_result = openai_manager.chat_with_history(mic_result)
    
    # Write the results to txt file as a backupp
    with open(BACKUP_FILE, "w") as file:
        file.write(str(openai_manager.chat_history))

    # Send it to 11Labs to turn into cool audio
    elevenlabs_output = elevenlabs_manager.text_to_audio(openai_result, ELEVENLABS_VOICE, False)


    # Play the mp3 file
    audio_manager.play_audio(elevenlabs_output, True, True, True)


    print("[green]\n!!!!!!!\nFINISHED PROCESSING DIALOGUE.\nREADY FOR NEXT INPUT\n!!!!!!!\n")
    