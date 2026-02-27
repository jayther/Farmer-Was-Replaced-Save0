import common

def plant_tree(x, y):
	if (x + y) % 2 == 0:
		plant(Entities.Tree)
	else:
		plant(Entities.Bush)

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
			if common.should_harvest():
				harvest()
			plant_plant(x, y)
			move(North)
	
	def plant_column_forever():
		change_hat(common.get_hat_from_entity(plant_type))
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
