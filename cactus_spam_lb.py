import common

# this doesnt work because replanting the same plot grows the same size cactus

def create_run(max_gold = -1):
	size = get_world_size()
	
	def spam_plant_column():
		for _ in range(size):
			till()
			s = 0
			while s != 5:
				harvest()
				plant(Entities.Cactus)
				s = measure()
				common.wait_ticks(1000)
			move(North)
		while not can_harvest():
			pass
		
	def spam_plant():
		drones = []
		for _ in range(size - 1):
			drones.append(spawn_drone(spam_plant_column))
			move(East)
		spam_plant_column()
		common.wait_for_drones(drones)
		
	def final_harvest():
		common.go_to_pos(size - 1, size - 1)
		harvest()
		
	def run():
		spam_plant()
		final_harvest()
		
	return run
	
if __name__ == '__main__':
	clear()
	runner = create_run(33554432)
	runner()