import pathlib
from cabon_sound import cabon_sound
import json
from utils import build_args

if __name__ == "__main__":
    config_path = pathlib.Path(input("Input config path: "))
    config = json.load(open(config_path / "config.json"))
    args = build_args(config)

    cabon_sounder = cabon_sound(args)
    cabon_sounder.run()
