import common

same_coords_max = 50

def create_run(col_start, col_end, max_gold = 10000):
	maze_size = col_end - col_start + 1
	maze_area = maze_size ** 2
	drones = []
	runs = 0
	treasure_coords = None
	same_coords_count = 0
	grass_seen_state = 0
	start_gold = num_items(Items.Gold)
	
	def start_reuse():
		global treasure_coords
		plant(Entities.Bush)
		substance = maze_size * 2**(num_unlocked(Unlocks.Mazes) - 1)
		use_item(Items.Weird_Substance, substance)
		treasure_coords = measure()
		
	def reuse():
		global treasure_coords
		global same_coords_count
		substance = maze_size * 2**(num_unlocked(Unlocks.Mazes) - 1)
		use_item(Items.Weird_Substance, substance)
		old_coords = treasure_coords
		treasure_coords = measure()
		if old_coords == treasure_coords:
			same_coords_count += 1
	
	def check_harvest():
		global runs
		global treasure_coords
		global same_coords_count
		global grass_seen_state
		entity_type = get_entity_type()
		if entity_type == Entities.Treasure:
			reuse()
			if grass_seen_state == 0:
				grass_seen_state = 1
			return True
		elif entity_type == Entities.Grass:
			if grass_seen_state == 0:
				return True
			return False
		else:
			if grass_seen_state == 0:
				grass_seen_state = 1
			new_coords = measure()
			if new_coords == None:
				same_coords_count = 0
				return False
			if treasure_coords != new_coords:
				runs += 1
				treasure_coords = new_coords
				same_coords_count = 0
			else:
				same_coords_count += 1
			return True
	
	def keep_harvesting():
		while num_items(Items.Gold) - start_gold < max_gold:
			check_harvest()
	
	def setup():
		global drones
		global mid_drone
		global runs
		global same_coords_count
		global grass_seen_state
		same_coords_count = 0
		runs = 0
		mid = maze_size // 2
		grass_seen_state = 0
		if len(drones) < maze_area - 1:
			for i in range(maze_size):
				for j in range(maze_size):
					if i == mid and j == mid:
						move(East)
						continue
					drone = spawn_drone(keep_harvesting)
					drones.append(drone)
					move(East)
				common.go_to_pos(0, i)
				move(North)
		common.go_to_pos(mid, mid)
		start_reuse()
		
	def exploit():
		prev_runs = 0
		while same_coords_count < same_coords_max:
			prev_runs = runs
			repeat = check_harvest()
			if runs != prev_runs:
				quick_print('runs', runs)
			if not repeat:
				break
		
		quick_print('exploit end')
		
	def end():
		# harvesting nothing will clear the maze
		if get_entity_type() == Entities.Treasure:
			# move if under is treasure
			move(North)
			harvest()
			move(South)
		else:
			harvest()
	
	def run():
		if maze_area > max_drones():
			print('too big')
			return
		setup()
		exploit()
		end()
	
	return run

if __name__ == "__main__":
	clear()
	runner = create_run(0, 4, 9863168)
	while True:
		runner()
