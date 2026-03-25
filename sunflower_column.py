import common

sun_map = {}
sun_col_start = 0
sun_col_end = 0
max_petals = 15
min_petals = 7
min_suns = 10
dedicated_sun_farmer = False
perma_ignore = None
max_gold = -1
start_gold = num_items(Items.Gold)
multi = False

def need_more_gold():
	if max_gold == -1:
		return True
	return num_items(Items.Gold) - start_gold < max_gold

def plant_sunflower():
	plant(Entities.Sunflower)
	common.maybe_water()
	
def use_hat():
	pass
	#if num_unlocked(Hats.Golden_Sunflower_Hat) > 0:
	#	change_hat(Hats.Golden_Sunflower_Hat)
	
def setup(col_start, col_end, max_gold_arg = -1, multi_arg = False):
	global sun_col_start
	global sun_col_end
	global perma_ignore
	global max_gold
	global start_gold
	global sun_map
	global multi
	
	max_gold = max_gold_arg
	start_gold = num_items(Items.Gold)
	
	sun_col_start = col_start
	sun_col_end = col_end
	perma_ignore = None
	orig_x = get_pos_x()
	orig_y = get_pos_y()
	drones = []
	sun_map = {}
	multi = multi_arg
	
	# plant
	common.go_to_pos(sun_col_start, 0)
	for x in range(sun_col_start, sun_col_end):
		if multi:
			drones.append(spawn_drone(plant_column))
		else:
			plant_column()
		move(East)
	plant_column()
	
	# measure for ignorable flowers
	ignore = set()
	common.go_to_pos(sun_col_start, 0)
	for x in range(sun_col_start, sun_col_end + 1):
		for y in range(get_world_size()):
			petals = measure()
			if petals == None:
				continue
			if petals <= min_petals:
				ignore.add((x, y))
			if len(ignore) >= min_suns:
				perma_ignore = ignore
				break
			sun_map[(x, y)] = petals
			move(North)
		if perma_ignore != None:
			break
		move(East)
	common.go_to_pos(orig_x, orig_y)

def plant_column():
	use_hat()
	for i in range(get_world_size()):
		if get_ground_type() != Grounds.Soil:
			till()
		if get_entity_type() != Entities.Sunflower:
			plant_sunflower()
		move(North)
		
def harvest_column(petals, ignore):
	x = get_pos_x()
	for y in range(get_world_size()):
		if (x,y) in ignore:
			move(North)
			continue
		
		count = measure()
		if petals == count:
			harvest()
		if not need_more_gold():
			break
		move(North)

def run():
	global perma_ignore
	num_cols = sun_col_end - sun_col_start + 1
	petal_map = {}
	ignore = set()
	if perma_ignore:
		ignore = perma_ignore
			
	# ignore the lowest petals
	if not perma_ignore:
		# map by petals
		for x in range(sun_col_start, sun_col_end + 1):
			for y in range(get_world_size()):
				petals = sun_map[(x,y)]
				if petals not in petal_map:
					petal_map[petals] = []
				petal_map[petals].append((x,y))
		
		all_lowest = True
		for petals in range(min_petals, max_petals + 1):
			if petals not in petal_map:
				continue
			if petals != min_petals:
				all_lowest = False
			
			suns = petal_map[petals]
			for sun in suns:
				ignore.add(sun)
				if len(ignore) >= min_suns:
					break
			if len(ignore) >= min_suns:
				break
		
		# if all ignored sunflowers have the lowest petal count,
		# then it's safe to set these as perma ignore
		# and don't have to remeasure
		if all_lowest:
			perma_ignore = ignore
	
	# keep harvesting from max to min
	for petals in range(max_petals, min_petals - 1, -1):			
		def create_harvest_column():
			use_hat()
			harvest_column(petals, ignore)
		
		common.go_to_pos(sun_col_start, 0)
		drones = []
		for x in range(sun_col_start, sun_col_end):
			if multi:
				drones.append(spawn_drone(create_harvest_column))
			else:
				create_harvest_column()
			move(East)
		harvest_column(petals, ignore)
		
		for drone in drones:
			wait_for(drone)
		
		if not need_more_gold():
			break
	
	# replant
	if need_more_gold():
		drones = []
		common.go_to_pos(sun_col_start, 0)
		for col in range(num_cols - 1):
			if multi:
				drones.append(spawn_drone(plant_column))
			else:
				plant_column()
			move(East)
		plant_column()
		
		for drone in drones:
			wait_for(drone)
	
	# remeasure
	if need_more_gold() and not perma_ignore:
		common.go_to_pos(sun_col_start, 0)
		for x in range(num_cols):
			for y in range(get_world_size()):
				petals = measure()
				sun_map[(x,y)] = petals
				move(North)
			move(East)

def create_run_lb(col_start, col_end, max_power = 1000, multi_arg = False):
	def runner():
		setup(col_start, col_end, max_power, multi_arg)
		run()
	return runner

def check_get_power(force = False, min_power = 2, is_dedicated = False):
	global dedicated_sun_farmer
	if dedicated_sun_farmer and not is_dedicated:
		return
	if not force and num_items(Items.Power) >= min_power:
		return
	orig_x = get_pos_x()
	orig_y = get_pos_y()
	common.go_to_pos(sun_col_start, 0)
	run()
	common.go_to_pos(orig_x, orig_y)

def wait_until_grown_column():
	use_hat()
	x = get_pos_x()
	baby_suns = set()
	for y in range(get_world_size()):
		if not can_harvest():
			baby_suns.add(y)
			ready = False
		move(North)
	
	while len(baby_suns) > 0:
		grown = []
		for y in baby_suns:
			common.go_to_pos(x, y)
			if can_harvest():
				grown.append(y)
		
		for y in grown:
			baby_suns.remove(y)
	
def wait_until_grown():
	orig_x = get_pos_x()
	orig_y = get_pos_y()
	common.go_to_pos(sun_col_start, 0)
	ready = False
	baby_suns = set()
	num_cols = sun_col_end - sun_col_start + 1
	
	drones = []
	for x in range(sun_col_start, sun_col_end):
		drones.append(spawn_drone(wait_until_grown_column))
		move(East)
	wait_until_grown_column()
	
	for drone in drones:
		wait_for(drone)
	
	common.go_to_pos(orig_x, orig_y)

def create_dedicated_runner(col_start, col_end, max_gold_arg = -1):
	global dedicated_sun_farmer
	dedicated_sun_farmer = True
	
	def dedicated_runner():
		#change_hat(Hats.Golden_Sunflower_Hat)
		setup(col_start, col_end, max_gold_arg)
		while True:
			wait_until_grown()
			check_get_power(True, 2, True)
			
	return dedicated_runner
	
def create_leaderboard_runner():
	global dedicated_sun_farmer
	dedicated_sun_farmer = True
	
	def runner():
		setup(0, 31, 100000)
		while num_items(Items.Power) < 100000:
			wait_until_grown()
			check_get_power(True, 2, True)
			
	return runner
