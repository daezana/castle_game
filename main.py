"""
Castle game.
Author: Daezana
Date: June 24, 2022.
Version 1.0
"""

import tkinter as tk
import tkinter.messagebox
import CONFIG  # program constants
import pygame
from PIL import Image, ImageTk
from random import randint

COORDS_DICT = dict()  # for coordinates of squares
COUNTER_LIFE = 0  # PV for lives lost
COUNTER_ITEMS = 0  # for item to collect
PUZZLES_ANSWERS = list()  # list of all questions-answers
PUZZLES_COORDS_DICT = dict()  # for indexed coordinates of questions-answers


def read_matrix(file: str) -> list[list[int]]:
    """
    Game plan reading function.

    Param: file: str. Path of file containing the plan to plot.

    Return: list[list[int]]. Matrix of which each sublist represents
    a horizontal row of plan squares.
    """
    assert type(file) is str

    with open(file, "r", encoding="utf-8") as plan:
        matrix = [list(map(int, line.split())) for line in plan]

    return matrix


def show_map(plan: list) -> None:
    """
    Maze map display function.

    For each element of the plan(matrix), draw a square
    at the corresponding location, in a specific color
    by the value of the element.

    Param: plan: matrix: list[list[int]]. Matrix of which each sublist represents
    a horizontal row of plan squares.

    Changing global variables: <COORDS_DICT>: key: tuple: top left corner coordinates square,
    value: tuple: indexed coordinates square, and <COUNTER_ITEMS>: total number of items to collect.
    Initialize <PUZZLES_COORDS_DICT>: assign tuple of indexed coordinates to a question-answer.
    """
    global COORDS_DICT, COUNTER_ITEMS

    # initialise questions
    init_list_puzzles_answers(CONFIG.PUZZLES_FILE)

    # x0, y0 : top left corner square
    # x1, y1 : low right corner square
    y0, y1 = 0, CONFIG.PXL_SIDE
    for index_row, row in enumerate(plan):
        x0, x1 = 0, CONFIG.PXL_SIDE
        for index_column, square in enumerate(row):

            if square == 0:
                color = CONFIG.CLR_COULOIR
            elif square == 1:
                color = CONFIG.CLR_MUR
            elif square == 2:
                color = CONFIG.CLR_OBJECTIF
            elif square == 3:
                color = CONFIG.CLR_PORTE
                random_int = randint(0, len(PUZZLES_ANSWERS) - 1)
                # randomize a question
                # assign indexed coordinates of a square 'door', top left corner, to a question
                PUZZLES_COORDS_DICT[index_row, index_column] = PUZZLES_ANSWERS.pop(random_int)
            elif square == 4:
                color = CONFIG.CLR_OBJET
                # add object to find
                COUNTER_ITEMS += 1
            else:
                color = CONFIG.CLR_CASES
            # color square
            game_canvas.create_rectangle(x0, y0, x1, y1,
                                         fill=color,
                                         outline='white')
            COORDS_DICT[(x0, y0)] = (index_row, index_column)
            x0 += CONFIG.PXL_SIDE
            x1 += CONFIG.PXL_SIDE
        y0 += CONFIG.PXL_SIDE
        y1 += CONFIG.PXL_SIDE


def init_list_puzzles_answers(file: str):
    """
    Param: file: str. Path of file. Each line has a question then separator character then answer.

    Initialize <PUZZLES_ANSWERS>: list of all questions-answers.
    """
    with open(file, 'r', encoding='utf-8') as f:
        for index, line in enumerate(f.readlines()):
            # remove end-of-line marker
            # add to a list another list containing a question with his answer
            PUZZLES_ANSWERS.extend([line.strip().split(CONFIG.SEP_PUZZLES_FILE)])


def pprint_text(message: str, char_max: int) -> str:
    """
    Param: message: str.
    Param: char_max: int. Maximum number of characters on a line.

    Returns the text given in parameter by adding line breaks
    every <char_max> characters, avoiding to cut a word during a line return.
    """
    counter = 0
    pp_message = ''
    for sentence in message.split('\n'):
        for word in sentence.split():
            if (counter + len(word) + 1) <= char_max:
                pp_message += word + ' '
                counter += len(word) + 1
            else:
                pp_message += '\n' + word + ' '
                counter = 0
        pp_message += '\n'
        counter = 0
    return pp_message


def all_lives() -> None:
    """
    Displays 5 images in the canvas <life_canvas>.
    The 5 images has its own tag according to the list: <CONFIG.TAGS_ICON_LIFE>.
    """
    x0, y0 = CONFIG.LIFE_MARG_EXT, CONFIG.LIFE_MARG_EXT
    for i, name in enumerate(CONFIG.TAGS_ICON_LIFE):
        life_canvas.create_image(x0, y0,
                                 anchor='nw',
                                 image=icon_life_image,
                                 tags=name)
        x0 += icon_life_image.width() + CONFIG.LIFE_MARG_INT


