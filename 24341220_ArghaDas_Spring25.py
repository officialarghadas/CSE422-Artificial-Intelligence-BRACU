#--------------------------------------task 1-------------------------------------
import random


# Define the chromosome structure
class Chromosome:
    def __init__(self, stop_loss, take_profit, trade_size):
        self.stop_loss = stop_loss
        self.take_profit = take_profit
        self.trade_size = trade_size
        self.fitness = 0


# Simulate trading to calculate fitness
def calculate_fitness(chromosome, historical_prices):
    capital = 1000  # Starting capital
    for price_change in historical_prices:
        trade_amount = capital * (chromosome.trade_size / 100)
        if price_change < -chromosome.stop_loss:
            loss = trade_amount * (chromosome.stop_loss / 100)
            capital -= loss
        elif price_change > chromosome.take_profit:
            profit = trade_amount * (chromosome.take_profit / 100)
            capital += profit
        else:
            capital += trade_amount * (price_change / 100)
    chromosome.fitness = capital - 1000


# Generate initial population
def initialize_population(size):
    population = []
    for _ in range(size):
        population.append(Chromosome(
            stop_loss=random.uniform(1, 99),
            take_profit=random.uniform(1, 99),
            trade_size=random.uniform(1, 99)
        ))
    return population


# Perform crossover
def crossover(parent1, parent2):
    split_point = random.randint(1, 2)
    if split_point == 1:
        return Chromosome(parent1.stop_loss, parent2.take_profit, parent2.trade_size), \
            Chromosome(parent2.stop_loss, parent1.take_profit, parent1.trade_size)
    else:
        return Chromosome(parent1.stop_loss, parent1.take_profit, parent2.trade_size), \
            Chromosome(parent2.stop_loss, parent2.take_profit, parent1.trade_size)


# Perform mutation
def mutate(chromosome, mutation_rate):
    if random.random() < mutation_rate:
        chromosome.stop_loss = random.uniform(1, 99)
    if random.random() < mutation_rate:
        chromosome.take_profit = random.uniform(1, 99)
    if random.random() < mutation_rate:
        chromosome.trade_size = random.uniform(1, 99)


# Main Genetic Algorithm
def genetic_algorithm(historical_prices, generations, population_size, mutation_rate):
    population = initialize_population(population_size)

    for _ in range(generations):
        # Calculate fitness
        for chromosome in population:
            calculate_fitness(chromosome, historical_prices)

        # Select parents (elitism: keep the top 2)
        population.sort(key=lambda x: x.fitness, reverse=True)
        new_population = population[:2]

        # Generate new offspring
        while len(new_population) < population_size:
            parent1, parent2 = random.sample(population[:10], 2)
            offspring1, offspring2 = crossover(parent1, parent2)
            mutate(offspring1, mutation_rate)
            mutate(offspring2, mutation_rate)
            new_population.extend([offspring1, offspring2])

        population = new_population

    # Return the best solution
    best_chromosome = max(population, key=lambda x: x.fitness)
    return best_chromosome


# Example usage
historical_prices = [-1.2, 3.4, -0.8, 2.1, -2.5, 1.7, -0.3, 5.8, -1.1, 3.5]
best_solution = genetic_algorithm(historical_prices, generations=10, population_size=20, mutation_rate=0.05)

# output
output = {
    "best_strategy": {
        "stop_loss": round(best_solution.stop_loss, 2),
        "take_profit": round(best_solution.take_profit, 2),
        "trade_size": round(best_solution.trade_size, 2),
    },
    #"Final_profit": round(best_solution.fitness, 2)
}
final_profit= round(best_solution.fitness, 2)
print(f'{output}, "Final_profit" : {final_profit}')

#--------------------------------------task 2-------------------------------------
# Perform two-point crossover
def two_point_crossover(parent1, parent2):
    # Representing chromosomes as lists for easy manipulation
    parent1_genes = [parent1.stop_loss, parent1.take_profit, parent1.trade_size]
    parent2_genes = [parent2.stop_loss, parent2.take_profit, parent2.trade_size]

    # Randomly choose two points ensuring the second point is after the first
    point1 = random.randint(0, 1)
    point2 = random.randint(point1 + 1, 2)

    # Create offspring by swapping genes between the two points
    offspring1_genes = parent1_genes[:point1] + parent2_genes[point1:point2] + parent1_genes[point2:]
    offspring2_genes = parent2_genes[:point1] + parent1_genes[point1:point2] + parent2_genes[point2:]

    # Convert back to Chromosome objects
    offspring1 = Chromosome(*offspring1_genes)
    offspring2 = Chromosome(*offspring2_genes)

    return offspring1, offspring2


# Example usage for Task 2
# Randomly select two parents from the initial population
population = initialize_population(4)  # Generate an initial population of size 4
parent1, parent2 = random.sample(population, 2)

# Perform two-point crossover
offspring1, offspring2 = two_point_crossover(parent1, parent2)

# Print the randomly generated population
#print("Randomly Generated Population:")
#for i, chromosome in enumerate(population):
    #print(f"Chromosome {i + 1}: {{'stop_loss': {round(chromosome.stop_loss, 2)}, "
          #f"'take_profit': {round(chromosome.take_profit, 2)}, "
          #f"'trade_size': {round(chromosome.trade_size, 2)}}}")

# Print the resultant offspring
print("\nOffspring after Two-Point Crossover:")
print("Offspring 1:", {
    "stop_loss": round(offspring1.stop_loss, 2),
    "take_profit": round(offspring1.take_profit, 2),
    "trade_size": round(offspring1.trade_size, 2)
})
print("Offspring 2:", {
    "stop_loss": round(offspring2.stop_loss, 2),
    "take_profit": round(offspring2.take_profit, 2),
    "trade_size": round(offspring2.trade_size, 2)
})
