import common
import sunflower_column
import tracker

start_track, end_track = tracker.create_tracker([Items.Pumpkin])

first_run = True
first_harvest = True

deads = set()
new_plants = True

def create_run(col_start, col_end, multi = False):
	def harvest_column():
		change_hat(Hats.Pumpkin_Hat)
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
				sunflower_column.check_get_power()
				if i != col_end:
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
				sunflower_column.check_get_power()
				if i != col_end:
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
				
				sunflower_column.check_get_power()
				if i != col_end:
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
		change_hat(Hats.Pumpkin_Hat)
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
			if not first_harvest:
				end_track()
			else:
				first_harvest = False
			start_track()
			
	return run
