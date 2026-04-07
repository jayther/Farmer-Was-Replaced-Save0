import common
from eiu_maps import get_item_from_entity

def plant_tree(x, y):
	if (x + y) % 2 == 0:
		return plant(Entities.Tree)
	else:
		return plant(Entities.Bush)
		
non_tilled_types = { Entities.Grass, Entities.Bush, Entities.Tree }

def create_basic_plant_lb(plant_type, goal_count, multi = False):
	moveable = get_world_size() > 1
	warned_no_plant = False
	tilled = plant_type not in non_tilled_types
	item_type = get_item_from_entity(plant_type)
	warn_count = 0
	item_yield = common.get_bonus(plant_type)
	plant_count = 0
	max_plant_count = 0
	
	if plant_type == Entities.Tree:
		item_yield *= 2
	
	if item_type == None:
		quick_print('WARNING:', plant_type, 'does not map to an item type')
	
	def need_more_items():
		return num_items(item_type) < goal_count
	
	def should_replant():
		#return True
		max_yield = item_yield * max_plant_count
		current_items = num_items(item_type)
		return current_items <= goal_count - max_yield
	
	def add_plant(amount = 1):
		global plant_count
		global max_plant_count
		plant_count += 1
		if plant_count > max_plant_count:
			max_plant_count = plant_count
	
	def remove_plant(amount = 1):
		global plant_count
		plant_count -= amount
	
	def plant_plant(x, y):
		global warned_no_plant
		global warn_count
		if tilled and get_ground_type() != Grounds.Soil:
			till()
		if plant_type == Entities.Tree:
			planted = plant_tree(x, y)
			if planted:
				add_plant()
		elif plant_type != Entities.Grass:
			planted = plant(plant_type)
			if planted:
				add_plant()
			elif not warned_no_plant:
				warned_no_plant = True
				warn_count += 1
				if warn_count >= get_world_size():
					while True:
						pass
		common.maybe_water()
	
	def plant_column():
		global warned_no_plant
		global plant_count
		warned_no_plant = False
		x = get_pos_x()
		for i in range(get_world_size()):
			y = get_pos_y()
			
			if can_harvest():
				entity_type = get_entity_type()
				if plant_type == Entities.Tree and entity_type == Entities.Bush:
					entity_type = Entities.Tree
				harvested = harvest()
				if harvested and entity_type == plant_type:
					remove_plant()
			
			if not need_more_items():
				break
			
			if get_entity_type() != plant_type and should_replant():
				plant_plant(x, y)
			
			if moveable:
				move(North)
	
	def plant_column_forever():
		# change_hat(common.get_hat_from_entity(plant_type))
		while need_more_items():
			plant_column()
	
	def multi_plant():
		drones = []
		cols = min(max_drones(), get_world_size())
		for col in range(cols - 1):
			drones.append(spawn_drone(plant_column_forever))
			move(East)
		plant_column_forever()
		common.wait_for_drones(drones)
	
	def run():
		if multi:
			multi_plant()
		else:
			plant_column()

	return run
	

def create_basic_plant(plant_type, tilled, custom_plant_fn = None, fertilize = False, multi_cols = (-1, -1)):
	multi = multi_cols[0] != -1 and multi_cols[1] != -1
	def plant_plant(x, y):
		if tilled and get_ground_type() != Grounds.Soil:
			till()
		if custom_plant_fn != None:
			custom_plant_fn(x, y)
		elif plant_type != Entities.Grass:
			plant(plant_type)
		if fertilize and num_items(Items.Fertilizer) > 0:
			use_item(Items.Fertilizer)
		if not fertilize:
			common.maybe_water()
	
	def plant_column():
		x = get_pos_x()
		for i in range(get_world_size()):
			y = get_pos_y()
			if can_harvest():
				harvest()
			plant_plant(x, y)
			move(North)
	
	def plant_column_forever():
		# change_hat(common.get_hat_from_entity(plant_type))
		while True:
			plant_column()
	
	def multi_plant():
		for col in range(multi_cols[0], multi_cols[1]):
			spawn_drone(plant_column_forever)
			move(East)
		plant_column_forever()
	
	def run():
		if multi:
			multi_plant()
		else:
			plant_column()

	return run
