import common
import sunflower_column

first_run = True

def create_run(start_col, end_col, max_cacti = -1):
	
	start_cacti = num_items(Items.Cactus)
	
	def need_more_cacti():
		if max_cacti == -1:
			return True
		return num_items(Items.Cactus) - start_cacti < max_cacti
	
	def plant_cactus():
		if get_ground_type() != Grounds.Soil:
			harvest()
			till()
		plant(Entities.Cactus)
		common.maybe_water()
	
	def plant_cactus_column():
		for _ in range(get_world_size()):
			plant_cactus()
			move(North)
		
	def plant_and_sort_column():
		plant_cactus_column()
		sort_column()
	
	def setup():
		common.go_to_pos(start_col, 0)
		drones = []
		for i in range(start_col, end_col):
			drones.append(spawn_drone(plant_and_sort_column))
			move(East)
		plant_and_sort_column()
		
		for drone in drones:
			wait_for(drone)
	
	def sort_column():
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
	
	def sort_row():
		row_size = get_world_size()
		row = get_pos_y()
		for i in range(row_size - 1):
			for j in range(i, row_size - 1):
				size_here = measure()
				size_east = measure(East)
				if size_east != None and size_here > size_east:
					swap(East)
				move(East)
			common.go_to_pos(0, row)
	
	def sort_and_harvest():
		
		row_drones = []
		
		common.go_to_pos(start_col, 0)
		
		# bubble right each row individually
		for row in range(start_col, end_col):
			row_drones.append(spawn_drone(sort_row))
			move(North)
			
		# main drone
		sort_row()
		
		for drone in row_drones:
			wait_for(drone)
		
		# all should be sorted, harvest here
		common.go_to_pos(end_col, get_world_size() - 1)
		harvest()
		common.go_to_pos(start_col, 0)
	
	def run():
		while need_more_cacti():
			setup()
			sort_and_harvest()
	
	return run

if __name__ == '__main__':
	clear()
	runner = create_run(0, 31, 33554432)
	runner()