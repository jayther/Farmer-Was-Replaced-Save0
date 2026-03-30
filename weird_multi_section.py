import common


def plant_tree(x, y):
	if (x + y) % 2 == 0:
		plant(Entities.Tree)
	# else, grass

def fertilize_pattern(x, y):
	if ((x * 3) + y) % 5 == 0:
	#	print(x, y)
		while num_items(Items.Fertilizer) < 2:
			pass
		use_item(Items.Fertilizer)
		use_item(Items.Weird_Substance)
		use_item(Items.Fertilizer)

def plant_column():
	#change_hat(Hats.Top_Hat)
	x = get_pos_x()
	for y in range(get_world_size()):
		plant_tree(x, y)
		move(North)

def fertilize_column():
	#change_hat(Hats.Top_Hat)
	x = get_pos_x()
	for y in range(get_world_size()):
		fertilize_pattern(x, y)
		move(North)
		
def harvest_column():
	#change_hat(Hats.Top_Hat)
	for i in range(get_world_size()):
		while not can_harvest():
			pass
		harvest()
		move(North)

def create_run(col_start, col_end, goal = -1):
	def need_more():
		if goal == -1:
			return True
		return num_items(Items.Weird_Substance) < goal
		
	def harvest_column():
		#change_hat(Hats.Top_Hat)
		for i in range(get_world_size()):
			while not can_harvest() and need_more():
				pass
			if not need_more():
				break
			harvest()
			if not need_more():
				break
			move(North)
	
	def run():
		common.go_to_pos(col_start, 0)
		
		# plant
		drones = []
		for i in range(col_start, col_end):
			drones.append(spawn_drone(plant_column))
			move(East)
		plant_column()
		
		common.go_to_pos(col_start, 0)
		
		for drone in drones:
			wait_for(drone)
			
		# fertilize
		drones = []
		for i in range(col_start, col_end):
			drones.append(spawn_drone(fertilize_column))
			move(East)
		fertilize_column()
		
		common.go_to_pos(col_start, 0)
		
		for drone in drones:
			wait_for(drone)
		
		# harvest
		drones = []
		for i in range(col_start, col_end):
			drones.append(spawn_drone(harvest_column))
			move(East)
		harvest_column()
		
		for drone in drones:
			wait_for(drone)
		
		common.go_to_pos(col_end, 0)
	return run