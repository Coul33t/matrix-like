import tcod as libtcod
from time import sleep
from random import randint

#TODO:
# Coloration of the first char before ' '
# DONE Force character creation until X successive characters
# Try to blit on arbitrary positions (instead of char)
# DONE Debug chain generation
class Column:
    def __init__(self, height):
        # TODO: chance of having blank (markov chain)
        self.characters = []
        # unit : 10ms
        self.speed = 1 + randint(0, 10)
        self.current_ticks = 0

        self.blank_to_char_chance = 10
        self.char_to_blank_chance = 50
        self.minimum_sequence_length = 15
        self.maximum_sequence_length = 40
        self.minimum_void_length = 15
        self.maximum_void_length = 100


        self.generate_column(height)

    def generate_column(self, height):
        for i in range(height):
            rand = randint(0, 100)

            if i == 0:
                if rand < 50:
                    self.characters.append(' ')
                else:
                    self.characters.append(self.get_random_char())

            else:
                self.characters.insert(0, self.generate_next_char())

    def generate_next_char(self):
        if len(self.characters) < 5:
            return self.get_random_char()

        rand = randint(0, 100)

        if self.characters[0] == ' ':
            if self.characters[0:self.minimum_void_length].count(' ') < self.minimum_void_length:
                return ' '
            elif self.characters[0:self.maximum_void_length].count(' ') == self.maximum_void_length:
                return self.get_random_char()
            elif rand < self.blank_to_char_chance:
                return self.get_random_char()
            else:
                return ' '

        else:
            if ' ' in self.characters[0:self.minimum_sequence_length]:
                return self.get_random_char()
            elif self.characters[0:self.maximum_sequence_length].count(' ') == 0:
                return ' '
            elif rand < self.char_to_blank_chance:
                return ' '
            else:
                return self.get_random_char()

    def go_down(self):
        self.characters.pop()
        self.characters.insert(0, self.generate_next_char())

    def get_random_char(self):
        return chr(randint(65, 122))


w, h = 100, 100

libtcod.console_set_custom_font('Anikki_square_8x8.png', libtcod.FONT_LAYOUT_ASCII_INROW)
libtcod.console_init_root(w, h, 'Test', False)
con = libtcod.console_new(w, h)
libtcod.console_set_default_foreground(con, libtcod.green)

# libtcod.console_put_char(con, 5, 5, 'A')

libtcod.console_blit(con, 0, 0, w, h, 0, 0, 0)
libtcod.console_flush()

key = libtcod.Key()

columns = [Column(h) for i in range(w)]

ticks = 0
lowest_speed = 11

while not libtcod.console_is_window_closed():
    libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, None)
    if key.vk == libtcod.KEY_ESCAPE:
        break


    for i, column in enumerate(columns):
        if ticks != 0 and column.speed % ticks == 0:
            for j, char in enumerate(column.characters):
                libtcod.console_put_char(con, i, j, char)

            column.go_down()

        else:
            column.current_ticks += 1


    libtcod.console_blit(con, 0, 0, w, h, 0, 0, 0)
    libtcod.console_flush()
    sleep(0.01)
    ticks += 1
    if ticks > lowest_speed:
        ticks = 0





