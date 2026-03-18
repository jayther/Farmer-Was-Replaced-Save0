import common

item_entity_map = {
	Items.Hay: Entities.Grass,
	Items.Wood: Entities.Bush,
	Items.Carrot: Entities.Carrot,
	Items.Pumpkin: Entities.Pumpkin,
	Items.Cactus: Entities.Cactus,
	Items.Bone: None,
	Items.Weird_Substance: None,
	Items.Gold: Entities.Treasure,
	Items.Power: None
}

entity_unlock_map = {
	Entities.Grass: Unlocks.Grass,
	Entities.Bush: Unlocks.Trees,
	Entities.Tree: Unlocks.Trees,
	Entities.Carrot: Unlocks.Carrots,
	Entities.Pumpkin: Unlocks.Pumpkins,
	Entities.Cactus: Unlocks.Cactus,
	Entities.Treasure: Unlocks.Mazes,
	Entities.Sunflower: Unlocks.Sunflowers
}

# power per 100 harvests
power_req_map = {
	Entities.Grass: 0.23,
	Entities.Bush: 0.53,
	Entities.Tree: 0.53,
	Entities.Carrot: 0.13,
	Entities.Pumpkin: 0.50,
	Entities.Cactus: 2.66,
	Entities.Treasure: 0.77,
	Entities.Dinosaur: 11.18
}
	
def get_maze_max_usable_drones():
	return common.floor(max_drones() ** 0.5) ** 2

def get_modded_cost(entity):
	costs = get_cost(entity)
	
	if entity in power_req_map:
		power_cost = power_req_map[entity]
		if entity == Entities.Treasure:
			usable_drones = get_maze_max_usable_drones()
		elif entity == Entities.Dinosaur:
			usable_drones = 1
		else:
			size = get_world_size()
			m_drones = max_drones()
			multi = m_drones >= size
			if multi:
				usable_drones = min(m_drones, size)
			else:
				usable_drones = 1
		
		# dividing by 100 because power_cost is per 100 harvests
		drones_power_cost = power_cost * usable_drones / 100
		if Items.Power in costs:
			costs[Items.Power] += drones_power_cost
		else:
			costs[Items.Power] = drones_power_cost
	
	return costs
	
def get_actual_costs(costs, farm_size, buffer_mul = 1):
	area = farm_size ** 2
	actual_costs = {}
	# add current costs
	for item in costs:
		quantized_cost = common.ceil(costs[item] / area) * area + area
		if item in actual_costs:
			actual_costs[item] += quantized_cost
		else:
			actual_costs[item] = quantized_cost
	
	for item in costs:
		entity = item_entity_map[item]
		if entity == None:
			continue
		
		unlock_type = entity_unlock_map[entity]
		yield = 2 ** (num_unlocked(unlock_type) - 1)
		
		if entity == Entities.Cactus:
			yield *= area ** 2
		elif entity == Entities.Pumpkin:
			pumpkin_mul = min(farm_size, 6)
			yield *= pumpkin_mul * 0.6 # 6 * (non-)spoil rate
		elif entity == Entities.Bush:
			yield *= 3
		
		single_cost = get_modded_cost(entity)
		for single_item in single_cost:
			single_cost[single_item] *= costs[item]
		
		preqs = get_actual_costs(single_cost, farm_size, buffer_mul)
		for preq_item in preqs:
			a_cost = preqs[preq_item] / yield
			if preq_item == Items.Power:
				quantized_cost = a_cost
			else:
				quantized_cost = common.ceil(a_cost / area) * area + area
			if preq_item in actual_costs:
				actual_costs[preq_item] += quantized_cost * buffer_mul
			else:
				actual_costs[preq_item] = quantized_cost * buffer_mul
		
		
	return actual_costs

if __name__ == '__main__':
	# c = get_actual_costs({ Items.Wood: 100, Items.Carrot: 100 }, 8)
	c = get_actual_costs({ Items.Cactus: 1000 }, get_world_size(), 1)
	quick_print('c:', c)
	c = get_actual_costs({ Items.Wood: 1000 }, get_world_size(), 1)
	quick_print('c:', c)
	c = get_actual_costs({ Items.Pumpkin: 1000 }, get_world_size(), 1)
	quick_print('c:', c)