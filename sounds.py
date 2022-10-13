from playsound import playsound
import pathlib
from pydub import AudioSegment
from utils import get_curtime
import os


class sound_mixer():
    def __init__(self, args):
        self.save_path = pathlib.Path(args.save_path)
        self.src_path = pathlib.Path(args.source_path)
        self.sounds = self.__get_sounds()
        self.duration_sec = args.total_duration * 1000
        self.interval = args.sound_interval * 1000
        self.frame = AudioSegment.silent(duration=self.duration_sec)
        self.cur_time = None
        self.save_path.mkdir(parents=True, exist_ok=True)

    def __get_sounds(self):
        sounds = [AudioSegment.from_wav(self.src_path / i) for i in os.listdir(self.src_path)]
        sound_dict = dict()

        for idx in range(len(sounds)):
            sound_dict[chr(idx+97)] = sounds[idx]

        return sound_dict

    def sound_mix(self, body):
        for i, body_char in enumerate(body):
            if ord(body_char) == 32:
                pass
            elif i < self.duration_sec // self.interval:
                self.frame = self.frame.overlay(self.sounds[body_char], position=self.interval * i)
            else:
                break
            print(f"{body_char}", end="")
        print()

    def save(self):
        self.frame.export(f"{self.save_path / self.cur_time}.wav", format="wav")

    def play(self):
        playsound(f'{self.save_path / self.cur_time}.wav')

    def run(self, body):
        self.cur_time = get_curtime()
        self.sound_mix(body)
        self.save()
        self.play()
