__author__ = 'andrewsmiley'
import traceback
# todo find leading and trailing string match to words
#todo build filler method to identify words that match letters in stack and leading or trailing words

def load_demo_board(filename):
    lines = open(filename).read().split('\n')
    temp_lines = [x.replace(' ', '').split(',') for x in lines]
    for line in temp_lines:
        del line[-1]
    return temp_lines


def load_letter_scores(filename):
    lines = open(filename).read().split('\n')
    return {x.split(',')[0]: int(x.split(',')[1]) for x in lines}


class Word:
    def __init__(self, word, x_pos, y_pos, vertical, score=0):
        self.word = word
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.vertical = vertical
        self.score = score

    def __str__(self):
        return self.word


board = []
board_values = load_demo_board('board_values.csv')
letter_scores = load_letter_scores('letter_values.csv')
words = open('enable1.txt').read().split('\r\n')


def distance_to_top(board, x_pos, y_pos):
    distance = 0
    for i in reversed(range(0, y_pos)):
        if board[i][x_pos] == '':
            distance += 1

        else:
            break
    return distance


def print_board(board):
    for line in board:
        l = ''
        for item in line:
            if len(item) > 0:
                l += '%s,' % (item)
            else:
                l += ' ,'
        print l


def is_word(word):
    return word in words


def find_trailing(tstring):
    return [x for x in words if x[-len(tstring):] == tstring]


def find_leading(lstring):
    return [x for x in words if x[:len(lstring)] == lstring]


def get_ajacent_word(board, x_pos, y_pos, vertical):
    pass


def process_horizontal_word(board, x_pos, y_pos):
    word = Word('', x_pos, y_pos, False)
    letters = []
    for i in range(x_pos, len(board)):
        letters.append(board[y_pos][i])
        if i != len(board) - 1:
            if board[y_pos][i + 1] == '':
                break
    #make sure the word we pulled is real
    if ''.join(letters) in words:
        word.word = ''.join(letters)
        return word


def process_vertical_word(board, x_pos, y_pos):
    word = Word('', x_pos, y_pos, True)
    letters = []
    for i in range(y_pos, len(board)):
        letters.append(board[i][x_pos])
        if i != len(board):
            if i + 1 < len(board) and board[i + 1][x_pos] == '':
                break
    if ''.join(letters) in words:
        word.word = ''.join(letters)
        return word


def explore_horizontal(board, x_pos, y_pos):
    # found_words= []

    #do the check to make sure we're not on the right edge
    if x_pos != len(board) - 1:
        word = []
        #check for the horitzonal first
        if board[y_pos][x_pos + 1] != '':

            found = process_horizontal_word(board, x_pos, y_pos)
            if found is not None:
                return found


def explore_vertical(board, x_pos, y_pos):
    if y_pos != len(board) - 1:
        #now check the vertical
        if board[y_pos + 1][x_pos] != '':
            found = process_vertical_word(board, x_pos, y_pos)

            if found is not None:
                return found
                # found_words.append(found)

                # return found_words


def distance_to_next_letter_horizontal_l_t_r(board, x_pos, y_pos):
    distance = 1
    for i in range(x_pos, 15):
        if board[y_pos][i + 1] != '':
            break
        else:
            distance += 1
    return distance


def distance_to_next_letter_horizontal_r_t_l(board, x_pos, y_pos):
    distance = 1
    for i in reversed(range(x_pos, 15)):
        if board[y_pos][i - 1] != '':
            break
        else:
            distance = distance + 1
    return distance


def distance_to_next_letter_vertical_t_t_b(board, x_pos, y_pos):
    distance = 1
    for i in range(y_pos, 15):
        if board[y_pos + 1][x_pos] != '':
            break
        else:
            distance = distance + 1
    return distance


def distance_to_next_letter_vertical_b_t_t(board, x_pos, y_pos):
    distance = 1
    for i in reversed(range(y_pos, 14)):
        if board[y_pos - 1][x_pos] != '':
            break
        else:
            distance = distance + 1
    return distance


