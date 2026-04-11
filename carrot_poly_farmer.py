import common
import timer

def safe_spawn_drone(fn):
	drone = None
	while drone == None:
		drone = spawn_drone(fn)
	return drone

def create_run(col_start, col_end, goal = -1):
	start_pos = (col_start, 0)
	
	def need_more():
		if goal == -1:
			return True
		return num_items(Items.Carrot) < goal
			
	def poly_planter(plant_type, pos):
		common.go_to_pos(pos[0], pos[1])
		
		if get_entity_type() == plant_type:
			return
		
		ground_type = get_ground_type()
		
		if plant_type == Entities.Carrot and ground_type == Grounds.Grassland:
			till()
		elif plant_type == Entities.Grass and ground_type == Grounds.Soil:
			till()
		
		if plant_type != Entities.Grass:
			plant(plant_type)
		else:
			harvest()
	
	def normalize_carrot():
		while get_ground_type() == Grounds.Grassland:
			till()
		if get_entity_type() != Entities.Carrot:
			plant(Entities.Carrot)
			common.maybe_water()
	
	def harvester():
		common.go_to_pos(start_pos[0], start_pos[1])
		
		# setup
		for _ in range(get_world_size()):
			normalize_carrot()
			move(North)
		
		# harvest
		while need_more():
			normalize_carrot()
			if can_harvest():
				plant_type, pos = get_companion()
				def create_planter():
					poly_planter(plant_type, pos)
				drone = safe_spawn_drone(create_planter)
				wait_for(drone)
				harvest()
				if (pos[0] % 2) == 0:
					def restore_planter():
						poly_planter(Entities.Carrot, pos)
						common.maybe_water()
					safe_spawn_drone(restore_planter)
			
			normalize_carrot()
			move(North)
	
	def run():
		global start_pos
		drones = []
		for x in range(col_start + 2, col_end + 1, 2):
			y = x * 8
			while y >= get_world_size():
				y -= get_world_size()
			start_pos = (x, y)
			drones.append(spawn_drone(harvester))
		
		start_pos = (col_start, 0)
		harvester()
		common.wait_for_drones(drones)
	
	return run

if __name__ == '__main__':
	#clear()
	timer.start('carrot')
	farmer = create_run(0, get_world_size() - 1, 3000000)
	farmer()
	duration = timer.end('carrot')
	quick_print('time to', goal, 'carrots:', duration, 's')
