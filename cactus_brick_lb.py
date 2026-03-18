import common


def create_run(max_cacti = -1):
	
	size = get_world_size()
	start_cacti = num_items(Items.Cactus)
	right_top = (size - 1, size - 1)
	delay_ticks = 0
	delay_interval = 600
	#sort_duration = 6000 #6250
	sort_duration = size * 187.5
	
	start_dim = 0
	end_dim = size - 1
	
	def need_more_cacti():
		if max_cacti == -1:
			return True
		return num_items(Items.Cactus) - start_cacti < max_cacti
	
	def plant_cactus():
		if get_ground_type() != Grounds.Soil:
			harvest()
			till()
		plant(Entities.Cactus)
	
	def plant_cactus_column():
		for _ in range(get_world_size()):
			plant_cactus()
			move(North)
			
	def setup():
		drones = []
		common.go_to_pos(0, 0)
		for _ in range(get_world_size() - 1):
			drones.append(spawn_drone(plant_cactus_column))
			move(East)
		plant_cactus_column()
		move(East)
		common.wait_for_drones(drones)
		
	def sort_column_child():
		y = get_pos_y()
		common.wait_ticks(delay_ticks)
		for _ in range(start_dim, end_dim + 1):
			start_ticks = get_tick_count()
			while get_tick_count() - start_ticks < sort_duration:
				size_prev = measure(South)
				size_here = measure()
				size_next = measure(North)
				if y > 0 and size_prev > size_here:
					swap(South)
					size_here = measure()
				
				if size_here > size_next:
					swap(North)
			move(East)
			
	def sort_columns():
		global delay_ticks
		global start_dim
		global end_dim
		brick_max_drones = size / 2
		drones = []
		max_delay_ticks = brick_max_drones * delay_interval
		
		start_dim = 0
		end_dim = size / 2 - 1
		for i in range(brick_max_drones):
			delay_ticks = max_delay_ticks - i * delay_interval
			drones.append(spawn_drone(sort_column_child))
			move(North)
			move(North)
		
		start_dim = size / 2
		end_dim = size - 1
		common.go_to_pos(start_dim, 0)
		for i in range(brick_max_drones - 1):
			delay_ticks = max_delay_ticks - i * delay_interval
			drones.append(spawn_drone(sort_column_child))
			move(North)
			move(North)
		delay_ticks = max_delay_ticks - i * delay_interval
		sort_column_child()
		common.wait_for_drones(drones)
		
	def sort_row_child():
		x = get_pos_x()
		common.wait_ticks(delay_ticks)
		for _ in range(start_dim, end_dim + 1):
			start_ticks = get_tick_count()
			while get_tick_count() - start_ticks < sort_duration:
				size_prev = measure(West)
				size_here = measure()
				size_next = measure(East)
				if x > 0 and size_prev > size_here:
					swap(West)
					size_here = measure()
				
				if size_here > size_next:
					swap(East)
			move(North)
		
	def sort_rows():
		global delay_ticks
		global start_dim
		global end_dim
		common.go_to_pos(0, 0)
		brick_max_drones = size / 2
		drones = []
		max_delay_ticks = brick_max_drones * delay_interval
		
		start_dim = 0
		end_dim = size / 2 - 1
		for i in range(brick_max_drones):
			delay_ticks = max_delay_ticks - i * delay_interval
			drones.append(spawn_drone(sort_row_child))
			move(East)
			move(East)
		
		start_dim = size / 2
		end_dim = size - 1
		common.go_to_pos(0, start_dim)
		for i in range(brick_max_drones - 1):
			delay_ticks = max_delay_ticks - i * delay_interval
			drones.append(spawn_drone(sort_row_child))
			move(East)
			move(East)
		delay_ticks = max_delay_ticks - i * delay_interval
		sort_row_child()
		common.wait_for_drones(drones)
		
	def final_harvest():
		x, y = right_top
		common.go_to_pos(x, y)
		harvest()
	
	def sort_and_harvest():
		sort_columns()
		sort_rows()
		final_harvest()
	
	def run():
		while need_more_cacti():
			setup()
			sort_and_harvest()
		
	return run	

if __name__ == '__main__':
	set_world_size(12)
	clear()
	runner = create_run(33554432)
	runner()