def find_words(board):
    '''
    note: words can only be played left to right and up to down
    '''
    found_vertical_tiles = []
    found_horizontal_tiles = []
    found_words = []
    board_copy = board[:]
    for i in range(0, len(board_copy)):
        # ii = i
        for ii in range(0, len(board_copy)):
            if i != len(board_copy) - 1:
                if '%s,%s' % (ii, i) in found_horizontal_tiles:
                    continue
                #if we're on the bottom row, we don't need to check
                #for vertical words cause we would have already found them
                if board_copy[i][ii] != '':
                    found = explore_horizontal(board, ii, i)
                    if found is not None:
                        [found_horizontal_tiles.append('%s,%s' % (x, found.y_pos)) for x in
                         range(found.x_pos, found.x_pos + len(found.word))]
                        found_words.append(found)

    for i in range(0, len(board_copy)):
        # ii = i
        for ii in range(0, len(board_copy)):
            if i != len(board_copy) - 1:
                if '%s,%s' % (ii, i) in found_vertical_tiles:
                    continue
                #if we're on the bottom row, we don't need to check
                #for vertical words cause we would have already found them
                if board_copy[i][ii] != '':
                    #if it's not a star meaning a found word and not an empty space, then we need to explore`
                    found = explore_vertical(board, ii, i)
                    if found is not None:
                        [found_vertical_tiles.append('%s,%s' % (found.x_pos, x)) for x in
                         range(found.y_pos, found.y_pos + len(found.word))]
                        found_words.append(found)

                    pass
    # for word in found_words:
    #     print word.word
    return found_words


def find_words_from_letters(letters):
    words_matching_length = [x for x in words if len(x) <= len(letters)]
    return [x for x in words_matching_length if can_make(letters, x, '')]


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
            word = ''.join(word)
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
            for ii in reversed(range(0, y_pos + 1)):
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

    if y_pos == len(board) - 1:
        return True

    for i in range(x_pos, x_pos + len(word)):
        if board[y_pos + 1][i] == '':
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
    if x_pos == len(board) - 1:
        return True
    for i in range(y_pos, y_pos + len(word)):
        if board[i][x_pos + 1] == '':
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
                #ok so if it's not a valid word, we need to ensure that it is not an intersecting word
                if x_pos != 0 and board[i][x_pos - 1] != '':
                    start = 0
                    for iii in reversed(range(0, x_pos - 1)):
                        if board[i][iii] != '':
                            start = iii
                        else:
                            break
                    intersecting_word = []
                    for iii in range(start, len(board)):
                        if board[i][iii] != '':
                            intersecting_word.append(board[i][iii])
                        else:
                            break
                    #now check to see if we're looking at an intersecting word..
                    if ''.join(intersecting_word) not in words:
                        return False
                else:
                    return False
    #


    return valid


def validate_vertical_stacked_rtl(board, x_pos, y_pos, word):
    valid = True
    if x_pos == len(board) - 1:
        return True
    for i in range(y_pos, y_pos + len(word)):
        if board[i][x_pos - 1] == '':
            continue
        else:
            word_list = []
            for ii in reversed(range(0, x_pos + 1)):
                if board[i][ii] != '':
                    word_list.append(board[i][ii])
                else:
                    break
            # if ''.join(list(word_list))
            if ''.join(reversed(word_list)) not in words:
                if x_pos != len(board) - 1 and board[i][x_pos + 1] != '':
                    start = 0
                    for iii in reversed(range(0, x_pos - 1)):
                        if board[i][iii] != '':
                            start = iii
                        else:
                            break
                    intersecting_word = []
                    for iii in range(start, len(board)):
                        if board[i][iii] != '':
                            intersecting_word.append(board[i][iii])
                        else:
                            break
                    #now check to see if we're looking at an intersecting word..
                    if ''.join(intersecting_word) not in words:
                        return False
                else:
                    return False
    return valid


def validate_horizontal_ltr(board, x_pos, y_pos):
    word_list = []
    for i in range(x_pos, len(board)):
        if board[y_pos][i] != '':
            word_list.append(board[y_pos][i])
        else:
            break
    return ''.join(word_list) in words


def validate_vertical_ttb(board, x_pos, y_pos):
    word_list = []
    for i in range(y_pos, len(board)):
        if board[i][x_pos] != '':
            word_list.append(board[i][x_pos])
        else:
            break
    return ''.join(word_list) in words


