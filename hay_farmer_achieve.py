import common

goal = 200000000
item_count = num_items(Items.Hay) + goal

def harvest_column():
	while True:
		harvest()
		move(North)
		
def poly_planter(plant_type, pos):
	common.go_to_pos(pos[0], pos[1])
	
	if get_entity_type() == plant_type:
		return
	
	if plant_type == Entities.Carrot:
		if get_ground_type() == Grounds.Grassland:
			till()
	elif get_ground_type() == Grounds.Soil:
		till()
	
	plant(plant_type)

def normalize_grass():
	if get_entity_type() != Entities.Grass:
		harvest()
	if get_ground_type() == Grounds.Soil:
		till()

def harvester():
	while num_items(Items.Hay) < item_count:
		normalize_grass()
		plant_type, pos = get_companion()
		def create_planter():
			poly_planter(plant_type, pos)
		drone = spawn_drone(create_planter)
		wait_for(drone)
		while not can_harvest():
			normalize_grass()
			common.maybe_water()
		harvest()
		move(North)

def farmer():
	drones = []
	for _ in range(get_world_size() / 2 - 1):
		drones.append(spawn_drone(harvester))
		move(East)
		move(East)
		
	harvester()
	common.wait_for_drones(drones)

farmer()