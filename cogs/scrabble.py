from random import shuffle

### User uses a command to start a scrabble game
###  Three other users can join, once one player other than the starter joins, they can choose to begin the game
### 100 tiles will be generated, seven will be dealt to each player under a spoiler tag
### PogBot will ping the starting player to input a word, after the player submits, 
### An api call will be made to a dictionary and check if their inputted word matches
### if it is a match, then it will the player their score and also give them new letters until they have 7 tiles
### The Bot will then prompt the next player to take their turn
### They need to com
###The process will repeat until all 100 tiles have been removed from the bag


LETTERS = {
    "A": 1,
    "B": 3,
    "C": 3,
    "D": 2,
    "E": 1,
    "F": 4,
    "G": 2,
    "H": 4,
    "I": 1,
    "J": 8,
    "K": 5,
    "L": 1,
    "M": 3,
    "N": 1,
    "O": 1,
    "P": 3,
    "Q": 10,
    "R": 1,
    "S": 1,
    "T": 1,
    "U": 1,
    "V": 4,
    "W": 4,
    "X": 8,
    "Y": 4,
    "Z": 10,

}

a = "<:regional_indicator_a:>"
b = "<:regional_indicator_b:>"
c = "<:regional_indicator_c:>"
d = "<:regional_indicator_d:>"
e = "<:regional_indicator_e:>"
f = "<:regional_indicator_f:>"
g = "<:regional_indicator_g:>"
h = "<:regional_indicator_h:>"
i = "<:regional_indicator_i:>"
j = "<:regional_indicator_j:>"
k = "<:regional_indicator_k:>"
l = "<:regional_indicator_l:>"
m = "<:regional_indicator_m:>"
n = "<:regional_indicator_n:>"
o = "<:regional_indicator_o:>"
p = "<:regional_indicator_p:>"
q = "<:regional_indicator_q:>"
r = "<:regional_indicator_r:>"
s = "<:regional_indicator_s:>"
t = "<:regional_indicator_t:>"
u = "<:regional_indicator_u:>"
v = "<:regional_indicator_v:>"
w = "<:regional_indicator_w:>"
x = "<:regional_indicator_x:>"
y = "<:regional_indicator_y:>"
z = "<:regional_indicator_z:>"


def scrabble_score(word):
    total = 0
    for letter in word:
        total += LETTERS[letter]
    return total

def getBoardStr(board):
    """Return a emoji-representation of the board"""
    return (
        f"{board['1']}|{board['2']}|{board['3']}    1 2 3\n"
        f"-+-+-    -+-+-\n"
        f"{board['4']}|{board['5']}|{board['6']}    4 5 6\n"
        f"-+-+-    -+-+-\n"
        f"{board['7']}|{board['8']}|{board['9']}    7 8 9"
    )