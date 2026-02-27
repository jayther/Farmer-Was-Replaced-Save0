import common
import sunflower_column

first_run = True

def create_run(start_col, end_col, multi = False):
	
	def plant_cactus():
		if get_ground_type() != Grounds.Soil:
			harvest()
			till()
		plant(Entities.Cactus)
		common.maybe_water()
	
	def plant_cactus_column():
		change_hat(Hats.Cactus_Hat)
		for _ in range(get_world_size()):
			plant_cactus()
			move(North)
	
	def setup():
		common.go_to_pos(start_col, 0)
		if multi:
			drones = []
			for i in range(start_col, end_col):
				drones.append(spawn_drone(plant_cactus_column))
				move(East)
			plant_cactus_column()
		else:
			for i in range(start_col, end_col + 1):
				plant_cactus_column()
				if i != end_col:
					move(East)
	
	def sort_and_harvest_single():
		common.go_to_pos(start_col, 0)
		
		col_size = get_world_size()
		
		# bubble up each column individually
		for col in range(start_col, end_col + 1):
			for i in range(0, col_size - 1):
				for j in range(i, col_size - 1):
					size_here = measure()
					size_north = measure(North)
					if size_here > size_north:
						swap(North)
					move(North)
				common.go_to_pos(col, 0)
				sunflower_column.check_get_power()
			move(East)
		
		row_size = end_col - start_col + 1
		
		# bubble right each row individually
		common.go_to_pos(start_col, 0)
		for row in range(0, col_size):
			for i in range(row_size - 1):
				for j in range(i, row_size - 1):
					size_here = measure()
					size_east = measure(East)
					if size_here > size_east:
						swap(East)
					move(East)
				common.go_to_pos(start_col, row)
				sunflower_column.check_get_power()
			move(North)
			
		# all should be sorted, harvest here
		common.go_to_pos(end_col, get_world_size() - 1)
		harvest()
		common.go_to_pos(end_col, 0)
	
	def sort_column():
		change_hat(Hats.Cactus_Hat)
		col_size = get_world_size()
		col = get_pos_x()
		
		for i in range(0, col_size - 1):
			for j in range(i, col_size - 1):
				size_here = measure()
				size_north = measure(North)
				if size_north != None and size_here > size_north:
					swap(North)
				move(North)
			common.go_to_pos(col, 0)
			sunflower_column.check_get_power()
	
	def sort_row(row_start, row_end):
		change_hat(Hats.Cactus_Hat)
		row_size = end_col - start_col + 1
		common.go_to_pos(start_col, row_start)
		for row in range(row_start, row_end + 1):
			for i in range(row_size - 1):
				for j in range(i, row_size - 1):
					size_here = measure()
					size_east = measure(East)
					if size_east != None and size_here > size_east:
						swap(East)
					move(East)
				common.go_to_pos(start_col, row)
				sunflower_column.check_get_power()
			if row < row_end:
				move(North)
	
	def sort_and_harvest_multi():
		common.go_to_pos(start_col, 0)
		
		col_drones = []
		
		# bubble up each column individually
		for col in range(start_col, end_col):
			col_drones.append(spawn_drone(sort_column))
			move(East)
			
		# main drone
		sort_column()
		
		for drone in col_drones:
			wait_for(drone)
		
		row_size = end_col - start_col + 1
		row_drones = []
		col_size = get_world_size()
		
		# bubble right each row section
		common.go_to_pos(start_col, 0)
		row_start = -1
		row_end = -1
		
		# row_size is also max row drones
		section_size = col_size / row_size
		section_row = 0
		
		# subtracting section_row by section_size enables us to
		# add remainder rows to some drones
		for row in range(0, col_size - section_size):
			if section_row < 1:
				row_start = row
				# if we have one usable drone left, let the main drone take the rest
				if len(row_drones) == row_size - 1:
					break
			
			section_row += 1
			if section_row >= section_size:
				row_end = row
				def create_sort_row():
					sort_row(row_start, row_end)
				row_drones.append(spawn_drone(create_sort_row))
				section_row -= section_size
				
			move(North)
		
		# main drone, take the remaining rows
		row_end = col_size - 1
		sort_row(row_start, row_end)
		
		for drone in row_drones:
			wait_for(drone)
		
		# all should be sorted, harvest here
		common.go_to_pos(end_col, get_world_size() - 1)
		harvest()
		common.go_to_pos(end_col, 0)
	
	def sort_and_harvest():
		if multi:
			sort_and_harvest_multi()
		else:
			sort_and_harvest_single()
	
	def run():
		global first_run
		if not first_run:
			sort_and_harvest()
		else:
			first_run = False
		setup()
	
	return run

	