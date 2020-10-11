import sys
import math
import functools

MAX_DEPTH = 6

board_size = int(input())  # The size of the board.
player_id = input()  # The ID of the player. 'A'=first player, 'B'=second player.

shared_moves = {
    'A2 R',
    'B2 L',
    'A1 R',
    'B1 L',
    'A1 T',
    'A2 B',
    'B1 T',
    'B2 B',
}

col_moves = {'T', 'B'}
row_moves = {'L', 'R'}


def flatten_boxes(boxes):
    list1 = functools.reduce(
        lambda m, box: m + list(map(lambda side: f'{box[0]} {side}', list(box[1]))), boxes, [])
    list2 = [i for i in list1 if not ((i[0]!='A' and i[-1] == 'L') or (i[1]!='1' and i[-1] == 'B'))]
    return list2


def remove_move(boxes, move):
    move_box, move_side = move.split(' ')
    clone = boxes[:]
    opposites = {
        'T': 'B',
        'B': 'T',
        'L': 'R',
        'R': 'L'
    }
    for i, box in enumerate(clone):
        if box[0] == move_box:
            new_sides = box[1].replace(move_side, '')
            clone[i] = (box[0], new_sides) if new_sides != '' else None
        elif (move in shared_moves and 
                ((move_box[0] == box[0][0] and move_side in col_moves) or 
                (move_box[1] == box[0][1] and move_side in row_moves) )):
            new_sides = box[1].replace(opposites[move_side], '')
            clone[i] = (box[0], new_sides) if new_sides != '' else None

    nonone = list(filter(lambda b: not (b is None), clone))

    return nonone


def is_candidate_closed_by(box, move):
    move_box, move_side = move.split(' ')

    opposites = {
        'T': 'B',
        'B': 'T',
        'L': 'R',
        'R': 'L'
    }

    if box[0] == move_box and box[1] == move_side:  # closes box
        return True
    elif move in shared_moves:
        if box[0] != move_box and box[1] == opposites[move_side] and move_box[0] == box[0][0] and move_side in col_moves:  # closes same cloumn
            return True
        elif box[0] != move_box and box[1] == opposites[move_side] and move_box[1] == box[0][1] and move_side in row_moves:  # closes same row
            return True

    return False


def closed_boxes(boxes, move):
    candidates = list(filter(lambda b: len(b[1]) == 1, boxes))
    closed = list(
        filter(lambda b: is_candidate_closed_by(b, move), candidates))

    return len(closed)


def minimax(boxes, max_turn, max_score, min_score, depth, alpha, beta, prnt = False):
    if depth == 0 or len(boxes) == 0: 
        return max_score - min_score

    if max_turn:
        max_eval = -1000000
        mv = ''
        children = flatten_boxes(boxes)
        children.sort(key=lambda move: closed_boxes(boxes, move), reverse=True)
        for move in children:
            new_moves = remove_move(boxes, move)
            closed = closed_boxes(boxes, move)
            new_max_score = max_score + closed
            new_max_turn = max_turn if closed > 0 else not max_turn
            rating = minimax(new_moves, new_max_turn, new_max_score, min_score, depth-1, alpha, beta)
            if rating > max_eval:
                max_eval = rating
                mv = move
            alpha = max(alpha,max_eval)
            if alpha >= beta:
                break
        if prnt:
            print(f'{mv} MSG {max_eval}')
        return max_eval
    else:
        min_eval = 1000000
        children = flatten_boxes(boxes)
        for move in children:
            new_moves = remove_move(boxes, move)
            closed = closed_boxes(boxes, move)
            new_min_score = min_score + closed
            new_max_turn = max_turn if closed > 0 else not max_turn
            rating = minimax(new_moves, new_max_turn, max_score, new_min_score, depth-1, alpha, beta)
            min_eval = min(rating, min_eval)
            beta = min(beta,min_eval)
            if beta<=alpha:
                break
        return min_eval


def move(boxes, player_score, opponent_score):
    minimax(boxes, True, player_score, opponent_score, MAX_DEPTH, -1000000, 1000000, True)

# game loop
while True:
    # player_score: The player's score.
    # opponent_score: The opponent's score.
    player_score, opponent_score = [int(i) for i in input().split()]
    boxes = []
    for i in range(int(input())):
        boxes.append(input().split())

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)
    
    # <box> <side> [MSG Optional message]
    move(boxes, player_score, opponent_score)
