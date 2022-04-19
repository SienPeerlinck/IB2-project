import math
import time

import numpy as np
import sdl2
import sdl2.ext
import pandas as pd
from sdl2.ext.compat import byteify
from sdl2.sdlmixer import *
import csv
import serial
# import arduinoComms

ser = serial.Serial('COM6', 9600, timeout=.1)
ser.close()
ser.open()

# Constanten
BREEDTE = 800
HOOGTE = 600

# sprites_im = np.array([lamp, keygold, keysilver, keybronze, donut, kaart])
p_sprite_worldco = np.array([[7.5, 7.5], [3.5, 3.5], [16, 20], [23, 22], [5, 7.5], [2.5, 7.5]])
sprites_bool = np.array([True, True, False, False, True, True])
breedte_sprite = 0.4
hoogte_sprite = 0.5
#
# Globale variabelen
#

# variabelen voor inventory
inventory = []  # inventory begint als lege lijst
p_pressed = False
spacebar_pressed = False
inventory_bekijken = False
key_m = False
key_up = False
virtualmouse = 0
virutalmousemotion = True

# positie van de speler
p_speler = np.array([2.0, 2.0])

# richting waarin de speler kijkt
r_speler = np.array([1 / math.sqrt(2), 1 / math.sqrt(2)])

# cameravlak
d_cameravlak = 1
r_cameravlak = np.array([-1 / math.sqrt(2), 1 / math.sqrt(2)])

# wordt op True gezet als het spel afgesloten moet worden
moet_afsluiten = False

i_horizontaal = np.array([0.0, 0.0])
i_verticaal = np.array([0.0, 0.0])
i_is_horizontaal = False
foto_x = 0
gesneden_blok = np.array([0, 0])

level = 1  # welk level we in zitten
key_x = False
nameEntry = True
nameEntryText = ""
starttimer = 0
framerate = 0
start_time_game = time.time()  # is voor de lifebar
start_flikker_tijd = 0  # is voor de lifebar
tijd_flikkeren_aan = 0  # is voor de lifebar
flikkeren = True  # is voor de lifebar
game_over = False  # is voor de lifebar
max_health = 120  # in aantal seconden
play_music = True

start_code = time.time()
# de "wereldkaart". Dit is een 2d matrix waarin elke cel een type van muur voorstelt
# Een 0 betekent dat op deze plaats in de game wereld geen muren aanwezig zijn
world_map = pd.read_excel(r'World_map.xlsx', sheet_name='Level1').to_numpy(np.int8)

# Vooraf gedefinieerde kleuren
kleuren = [
    sdl2.ext.Color(0, 0, 0),  # 0 = Zwart
    sdl2.ext.Color(255, 0, 0),  # 1 = Rood
    sdl2.ext.Color(0, 255, 0),  # 2 = Groen
    sdl2.ext.Color(0, 0, 255),  # 3 = Blauw
    sdl2.ext.Color(64, 64, 64),  # 4 = Donker grijs
    sdl2.ext.Color(128, 128, 128),  # 5 = Grijs
    sdl2.ext.Color(192, 192, 192),  # 6 = Licht grijs
    sdl2.ext.Color(255, 255, 255),  # 7 = Wit
]

# kleuren voor de skyblocks => wordt in de volgende versie vervangen door een 'spriteAchtergrondAfbeelding'
# werkt met levels dus kleuren_skybloks[level] => geeft het kleur van het level weer
kleuren_skyblocks = np.array([
    sdl2.ext.Color(58, 112, 159),  # 0 = lichtblauw
    sdl2.ext.Color(58, 112, 159),  # 1 = lichtblauw
    sdl2.ext.Color(16, 48, 91),  # 2 = donkerblauw
    sdl2.ext.Color(16, 91, 82),  # 3 = donkerblauwgroen
])


