import os

import pygame

from ..files.paths import SOUND_DIR_PATH

pygame.mixer.init()


class Sounds:

    __sounds = {
        sound.removesuffix(".wav"): [
            pygame.mixer.Sound(os.path.join(SOUND_DIR_PATH, sound)),
            False,
        ]
        for sound in os.listdir(SOUND_DIR_PATH)
    }

    __player_boosts = {}

    @staticmethod
    def play(sound_name: str):
        Sounds.__sounds[sound_name][0].play()

    @staticmethod
    def start_boost(player_name):
        if not Sounds.__player_boosts[player_name][1]:
            Sounds.__player_boosts[player_name][0].play()
            Sounds.__player_boosts[player_name][1] = True

    @staticmethod
    def end_boost(player_name):
        if (
            s := Sounds.__player_boosts.get(player_name, None)
        ) is not None and Sounds.__player_boosts[player_name][1]:
            Sounds.__player_boosts[player_name][1] = False
            s[0].stop()

    @staticmethod
    def add_player(player_name):
        Sounds.__player_boosts[player_name] = [
            pygame.mixer.Sound(os.path.join(SOUND_DIR_PATH, "boost5.wav")),
            False,
        ]

    @staticmethod
    def stop_all_boost_sounds():
        for k in Sounds.__player_boosts.keys():
            Sounds.__player_boosts[k][0].stop()
            Sounds.__player_boosts[k][1] = False

    @staticmethod
    def reset():
        Sounds.__player_boosts.clear()
