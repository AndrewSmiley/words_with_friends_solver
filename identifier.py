__author__ = 'andrewsmiley'
#todo find leading and trailing string match to words
#todo build filler method to identify words that match letters in stack and leading or trailing words
class Word:
    def __init__(self, word, x_pos, y_pos, vertical):
        self.word = word
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.vertical = vertical

    def __str__(self):
        return self.word

board =[]
words = open('enable1.txt').read().split('\r\n')


def distance_to_top(board, x_pos, y_pos):
    distance = 0
    for i in reversed(range(0, y_pos)):
        if board[i][x_pos] == '':
            distance += 1

        else:
            break
    return distance



def load_demo_board(filename):
    lines = open(filename).read().split()
    return [x.split(',') for x in lines]
def is_word(word):
    return word in words
def find_trailing(tstring):
    return [x for x in words if x[-len(tstring):] == tstring]
def find_leading(lstring):
    return [x for x in words if x[:len(lstring)] == lstring]
def get_ajacent_word(board, x_pos, y_pos, vertical):
    pass

def process_horizontal_word(board, x_pos, y_pos):
    word = Word('',x_pos, y_pos, False)
    letters = []
    for i in range(x_pos, len(board)):
        letters.append(board[y_pos][i])
        if i != len(board)-1:
            if board[y_pos][i+1] == '':
                break
    #make sure the word we pulled is real
    if ''.join(letters) in words:
        word.word = ''.join(letters)
        return word

def process_vertical_word(board, x_pos, y_pos):
    word = Word('',x_pos, y_pos, True)
    letters = []
    for i in range(y_pos, len(board)):
        letters.append(board[i][x_pos])
        if i != len(board):
            if board[i+1][x_pos] == '':
                break
    if ''.join(letters) in words:
        word.word = ''.join(letters)
        return word

def explore_horizontal(board, x_pos, y_pos):
    # found_words= []

    #do the check to make sure we're not on the right edge
    if x_pos != len(board)-1:
        word = []
        #check for the horitzonal first
        if board[y_pos][x_pos +1] != '':

            found = process_horizontal_word(board, x_pos, y_pos)
            if found is not None:
                return found


def explore_vertical(board, x_pos, y_pos):
    if y_pos != len(board)-1:
        #now check the vertical
        if board[y_pos+1][x_pos] != '':
            found = process_vertical_word(board, x_pos, y_pos)

            if found is not None:
                return found
                # found_words.append(found)

    # return found_words



def distance_to_next_letter_horizontal_l_t_r(board, x_pos, y_pos):
    distance = 1
    for i in range(x_pos, 15):
        if board[y_pos][i+1] != '':
            break
        else:
            distance += 1
    return distance
def distance_to_next_letter_horizontal_r_t_l(board, x_pos, y_pos):
    distance = 1
    for i in reversed(range(x_pos, 15)):
        if board[y_pos][i-1] != '':
            break
        else:
            distance = distance+1
    return distance
def distance_to_next_letter_vertical_t_t_b(board, x_pos, y_pos):
    distance = 1
    for i in range(y_pos, 15):
        if board[y_pos+1][x_pos] != '':
            break
        else:
            distance = distance + 1
    return distance

def distance_to_next_letter_vertical_b_t_t(board, x_pos, y_pos):
    distance = 1
    for i in reversed(range(y_pos, 14)):
        if board[y_pos-1][x_pos] != '':
            break
        else:
            distance = distance + 1
    return distance


def find_words(board):
    '''
    note: words can only be played left to right and up to down
    '''
    found_vertical_tiles= []
    found_horizontal_tiles= []
    found_words= []
    board_copy = board[:]
    for i in range(0,len(board_copy)):
        # ii = i
        for ii in range(0, len(board_copy)):
            if i != len(board_copy)-1:
                if '%s,%s' %(ii, i) in found_horizontal_tiles:
                    continue
                #if we're on the bottom row, we don't need to check
                #for vertical words cause we would have already found them
                if board_copy[i][ii] != '':
                    found = explore_horizontal(board, ii, i)
                    if found is not None:
                        [found_horizontal_tiles.append('%s,%s' %(x, found.y_pos)) for x in range(found.x_pos, found.x_pos+len(found.word))]
                        found_words.append(found)

    for i in range(0,len(board_copy)):
        # ii = i
        for ii in range(0, len(board_copy)):
            if i != len(board_copy)-1:
                if '%s,%s' %(ii, i) in found_vertical_tiles:
                    continue
                #if we're on the bottom row, we don't need to check
                #for vertical words cause we would have already found them
                if board_copy[i][ii] != '':
                    #if it's not a star meaning a found word and not an empty space, then we need to explore`
                    found = explore_vertical(board, ii, i)
                    if found is not None:
                        [found_vertical_tiles.append('%s,%s' %(found.x_pos, x)) for x in range(found.y_pos, found.y_pos+len(found.word))]
                        found_words.append(found)

                    pass
    for word in found_words:
        print word.word


def find_potential_moves(board,letters):

        for i in range(0,len(board)):
        # ii = i
            for ii in range(0, len(board)):
                pass


def can_make(letters, word, given_letters):
    if len(given_letters) == 1:
        index = word.find(given_letters)
        word = list(word)
        del word[index]
        word = ''.join(word)
    else:
        word = word.replace(given_letters, '')
    letters_copy = ''.join(letters)
    for letter in word:
        if len(letters_copy) > 0 and letter in letters_copy:
            index = letters_copy.find(letter)
            letters_copy = list(letters_copy)
            del letters_copy[index]
            letters_copy = ''.join(letters_copy)
            index = word.find(letter)
            word = list(word)
            del word[index]
            word= ''.join(word)
        elif len(letters_copy) > 0 and letter not in letters_copy:
            return False


    return len(word) == 0

