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

	
def plant_multi(start, end):
	for _ in range(start, end + 1):
		plant_column()
		move(East)
		

def fertilize_multi(start, end):
	for _ in range(start, end + 1):
		fertilize_column()
		move(East)


def create_run(col_start, col_end, goal = -1, num_usable_drones = -1):
	num_cols = col_end - col_start + 1
	
	def get_usable_drones():
		if num_usable_drones == -1:
			return max_drones()
		return min(max_drones(), num_usable_drones)
	
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
	
	def harvest_multi(start, end):
		for _ in range(start, end + 1):
			harvest_column()
			if not need_more():
				break
			move(East)
	
	def run():
		common.go_to_pos(col_start, 0)
		
		drone_section_size = 1
		all_end = col_end
		m_drones = get_usable_drones()
		if m_drones < num_cols:
			drone_section_size = common.floor(num_cols / m_drones)
			all_end = col_start + (drone_section_size * m_drones - 1)
		
		# plant
		drones = []
		if drone_section_size == 1:
			for i in range(col_start, all_end):
				drones.append(spawn_drone(plant_column))
				move(East)
			plant_column()
		else:
			for x in range(col_start, all_end - drone_section_size, drone_section_size):
				start = x
				end = x + drone_section_size - 1
				
				def create_plant_task():
					plant_multi(start, end)
				
				drones.append(spawn_drone(create_plant_task))
				
				for _ in range(drone_section_size):
					move(East)
					
			start = x
			end = x + drone_section_size - 1
			plant_multi(start, end)
		
		common.go_to_pos(col_start, 0)
		
		for drone in drones:
			wait_for(drone)
			
		# fertilize
		drones = []
		if drone_section_size == 1:
			for i in range(col_start, all_end):
				drones.append(spawn_drone(fertilize_column))
				move(East)
			fertilize_column()
		else:
			for x in range(col_start, all_end - drone_section_size, drone_section_size):
				start = x
				end = x + drone_section_size - 1
				
				def create_fertilize_task():
					fertilize_multi(start, end)
				
				drones.append(spawn_drone(create_fertilize_task))
				
				for _ in range(drone_section_size):
					move(East)
					
			start = x
			end = x + drone_section_size - 1
			fertilize_multi(start, end)
		
		common.go_to_pos(col_start, 0)
		
		for drone in drones:
			wait_for(drone)
		
		# harvest
		drones = []
		if drone_section_size == 1:
			for i in range(col_start, all_end):
				drones.append(spawn_drone(harvest_column))
				move(East)
			harvest_column()
		else:
			for x in range(col_start, all_end - drone_section_size, drone_section_size):
				start = x
				end = x + drone_section_size - 1
				
				def create_harvest_task():
					harvest_multi(start, end)
				
				drones.append(spawn_drone(create_harvest_task))
				
				for _ in range(drone_section_size):
					move(East)
					
			start = x
			end = x + drone_section_size - 1
			harvest_multi(start, end)
		
		for drone in drones:
			wait_for(drone)
		
		common.go_to_pos(col_end, 0)
	return run


if __name__ == '__main__':
	og_size = get_world_size()
	set_world_size(22)
	goal = 1000000
	abs_goal = num_items(Items.Weird_Substance) + goal
	runner = create_run(0, 21, abs_goal, 4)
	while num_items(Items.Weird_Substance) < abs_goal:
		runner()
	set_world_size(og_size)
