import common
import timer

def create_run(col_start, col_end, goal = -1):
	start_pos = (0, 0)
	
	def need_more():
		if goal == -1:
			return True
		return num_items(Items.Wood) < goal
			
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
		common.maybe_water()
	
	def normalize_carrot():
		while get_ground_type() == Grounds.Grassland:
			till()
		if get_entity_type() != Entities.Carrot:
			plant(Entities.Carrot)
	
	def normalize_tree():
		#x = get_pos_x()
		#y = get_pos_y()
		entity_type = get_entity_type()
		if entity_type != Entities.Tree:
			plant(Entities.Tree)
			common.maybe_water()
		#if entity_type != Entities.Tree or entity_type != Entities.Bush:
		#	if (x + y) % 2 == 0:
		#		plant(Entities.Tree)
		#
		#	else:
		#		plant(Entities.Bush)
	
	def harvester():
		common.go_to_pos(start_pos[0], start_pos[1])
		
		# setup
		for _ in range(get_world_size()):
			normalize_tree()
			move(North)
		
		# harvest
		restore_drone = None
		while need_more():
			normalize_tree()
			if can_harvest():
				companion = None
				while companion == None:
					companion = get_companion()
					if companion == None:
						normalize_tree()
				plant_type, pos = companion
				def create_planter():
					poly_planter(plant_type, pos)
				if restore_drone != None:
					wait_for(restore_drone)
				drone = spawn_drone(create_planter)
				wait_for(drone)
				harvest()
				if (pos[0] % 2) == 0:
					def restore_planter():
						poly_planter(Entities.Tree, pos)
					restore_drone = spawn_drone(restore_planter)
				else:
					restore_drone = None
			
			normalize_tree()
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
	clear()
	timer.start('wood')
	farmer = create_run(0, get_world_size() - 1, 1000000000)
	farmer()
	duration = timer.end('wood')
	quick_print('time to', goal, 'wood:', duration, 's')