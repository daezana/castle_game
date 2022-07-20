"""
Castle game. CONFIGURATION, CONSTANTS.
Author: Daezana
Date: June 24, 2022.
Version 1.0.
"""

# GEOMETRY GRID
# x -> column, y -> row
# root: lifeCanvas: row=0, column=1, rowspan=, columnspan=2, sticky='e',
# root: gameCanvas: row=3, column=0, rowspan=, columnspan=3, sticky=,
# root: dialogueFrame: row=1, column=0, rowspan=2, columnspan=, sticky=, grid_propagate(False)
# root: responseFrame: row=2, column=1, rowspan=, columnspan=2, sticky=,
# dialogueFrame: dialogueLabel: row=, column=, rowspan=, columnspan=, sticky='news',
# responseFrame: response1button: row=0, column=0, rowspan=, columnspan=, sticky='news',
# responseFrame: response2button: row=0, column=1, rowspan=, columnspan=, sticky='news',

# SIZE
GAME_WIDTH = 380  # NB_COLUMN * PXL_SIDE
GAME_HEIGHT = 540  # NB_ROW * PXL_SIDE
LIVES_WIDTH = 143  # 2*life_marg_ext + 5*(icon_width/reduce) + 4*life_marg_int
LIVES_HEIGHT = 33  # 2*life_marg_ext + (icon_width/reduce)
DIALOGUE_WIDTH = 237  # GAME_WIDTH - LIVES_WIDTH
DIALOGUE_HEIGHT = 66  # 2*LIVES_HEIGHT
RESPONSES_WIDTH = 93  # LIVES_WIDTH - 50
RESPONSES_HEIGHT = 33  # LIVES_HEIGHT
SOUND_HEIGHT = 33  # LIVES_HEIGHT
SOUND_WIDTH = 120

# PLAN
NB_COLUMN = 19
NB_ROW = 27
PXL_SIDE = 20
PXL_REDUCE_PLAYER = 3

# TEXTS SIZE
CHARS_MAX = 36

# IMAGE SIZE
LIFE_MARG_EXT = 5
LIFE_MARG_INT = 2


# TEXTS
TITLE_GAME = 'Jeu du château'
TITLE_QUESTION = 'Garde'
TITLE_END = 'Fin du Jeu'
AD_INITIALISATION = 'Pour sortir du labyrinthe, vous devez récupérer toutes les caisses vertes et trouver la sortie.'
AD_FALSE_ANSWER = 'Mauvaise réponse.\nLa porte vous reste fermée.'
AD_TRUE_ANSWER = 'Bonne réponse.\nVous pouvez continuer, mais restez sur vos gardes.'
AD_END_WIN = "Bravo ! Vous avez réussi.\nVoulez recommencez ?"
AD_END_LOSE = "Dommage ! Vous avez perdu.\nVoulez recommencez ?"
AD_NOT_ALL_PICK_UP = "Vous n'avez pas ramassez tous les objets.\nVous ne pouvez pas sortir."


# COLORS
CLR_MAIN_BG = '#d9d9d9'
CLR_GAME_BG = '#f2f2f2'
CLR_CASES = 'white'
CLR_COULOIR = 'white'
CLR_MUR = 'grey'
CLR_OBJECTIF = 'yellow'
CLR_PORTE = 'orange'
CLR_OBJET = 'green'
CLR_VUE = 'wheat'
CLR_EXTERIEUR = 'white'
CLR_PLAYER = '#cc0000'


# FILES
PLAN_CHATEAU = "plan_chateau.txt"
PUZZLES_FILE = 'puzzles_responses_fr.txt'
SEP_PUZZLES_FILE = '--'
ICON_FILE = 'images/castle_icon_open_clipart_vectors_27383_pixabay.ico'
MUSIC_FILE = 'sounds/voxel_revolution_kevin_macleod.ogg'


# PLAYER
START_POSITION = (20, 0)  # top left corner square

# LIFE MANAGEMENT
LIFE_ICON = 'images/heart_red_clker_free_vector_images_pixabay.png'
LIFE_ICON_SIZE = (50, 46)
ICON_REDUCE = 2
TAGS_ICON_LIFE = ['heart1', 'heart2', 'heart3', 'heart4', 'heart5']

# ICONS
STOP_ICON = 'images/sound_lower_raphaelsilva_pixabay_transparency.png'  # (1280, 1280)
STOP_ICON_SIZE = (25, 25)
PLAY_ICON = 'images/sound_higher_raphaelsilva_pixabay_transparency.png'  # (1280, 1280)
PLAY_ICON_SIZE = (25, 25)