def update_board(board, word):
    try:
        if word.vertical:
            counter = 0
            for i in range(word.y_pos, word.y_pos + len(word.word)):
                if board[i][word.x_pos] == '' or board[i][word.x_pos] == word.word[counter]:
                    board[i][word.x_pos] = word.word[counter]
                    counter += 1
                else:
                    return False

        else:
            counter = 0
            for i in range(word.x_pos, word.x_pos + len(word.word)):
                if board[word.y_pos][i] == '' or board[word.y_pos][i] == word.word[counter]:
                    board[word.y_pos][i] = word.word[counter]
                    counter += 1
                else:
                    return False
    except Exception, e:
        traceback.print_exc()
        return False

    return True


def get_letter_positions(word, letter):
    positions = []
    for i in range(0, len(word)):
        if word[i] == letter:
            positions.append(i)
    return positions


#todo write function to validate that the spaces for the new word are not overwriting any existing letters
def find_moves(board, letters):
    #get our wrods
    moves = []
    words_on_board = find_words(board)
    #iterate over them  and then iterate over the letters and see if we can make a word by going...
    #todo left of the letter
    #todo right of the letter
    #todo ending in the letter
    #todo starting with the letter
    #todo containing the letter vertically
    #todo containing the letter horizontally
    #todo starting with the whole word
    #todo ending with the whole word
    words_from_letters = find_words_from_letters(letters)
    for word in words_on_board:
        trailing_words = [x for x in find_trailing(word.word) if can_make(letters, x, word.word)]
        leading_words = [x for x in find_leading(word.word) if can_make(letters, x, word.word)]
        if word.vertical:
            # pass
            #             # do left of the letter first
            #             # make sure we can play to the left
            for i in range(word.y_pos, word.y_pos + len(word.word)):
                #                 # pass
                #                 # print "words around %s in %s" %( board[i][word.x_pos], word)
                #                 if word.x_pos != 0:
                #                     for potential_word in words_from_letters:
                #                         #make sure we can play above
                #                         if i+1 - len(potential_word)  >-1:
                #                             _word =Word(potential_word, word.x_pos-1, i-len(potential_word)+1, True)
                #                             if validate_rules(board, _word ):
                #                                 # print "to the left"
                #                                 # print "%s %s %s" %(_word, _word.x_pos, _word.y_pos)
                #                                 # temp_board = [[y for y in x] for x in board]
                #                                 # update_board(temp_board, _word)
                #                                 # print_board(temp_board)
                #                                 moves.append(_word)
                #                     #now do the right of the letter
                #                 if word.x_pos < len(board)-1:
                #                         for potential_word in words_from_letters:
                #                             #make sure that the length of the
                #                             if i+1 - len(potential_word)  > -1:
                #                                 _word = Word(potential_word, word.x_pos+1, i-len(potential_word)+1, True)
                #                                 if validate_rules(board, _word):
                #                                     # print "to the right"
                #                                     # print "%s %s %s" % (_word, _word.x_pos, _word.y_pos)
                #
                #
                #                                     # temp_board = [[y for y in x] for x in board]
                #                                     # update_board(temp_board, _word)
                #                                     # print_board(temp_board)
                #                                     moves.append(_word)
                # now do intersecting the letter horizontally
                if 0 < word.x_pos < (len(board) - 1):
                    _letters = [x for x in letters]
                    _letters.append(board[i][word.x_pos])
                    #iterate over the words that contain the letter, now we need to validate each potential placement of the word
                    for potential_word in find_words_from_letters(_letters):
                        #ok so now we need to find the position of the letters in the word
                        letter_positions = get_letter_positions(potential_word, board[i][word.x_pos])
                        #now we need to iterate over the positions of the letter and try placing the word there
                        for position in letter_positions:
                            _word = Word(potential_word, word.x_pos - position, i, False)
                            if validate_rules(board, _word):
                                print "found intersecting word %s" % (potential_word)
                                moves.append(_word)
                            #
                            #
                            #
                            #             for leading_word in leading_words:
                            #                 if leading_word != word.word  and len(leading_word.replace(word.word, '')) + ((word.y_pos+len(word.word))-1) < len (board):
                            #                     _word = Word(leading_word, word.x_pos, word.y_pos, True)
                            #                     if validate_rules(board, _word):
                            #                         # print "%s %s %s" % (_word, _word.x_pos, _word.y_pos)
                            # #                        temp_board = [[y for y in x] for x in board]
                            # #                         update_board(temp_board, _word)
                            # #                         print_board(temp_board)
                            #                         moves.append(_word)
                            #             for trailing_word in trailing_words:
                            #
                            #                 if trailing_word != word.word and word.y_pos - len(trailing_word.replace(word.word, '')) >= 0:
                            #                     _word = Word(trailing_word, word.x_pos, word.y_pos-len(trailing_word.replace(word.word, '')), True)
                            #                     if validate_rules(board, _word):
                            #                         # print "%s %s %s" % (_word, _word.x_pos, _word.y_pos)
                            #                         # temp_board = [[y for y in x] for x in board]
                            #                         # update_board(temp_board, _word)
                            #                         # print_board(temp_board)
                            #                         moves.append(_word)
                            #     # if

                            # else:
                            # #todo fill in the stuff for horizontal words now
                            # for i in range(word.x_pos, word.x_pos+len(word.word)):
                            #     # print "words around %s in %s" % ( board[word.y_pos][i], word)
                            #     # make sure we can play above the  letter
                            #     if word.y_pos != 0:
                            #         for potential_word in words_from_letters:
                            #             #make sure the length of the potential word does not exceed the board
                            #             if i+1 - len(potential_word) > -1:
                            #                 _word = Word(potential_word, i-len(potential_word)+1, word.y_pos-1, vertical=False)
                            #                 if validate_rules(board, _word):
                            #                     # print "%s %s %s" % (_word, _word.x_pos, _word.y_pos)
                            #                     # temp_board = [[y for y in x] for x in board]
                            #                     # update_board(temp_board, _word)
                            #                     # print_board(temp_board)
                            #                     moves.append(_word)
                            #             # now play below the letter
                            #     if word.y_pos < len(board)-1:
                            #         for potential_word in words_from_letters:
                            #             #make sure we can play the word
                            #             if i + 1 - len(potential_word) > -1:
                            #                 _word = Word(potential_word, i - len(potential_word) + 1, word.y_pos + 1, vertical=False)
                            #                 if validate_rules(board, _word):
                            #                     # print "%s %s %s" % (_word, _word.x_pos, _word.y_pos)
                            #                     # temp_board = [[y for y in x] for x in board]
                            #                     # update_board(temp_board, _word)
                            #                     # print_board(temp_board)
                            #                     moves.append(_word)

                            #now do the word intersecting vertically
                            # if 0 < word.y_pos < (len(board) -1):
                            #     _letters= [x for x in letters]
                            #     _letters.append(board[word.y_pos][i])
                            #     #iterate over the words that contain the letter, now we need to validate each potential placement of the word
                            #     for potential_word in find_words_from_letters(_letters):
                            #         #ok so now we need to find the position of the letters in the word
                            #         letter_positions = get_letter_positions(potential_word, board[word.y_pos][i])
                            #         #now we need to iterate over the positions of the letter and try placing the word there
                            #         for position in letter_positions:
                            #             _word = Word(potential_word, i , word.y_pos-position, True)
                            #             if validate_rules(board, _word):
                            #                 print "found intersecting word %s" %(potential_word)
                            #                 moves.append(_word)

                            # for leading_word in leading_words:
                            #     if leading_word != word.word  and len(leading_word[:len(word.word)]) + ((word.x_pos+len(word.word))-1) < len (board):
                            #             _word = Word(leading_word, word.x_pos, word.y_pos, False)
                            #             if validate_rules(board, _word):
                            #                 # print "%s %s %s" % (_word, _word.x_pos, _word.y_pos)
                            #                 # temp_board = [[y for y in x] for x in board]
                            #                 # update_board(temp_board, _word)
                            #                 # print_board(temp_board)
                            #                 moves.append(_word)
                            #
                            #     pass
                            # for trailing_word in trailing_words:
                            #     if trailing_word != word.word  and  word.x_pos - len(trailing_word.replace(word.word, '')) >= 0:
                            #             _word = Word(trailing_word, word.x_pos-len(trailing_word[len(word.word):]), word.y_pos, False)
                            #             if validate_rules(board, _word):
                            #                 # print "%s %s %s" % (_word, _word.x_pos, _word.y_pos)
                            #                 # temp_board = [[y for y in x] for x in board]
                            #                 # update_board(temp_board, _word)
                            #                 # print_board(temp_board)
                            #                 moves.append(_word)
                            #
    for i in range(0, len(moves)):
        temp_board = [[y for y in x] for x in board]
        update_board(temp_board, moves[i])
        moves[i].score = calculate_word_score(temp_board, moves[i])
    #
    moves.sort(key=lambda x: x.score, reverse=True)
    #     # pass
    temp_board = [[y for y in x] for x in board]
    update_board(temp_board, moves[0])

    print "The recomended play is %s at x: %s y: %s for %s points" % (
    moves[0].word, moves[0].x_pos, moves[0].y_pos, moves[0].score)
    print_board(temp_board)
    #here we'll find the words
    #process the potential moves
    #and return them


