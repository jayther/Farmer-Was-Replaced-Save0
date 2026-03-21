import common
import entity_item_mapping

item_entity_map = {
	Items.Hay: Entities.Grass,
	Items.Wood: Entities.Bush,
	Items.Carrot: Entities.Carrot,
	Items.Pumpkin: Entities.Pumpkin,
	Items.Cactus: Entities.Cactus,
	Items.Bone: Entities.Dinosaur,
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

item_unlock_map = {
	Items.Hay: Unlocks.Grass,
	Items.Wood: Unlocks.Trees,
	Items.Carrot: Unlocks.Carrots,
	Items.Pumpkin: Unlocks.Pumpkins,
	Items.Cactus: Unlocks.Cactus,
	Items.Bone: Unlocks.Dinosaurs,
	Items.Weird_Substance: None,
	Items.Gold: Entities.Treasure,
	Items.Power: None
}

# power per 100 harvests
power_req_map = {
	Entities.Grass: 0.43, # 0.23
	Entities.Bush: 0.93, # 0.53
	Entities.Tree: 0.93, # 0.53
	Entities.Carrot: 3.03, # 0.13
	Entities.Pumpkin: 11.70, # 0.50
	Entities.Cactus: 10.76, # 2.66
	Entities.Treasure: 0.37, # 0.77
	Entities.Dinosaur: 0.28 # 11.18
}

quant_item_order = [
	Items.Hay,
	Items.Wood,
	Items.Carrot,
	Items.Pumpkin,
	Items.Cactus,
	Items.Bone,
	Items.Weird_Substance,
	Items.Gold
]

pumpkin_spoil_rate = 0.3 # 20% with some room for 2nd+ replants
substance_mul = 0.5 # we don't seem to use the whole stash somehow
	
def get_maze_max_usable_drones():
	return common.floor(max_drones() ** 0.5) ** 2


def add_power_costs(costs, farm_size):
	total_power_cost = 0
	for item in costs:
		entity = item_entity_map[item]
		if entity == None:
			continue
		
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
		
		area_yield = get_area_yield(item, farm_size)
		single_yield = area_yield / (farm_size ** 2)
		req_entities = costs[item] / single_yield
		
		drones_power_cost = power_cost * usable_drones
		# dividing by 100 because power_cost is per 100 harvests
		full_power_cost = req_entities * (drones_power_cost / 100)
		total_power_cost += full_power_cost
		quick_print('full power cost for', item, ':', full_power_cost)
	
	costs[Items.Power] = total_power_cost * 1.20 # compensate for power loss from sunflower farm step


def get_area_yield(item, farm_size):
	area = farm_size ** 2
	unlock_type = item_unlock_map[item]
	if unlock_type == None:
		return area
	
	bonus_mul = 2 ** (num_unlocked(unlock_type) - 1)
	
	if item == Items.Gold:
		return area * bonus_mul
	if item == Items.Cactus:
		return (area ** 2) * bonus_mul
	if item == Items.Pumpkin:
		pumpkin_mul = min(farm_size, 6)
		return common.ceil(area * pumpkin_mul * (1 - pumpkin_spoil_rate)) * bonus_mul
	if item == Items.Wood:
		# rounded up average of farming both bushes and trees
		return area * 3 * bonus_mul
	
	return area * bonus_mul


def get_quantized_cost(num, item, farm_size):
	# dont quantize power
	if item == Items.Power:
		return num
	
	area = farm_size ** 2
	area_yield = get_area_yield(item, farm_size)
	full_harvests = common.ceil(num / area_yield)
	quantized_cost = full_harvests * area_yield
	#quick_print('-----')
	#quick_print('get_quantized_cost', num, item, farm_size)
	#quick_print('area:', area)
	#quick_print('area_yield:', area_yield)
	#quick_print('full_harvests:', full_harvests)
	#quick_print('quantized_cost:', quantized_cost)
	return quantized_cost

def recursive_actual_costs(costs, farm_size, buffer_mul = 1, extra_items = {}):
	area = farm_size ** 2
	actual_costs = {}
	
	# current costs
	for item in costs:
		quantized_cost = get_quantized_cost(costs[item], item, farm_size)
		#quick_print('quantizing:', item, ':', costs[item], '->', quantized_cost)
		if item in actual_costs:
			actual_costs[item] += quantized_cost * buffer_mul
		else:
			actual_costs[item] = quantized_cost * buffer_mul
		
		extra = actual_costs[item] - costs[item]
		if item in extra_items:
			extra_items[item] += extra
		else:
			extra_items[item] = extra
	
	# prerequisites
	for item in costs:
		entity = item_entity_map[item]
		if entity == None:
			continue
		
		area_yield = get_area_yield(item, farm_size)
		single_yield = area_yield / area
		entities_req = actual_costs[item] / single_yield
		
		preqs = {}
		single_costs = get_cost(entity)
		for single_item in single_costs:
			if single_item == Items.Weird_Substance:
				subs_per_area = farm_size * 2**(num_unlocked(Unlocks.Mazes) - 1)
				preqs[single_item] = actual_costs[item] / area_yield * subs_per_area * substance_mul
			else:
				preqs[single_item] = single_costs[single_item] * entities_req
		
		#quick_print('single costs for', item, ':', single_costs)
		#quick_print('preqs for', actual_costs[item], item, ':', preqs)
		combined_preqs = recursive_actual_costs(preqs, farm_size, buffer_mul, extra_items)
		
		for preq_item in combined_preqs:
			req_cost = combined_preqs[preq_item]
			
			# we got some extra items due to quantizing, so remove redundant costs
			#if preq_item in extra_items:
			#	diff = extra_items[preq_item] - req_cost
			#	if diff >= 0:
			#		req_cost = 0
			#		extra_items[preq_item] -= req_cost
			#	else:
			#		req_cost = -diff
			#		extra_items[preq_item] = 0
			
			quantized_cost = get_quantized_cost(req_cost, preq_item, farm_size)
			#quick_print('quantizing:', preq_item, ':', req_cost, '->', quantized_cost)
			
				
			if preq_item in actual_costs:
				actual_costs[preq_item] += quantized_cost * buffer_mul
			else:
				actual_costs[preq_item] = quantized_cost * buffer_mul
			
		
	return actual_costs


def get_actual_costs(costs, farm_size, buffer_mul = 1):
	actual_costs = recursive_actual_costs(costs, farm_size, buffer_mul)
	# TODO quantize
	
	#extra_items = {}
	
	#for item in actual_costs:
	#	quantized_cost = get_quantized_cost(actual_costs[item], item, farm_size)
	#	extra_singles = quantized_cost - actual_costs[item]
	#	extra_items[item] = extra_singles
	
	add_power_costs(actual_costs, farm_size)
	
	return actual_costs

if __name__ == '__main__':
	# c = get_actual_costs({ Items.Wood: 100, Items.Carrot: 100 }, 8)
	c = get_actual_costs({ Items.Cactus: 10000 }, get_world_size(), 1)
	quick_print('c:', c)
	c = get_actual_costs({ Items.Wood: 1000 }, get_world_size(), 1)
	quick_print('c:', c)
	c = get_actual_costs({ Items.Pumpkin: 1000 }, get_world_size(), 1)
	quick_print('c:', c)