#
# Verwerkt alle input van het toetsenbord en de muis
#
# Argumenten:
# @delta       Tijd in milliseconden sinds de vorige oproep van deze functie
#
def verwerk_input():
    global moet_afsluiten
    global p_speler
    global r_speler
    global key_x
    global nameEntry
    global nameEntryText
    global starttimer
    global p_pressed
    global spacebar_pressed
    global inventory_bekijken
    global key_up
    global virtualmouse
    global virtualmousemotion

    # Handelt alle input events af die zich voorgedaan hebben sinds de vorige
    # keer dat we de sdl2.ext.get_events() functie hebben opgeroepen

    # Beweging met knop op controller
    speed = 0.25
    if key_up:
        if world_map[round(np.floor(p_speler[1] + speed * r_speler[1]))] \
                [round(np.floor(p_speler[0] + speed * r_speler[0]))] == 0:
            p_speler[0] += speed * r_speler[0]
            p_speler[1] += speed * r_speler[1]
        elif world_map[round(np.floor(p_speler[1] + speed * r_speler[1]))][round(p_speler[0])] == 0:
            p_speler[1] += speed * r_speler[1] / 2  # bewegen langs muur volgens y-coordinaat
        elif world_map[round(r_speler[1])][round(np.floor(p_speler[0] + speed * r_speler[0]))] == 0:
            p_speler[0] += speed * r_speler[0] / 2  # bewegen langs muur volgens x-coordinaat

    events = sdl2.ext.get_events()
    for event in events:
        key = event.key.keysym.sym
        if nameEntry:
            nameEntryText = nameEntryText.capitalize()
            if event.type == sdl2.SDL_KEYDOWN:
                if key == sdl2.SDLK_a:
                    nameEntryText += "a"
                if key == sdl2.SDLK_b:
                    nameEntryText += "b"
                if key == sdl2.SDLK_c:
                    nameEntryText += "c"
                if key == sdl2.SDLK_d:
                    nameEntryText += "d"
                if key == sdl2.SDLK_e:
                    nameEntryText += "e"
                if key == sdl2.SDLK_f:
                    nameEntryText += "f"
                if key == sdl2.SDLK_g:
                    nameEntryText += "g"
                if key == sdl2.SDLK_h:
                    nameEntryText += "h"
                if key == sdl2.SDLK_i:
                    nameEntryText += "i"
                if key == sdl2.SDLK_j:
                    nameEntryText += "j"
                if key == sdl2.SDLK_k:
                    nameEntryText += "k"
                if key == sdl2.SDLK_l:
                    nameEntryText += "l"
                if key == sdl2.SDLK_m:
                    nameEntryText += "m"
                if key == sdl2.SDLK_n:
                    nameEntryText += "n"
                if key == sdl2.SDLK_o:
                    nameEntryText += "o"
                if key == sdl2.SDLK_p:
                    nameEntryText += "p"
                if key == sdl2.SDLK_q:
                    nameEntryText += "q"
                if key == sdl2.SDLK_r:
                    nameEntryText += "r"
                if key == sdl2.SDLK_s:
                    nameEntryText += "s"
                if key == sdl2.SDLK_t:
                    nameEntryText += "t"
                if key == sdl2.SDLK_u:
                    nameEntryText += "u"
                if key == sdl2.SDLK_v:
                    nameEntryText += "v"
                if key == sdl2.SDLK_w:
                    nameEntryText += "w"
                if key == sdl2.SDLK_x:
                    nameEntryText += "x"
                if key == sdl2.SDLK_y:
                    nameEntryText += "y"
                if key == sdl2.SDLK_z:
                    nameEntryText += "z"
                if key == sdl2.SDLK_SPACE:
                    nameEntryText += " "
                if key == sdl2.SDLK_BACKSPACE:
                    nameEntryText = nameEntryText[:-1]
                if key == sdl2.SDLK_RETURN:
                    starttimer = time.time()
                    Mix_FadeOutChannel(1, 1000)
                    nameEntry = False

        else:
            # Een SDL_QUIT event wordt afgeleverd als de gebruiker de applicatie
            # afsluit door bv op het kruisje te klikken
            if event.type == sdl2.SDL_QUIT:
                moet_afsluiten = True
                break
            # Een SDL_KEYDOWN event wordt afgeleverd wanneer de gebruiker een
            # toets op het toetsenbord indrukt.
            # Let op: als de gebruiker de toets blijft inhouden, dan zien we
            # maar 1 SDL_KEYDOWN en 1 SDL_KEYUP event.

            # voorlopige beweging
            elif event.type == sdl2.SDL_KEYDOWN:  # or event.type == sdl2.SDL_KEYDOWN
                key = event.key.keysym.sym
                speed = 0.25  # 0.5 #0.125
                if key == sdl2.SDLK_q:
                    moet_afsluiten = True
                elif key == sdl2.SDLK_UP:  # or key == sdl2.SDLK_UP
                    if world_map[round(np.floor(p_speler[1] + speed * r_speler[1]))] \
                        [round(np.floor(p_speler[0] + speed * r_speler[0]))] == 0:
                        p_speler[0] += speed * r_speler[0]
                        p_speler[1] += speed * r_speler[1]
                        continue
                    elif world_map[round(np.floor(p_speler[1] + speed * r_speler[1]))][round(p_speler[0])] == 0:
                        p_speler[1] += speed * r_speler[1] / 2  # bewegen langs muur volgens y-coordinaat
                        continue
                    elif world_map[round(r_speler[1])][round(np.floor(p_speler[0] + speed * r_speler[0]))] == 0:
                        p_speler[0] += speed * r_speler[0] / 2  # bewegen langs muur volgens x-coordinaat
                        continue
                elif key == sdl2.SDLK_DOWN:
                    if world_map[round(np.floor(p_speler[1] - speed * r_speler[1]))][
                        round(np.floor(p_speler[0] - speed * r_speler[0]))] == 0:
                        p_speler[0] -= speed * r_speler[0]
                        p_speler[1] -= speed * r_speler[1]
                        continue
                elif key == sdl2.SDLK_RIGHT:
                    if world_map[round(np.floor(p_speler[1] + speed * r_speler[0]))][
                        round(np.floor(p_speler[0] - speed * r_speler[1]))] == 0:
                        p_speler[0] -= speed * r_speler[1]
                        p_speler[1] += speed * r_speler[0]
                        continue
                elif key == sdl2.SDLK_LEFT:
                    if world_map[round(np.floor(p_speler[1] - speed * r_speler[0]))][
                        round(np.floor(p_speler[0] + speed * r_speler[1]))] == 0:
                        p_speler[0] += speed * r_speler[1]
                        p_speler[1] -= speed * r_speler[0]
                        continue
                elif key == sdl2.SDLK_x:
                    key_x = True
                elif key == sdl2.SDLK_p:
                    p_pressed = True
                elif key == sdl2.SDLK_i:
                    inventory_bekijken = not inventory_bekijken
                elif key == sdl2.SDLK_SPACE:
                    spacebar_pressed = True
                break

            elif event.type == sdl2.SDL_KEYUP:  # toets loslaten
                # key = event.key.keysym.sym
                if key == sdl2.SDLK_p:
                    p_pressed = False

            # Analoog aan SDL_KEYDOWN. Dit event wordt afgeleverd wanneer de
            # gebruiker een muisknop indrukt
            elif event.type == sdl2.SDL_MOUSEBUTTONDOWN:
                button = event.button.button
                if button == sdl2.SDL_BUTTON_LEFT:
                    # ...
                    continue
            # Een SDL_MOUSEWHEEL event wordt afgeleverd wanneer de gebruiker
            # aan het muiswiel draait.
            elif event.type == sdl2.SDL_MOUSEWHEEL:
                if event.wheel.y > 0:
                    # ...
                    continue
            # Wordt afgeleverd als de gebruiker de muis heeft bewogen.
            # Aangezien we relative motion gebruiken zijn alle coordinaten
            # relatief tegenover de laatst gerapporteerde positie van de muis.
            elif event.type == sdl2.SDL_MOUSEMOTION:
                # Aangezien we in onze game maar 1 as hebben waarover de camera
                # kan roteren zijn we enkel geinteresseerd in bewegingen over de
                # X-as
                beweging = event.motion.xrel
                a = 0.00125 * beweging
                print("beweging:", a)
                r_speler_rot = np.array([r_speler[0], r_speler[1]])
                r_rot = np.array([[np.cos(a), np.sin(a)], [-np.sin(a), np.cos(a)]])
                r_speler = np.matmul(r_speler_rot, r_rot)
                continue
            # elif virutalmousemotion:
            #     beweging = virtualmouse
            #     print("heeey")
            #     a = 0.00125 * beweging
            #     r_speler_rot = np.array([r_speler[0], r_speler[1]])
            #     r_rot = np.array([[np.cos(a), np.sin(a)], [-np.sin(a), np.cos(a)]])
            #     r_speler = np.matmul(r_speler_rot, r_rot)
            #     continue


    # Polling-gebaseerde input. Dit gebruiken we bij voorkeur om bv het ingedrukt
    # houden van toetsen zo accuraat mogelijk te detecteren
    key_states = sdl2.SDL_GetKeyboardState(None)

    # if key_states[sdl2.SDL_SCANCODE_UP] or key_states[sdl2.SDL_SCANCODE_W]:
    # beweeg vooruit...

    if key_states[sdl2.SDL_SCANCODE_ESCAPE]:
        moet_afsluiten = True

