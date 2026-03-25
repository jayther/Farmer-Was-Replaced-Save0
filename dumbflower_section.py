import common

def create_run(col_start, col_end, max_power = -1):
	start_power = num_items(Items.Power)
	def need_more_power():
		if max_power == -1:
			return True
		return num_items(Items.Power) - start_power < max_power
	
	def setup_sunflower():
		if get_ground_type() != Grounds.Soil:
			till()
		plant(Entities.Sunflower)
		common.maybe_water()
	
	def harvest_column():
		while need_more_power():
			if can_harvest():
				harvest()
			plant(Entities.Sunflower)
			common.maybe_water()
			move(North)
		
	def setup_column():
		for _ in range(get_world_size()):
			setup_sunflower()
			move(North)
	
	def run_child():
		setup_column()
		harvest_column()
		
	def run():
		drones = []
		for i in range(col_start, col_end):
			drones.append(spawn_drone(run_child))
			move(East)
		run_child()
		
		for drone in drones:
			wait_for(drone)
	
	return run

if __name__ == '__main__':
	clear()
	runner = create_run(0, 31, 100000)
	runner()
