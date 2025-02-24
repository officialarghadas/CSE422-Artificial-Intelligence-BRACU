import heapq

inputs = open('input.txt', 'r')
outputs = open('output.txt', 'w')

cities_heu = {}
step_cost = {}

for i in inputs:
   paths = i.split()
   name,h_value, direct_path = paths[0], paths[1], paths[2:]
   if name not in cities_heu:
    cities_heu[name] = int(paths[1])
    step_cost[name] = direct_path

outputs.write(str(step_cost))
#outputs.write(str(len(step_cost[visited])))
inputs.close()
outputs.close()


#start_node = input("Please Enter Starting City: ")
#end_goal = input("Please Enter Your Destination: ")

start_node = "Arad"
end_goal = "Bucharest"

def star_algo(cities_heu, step_cost, start_node, end_goal):

  list = []
  cost = 0
  opti_path = ["Arad"]
  total_distance = 0

  heapq.heappush(list, (start_node, 0+cities_heu[start_node]))

  while list != None:

      visited, total_cost = heapq.heappop(list)

      for visited in step_cost:
        if visited != end_goal:
          for j in range(0, len(step_cost[visited])-1, 2):
            cost = int(step_cost[visited][j+1])
            city = step_cost[visited][j]
            heapq.heappush(list, (step_cost[visited][j], cost+cities_heu[city]))

            visited, total_cost = heapq.heappop(list)

          total_distance += total_cost
          opti_path.append(visited)
          if visited != start_node:
            continue


        return opti_path, total_distance



#start_node = input("Please Enter Starting City: ")
#end_goal = input("Please Enter Your Destination: ")

start_node = "Arad"
end_goal = "Bucharest"

opti_path, total_distance = star_algo(cities_heu, step_cost, start_node, end_goal)

if opti_path is None:
  print("NONE OF PATH IS OPTIMAL")
else:
  print(f"Path: {' -> '.join(opti_path)}")
  print(f"Total distance: {total_distance} km")

inputs.close()
outputs.close()

