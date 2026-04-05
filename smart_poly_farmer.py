import common

# wait, this isn't going to work because no shared memory

entity_item_map = {
	Entities.Grass: Items.Hay,
	Entities.Bush: Items.Wood,
	Entities.Tree: Items.Wood,
	Entities.Carrot: Items.Carrot
}

def create_run(entity_type, col_start, col_end, goal = -1):
	item_type = entity_item_map[entity_type]
		
	def need_more():
		if goal == -1:
			return True
		return num_items(item_type) < goal
	
	def task():
		companion_map = {}
		
	
	def run():
		common.go_to_pos(col_start, 0)
		drones = []
		for _ in range(col_start, col_end):
			drones.append(spawn_drone(task))
		task()
		common.wait_for_drones(drones)
	
	return run