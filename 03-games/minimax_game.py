import sys
import math
import functools
import datetime

MAX_DEPTH = 3
total_flatten = 0
board_size = int(input())  # The size of the board.
player_id = input()  # The ID of the player. 'A'=first player, 'B'=second player.

def flatten_boxes(boxes):
    list1 = functools.reduce(
        lambda m, box: m + list(map(lambda side: f'{box[0]} {side}', list(box[1]))), boxes, [])
    list2 = [i for i in list1 if not (
        (i[0] != 'A' and i[-1] == 'L') or (i[1] != '1' and i[-1] == 'B'))]
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
        elif ((move_side == 'R' and move_box[1] == box[0][1] and ord(move_box[0])+1 == ord(box[0][0])) or
                (move_side == 'T' and move_box[0] == box[0][0] and ord(move_box[1])+1 == ord(box[0][1])) ):
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
    # closes same cloumn
    if move_side == 'R' and move_box[1] == box[0][1] and ord(move_box[0])+1 == ord(box[0][0]):
        return True
    # closes same row
    elif move_side == 'T' and move_box[0] == box[0][0] and ord(move_box[1])+1 == ord(box[0][1]):
        return True

    return False


def closed_boxes(boxes, move):
    candidates = list(filter(lambda b: len(b[1]) == 1, boxes))
    closed = list(
        filter(lambda b: is_candidate_closed_by(b, move), candidates))

    return len(closed)

# boxes [('A1', 'LTRB'), ('A2', 'LTRB'), ('B1', 'LTRB'), ('B2', 'LTRB')] - primera optimizacion, eliminar jugadas repetidas


def minimax(boxes, max_turn, max_score, min_score, depth, alpha, beta, prnt=False):
    # segunda optimizacion, cortar en profundidad y evaluar
    if depth == 0 or len(boxes) == 0:
        return max_score - min_score

    global total_flatten
    ans = 0
    if max_turn:
        max_eval = -1000000
        mv = ''

        #start = datetime.datetime.now()
        children = flatten_boxes(boxes)
        #children.sort(key=lambda move: closed_boxes(boxes, move), reverse=True)
        #end = datetime.datetime.now()
        #total_flatten=total_flatten+(end-start).total_seconds()*1000

        
        for move in children:
            new_moves = remove_move(boxes, move)
            # tercera optimizacion, usar numero de cajas cerradas para ordenar movimientos
            closed = closed_boxes(boxes, move)
            new_max_score = max_score + closed
            new_max_turn = max_turn if closed > 0 else not max_turn
            rating = minimax(new_moves, new_max_turn,
                             new_max_score, min_score, depth-1, alpha, beta)
            # cuarta optimizacion, usar poda alfa-beta
            if rating > max_eval:
                max_eval = rating
                mv = move
            alpha = max(alpha, max_eval)
            if alpha >= beta:
                break
        if prnt:
            print(f'{mv} MSG {max_eval}')
        ans = max_eval
    else:
        min_eval = 1000000

        #start = datetime.datetime.now()
        children = flatten_boxes(boxes)
        #children.sort(key=lambda move: closed_boxes(boxes, move), reverse=True)
        #end = datetime.datetime.now()
        #total_flatten=total_flatten+(end-start).total_seconds()*1000

        for move in children:
            new_moves = remove_move(boxes, move)
            closed = closed_boxes(boxes, move)
            new_min_score = min_score + closed
            new_max_turn = max_turn if closed > 0 else not max_turn
            rating = minimax(new_moves, new_max_turn, max_score,
                             new_min_score, depth-1, alpha, beta)
            min_eval = min(rating, min_eval)
            beta = min(beta, min_eval)
            if beta <= alpha:
                break
        ans = min_eval
    return ans


def move(boxes, player_score, opponent_score):
    minimax(boxes, True, player_score, opponent_score, MAX_DEPTH, -1000000, 1000000, True)

# game loop
# while True:
#     # player_score: The player's score.
#     # opponent_score: The opponent's score.

#     total_flatten = 0
#     player_score, opponent_score = [int(i) for i in input().split()]
#     boxes = []
#     for i in range(int(input())):
#         boxes.append(input().split())

#     # Write an action using print
#     # To debug: print("Debug messages...", file=sys.stderr, flush=True)
    
#     # <box> <side> [MSG Optional message]
#     start = datetime.datetime.now()
#     move(boxes, player_score, opponent_score)
#     end = datetime.datetime.now()
#     print((end-start).total_seconds()*1000, file=sys.stderr, flush=True)

#     print(f'total flat: {total_flatten}', file=sys.stderr, flush=True)