def mousemovement(vmouse):
    global r_speler
    beweging = vmouse
    a = - 0.125 * beweging
    r_speler_rot = np.array([r_speler[0], r_speler[1]])
    r_rot = np.array([[np.cos(a), np.sin(a)], [-np.sin(a), np.cos(a)]])
    r_speler = np.matmul(r_speler_rot, r_rot)


def bereken_r_straal(r_speler, kolom):
    global r_cameravlak
    r_cameravlak = np.array([-1 * r_speler[1], r_speler[0]])  # rotatie over -90°
    r_straal = np.array([d_cameravlak * r_speler[0] + (-1 + 2 * kolom / BREEDTE) * r_cameravlak[0],
                         d_cameravlak * r_speler[1] + (-1 + 2 * kolom / BREEDTE) * r_cameravlak[1]])
    r_straal = np.array([r_straal[0] / np.linalg.norm(r_straal), r_straal[1] / np.linalg.norm(r_straal)])
    return r_straal


def raycast(p_speler, r_straal):
    global i_horizontaal
    global i_verticaal
    global i_is_horizontaal
    global gesneden_blok

    # stap 0: Initialiseer x en y met waarde 0
    x = 0
    y = 0

    # stap 1: bereken delta_h en delta_v
    delta_h = 1 / np.abs(r_straal[1])
    delta_v = 1 / np.abs(r_straal[0])

    # stap 2: bereken d_horizontaal
    if r_straal[1] < 0:
        d_horizontaal = (p_speler[1] - np.floor(p_speler[1])) * delta_h
    else:
        d_horizontaal = (1 - p_speler[1] + np.floor(p_speler[1])) * delta_h

    # stap 2: bereken d_verticaal
    if r_straal[0] < 0:
        d_verticaal = (p_speler[0] - np.floor(p_speler[0])) * delta_v
    else:
        d_verticaal = (1 - p_speler[0] + np.floor(p_speler[0])) * delta_v

    # stap 3-6:
    while True:
        # horizontale intersectiepunten:
        if d_horizontaal + x * delta_h <= d_verticaal + y * delta_v:
            i_horizontaal = np.array([p_speler[0] + (d_horizontaal + x * delta_h) * r_straal[0],
                                      round(p_speler[1] + (d_horizontaal + x * delta_h) * r_straal[1])])
            i_is_horizontaal = True
            if r_straal[1] >= 0:
                gesneden_blok = np.array([int(i_horizontaal[1]), int(np.floor(i_horizontaal[0]))])
                if world_map[gesneden_blok[0]][gesneden_blok[1]] != 0:
                    d_muur = d_horizontaal + x * delta_h
                    d_muur = d_muur * np.dot(r_speler, r_straal)
                    return d_muur
            else:
                gesneden_blok = np.array([int(i_horizontaal[1] - 1), int(np.floor(i_horizontaal[0]))])
                if world_map[gesneden_blok[0]][gesneden_blok[1]] != 0:
                    d_muur = d_horizontaal + x * delta_h
                    d_muur = d_muur * np.dot(r_speler, r_straal)
                    return d_muur
            x += 1
        else:
            i_verticaal = np.array([round(p_speler[0] + (d_verticaal + y * delta_v) * r_straal[0]),
                                    p_speler[1] + (d_verticaal + y * delta_v) * r_straal[1]])
            i_is_horizontaal = False
            if r_straal[0] >= 0:
                gesneden_blok = np.array([int(np.floor(i_verticaal[1])), int(i_verticaal[0])])
                if world_map[gesneden_blok[0]][gesneden_blok[1]] != 0:
                    d_muur = d_verticaal + y * delta_v
                    d_muur = d_muur * np.dot(r_speler, r_straal)
                    return d_muur
            else:
                gesneden_blok = np.array([int(np.floor(i_verticaal[1])), int(i_verticaal[0] - 1)])
                if world_map[gesneden_blok[0]][gesneden_blok[1]] != 0:
                    d_muur = d_verticaal + y * delta_v
                    d_muur = d_muur * np.dot(r_speler, r_straal)
                    return d_muur
            y += 1


def render_kolom(renderer, window, kolom, d_muur):
    global foto_x
    global texture_list
    global level
    wall_texture = texture_list[world_map[gesneden_blok[0]][gesneden_blok[1]]]
    breedte = wall_texture.size[0]  # 256
    hoogte = wall_texture.size[1]  # 256
    top = np.floor(window.size[1] * (d_muur + 1) / (2 * d_muur)).astype('int')
    bottom = np.floor(window.size[1] * (d_muur - 1) / (2 * d_muur)).astype('int')
    if i_is_horizontaal:  # als het een horizontale intersectie is:
        foto_x = breedte * (i_horizontaal[0] - np.floor(i_horizontaal[0]))
    if not i_is_horizontaal:  # als het een verticale intersectie is:
        foto_x = breedte * (i_verticaal[1] - np.floor(i_verticaal[1]))
    renderer.copy(wall_texture, srcrect=(int(foto_x), 0, 1, hoogte),
                  dstrect=(kolom, bottom, 1, top - bottom))  # blokjes