def calculate_attached_word_vertical(_board, x_pos, y_pos):
    #first check to see if we are at the first letter or the last letter
    starting_point = y_pos
    if y_pos > 0 and _board[y_pos - 1] != '':

        for i in reversed(range(y_pos, 0)):
            if board[i - 1][x_pos] != '':
                starting_point = i - 1
    word = []
    for i in range(starting_point, len(board)):
        if _board[i][x_pos] != '':
            word.append(board[i][x_pos])
        else:
            break
    word = Word(''.join(word), x_pos, starting_point, True)
    return calculate_word_score(_board, word)


def calculate_word_score(_board, word):
    word_score = 0
    multiplier = 1
    if word.vertical:

        for i in range(word.y_pos, word.y_pos + len(word.word)+1):

            letter_score = letter_scores[_board[i][word.x_pos]]

            if 0 < word.y_pos < len(board) and (board[word.y_pos - 1][i] != '' or board[word.y_pos + 1][i] != ''):
                letter_score += calculate_attached_word_vertical(_board, word.x_pos, word.y_pos)
            if board_values[i][word.x_pos] == 'tl' and board[i][word.x_pos] == '':
                letter_score = letter_score * 3

            if board_values[i][word.x_pos] == 'dl' and board[i][word.x_pos] == '':
                letter_score = letter_score * 2
            if board_values[i][word.x_pos] == 'tw' and board[i][word.x_pos] == '':
                multiplier = 3
            if board_values[i][word.x_pos] == 'dw' and board[i][word.x_pos] == '':
                multiplier = 2
            word_score += letter_score

    else:
        for i in range(word.x_pos, word.x_pos + len(word.word)):
            letter_score = letter_scores[_board[word.y_pos][i]]
            if (0 <= word.y_pos < len(board) - 1 and board[word.y_pos + 1][i] != '') ^ (
                        0 < word.y_pos < len(board) and board[word.y_pos - 1][i] != ''):
                word_score += calculate_attached_word_vertical(_board, i,word.y_pos)

            if board_values[word.y_pos][i] == 'tl' and board[word.y_pos][i] == '':
                letter_score = letter_score * 3
            if board_values[word.y_pos][i] == 'dl' and board[word.y_pos][i] == '':
                letter_score = letter_score * 2
            if board_values[word.y_pos][i] == 'tw' and board[word.y_pos][i] == '':
                multiplier = 3
            if board_values[word.y_pos][i] == 'dw' and board[word.y_pos][i] == '':
                multiplier = 2
            word_score += letter_score
    if word.word == 'wife':
        print "wife score is %s" % (word_score * multiplier)
    return word_score * multiplier


def validate_rules(board, word, leading_word=False, trailing_word=False):
    valid = True
    temp_board = [[y for y in x] for x in board]
    # update_board(temp_board, word)
    if update_board(temp_board, word):
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
        return valid


#gonna write up real quick a little test case

board = load_demo_board('chris_game2.csv')
# temp_board = [[y for y in x] for x in board]
# _word = Word('streak', 9, 5, True)
# update_board(temp_board, _word)
# validate_vertical_stacked_rtl(temp_board, _word.x_pos, _word.y_pos, _word.word)
# print_board(board)
letters = 'eiaefwi'
word = Word("wife", 10, 1, False)
temp_board = [[y for y in x] for x in board]
update_board(temp_board, word)
calculate_word_score(temp_board, word)
# find_moves(board, letters)