def validate_horizontal_stacked_btt(board, x_pos, y_pos, word):
    valid = True
    if y_pos == 0:
        return True

    for i in range(x_pos, x_pos + len(word)):
        if board[y_pos - 1][i] == '':
            continue
        else:
            word_list = []
            for ii  in reversed(range(0, y_pos+1)):
                if board[ii][i] != '':
                    word_list.append(board[ii][i])
                else:
                    break
            if ''.join(reversed(list(word_list))) not in words:
                valid = False
                break

    return valid


def validate_horizontal_stacked_ttb(board, x_pos, y_pos, word):
    valid = True

    if y_pos == len(board)-1:
        return True

    for i in range(x_pos, x_pos+len(word)):
        if board[y_pos+1][i] == '':
            continue
        else:
            word_list = []
            for ii in range(y_pos, len(board)):
                if board[ii][i] != '':
                    word_list.append(board[ii][i])
                else:
                    break
                #should i just assign valid here?
            if ''.join(list(word_list)) not in words:
                valid = False
                break

    return valid
def validate_vertical_stacked_ltr(board, x_pos, y_pos, word):
    valid = True
    if x_pos ==len(board)-1:
        return True
    for i in range(y_pos, y_pos+len(word)):
        if board[i][x_pos+1] == '':
            continue
        else:
            word_list = []
            for ii in range(x_pos, len(board)):
                if board[i][ii] != '':
                    word_list.append(board[i][ii])
                else:
                    break
            # if ''.join(list(word_list))
            if ''.join(list(word_list)) not in words:
                valid = False
                break
    return valid
def validate_vertical_stacked_rtl(board, x_pos, y_pos, word):
    valid = True
    if x_pos ==len(board)-1:
        return True
    for i in range(y_pos, y_pos+len(word)):
        if board[i][x_pos-1] == '':
            continue
        else:
            word_list = []
            for ii in reversed(range(0, x_pos+1)):
                if board[i][ii] != '':
                    word_list.append(board[i][ii])
                else:
                    break
            # if ''.join(list(word_list))
            if ''.join(reversed(word_list)) not in words:
                valid = False
                break
    return valid
def validate_horizontal_ltr(board, x_pos, y_pos):

    word_list =[]
    for i in range(x_pos, len(board)):
        if board[y_pos][i] != '':
            word_list.append(board[y_pos][i])
        else:
            break
    return ''.join(word_list) in words
def validate_vertical_ttb(board, x_pos, y_pos):
        word_list=[]
        for i in range(y_pos, len(board)):
            if board[i][x_pos] != '':
                word_list.append(board[i][x_pos])
            else:
                break
        return ''.join(word_list) in words



def update_board(board, word):
    if word.vertical:
        counter= 0
        for i in range(word.y_pos, word.y_pos+len(word.word)):

            board[i][word.x_pos] = word.word[counter]
            counter += 1

    else:
        counter = 0
        for i in range(word.x_pos, word.x_pos+len(word.word)):

            board[word.y_pos][i] = word.word[counter]
            counter += 1

#todo write function to validate that the spaces for the new word are not overwriting any existing letters

def find_moves(board):
    #here we'll find the words
    #process the potential moves
    #and return them

    pass
def validate_rules(board, word ):
    valid= True
    temp_board = board[:]
    update_board(temp_board, word)
    if not word.vertical:
        #todo rule for horizontal stacked words top to bottom
        valid = validate_horizontal_stacked_ttb(temp_board, word.x_pos, word.y_pos, word.word)
        if not valid:
            return valid

        #todo rule for horizontal stacked words bottom to top
        valid = validate_horizontal_stacked_btt(temp_board, word.x_pos, word.y_pos, word.word)
        if not valid:
            return valid
        # todo rule for word starting at position left to right
        valid = validate_horizontal_ltr(temp_board, word.x_pos, word.y_pos)
        if not valid:
            return valid

    # todo rule for word starting at position with intersecting letter horizontally
    else:
        #todo rule for vertical stacked words left to right
        valid = validate_vertical_stacked_ltr(temp_board, word.x_pos, word.y_pos, word.word)
        if not valid:
            return valid

        #todo rule for vertical stacked words right to left


        valid = validate_vertical_stacked_rtl(temp_board, word.x_pos, word.y_pos, word.word)
        if not valid:
            return valid

    #todo rule for word starting at position top to bottom
        valid = validate_vertical_ttb(temp_board, word.x_pos, word.y_pos)
        if not valid:
            return valid

    #todo rule for word starting at position with intersecting letter vertically
    pass


#gonna write up real quick a little test case
board = load_demo_board('demo_board_2.csv')
# board[3][5]= 'a'
# board[4][5]='h'
# validate_vertical_stacked_ltr(board,5,3, 'ah')
word = Word('tame',14,2,True)
validate_rules(board,word)
# print distance_to_next_letter_horizontal_l_t_r(load_demo_board('demo_board.csv'),10, 3 )
# load_demo_board('demo_board.csv')
# [board.append(['' for x in range(0, 15)]) for x in range(0, 16)]
#
# find_words(load_demo_board('demo_board.csv'))
# _letters = list('elele')
# # _letters = ['w','u','v','u','c','u', 'e']
#
# word = ''
# # can_make(_letters,'reccer', word )
# # can_make(_letters, 'tine', 'ti')
# print "leading words"
# found = [x for x in find_leading(word) if can_make(_letters,x, word)]
#
# print "trailing words"
# found = [x for x in find_trailing(word) if can_make(_letters,x, word)]
# for x in found:
#     print x
# pass