def show_question(question: str, response: str):
    """
    Displays question in the frame <dialogue_frame>.
    Block player movements until the question is answered.

    Param: question: str.
    Param: response: str.
    """

    def valid(event):
        """
        If the player's answer is valid,
        allow the player to cross.
        Otherwise, the player loses a life.
        """
        global COUNTER_LIFE
        response_entry.destroy()
        if response_var.get().lower() == response:
            r = COORDS_DICT[player.goto][0]
            c = COORDS_DICT[player.goto][1]
            plan_matrice[r][c] = 0  # door erasing, reinit square
            # text good answer
            dialogue_var.set(pprint_text(CONFIG.AD_TRUE_ANSWER,
                                         CONFIG.CHARS_MAX))
            move()
        else:
            # one life lost
            life_canvas.delete(CONFIG.TAGS_ICON_LIFE[COUNTER_LIFE])
            COUNTER_LIFE += 1
            # text wrong answer
            dialogue_var.set(pprint_text(CONFIG.AD_FALSE_ANSWER,
                                         CONFIG.CHARS_MAX))
            # all lives lost
            if COUNTER_LIFE == 5:
                end_game(0)
        # unlock player movements
        root.bind('<Down>', go_down)
        root.bind('<Up>', go_up)
        root.bind('<Left>', go_left)
        root.bind('<Right>', go_right)

    # block player movements
    root.unbind('<Down>')
    root.unbind('<Up>')
    root.unbind('<Left>')
    root.unbind('<Right>')

    # show question
    dialogue_var.set(question)
    # Entry
    response_var = tk.StringVar()
    # to answer the question
    response_entry = tk.Entry(response_frame,
                              textvariable=response_var,
                              )
    response_entry.grid(row=0,
                        column=0,
                        sticky='news'
                        )
    # valid answer after pressing return
    root.bind('<Return>', valid)


def restart(choice: bool):
    """
    Param: choice: bool. If True: restart a game, otherwise: exit the game.

    Changing global variables: <COUNTER_LIFE>: reinitialize,
    and <plan_matrice>: reinitialize.
    """
    global COUNTER_LIFE, plan_matrice
    # if player wants to restart a game
    if choice:
        COUNTER_LIFE = 0  # reinit
        all_lives()  # reinit lives
        # reposition player localisation
        game_canvas.delete('iconPlayer')
        player.restart()
        # reinit map
        plan_matrice = read_matrix(CONFIG.PLAN_CHATEAU)
        show_map(plan_matrice)
        # reposition icon player
        game_canvas.create_rectangle(player.coordinates_square_player(CONFIG.PXL_SIDE),
                                     fill=CONFIG.CLR_VUE,
                                     outline='white')
        game_canvas.create_oval(player.coordinates_square_player(CONFIG.PXL_SIDE,
                                                                 CONFIG.PXL_REDUCE_PLAYER),
                                fill=CONFIG.CLR_PLAYER,
                                outline=CONFIG.CLR_PLAYER,
                                tags='iconPlayer'
                                )
    # if player doesn't want to restart
    else:
        # stop music
        pygame.mixer.music.stop()
        root.quit()


def end_game(result: int):
    """
    Display whether the player has won or lost.
    And ask if the player wants to play again.

    Param: result: int. If 1 player wins, otherwise he loses.
    """
    dialogue_var.set('')
    if result:
        move()
        end_msg_toplevel = tkinter.messagebox.askyesno(CONFIG.TITLE_END,
                                                       CONFIG.AD_END_WIN, )
        restart(end_msg_toplevel)
    else:
        end_msg_toplevel = tkinter.messagebox.askyesno(CONFIG.TITLE_END,
                                                       CONFIG.AD_END_LOSE, )
        restart(end_msg_toplevel)


