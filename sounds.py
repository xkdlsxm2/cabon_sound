from playsound import playsound
import pathlib
from pydub import AudioSegment
from utils import get_curtime
import os


class sound_mixer():
    def __init__(self, duration_sec=15, interval_ms=200):
        self.src_path = pathlib.Path(r"C:\Users\z0048drc\Desktop\cabon_sound\sources")
        self.sounds = [AudioSegment.from_wav(self.src_path / i) for i in os.listdir(self.src_path)]
        self.duration_sec = duration_sec
        self.frame = AudioSegment.silent(duration=1000 * duration_sec)
        self.interval = interval_ms
        self.cur_time = None

    def sound_mix(self, body):
        for i, body_ascii in enumerate(body):
            # todo: Correct the hard coded length "75"
            if i < 75:
                sound_idx = body_ascii % len(self.sounds)
                self.frame = self.frame.overlay(self.sounds[sound_idx], position=self.interval * i)

    def save(self):
        self.frame.export(f"{self.cur_time}.wav", format="wav")

    def play(self):
        playsound(f'{self.cur_time}.wav')

    def run(self, body):
        self.cur_time = get_curtime()
        self.sound_mix(body)
        self.save()
        self.play()