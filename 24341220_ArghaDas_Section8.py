#####Task 1######

import random
import math

def strength(x):
    """Calculate strength based on the given formula."""
    return (math.log2(x + 1) + x) / 10

def utility_function(maxV, minV):
    """Calculate the utility value using the given formula."""
    i = random.choice([0, 1])
    return strength(maxV) - strength(minV) + ((-1) ** i * random.randint(1, 10) / 10)

def minimax(depth, is_maximizing, alpha, beta, maxV, minV):
    """Minimax algorithm with alpha-beta pruning."""
    if depth == 0:  # If leaf node, return computed utility value
        return utility_function(maxV, minV)

    if is_maximizing:
        max_eval = float('-inf')
        for _ in range(2):  # Two possible moves
            eval_value = minimax(depth - 1, False, alpha, beta, maxV, minV)
            max_eval = max(max_eval, eval_value)
            alpha = max(alpha, eval_value)
            if beta <= alpha:  # Prune remaining branches
                break
        return max_eval
    else:
        min_eval = float('inf')
        for _ in range(2):  # Two possible moves
            eval_value = minimax(depth - 1, True, alpha, beta, maxV, minV)
            min_eval = min(min_eval, eval_value)
            beta = min(beta, eval_value)
            if beta <= alpha:  # Prune remaining branches
                break
        return min_eval

def simulate_games(starting_player, carlsen_strength, caruana_strength):
    """Simulates four games between Carlsen and Caruana."""
    results = {"Magnus Carlsen Wins": 0, "Fabiano Caruana Wins": 0, "Draws": 0}
    
    for game in range(4):
        # Determine Max and Min for this game
        if (game % 2 == 0 and starting_player == 0) or (game % 2 == 1 and starting_player == 1):
            maxV, minV = carlsen_strength, caruana_strength
            max_player = "Magnus Carlsen"
            min_player = "Fabiano Caruana"
        else:
            maxV, minV = caruana_strength, carlsen_strength
            max_player = "Fabiano Caruana"
            min_player = "Magnus Carlsen"
        
        # Get utility value using Minimax
        utility = minimax(5, True, float('-inf'), float('inf'), maxV, minV)
        
        # Determine the winner
        if utility > 0:
            winner = max_player
            results[f"{max_player} Wins"] += 1
        elif utility < 0:
            winner = min_player
            results[f"{min_player} Wins"] += 1
        else:
            winner = "Draw"
            results["Draws"] += 1

        print(f"Game {game + 1} Winner: {winner} (Utility value: {round(utility, 2)})")

    # Print final results
    print("\nOverall Results:")
    for key, value in results.items():
        print(f"{key}: {value}")
    
    if results["Magnus Carlsen Wins"] > results["Fabiano Caruana Wins"]:
        print("Overall Winner: Magnus Carlsen")
    elif results["Magnus Carlsen Wins"] < results["Fabiano Caruana Wins"]:
        print("Overall Winner: Fabiano Caruana")
    else:
        print("Overall Winner: Draw")

# Taking Inputs
starting_player = int(input("Enter starting player for game 1 (0 for Carlsen, 1 for Caruana): "))
carlsen_strength = float(input("Enter base strength for Carlsen: "))
caruana_strength = float(input("Enter base strength for Caruana: "))

# Run the simulation
simulate_games(starting_player, carlsen_strength, caruana_strength)



########task 2##################


#2
import math
import random

def strength(x):
    return math.log2(x + 1) + x / 10

def utility(maxV, minV):
    t = random.randint(0, 1)
    random_component = (-1) ** t * random.randint(1, 10) / 10
    return strength(maxV) - strength(minV) + random_component

def minimax(depth, is_maximizing, alpha, beta, maxV, minV):
    if depth == 5:
        return utility(maxV, minV)
    
    if is_maximizing:
        max_eval = -math.inf
        for _ in range(2):  # Branching factor = 2
            eval = minimax(depth + 1, False, alpha, beta, maxV, minV)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = math.inf
        for _ in range(2):  # Branching factor = 2
            eval = minimax(depth + 1, True, alpha, beta, maxV, minV)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def minimax_with_mind_control(depth, is_maximizing, alpha, beta, maxV, minV):
    if depth == 5:
        return utility(maxV, minV)
    
    if is_maximizing:
        max_eval = -math.inf
        for _ in range(2):  # Branching factor = 2
            # MAX player controls MIN player's move
            eval = minimax_with_mind_control(depth + 1, False, alpha, beta, maxV, minV)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        # MIN player's move is controlled by MAX player
        return minimax_with_mind_control(depth + 1, True, alpha, beta, maxV, minV)

def main():
    first_player = int(input("Enter who goes first (0 for Light, 1 for L): "))
    cost = float(input("Enter the cost of using Mind Control: "))
    light_strength = float(input("Enter base strength for Light: "))
    l_strength = float(input("Enter base strength for L: "))
    
    maxV = light_strength if first_player == 0 else l_strength
    minV = l_strength if first_player == 0 else light_strength
    
    # Minimax without mind control
    value_without_mc = minimax(0, True, -math.inf, math.inf, maxV, minV)
    
    # Minimax with mind control
    value_with_mc = minimax_with_mind_control(0, True, -math.inf, math.inf, maxV, minV)
    
    # Subtract the cost of mind control
    value_with_mc_cost = value_with_mc - cost
    
    print(f"Minimax value without Mind Control: {value_without_mc:.2f}")
    print(f"Minimax value with Mind Control: {value_with_mc:.2f}")
    print(f"Minimax value with Mind Control after incurring the cost: {value_with_mc_cost:.2f}")
    
    # Decision logic
    if value_without_mc > 0 and value_with_mc_cost > value_without_mc:
        print("Light should use Mind Control.")
    elif value_without_mc > 0 and value_with_mc_cost <= value_without_mc:
        print("Light should NOT use Mind Control as the position is already winning.")
    elif value_without_mc < 0 and value_with_mc_cost > 0:
        print("Light should use Mind Control.")
    elif value_without_mc < 0 and value_with_mc_cost <= 0:
        print("Light should NOT use Mind Control as the position is losing either way.")
    elif value_without_mc > 0 and value_with_mc_cost < 0:
        print("Light should NOT use Mind Control as it backfires.")
    else:
        print("Light should NOT use Mind Control.")

if __name__ == "__main__":
    main()