def allow_move():
    """
    Allows movement according to the rules of the game.

    Changing global variables: <plan_matrice>: plan of indexed coordinates defining
    corridors, walls, doors, objets and the exit of the maze.
    and <COUNTER_ITEMS>: items to collect.
    """
    global plan_matrice, COUNTER_ITEMS
    # coordinates must be in the plan
    if 0 <= player.goto[0] <= CONFIG.GAME_WIDTH - CONFIG.PXL_SIDE and \
            0 <= player.goto[1] <= CONFIG.GAME_HEIGHT - CONFIG.PXL_SIDE:
        # indexed coordinates of the next square
        r_togo = COORDS_DICT[player.goto][0]
        c_togo = COORDS_DICT[player.goto][1]
        # item to collect
        if plan_matrice[r_togo][c_togo] == 4:
            plan_matrice[r_togo][c_togo] = 0  # reinit square
            COUNTER_ITEMS -= 1  # removes an object from the counter
            move()
        # door
        elif plan_matrice[r_togo][c_togo] == 3:
            show_question(pprint_text(PUZZLES_COORDS_DICT[r_togo, c_togo][0],
                                      CONFIG.CHARS_MAX),
                          PUZZLES_COORDS_DICT[r_togo, c_togo][1].lower())
        # exit
        elif plan_matrice[r_togo][c_togo] == 2:
            # if all items are collected
            if COUNTER_ITEMS == 0:
                end_game(1)
            else:
                dialogue_var.set(pprint_text(CONFIG.AD_NOT_ALL_PICK_UP,
                                             CONFIG.CHARS_MAX))
        # corridors
        elif plan_matrice[r_togo][c_togo] == 0:
            dialogue_var.set('')
            move()


def move():
    """
    Moves the player icon.
    Assigns the new coordinates to the <player> instance of the <Player> class.
    """
    # new coordinates
    player.coordinates = player.goto
    game_canvas.delete('iconPlayer')
    game_canvas.create_rectangle(player.coordinates_square_player(CONFIG.PXL_SIDE),
                                 fill=CONFIG.CLR_VUE,
                                 outline='white')
    game_canvas.create_oval(player.coordinates_square_player(CONFIG.PXL_SIDE,
                                                             CONFIG.PXL_REDUCE_PLAYER),
                            fill=CONFIG.CLR_PLAYER,
                            outline=CONFIG.CLR_PLAYER,
                            tags='iconPlayer'
                            )


def go_down(event):
    """
    Assign the requested coordinates to the <goto> attribute of the
    <player> instance of the <Player> class.
    Asks to check if the movement is possible.
    """
    x = player.coordinates[0]
    y = player.coordinates[1] + CONFIG.PXL_SIDE
    player.goto = (x, y)
    allow_move()


def go_up(event):
    """
    Assign the requested coordinates to the <goto> attribute of the
    <player> instance of the <Player> class.
    Asks to check if the movement is possible.
    """
    x = player.coordinates[0]
    y = player.coordinates[1] - CONFIG.PXL_SIDE
    player.goto = (x, y)
    allow_move()


def go_left(event):
    """
    Assign the requested coordinates to the <goto> attribute of the
    <player> instance of the <Player> class.
    Asks to check if the movement is possible.
    """
    x = player.coordinates[0] - CONFIG.PXL_SIDE
    y = player.coordinates[1]
    player.goto = (x, y)
    allow_move()


def go_right(event):
    """
    Assign the requested coordinates to the <goto> attribute of the
    <player> instance of the <Player> class.
    Asks to check if the movement is possible.
    """
    x = player.coordinates[0] + CONFIG.PXL_SIDE
    y = player.coordinates[1]
    player.goto = (x, y)
    allow_move()


def click_sound_button():
    """
    If the user clicks and the sound is playing the sound is paused,
    if the sound is already paused, unpause it.
    Change sound button icon.
    """
    # pause sound
    if sound_button_var.get():
        pygame.mixer.music.pause()
        sound_button.config(image=sound_play_image)
        sound_button_var.set(0)
    # unpause sound
    else:
        pygame.mixer.music.unpause()
        sound_button.config(image=sound_stop_image)
        sound_button_var.set(1)


class Player:
    def __init__(self, ):
        self.name = 'Player1'
        self.coordinates = CONFIG.START_POSITION  # top left corner square
        self.goto = (0, 0)

    def restart(self):
        """
        Init <goto> and <coordinates> attributes.
        """
        self.coordinates = CONFIG.START_POSITION
        self.goto = (0, 0)

    def coordinates_square_player(self, side: int, margin=0) -> tuple:
        """
        Return coordinates of a square at the current position given
        by self.coordinates.

        Param: side: int. Side of the square.
        Param: margin: int. Outer margin size.

        Return: tuple. x0, y0: top left corner, x1, y1: low right corner.
        """
        if margin:
            x0 = self.coordinates[0] + margin
            y0 = self.coordinates[1] + margin
            x1 = self.coordinates[0] + side - margin
            y1 = self.coordinates[1] + side - margin
        else:
            x0, y0 = self.coordinates
            x1, y1 = self.coordinates[0] + side, player.coordinates[1] + side
        return x0, y0, x1, y1


# MAIN WINDOW
root = tk.Tk()
root.title(CONFIG.TITLE_GAME)
root.resizable(False, False)
root.config(bg=CONFIG.CLR_MAIN_BG,
            )

