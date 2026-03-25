import common
import sunflower_column
import tracker
import timer

start_track, end_track = tracker.create_tracker([Items.Pumpkin])

def use_hat():
	pass
	#if num_unlocked(Hats.Pumpkin_Hat) > 0:
	#	change_hat(Hats.Pumpkin_Hat)

def create_run_one_min(col_start, col_end, goal = -1):
	start_items = num_items(Items.Pumpkin)
	
	def need_more():
		if goal == -1:
			return True
		return num_items(Items.Pumpkin) - start_items < goal
	
	def maybe_replace():
		replaced = False
		
		if get_ground_type() != Grounds.Soil:
			replaced = True
			harvest()
			till()
			plant(Entities.Pumpkin)
		elif get_entity_type() == None:
			replaced = True
			plant(Entities.Pumpkin)
		elif get_entity_type() == Entities.Dead_Pumpkin:
			replaced = True
			harvest()
			plant(Entities.Pumpkin)
		elif not can_harvest():
			replaced = True
		
		common.maybe_water()
		
		return replaced
		
	def check_and_replace():
		x = get_pos_x()
		common.go_to_pos(x, 0)
		dead_indexes = set()
		
		# plant
		for i in range(get_world_size()):
			maybe_replace()
			move(North)
			dead_indexes.add(i)
		
		# check and replace
		while len(dead_indexes) > 0:
			not_dead = set()
			for i in dead_indexes:
				common.go_to_pos(x, i)
				replaced = maybe_replace()
				if not replaced:
					not_dead.add(i)
			
			for i in not_dead:
				dead_indexes.remove(i)
	
	def run():
		while need_more():
			common.go_to_pos(0, 0)
			drones = []
			for _ in range(get_world_size() - 1):
				drones.append(spawn_drone(check_and_replace))
				move(East)
			check_and_replace()
			common.wait_for_drones(drones)
			harvest()
		
	return run
			

def create_run(col_start, col_end, multi = False):

	first_run = True
	first_harvest = True
	
	deads = set()
	new_plants = True
	
	def harvest_column():
		use_hat()
		for j in range(get_world_size()):
			if common.should_harvest():
				harvest()
			plant(Entities.Pumpkin)
			common.maybe_water()
			move(North)
	
	def normal_harvest():
		# reset dead pumpkin set
		global deads
		global new_plants
		deads = set()
		new_plants = True
		
		if multi:
			drones = []
			for i in range(col_start, col_end):
				drones.append(spawn_drone(harvest_column))
				move(East)
			harvest_column()
			for drone in drones:
				wait_for(drone)
		else:
			for i in range(col_start, col_end + 1):
				harvest_column()
				move(East)
	
	def maybe_replace():
		replaced = False
		
		if get_ground_type() != Grounds.Soil:
			replaced = True
			harvest()
			till()
			plant(Entities.Pumpkin)
		elif get_entity_type() == None:
			replaced = True
			plant(Entities.Pumpkin)
		elif get_entity_type() == Entities.Dead_Pumpkin:
			replaced = True
			harvest()
			plant(Entities.Pumpkin)
		elif not can_harvest():
			replaced = True
		
		common.maybe_water()
		
		return replaced
	
	def maybe_replace_column():
		for _ in range(get_world_size()):
			maybe_replace()
			move(North)

	def check_and_replace_single():
		global first_run
		global new_plants
		global deads
		has_dead = False
		
		if first_run:
			first_run = False
			has_dead = True # dont try to harvest in the 2nd run
			for i in range(col_start, col_end + 1):
				maybe_replace_column()
				move(East)
						
		elif new_plants:
			# new plants from past harvest, so check everything
			new_plants = False
			for i in range(col_start, col_end + 1):
				for j in range(get_world_size()):
					replaced = maybe_replace()
					if replaced:
						has_dead = True
						deads.add((i, j))
					move(North)
				
				move(East)
		else:
			# tracked the dead pumpkins in the last pass, so only check those
			not_dead = set()
			for (i, j) in deads:
				common.go_to_pos(i, j)
				replaced = maybe_replace()
				if replaced:
					has_dead = True
				else:
					not_dead.add((i, j))
			
			# remove the not dead pumpkins from the dead set
			for (i, j) in not_dead:
				deads.remove((i, j))
			
			# go to ending position
			common.go_to_pos(col_end, 0)
		
		return has_dead
		
	def check_and_replace_multi_column():
		use_hat()
		dead_indexes = set()
		first = True
		first_plants = True
		col = get_pos_x()
		
		while first or first_plants or len(dead_indexes) > 0:
			if first:
				first = False
				maybe_replace_column()
			elif first_plants:
				first_plants = False
				for i in range(get_world_size()):
					replaced = maybe_replace()
					if replaced:
						dead_indexes.add(i)
					move(North)
			else:
				not_dead = set()
				for i in dead_indexes:
					common.go_to_pos(col, i)
					replaced = maybe_replace()
					if not replaced:
						not_dead.add(i)
				
				for i in not_dead:
					dead_indexes.remove(i)				
	
	def check_and_replace_multi():
		drones = []
		for i in range(col_start, col_end):
			drones.append(spawn_drone(check_and_replace_multi_column))
			move(East)
		check_and_replace_multi_column()
		
		for drone in drones:
			wait_for(drone)
			
		return False
	
	def check_and_replace():
		if multi:
			return check_and_replace_multi()
		else:
			return check_and_replace_single()
	
	def run():
		global first_harvest
		has_dead = check_and_replace()
			
		if not has_dead:
			common.go_to_pos(col_start, 0)
			normal_harvest()
			
	return run

if __name__ == '__main__':
	clear()
	goal = 20000000
	runner = create_run_one_min(0, get_world_size() - 1, goal)
	timer.start('pumpkin')
	runner()
	duration = timer.end('pumpkin')
	quick_print('time to', goal, 'pumpkins:', duration, 's')
