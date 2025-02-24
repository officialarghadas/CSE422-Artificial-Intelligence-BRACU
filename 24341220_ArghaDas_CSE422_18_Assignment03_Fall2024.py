import random

leaf_nodes = [random.choice([-1, 1]) for i in range(2 ** 5)]

def alphabeta_pruning(depth, node_index, is_max, alpha, beta):

    if depth == 5:
        return leaf_nodes[node_index]

    if is_max:
        mx = float('-inf')

        for i in range(2):
            val = alphabeta_pruning(depth + 1, node_index * 2 + i, False, alpha, beta)
            mx = max(mx, val)
            alpha = max(alpha, val)

            if beta <= alpha:
                break

        return mx

    else:
        mn = float('inf')

        for i in range(2):
            val = alphabeta_pruning(depth + 1, node_index * 2 + i, True, alpha, beta)
            mn = min(mn, val)
            beta = min(beta, val)

            if beta <= alpha:
                break

        return mn


starting_player = int(input("Enter the starting player (0 for Scorpion, 1 for Sub-Zero): "))
total_rounds = 3
scorpion_rounds_won = 0
subzero_rounds_won = 0
rounds_played = 0
current_player = starting_player
round_winners = []


while scorpion_rounds_won <= (total_rounds // 2) and subzero_rounds_won <= (total_rounds // 2):

    if current_player == 0:
        result = alphabeta_pruning(0, 0, False, float('-inf'), float('inf'))  # Scorpion min
    else:
        result = alphabeta_pruning(0, 0, True, float('-inf'), float('inf'))  # Subzero max

    if result == -1:
        round_winners.append("Scorpion")
        scorpion_rounds_won += 1
    else:
        round_winners.append("Sub-Zero")
        subzero_rounds_won += 1

    current_player = 1 - current_player
    rounds_played += 1

if scorpion_rounds_won > subzero_rounds_won:
    game_winner = "Scorpion"
else:
    game_winner = "Sub-Zero"


print(f"Game Winner: {game_winner}")
print(f"Total Rounds Played: {rounds_played}")
for i, winner in enumerate(round_winners):
    print(f"Winner of Round {i+1}: {winner}")



#part 2 


def alphabeta_pruning(tree, depth, is_max, alpha, beta, magic=False):

    if depth == 3:
        return tree

    if is_max:
        mx = float('-inf')

        if magic:
            for i in tree:
                val = alphabeta_pruning(i, depth + 1, True, alpha, beta)
                mx = max(mx, val)
                alpha = max(alpha, val)

                if beta <= alpha:
                    break

            return mx

        else:
            for i in tree:
                val = alphabeta_pruning(i, depth + 1, False, alpha, beta)
                mx = max(mx, val)
                alpha = max(alpha, val)

                if beta <= alpha:
                    break

            return mx

    else:
        mn = float('inf')

        for i in tree:
            val = alphabeta_pruning(i, depth + 1, True, alpha, beta)
            mn = min(mn, val)
            beta = min(beta, val)

            if beta <= alpha:
                break

        return mn


def pacman_game(c):

    tree = [
        [[3, 6], [2, 3]],
        [[7, 1], [2, 0]]
    ]

    without_magic = alphabeta_pruning(tree, 0, True, float('-inf'), float('inf'))
    with_magic = max(alphabeta_pruning(tree[0], 1, True, float('-inf'), float('inf'), True) - c, alphabeta_pruning(tree[1], 1, True, float('-inf'), float('inf'), True) - c)

    if with_magic > without_magic:
        return f"The best strategy is to use dark magic. Best score: {with_magic}"
    else:
        return f"The best strategy is to not use dark magic. Best score: {without_magic}"

user_input=int(input("input a number:"))
print(pacman_game(user_input))