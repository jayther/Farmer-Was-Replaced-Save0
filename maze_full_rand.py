import common

directions = [North, East, South, West]

opp_dir_map = {
	North: South,
	East: West,
	South: North,
	West: East
}

def rand_dir():
	return directions[random() * len(directions)]

def dir_filter_fn(dir, _):
	return can_move(dir)

def create_run(col_min, col_max, max_gold = -1):
	maze_size = col_max - col_min + 1
	
	start_gold = num_items(Items.Gold)
	drones = []
	waiting = False
	cur_dir = None # common.rand_item(directions)
	
	def need_more_gold():
		if max_gold == -1:
			return True
		return num_items(Items.Gold) - start_gold < max_gold
	
	def wait_for_hedge():
		global waiting
		
		while waiting:
			if get_entity_type() != Entities.Grass:
				waiting = False
		
	
	def has_ended():		
		return get_entity_type() == Entities.Grass

	def maze_start(first = False):		
		if first:
			plant(Entities.Bush)
		substance = maze_size * 2**(num_unlocked(Unlocks.Mazes) - 1)
		use_item(Items.Weird_Substance, substance)
	
	
	def maybe_harvest():		
		if get_entity_type() != Entities.Treasure:
			return
		
		maze_start()
		
		# if it didn't change places, we've probably reached the end
		if get_entity_type() == Entities.Treasure:
			harvest()
		
	def traverse():
		global cur_dir
		
		maybe_harvest()
		
		possible_dirs = common.filter(directions, dir_filter_fn)
		possible_len = len(possible_dirs)
		
		if possible_len == 1:
			# dead end? go to the only possible direction
			cur_dir = possible_dirs[0]
			move(cur_dir)
			
		elif possible_len == 2:
			# hallway
			first_dir = possible_dirs[0]
			second_dir = possible_dirs[1]
			opp_dir = opp_dir_map[cur_dir]
			if first_dir == cur_dir or second_dir == cur_dir:
				# in a straight hallway, keep going in cur dir
				move(cur_dir)
			elif opp_dir == first_dir:
				# in a corner, keep going around the corner
				cur_dir = second_dir
				move(cur_dir)
			else:
				# in a corner, keep going around the corner
				cur_dir = first_dir
				move(cur_dir)
		
		else:
			# t-intersection or 4-way intersection
			opp_dir = opp_dir_map[cur_dir]
			
			# exclude the direction we came from
			def exclude_opp_fn(dir, _):
				return dir != opp_dir
			possible_dirs = common.filter(directions, exclude_opp_fn)
			
			# randomize which path
			cur_dir = common.rand_item(possible_dirs)
			move(cur_dir)
		
	def traverse_child():
		global waiting
		global cur_dir
		cur_dir = common.rand_item(directions)
		waiting = True
		wait_for_hedge()
		while not has_ended():
			traverse()
		
	def traverse_main():
		treasure_coords = measure()
		global cur_dir
		cur_dir = common.rand_item(directions)
		
		while treasure_coords != None:
			traverse()
			treasure_coords = measure()
	
	def start():
		global drones
		
		if len(drones) == 0:
			# full setup
			common.go_to_pos(0, 0)
			for _ in range(maze_size - 1):
				drones.append(spawn_drone(traverse_child))
				move(North)
				move(East)
		else:
			# partial setup
			while num_drones() < max_drones():
				drones.append(spawn_drone(traverse_child))
		
		maze_start(True)
		
	def end():
		# harvesting nothing will clear the maze
		harvest()
		
	def run():
		start()
		traverse_main()
		end()
		
		
	return run
	
if __name__ == '__main__':
	clear()
	runner = create_run(0, 31, 9863168)
	runner()
	
	