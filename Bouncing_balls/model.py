from typing import List, Tuple
import config
import random

#Podstawowe dane symulacji
TRACK_LENGTH = 1.0
DEFAULT_VEL = 1.0
ERROR_STEP = config.ERROR_STEP
MAX_ERROR = config.MAX_ERROR

#Współczynnik losowości sprawia, że każda prędkość kuli jest jeszcze leciutko modyfikowana
#Kule nie mogą się już trywialnie spotkać po dłuższym czasie
RANDOMNESS_FACTOR = ERROR_STEP/3

assert MAX_ERROR <= TRACK_LENGTH
assert ERROR_STEP < MAX_ERROR

DEFAULT_NUM = round(MAX_ERROR/ERROR_STEP)

#Wyliczanie poszczególnych prędkości wszysktich kul
CELLS_VEL = [DEFAULT_VEL + ERROR_STEP*i + RANDOMNESS_FACTOR * random.uniform(-1,1) for i in range(-DEFAULT_NUM,DEFAULT_NUM + 1)]
CELLS_VEL[DEFAULT_NUM] = DEFAULT_VEL
CELLS = len(CELLS_VEL)

#Tutaj przechowywane będą wszystkie wyliczone parametry kul
Cache  : List[Tuple[int,float,int]] = [(0, 0, 0) for _ in range(CELLS)]

#Liczenie kolejno kierunku, pozycji i liczby odbić kuli w zależności od czasu i prędkości
def get_relative_ball_info(t: float, v: float):
    pre = (t * v) % (2 * TRACK_LENGTH)
    pre_nob = int((t * v) // (2 * TRACK_LENGTH))

    if pre >= TRACK_LENGTH:
        return (-1, 2 * TRACK_LENGTH - pre, 2*pre_nob + 1) 
    else:
        return (1, pre, 2*pre_nob)

#Aktualizacja informacji o kulach
def update_pos(t: float):
    global Cache
    for i in range(CELLS):
        Cache[i] = get_relative_ball_info(t, CELLS_VEL[i])

#Zdobycie minimalnej i maksymalnej pozycji kul przy aktualnym stanie tablicy Cache
def get_min_max_x():
    min_x = 1.0
    max_x = 0.0

    for (_,x,_) in Cache:
        min_x = min(x,min_x)
        max_x = max(x,max_x)

    return (min_x, max_x)

#Liczenie błędów zwrotu, pozycji i odbić
#Odbicia są liczone starą metodą, którą odrzuciłem dla liczenia błędu pozycji
#ale uznałem, że odbicia nie są na tyle istotne, żeby je też aktualizować
def calculate_error():
    (min_x, max_x) = get_min_max_x()
    delta_x = (max_x-min_x)
    delta_b = 0
    known_dir = True
    for (dir,_,b) in Cache:
        delta_b = max(abs(b-Cache[DEFAULT_NUM][2]),delta_b)
        known_dir = known_dir and (dir == Cache[DEFAULT_NUM][0]) 
    return (known_dir, delta_x, delta_b)