def cam_position_sprite():
    r_cameravlak = [-1 * r_speler[1], r_speler[0]]
    p_sprite_camco = np.zeros((p_sprite_worldco.shape[0], 2))
    p_sprite_camco2 = np.zeros((p_sprite_worldco.shape[0], 2))
    determinant = (r_cameravlak[0] * r_speler[1]) - (r_cameravlak[1] * r_speler[0])
    adj_matrix = np.array([[r_speler[1], -1 * r_cameravlak[1]], [-1 * r_speler[0], r_cameravlak[0]]])
    for i in range(0, p_sprite_camco.shape[0]):
        p_sprite_camco[i] = p_sprite_worldco[i] - p_speler
        p_sprite_camco[i] = (1 / determinant) * (np.matmul(adj_matrix, p_sprite_camco[i]))
        if p_sprite_camco[i][1] == 0:
            p_sprite_camco2[i] = np.array([0, d_cameravlak])
        else:
            p_sprite_camco2[i] = np.array([p_sprite_camco[i][0] / p_sprite_camco[i][1], d_cameravlak])
    return p_sprite_camco, p_sprite_camco2


def sort_sprites(p_sprite_camco, p_sprite_camco2, sprites_im):
    afstand = np.zeros(1)
    new_camco = np.zeros((1, 2))
    new_camco2 = np.zeros((1, 2))
    new_sprites = np.zeros(1)
    index = np.zeros(sprites_im.size)
    for i in range(1, sprites_im.size):
        index[i] = index[i - 1] + 1
    for j in range(0, sprites_im.size):
        for s in range(0, afstand.size):
            a_buffer = math.sqrt((p_sprite_camco[j][0] ** 2) + (p_sprite_camco[j][1] ** 2))
            if a_buffer >= afstand[s]:
                afstand = np.insert(afstand, s, values=a_buffer, axis=0)
                new_camco = np.insert(new_camco, s, values=p_sprite_camco[j], axis=0)
                new_camco2 = np.insert(new_camco2, s, values=p_sprite_camco2[j], axis=0)
                new_sprites = np.insert(new_sprites, s, values=index[j], axis=0)
    afstand = np.delete(afstand, afstand.size - 1)
    new_camco = np.delete(new_camco, new_camco.shape[0] - 1, 0)
    new_camco2 = np.delete(new_camco2, new_camco2.shape[0] - 1, 0)
    new_sprites = np.delete(new_sprites, new_sprites.shape[0] - 1, 0)
    return afstand, new_camco, new_camco2, new_sprites


def render_sprites(renderer, kolom, d_muur, sprites_im, sprites_bool, sprites_sort, p_sprite_camco, p_sprite_camco2,
                   afstand):
    for i in range(0, sprites_sort.size):
        j = int(sprites_sort[i])
        if sprites_bool[j]:
            if p_sprite_camco[i][1] >= 0 and d_muur > afstand[i] and -1 < p_sprite_camco2[i][0] < 1:
                breedte_sprite_scherm = int(breedte_sprite * 800 / afstand[i])
                x1_src = int((kolom - ((p_sprite_camco2[i][0] + 1) / 2 * BREEDTE - breedte_sprite_scherm / 2)) * (
                        afstand[i] / 4))
                y2_src = sprites_im[j].size[1]
                x1_dest = kolom
                y1_dest = int(
                    (math.floor((HOOGTE / 2) - ((HOOGTE / 2) / afstand[i])) + (1 - breedte_sprite) * 600 / afstand[i]))
                y2_dest = int(hoogte_sprite * 600 / afstand[i])
                renderer.copy(sprites_im[j], srcrect=(x1_src, 0, 1, y2_src), dstrect=(x1_dest, y1_dest, 1, y2_dest))


def teken_mini_map(renderer, p_speler):
    global world_map
    # oprapen van de 'kaart' verandert staat van key_m
    if key_m:
        # renderer.fill tekent een rechthoekje (begin_x, begin_y, breedte, hoogte), kleur
        renderer.fill((8, 5, 3 * world_map.shape[1] + 2, 3 * world_map.shape[0] + 5), sdl2.ext.Color(63, 23, 23, 128))
        # we lopen heel de world_map af en kijken waar een blokje staat,
        # daar tekenen we een wit blokje van 2 breed/hoog met alles 3 keer vergroot
        for i in range(-1, world_map.shape[0], 1):
            for j in range(0, world_map.shape[1], 1):
                if world_map[i][j] != 0:
                    renderer.fill((10 + 3 * j, 10 + 3 * i, 2, 2), sdl2.ext.Color(255, 255, 255))
        # de positie van de sprites wordt met een blauw blokje getekend
        for x in range(0, p_sprite_worldco.shape[0]):
            if sprites_bool[x]:
                renderer.fill((10 + 3 * int(p_sprite_worldco[x][0]), 10 + 3 * int(p_sprite_worldco[x][1]), 2, 2),
                              sdl2.ext.Color(10, 65, 255))
        # de positie van onze speler wordt met een geel blokje getekend
        renderer.fill((10 + 3 * int(p_speler[0]), 10 + 3 * int(p_speler[1]), 2, 2), sdl2.ext.Color(255, 255, 0))


def teken_mini_sleutels(renderer, sprites_im, keywhite):
    global sprites_bool
    global level
    for sleutel in range(1, level + 1, 1):
        if sprites_bool[sleutel]:
            renderer.copy(keywhite, srcrect=(0, 0, keywhite.size[0], keywhite.size[0]),
                          dstrect=(600 + 25 * sleutel, 65, 20, 20))
        if not sprites_bool[sleutel]:
            renderer.copy(sprites_im[sleutel], srcrect=(0, 0, sprites_im[sleutel].size[0], sprites_im[sleutel].size[0]),
                          dstrect=(600 + 25 * sleutel, 65, 20, 20))


def teken_interruptscherm(renderer, scherm_sprite):
    renderer.copy(scherm_sprite, srcrect=(0, 0, scherm_sprite.size[0], scherm_sprite.size[1]),
                  dstrect=(0, 0, BREEDTE, HOOGTE))


