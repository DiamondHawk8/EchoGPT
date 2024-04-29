import tkinter as tk
from pydub import AudioSegment
import threading
import simpleaudio as sa
import time

class AudioVisualizer:
    def __init__(self, background_image_path, character_image_path, audio_file_path):
        self.background_image_path = background_image_path
        self.character_image_path = character_image_path
        self.audio_file_path = audio_file_path
        self.root = tk.Tk()
        self.setup_gui()

    def setup_gui(self):
        self.root.title("Audio Visualizer")
        self.root.geometry("1792x1024")

        background_image = tk.PhotoImage(file=self.background_image_path)
        background_label = tk.Label(self.root, image=background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        character_image = tk.PhotoImage(file=self.character_image_path)
        self.character_label = tk.Label(self.root, image=character_image)
        self.character_label.image = character_image  # Keep a reference!
        self.character_label.pack(pady=200)

    def play_audio_and_animate(self):
        wave_obj = sa.WaveObject.from_wave_file(self.audio_file_path)
        play_obj = wave_obj.play()
        audio = AudioSegment.from_file(self.audio_file_path)
        duration_per_chunk = 100  # ms

        for segment in audio[::duration_per_chunk]:
            volume = segment.dBFS
            position = min(max(-volume, 0), 100)  # Normalize volume to a suitable range for y-position
            self.character_label.place_configure(y=position)
            time.sleep(duration_per_chunk / 1000.0)  # Wait for the chunk's duration
        play_obj.wait_done()

    def start(self):
        audio_thread = threading.Thread(target=self.play_audio_and_animate)
        audio_thread.start()
        self.root.mainloop()


if __name__ == '__main__':
    visualizer = AudioVisualizer('path_to_background.png', 'path_to_character.png', 'path_to_audio.mp3')
    visualizer.start()