# ICON WINDOWS
root.iconbitmap(default=CONFIG.ICON_FILE)

# GAME ZONE
game_canvas = tk.Canvas(root,
                        bd=0,
                        highlightthickness=0,
                        width=CONFIG.GAME_WIDTH,
                        height=CONFIG.GAME_HEIGHT,
                        bg=CONFIG.CLR_GAME_BG,
                        )
game_canvas.grid(row=3, column=0, columnspan=3, )

# game plan
plan_matrice = read_matrix(CONFIG.PLAN_CHATEAU)
show_map(plan_matrice)

# DIALOGUES
dialogue_var = tk.StringVar()
dialogue_var.set(pprint_text(CONFIG.AD_INITIALISATION,
                             CONFIG.CHARS_MAX))
dialogue_frame = tk.Frame(root,
                          bg=CONFIG.CLR_MAIN_BG,
                          width=CONFIG.DIALOGUE_WIDTH,
                          height=CONFIG.DIALOGUE_HEIGHT)

dialogue_label = tk.Label(dialogue_frame,
                          bg=CONFIG.CLR_MAIN_BG,
                          textvariable=dialogue_var,
                          )
dialogue_label.grid(sticky='news')
dialogue_frame.grid(row=1, column=0, rowspan=2, )
dialogue_frame.grid_propagate(False)  # prevent automatic resizing

# Responses
response_frame = tk.Frame(root,
                          bg=CONFIG.CLR_MAIN_BG,
                          width=CONFIG.RESPONSES_WIDTH,
                          height=CONFIG.RESPONSES_HEIGHT,
                          )
response_frame.grid(row=2, column=1, columnspan=2,
                    )

# Lives
icon_life_image = tk.PhotoImage(file=CONFIG.LIFE_ICON).subsample(
    CONFIG.ICON_REDUCE)
life_canvas = tk.Canvas(root,
                        bg=CONFIG.CLR_MAIN_BG,
                        bd=0,
                        highlightthickness=0,
                        width=CONFIG.LIVES_WIDTH,
                        height=CONFIG.LIVES_HEIGHT,
                        )
all_lives()
life_canvas.grid(row=0, column=1, columnspan=2, sticky='e')

# GamePlay
player = Player()  # new player
game_canvas.create_rectangle(player.coordinates_square_player(CONFIG.PXL_SIDE),
                             fill=CONFIG.CLR_VUE,
                             outline='white')
game_canvas.create_oval(player.coordinates_square_player(CONFIG.PXL_SIDE,
                                                         CONFIG.PXL_REDUCE_PLAYER),
                        fill=CONFIG.CLR_PLAYER,
                        outline=CONFIG.CLR_PLAYER,
                        tags='iconPlayer'
                        )

# Movements
root.bind('<Down>', go_down)
root.bind('<Up>', go_up)
root.bind('<Left>', go_left)
root.bind('<Right>', go_right)

# SOUND FRAME
sound_frame = tk.Frame(root,
                       bg=CONFIG.CLR_MAIN_BG,
                       height=CONFIG.SOUND_HEIGHT,
                       width=CONFIG.SOUND_WIDTH)
sound_frame.grid(row=0,
                 column=0,
                 sticky='w')
sound_frame.grid_propagate(False)

# Sound icons
sound_stop_image = ImageTk.PhotoImage(Image.open(
    CONFIG.STOP_ICON).resize(CONFIG.STOP_ICON_SIZE))
sound_play_image = ImageTk.PhotoImage(Image.open(
    CONFIG.PLAY_ICON).resize(CONFIG.PLAY_ICON_SIZE))

# Button play-pause
sound_button_var = tk.IntVar()
sound_button_var.set(1)  # initialise to 1, music playing
sound_button = tk.Button(sound_frame,
                         textvariable=sound_button_var,
                         image=sound_stop_image,
                         relief='flat',
                         bg=CONFIG.CLR_MAIN_BG,
                         activebackground=CONFIG.CLR_MAIN_BG,
                         borderwidth=0,
                         command=click_sound_button,
                         )
sound_button.grid()

# SOUND GESTION
pygame.mixer.init()
pygame.mixer.music.load(CONFIG.MUSIC_FILE)
pygame.mixer.music.play(-1,  # loop
                        fade_ms=10000)  # fade in
pygame.mixer.music.set_volume(0.6)

# GEOMETRY SIZE WINDOW
root.update()
# center the window
root.geometry(f"{root.winfo_width()}x{root.winfo_height()}"
              f"+{root.winfo_screenwidth() // 2 - root.winfo_width() // 2}"
              f"+{root.winfo_screenheight() // 2 - root.winfo_height() // 2}")

root.mainloop()