def schrijftekst(chars, charpath, drogetekst, xpos, ypos, renderer, scale):
    for j in drogetekst:
        for i in range(chars.shape[0]):
            if j == chars[i]:
                breedte = int(round(charpath[i].size[0] * scale))
                hoogte = int(round(charpath[i].size[1] * scale))
                ypos -= int(round(charpath[i].size[1] * scale))
                renderer.copy(charpath[i], srcrect=(0, 0, charpath[i].size[0], charpath[i].size[1]),
                              dstrect=(int(xpos), int(ypos), int(breedte), int(hoogte)))
                xpos += int(round(charpath[i].size[0] * scale + 2 * scale))
                ypos += int(round(charpath[i].size[1] * scale))
                break
            elif j == " ":
                xpos += int(round(charpath[0].size[0] * scale / 2 + 2 * scale))
                break


def berekentijd(tijd, minuut0):
    m = int(round(tijd // 60))  # conversie naar minuten en ...
    s = int(tijd % 60)  # ...seconden
    if minuut0 and m < 10:
        m = "0" + str(m)
    if minuut0 and s < 10:
        s = "0" + str(s)
    return m, s


def schrijf_timer(time, starttime, maxtijd, chars, charpath, renderer):
    leveltijd = maxtijd - time.time() + starttime
    m, s = berekentijd(leveltijd, True)
    schrijftekst(chars, charpath, str(m) + ":" + str(s), 628, 50, renderer, 1)


def schrijftop5(chars, charpath, renderer):
    i = 1
    with open('scoreboard.csv', encoding="utf8") as f:
        csv_reader = csv.DictReader(f)
        for line in csv_reader:
            if i > 5:
                break
            m, s = berekentijd(int(float(line["time"])), False)
            schrijftekst(chars, charpath, f"{i}. {line['name']}", 150, 275 + 45 * i, renderer, 1)
            schrijftekst(chars, charpath, f"{m} min {s} sec", 450, 275 + 45 * i, renderer, 1)
            i += 1


def save_sboard(naam, timer):
    fieldnames = ['name', 'time']
    row = [{'name': naam, 'time': timer}]
    with open('scoreboard_newscore.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(row)
    df_sb0 = pd.read_csv("scoreboard.csv")
    df_sb1 = pd.read_csv("scoreboard_newscore.csv")
    pd.concat([df_sb0, df_sb1]).to_csv("scoreboard.csv", index=False)


def sort_sboard():
    df = pd.read_csv("scoreboard.csv")
    sorted_df = df.sort_values(by=["time"], ascending=True)
    sorted_df.to_csv('scoreboard.csv', index=False)


def teken_life_bar(renderer):
    global flikkeren
    global start_flikker_tijd
    global tijd_flikkeren_aan
    global game_over
    # renderer.fill tekent een rechthoekje (begin_x, begin_y, breedte, hoogte), kleur
    health_in_seconds = max_health - (time.time() - start_time_game)
    health = health_in_seconds / max_health * 100  # in procent
    x_health = round(health * 8)  # in aantal pixels
    renderer.fill((0, 598, 800, 2), sdl2.ext.Color(128, 128, 128, 20))
    if not flikkeren and health_in_seconds < 10:
        flikkeren = True
        start_flikker_tijd = time.time()
    if flikkeren and health_in_seconds > 10:
        flikkeren = False
    if flikkeren:
        tijd_flikkeren_aan = time.time() - start_flikker_tijd
        if tijd_flikkeren_aan >= 0.35:
            renderer.fill((0, 598, 800, 2), sdl2.ext.Color(255, 255, 255, 20))
        if tijd_flikkeren_aan >= 0.7:
            renderer.fill((0, 598, 800, 2), sdl2.ext.Color(128, 128, 128, 20))
            start_flikker_tijd = time.time()
    renderer.fill((0, 598, x_health, 2), sdl2.ext.Color(255, 50, 50, 20))
    if health_in_seconds <= 0:
        game_over = True


def reset():
    global world_map
    global p_speler
    global start_time_game
    global flikkeren
    global level
    global game_over
    global key_x
    global p_sprite_worldco
    global sprites_bool
    global inventory
    global play_music
    if key_x:
        game_over = False
        start_time_game = time.time()
        key_x = False
        Mix_FadeOutChannel(2, 1000)
        play_music = True
    level = 1
    world_map = pd.read_excel(r'World_map.xlsx', sheet_name='Level1').to_numpy(np.int8)
    p_speler = np.array([3.0, 3.0])
    flikkeren = True
    p_sprite_worldco = np.array([[7.5, 7.5], [3.5, 3.5], [16, 20], [23, 22], [5, 7.5], [2.5, 7.5]])
    sprites_bool = np.array([True, True, False, False, True, True])
    inventory = []


# 1. Als dicht genoeg in de buurt van sprite en op bepaald toets (p) gedrukt dan wordt functie pick_up opgeroepen
# (in verwerk_input p_pressed op True zetten)
def pick_up(sprite):
    global p_pressed
    global inventory
    inventory.append(sprite)
    p_pressed = False
    # (check ook eerst of sprite True is voor pickup)


# 2. Inventory bekijken als op toets i wordt gedrukt
# (in verwerk_input inventory_bekijken toggelen)
# Eerst algemene achtergrond van lege iventory tekenen (leeg_inv)
# Dan for-lus over alle items in inventory en die op een vaste plaats tekenen.
def teken_inventory(renderer):
    global inventory
    inv_coord = [(90, 200), (230, 200), (370, 200), (510, 200), (650, 200),
                 (90, 370), (230, 370), (370, 370), (510, 370), (650, 370)]
    i = 0
    breedte = 130  # breedte van de getekende sprite in inventory
    hoogte = 140  # hoogte van dde getekende sprite in inventory
    leeg_inv = factory.from_image(resources.get_path("leeg_inv.png"))
    renderer.copy(leeg_inv, srcrect=(0, 0, leeg_inv.size[0], leeg_inv.size[1]),
                  dstrect=(0, 0, BREEDTE, HOOGTE))
    for item in inventory:
        renderer.copy(item, srcrect=(0, 0, breedte, int((breedte / item.size[0]) * item.size[1])),
                      dstrect=(inv_coord[i][0], inv_coord[i][1], breedte, hoogte))
        i += 1
        if i >= 10:
            return


def delete_from_inventory(item):
    global inventory
    index = inventory.index(item)
    del inventory[index]


def main():
    global resources
    global factory
    global world_map
    global p_speler
    global r_speler
    global texture_list
    global moet_afsluiten
    global level
    global starttimer
    global framerate
    global start_time_game
    global inventory
    global key_m
    global p_sprite_worldco
    global sprites_bool
    global play_music
    global p_pressed
    global key_up
    global virtualmouse
    global virutalmousemotion
    # Initialiseer de SDL2 bibliotheek
    sdl2.ext.init()

    # Maak een venster aan om de game te renderen
    window = sdl2.ext.Window("3D-game - Escaperoom®", size=(BREEDTE, HOOGTE))
    window.show()

    # Begin met het uitlezen van input van de muis en vraag om relatieve coordinaten
    sdl2.SDL_SetRelativeMouseMode(True)

    # Maak een renderer aan zodat we in ons venster kunnen renderen
    renderer = sdl2.ext.Renderer(window)

    # Inladen van alle textures/sprites
    resources = sdl2.ext.Resources(__file__, "resources")
    factory = sdl2.ext.SpriteFactory(sdl2.ext.TEXTURE, renderer=renderer)
    wall_texture1 = factory.from_image(resources.get_path("muur4.png"))
    wall_texture2 = factory.from_image(resources.get_path("muur2.png"))
    wall_texture3 = factory.from_image(resources.get_path("muur1.png"))
    wall_texture4 = factory.from_image(resources.get_path("muur5.png"))
    wall_texture5 = factory.from_image(resources.get_path("muur3.png"))
    wall_texture6 = factory.from_image(resources.get_path("muur6.png"))
    wall_texture7 = factory.from_image(resources.get_path("portaal1.png"))
    wall_texture8 = factory.from_image(resources.get_path("portaal2.png"))
    wall_texture9 = factory.from_image(resources.get_path("portaal3.png"))

    texture_list = np.array([
        0,
        wall_texture1,
        wall_texture2,
        wall_texture3,
        wall_texture4,
        wall_texture5,
        wall_texture6,
        wall_texture7,
        wall_texture8,
        wall_texture9,
    ])

    # sprites
    # coördinaten op lijn 16
    lamp = factory.from_image(resources.get_path("Lamppost.png"))
    keygold = factory.from_image(resources.get_path("key-gold.png"))
    keysilver = factory.from_image(resources.get_path("key-silver.png"))
    keybronze = factory.from_image(resources.get_path("key-bronze.png"))
    keywhite = factory.from_image(resources.get_path("key-white.png"))
    donut = factory.from_image(resources.get_path("donut.png"))
    kaart = factory.from_image(resources.get_path("map.png"))
    sprites_im = np.array([lamp, keygold, keysilver, keybronze, donut, kaart])

    # interruptscreen
    startscherm = factory.from_image(resources.get_path("startscherm.png"))
    game_over_scherm = factory.from_image(resources.get_path("game_over_scherm.png"))
    endscherm = factory.from_image(resources.get_path("endscreen.png"))
    scoreboardscherm = factory.from_image(resources.get_path("scoreboard.png"))

    # Geluid
    Mix_OpenAudio(44100, MIX_DEFAULT_FORMAT, 2, 1024)
    pickupsound = Mix_LoadWAV(byteify(resources.get_path("ping.wav"), "utf-8"))
    levelup = Mix_LoadWAV(byteify(resources.get_path("levelup.wav"), "utf-8"))
    introsong = Mix_LoadWAV(byteify(resources.get_path("introsong.wav"), "utf-8"))
    eetgeluidje = Mix_LoadWAV(byteify(resources.get_path("crunch.7.wav"), "utf-8"))
    pagina = Mix_LoadWAV(byteify(resources.get_path("turn_page.wav"), "utf-8"))
    gameoversong = Mix_LoadWAV(byteify(resources.get_path("game_over_song.wav"), "utf-8"))

    # letters
    chars = np.array(
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P",
         "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
         "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v",
         "w", "x", "y", "z", ":", "|", "."])

    ch0 = factory.from_image(resources.get_path("0.png"))
    ch1 = factory.from_image(resources.get_path("1.png"))
    ch2 = factory.from_image(resources.get_path("2.png"))
    ch3 = factory.from_image(resources.get_path("3.png"))
    ch4 = factory.from_image(resources.get_path("4.png"))
    ch5 = factory.from_image(resources.get_path("5.png"))
    ch6 = factory.from_image(resources.get_path("6.png"))
    ch7 = factory.from_image(resources.get_path("7.png"))
    ch8 = factory.from_image(resources.get_path("8.png"))
    ch9 = factory.from_image(resources.get_path("9.png"))
    chA = factory.from_image(resources.get_path("A.png"))
    chB = factory.from_image(resources.get_path("B.png"))
    chC = factory.from_image(resources.get_path("C.png"))
    chD = factory.from_image(resources.get_path("D.png"))
    chE = factory.from_image(resources.get_path("E.png"))
    chF = factory.from_image(resources.get_path("F.png"))
    chG = factory.from_image(resources.get_path("G.png"))
    chH = factory.from_image(resources.get_path("H.png"))
    chI = factory.from_image(resources.get_path("I.png"))
    chJ = factory.from_image(resources.get_path("J.png"))
    chK = factory.from_image(resources.get_path("K.png"))
    chL = factory.from_image(resources.get_path("L.png"))
    chM = factory.from_image(resources.get_path("M.png"))
    chN = factory.from_image(resources.get_path("N.png"))
    chO = factory.from_image(resources.get_path("O.png"))
    chP = factory.from_image(resources.get_path("P.png"))
    chQ = factory.from_image(resources.get_path("Q.png"))
    chR = factory.from_image(resources.get_path("R.png"))
    chS = factory.from_image(resources.get_path("S.png"))
    chT = factory.from_image(resources.get_path("T.png"))
    chU = factory.from_image(resources.get_path("U.png"))
    chV = factory.from_image(resources.get_path("V.png"))
    chW = factory.from_image(resources.get_path("W.png"))
    chX = factory.from_image(resources.get_path("X.png"))
    chY = factory.from_image(resources.get_path("Y.png"))
    chZ = factory.from_image(resources.get_path("Z.png"))
    cha = factory.from_image(resources.get_path("a_lower.png"))
    chb = factory.from_image(resources.get_path("b_lower.png"))
    chc = factory.from_image(resources.get_path("c_lower.png"))
    chd = factory.from_image(resources.get_path("d_lower.png"))
    che = factory.from_image(resources.get_path("e_lower.png"))
    chf = factory.from_image(resources.get_path("f_lower.png"))
    chg = factory.from_image(resources.get_path("g_lower.png"))
    chh = factory.from_image(resources.get_path("h_lower.png"))
    chi = factory.from_image(resources.get_path("i_lower.png"))
    chj = factory.from_image(resources.get_path("j_lower.png"))
    chk = factory.from_image(resources.get_path("k_lower.png"))
    chl = factory.from_image(resources.get_path("l_lower.png"))
    chm = factory.from_image(resources.get_path("m_lower.png"))
    chn = factory.from_image(resources.get_path("n_lower.png"))
    cho = factory.from_image(resources.get_path("o_lower.png"))
    chp = factory.from_image(resources.get_path("p_lower.png"))
    chq = factory.from_image(resources.get_path("q_lower.png"))
    chr = factory.from_image(resources.get_path("r_lower.png"))
    chs = factory.from_image(resources.get_path("s_lower.png"))
    cht = factory.from_image(resources.get_path("t_lower.png"))
    chu = factory.from_image(resources.get_path("u_lower.png"))
    chv = factory.from_image(resources.get_path("v_lower.png"))
    chw = factory.from_image(resources.get_path("w_lower.png"))
    chx = factory.from_image(resources.get_path("x_lower.png"))
    chy = factory.from_image(resources.get_path("y_lower.png"))
    chz = factory.from_image(resources.get_path("z_lower.png"))
    chdup = factory.from_image(resources.get_path("dup.png"))
    chbar = factory.from_image(resources.get_path("bar.png"))
    chpun = factory.from_image(resources.get_path("pun.png"))

    charpath = np.array(
        [ch0, ch1, ch2, ch3, ch4, ch5, ch6, ch7, ch8, ch9, chA, chB, chC, chD, chE, chF, chG, chH, chI, chJ, chK, chL,
         chM, chN, chO, chP,
         chQ, chR, chS, chT, chU, chV, chW, chX, chY, chZ,
         cha, chb, chc, chd, che, chf, chg, chh, chi, chj, chk, chl, chm, chn, cho, chp, chq, chr, chs, cht, chu, chv,
         chw, chx, chy, chz, chdup, chbar, chpun])

    number_chars = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, ":"])

    number_0 = factory.from_image(resources.get_path("number_0.png"))
    number_1 = factory.from_image(resources.get_path("number_1.png"))
    number_2 = factory.from_image(resources.get_path("number_2.png"))
    number_3 = factory.from_image(resources.get_path("number_3.png"))
    number_4 = factory.from_image(resources.get_path("number_4.png"))
    number_5 = factory.from_image(resources.get_path("number_5.png"))
    number_6 = factory.from_image(resources.get_path("number_6.png"))
    number_7 = factory.from_image(resources.get_path("number_7.png"))
    number_8 = factory.from_image(resources.get_path("number_8.png"))
    number_9 = factory.from_image(resources.get_path("number_9.png"))
    number_dup = factory.from_image(resources.get_path("number_dup.png"))

    number_charpath = np.array(
        [number_0, number_1, number_2, number_3, number_4, number_5, number_6, number_7, number_8, number_9,
         number_dup])

    # startmuziek afspelen
    if nameEntry:
        Mix_PlayChannel(1, introsong, 0)  # speelt de startmuziek
        Mix_Volume(1, 35)  # volume van de muziek

    eindespel = False

    # Blijf frames renderen tot we het signaal krijgen dat we moeten afsluiten
    while not moet_afsluiten:

        data = ser.readline().decode().strip()
        print(data)
        # try:
        if data == "G1":
            p_pressed = True
        elif data == "G0":
            p_pressed = False
        elif data == "B2":
            key_up = True
        elif data == "B7":
            key_up = False
        elif data != "" and data[0] == "D":
            # print(data)
            data2 = data[1:]
            # print(data2)
            mousemovement(float(data2))


        # Onthoud de huidige tijd
        start_time = time.time()
        kolom = 0

        (p_sprite_camco, p_sprite_camco2) = cam_position_sprite()
        afstand, p_sprite_camco, p_sprite_camco2, sprites_sort = sort_sprites(p_sprite_camco,
                                                                              p_sprite_camco2, sprites_im)

        # Reset de rendering context
        renderer.clear()

        # tijdsmeter
        delta_2 = 0.0
        start_time_2 = time.time()
        einde_time_2 = time.time()
        delta_2 += einde_time_2 - start_time_2

        # teken de achtergrond
        # renderer.fill tekent een rechthoekje (begin_x, begin_y, breedte, hoogte), kleur
        renderer.fill((0, 0, BREEDTE, HOOGTE // 2), kleuren_skyblocks[level])
        renderer.fill((0, HOOGTE // 2, BREEDTE, HOOGTE // 2), sdl2.ext.Color(69, 69, 69))

        # Render de huidige frame
        for kolom in range(1, window.size[0]):
            r_straal = bereken_r_straal(r_speler, kolom)
            d_muur = raycast(p_speler, r_straal)
            render_kolom(renderer, window, kolom, d_muur)
            render_sprites(renderer, kolom, d_muur, sprites_im, sprites_bool, sprites_sort, p_sprite_camco,
                           p_sprite_camco2, afstand)

        # Minimap tekenen
        if key_m:
            teken_mini_map(renderer, p_speler)
        teken_life_bar(renderer)
        # timer
        schrijf_timer(time, starttimer, 600, number_chars, number_charpath, renderer)
        # tekst
        schrijftekst(chars, charpath, "Level: " + str(level), 10, 590, renderer, 0.5)
        schrijftekst(chars, charpath, "Framerate: " + str(framerate), 330, 590, renderer, 0.5)
        schrijftekst(chars, charpath, "Player: " + str(nameEntryText), 650, 590, renderer, 0.5)
        # teken minisleutel
        teken_mini_sleutels(renderer, sprites_im, keywhite)

        # Start- en beginscherm + GAME OVER scherm
        if nameEntry:
            start_time_game = time.time()
            teken_interruptscherm(renderer, startscherm)
            if int(1.5 * time.time()) % 2 == 0:
                schrijftekst(chars, charpath, nameEntryText, 350, 340, renderer, 1)
            else:
                schrijftekst(chars, charpath, nameEntryText + "|", 350, 340, renderer, 1)
        if game_over and not eindespel:
            if play_music:
                Mix_PlayChannel(2, gameoversong, 0)
                play_music = False
            teken_interruptscherm(renderer, game_over_scherm)
            reset()

        # inventory:
        for x in range(0, p_sprite_worldco.shape[0]):
            if p_speler[0] - 0.5 <= p_sprite_worldco[x][0] < p_speler[0] + 0.5 \
                    and p_speler[1] - 0.5 <= p_sprite_worldco[x][1] < p_speler[1] + 0.5:
                sprite = sprites_im[x]
                if sprites_bool[x]:
                    if p_pressed:
                        pick_up(sprite)
                        sprites_bool[x] = False
                        if sprite == donut:
                            start_time_game += 25
                            ser.write(b'98')
                            if start_time_game > time.time():
                                start_time_game = time.time()
                            delete_from_inventory(sprite)
                            Mix_PlayChannel(-1, eetgeluidje, 0)
                        elif sprite == kaart:
                            key_m = True
                            Mix_PlayChannel(-1, pagina, 0)
                        else:
                            Mix_PlayChannel(-1, pickupsound, 0)
                            ser.write(b'98')
                if int(1.5 * time.time()) % 2 == 0 and sprites_bool[x]:
                    schrijftekst(chars, charpath, "Druk op P om vast te nemen", 130, 340, renderer, 1)

        if inventory_bekijken:
            teken_inventory(renderer=renderer)

        # level overgang 1 naar 2
        if world_map[round(np.floor(p_speler[1] + 0.5 * r_speler[1]))][
            round(np.floor(p_speler[0] + 0.5 * r_speler[0]))] == 7:
            if keygold in inventory:
                p_speler = np.array([6.0, 12.0])
                world_map = pd.read_excel(r'World_map.xlsx', sheet_name='Level2').to_numpy(np.int8)
                level += 1
                delete_from_inventory(keygold)
                if kaart in inventory:
                    delete_from_inventory(kaart)
                p_sprite_worldco = np.array([[10, 18], [2, 23], [22, 15], [23, 22], [18, 10], [4, 4]])
                sprites_bool = np.array([True, True, True, False, True, True])
                key_m = False
                start_time_game = time.time()
                Mix_PlayChannel(-1, levelup, 0)
                ser.write(b'116')
            else:
                if int(1.5 * time.time()) % 2 == 0:
                    schrijftekst(chars, charpath, "Je hebt een sleutel nodig", 170, 340, renderer, 1)

        # level overgang 2 naar 3
        if world_map[round(np.floor(p_speler[1] + 0.5 * r_speler[1]))][
            round(np.floor(p_speler[0] + 0.5 * r_speler[0]))] == 8:
            if keygold and keysilver in inventory:
                p_speler = np.array([19.0, 34.0])
                # r_speler = np.array([1 / math.sqrt(2), 1 / math.sqrt(2)])
                world_map = pd.read_excel(r'World_map.xlsx', sheet_name='Level3').to_numpy(np.int8)
                level += 1
                delete_from_inventory(keygold)
                delete_from_inventory(keysilver)
                if kaart in inventory:
                    delete_from_inventory(kaart)
                p_sprite_worldco = np.array([[18, 50], [3, 40], [26, 10], [13, 4], [12, 25], [13, 28]])
                sprites_bool = np.array([True, True, True, True, True, True])
                key_m = False
                start_time_game = time.time()
                Mix_PlayChannel(-1, levelup, 0)
                ser.write(b'116')

            else:
                if int(1.5 * time.time()) % 2 == 0:
                    schrijftekst(chars, charpath, "Je hebt twee sleutels nodig", 170, 340, renderer, 1)

        # level overgang 3 naar eindescherm
        if world_map[round(np.floor(p_speler[1] + 0.5 * r_speler[1]))][
            round(np.floor(p_speler[0] + 0.5 * r_speler[0]))] == 9:
            if keygold and keysilver and keybronze in inventory:
                Mix_PlayChannel(1, introsong, 0)
                Mix_Volume(1, 35)  # volume van de muziek
                endtimer = time.time() - starttimer
                endtimer_m, endtimer_s = berekentijd(endtimer, False)
                save_sboard(nameEntryText, endtimer)
                sort_sboard()
                eindespel = True
                inventory = []
                ser.write(b'116')
            else:
                if int(1.5 * time.time()) % 2 == 0 and not eindespel:
                    schrijftekst(chars, charpath, "Je hebt drie sleutels nodig", 170, 340, renderer, 1)
        if eindespel:
            if not spacebar_pressed:
                teken_interruptscherm(renderer, endscherm)
            if spacebar_pressed:
                teken_interruptscherm(renderer, scoreboardscherm)
                schrijftekst(chars, charpath, str(endtimer_m) + " min " + str(endtimer_s) + " sec", 365, 220, renderer,
                             1)
                schrijftop5(chars, charpath, renderer)

        # Verwissel de rendering context met de frame buffer
        renderer.present()
        end_time = time.time()
        delta = end_time - start_time
        framerate = round(1 / delta, 2)

        verwerk_input()
        window.refresh()

    # Sluit SDL2 af
    sdl2.ext.quit()


if __name__ == '__main__':
    main()
