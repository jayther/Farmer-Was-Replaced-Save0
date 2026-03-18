import common
clear()
maze_size = get_world_size() / 4
num_mazes = get_world_size() ** 2 / maze_size ** 2

quick_print(num_mazes)

spawn_points = []

for x in range(maze_size / 2, get_world_size(), maze_size):
	for y in range(maze_size / 2, get_world_size(), maze_size):
		spawn_points.append((x,y))

start_point = spawn_points[0]

def start():
	common.go_to_pos(start_point[0], start_point[1])
	common.wait(0.5)
	plant(Entities.Bush)
	substance = maze_size * 2**(num_unlocked(Unlocks.Mazes) - 1)
	use_item(Items.Weird_Substance, substance)
	
	entity_type = get_entity_type()
	quick_print('entity type:', entity_type)
	common.wait(5)
	

for i in range(1, len(spawn_points)):
	start_point = spawn_points[i]
	spawn_drone(start)

start_point = spawn_points[0]
start()
