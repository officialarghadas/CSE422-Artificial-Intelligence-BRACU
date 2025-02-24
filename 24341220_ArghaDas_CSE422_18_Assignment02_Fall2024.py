import random

# Input handling
with open("Assignment2_input.txt", 'r') as input_file:
    lines = input_file.readlines()
    N, T = map(int, lines[0].split())  # Number of courses (N) and timeslots (T)
    courses = [line.strip() for line in lines[1:]]

# Generate a random course schedule chromosome
def course_schedule_array_generator(NC, NS):
    binary = ['0', '1']
    schedule = ''.join(random.choice(binary) for _ in range(NC * NS))
    return schedule if '1' in schedule else course_schedule_array_generator(NC, NS)

# Generate an initial population of chromosomes
def population_array_generator(n):
    return [course_schedule_array_generator(N, T) for _ in range(n)]

# Fitness function
def fitness_check(string, nc, ns):
    # Split chromosome into timeslot segments
    timeslots = [string[i * nc:(i + 1) * nc] for i in range(ns)]

    # Overlap penalty
    overlap_penalty = sum(max(sum(map(int, timeslot)) - 1, 0) for timeslot in timeslots)

    # Consistency penalty
    course_counts = [0] * nc
    for timeslot in timeslots:
        for i, bit in enumerate(timeslot):
            course_counts[i] += int(bit)
    consistency_penalty = sum(abs(count - 1) for count in course_counts)

    return overlap_penalty + consistency_penalty

# Single-point crossover
def single_point_crossover(crome1, crome2):
    point = random.randint(1, len(crome1) - 1)
    return (crome1[:point] + crome2[point:], crome2[:point] + crome1[point:])

# Mutation function
def mutation(crome):
    point = random.randint(0, len(crome) - 1)
    mutated = crome[:point] + random.choice(['0', '1']) + crome[point + 1:]
    return mutated if '1' in mutated else mutation(crome)

# Genetic algorithm
def genetic_algo(population):
    population_store = population.copy()
    for _ in range(100):  # Limit iterations to 100
        first = random.choice(population_store)
        second = random.choice(population_store)
        off1, off2 = single_point_crossover(first, second)
        off1 = mutation(off1)
        off2 = mutation(off2)
        population_store.append(off1)
        population_store.append(off2)
        population_store.remove(min(population_store, key=lambda j: fitness_check(j, N, T)))

        for individual in population_store:
            if fitness_check(individual, N, T) == 0:  # Perfect fitness
                return individual, 0

    # Return best individual if perfect fitness isn't found
    best_individual = min(population_store, key=lambda j: fitness_check(j, N, T))
    return best_individual, fitness_check(best_individual, N, T)

# Part 2: Two-point crossover
def double_point_crossover(crome1, crome2):
    point1 = random.randint(1, len(crome1) - 2)
    point2 = random.randint(point1 + 1, len(crome1) - 1)
    print(f"Point 1 between: {point1 - 1} and {point1}")
    print(f"Point 2 between: {point2 - 1} and {point2}")

    c1p1, c1p2, c1p3 = crome1[:point1], crome1[point1:point2], crome1[point2:]
    c2p1, c2p2, c2p3 = crome2[:point1], crome2[point1:point2], crome2[point2:]
    offspring1 = c1p1 + c2p2 + c1p3
    offspring2 = c2p1 + c1p2 + c2p3
    return offspring1, offspring2

# Main execution
population = population_array_generator(4)  # Initial population size 4
print("Initial Population:", population)
target, fitness = genetic_algo(population)
print("Best Chromosome:", target)
print("Fitness Value:", -1 * fitness)

# Part 2: Two-point crossover
print("_________________Part 2___________________")
offspring1, offspring2 = double_point_crossover("001100010", "111100010")
print("Offspring 1:", offspring1)
print("Offspring 2:", offspring2)
