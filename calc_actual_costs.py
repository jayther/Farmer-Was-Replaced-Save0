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
	Items.Weird_Substance: Entities.Hedge,
	Items.Gold: Entities.Treasure,
	Items.Power: None
}

# power per 100 harvests
power_req_map = {
	Entities.Grass: 7.28, # 0.23
	Entities.Bush: 11.69, # 0.53
	Entities.Tree: 11.69, # 0.53
	Entities.Carrot: 16.04, # 0.13
	Entities.Pumpkin: 17.93, # 0.50
	Entities.Cactus: 80.32, # 2.66
	Entities.Treasure: 0.37, # 0.77
	Entities.Dinosaur: 0.16, # 11.18
	Entities.Hedge: 1.03 # actually weird_substance
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


def get_bonus(unlock_type):
	return 2 ** (num_unlocked(unlock_type) - 1)


# same calculations as fastest_lb
def get_maze_max_usable_drones():
	return common.floor(max_drones() ** 0.5) ** 2


# power per 1000 gold
def get_power_req_from_maze_size(maze_size):
	return 1 / (0.4 * maze_size + 0.2) + 0.15


# size of mini-mazes for maze_multi_reuse
# same calculations as fastest_lb
def get_multi_maze_size(farm_size):
	max_num_mazes_side = common.floor(max_drones() ** 0.5)
	return common.floor(farm_size / max_num_mazes_side)
	
	
def get_power_cost(cost, item, farm_size):
	
	if item == Items.Weird_Substance:
		entity = Entities.Hedge
	else:
		entity = item_entity_map[item]
	
	if entity == None:
		continue
	
	if entity == Entities.Treasure:
		# same calculations as fastest_lb
		multi_maze_size = get_multi_maze_size(farm_size)
		# power per 1000 gold
		power_cost = get_power_req_from_maze_size(multi_maze_size)
		usable_drones = get_maze_max_usable_drones()
		
		full_power_cost = cost * (power_cost / 1000) * usable_drones
	else:
		power_cost = power_req_map[entity]
		if entity == Entities.Dinosaur:
			usable_drones = 1
		else:
			#size = get_world_size()
			#m_drones = max_drones()
			#multi = m_drones >= size
			#if multi:
			#	usable_drones = min(m_drones, size)
			#else:
			#	usable_drones = 1
			usable_drones = 1
		
		area_yield = get_area_yield(item, farm_size)
		single_yield = area_yield / (farm_size ** 2)
		req_entities = cost / single_yield
		
		drones_power_cost = power_cost * usable_drones
		# dividing by 100 because power_cost is per 100 harvests
		full_power_cost = req_entities * (drones_power_cost / 100)
		
	return full_power_cost


def add_power_costs(costs, farm_size):
	total_power_cost = 0
	for item in costs:
		full_power_cost = get_power_cost(costs[item], item, farm_size)
		
		if full_power_cost == 0:
			continue
		
		total_power_cost += full_power_cost
		quick_print('full power cost for', item, ':', full_power_cost)
	
	costs[Items.Power] = total_power_cost * 1.20 # compensate for power loss from sunflower farm step

def get_usable_area(item, farm_size):
	m_drones = max_drones()
	
	if m_drones == 1:
		return farm_size ** 2
		
	if item == Items.Hay or item == Items.Wood or item == Items.Carrot:
		return min(m_drones, farm_size) * farm_size
	
	return farm_size ** 2

def suggest_power_corrections(costs, items_power_used, items_farmed, items_power_empty, farm_size):
	suggestions = {}
	m_drones = max_drones()
	for item in items_power_used:
		if item == Items.Power:
			continue
		
		if item in items_power_empty and items_power_empty[item]:
			continue
		
		entity = item_entity_map[item]
		if entity == None:
			continue
		
		unlock_type = item_unlock_map[item]
		if unlock_type == None:
			continue
		
		items = items_farmed[item]
		if items == 0:
			continue
		
		#og_power_rate = power_req_map[entity]
		#og_power_cost = get_power_cost(costs[item], item, farm_size)
		power_used = -items_power_used[item]
		drone_power_used = power_used / m_drones
		area_yield = get_area_yield(item, farm_size)
		area = get_usable_area(item, farm_size)
		single_yield = area_yield / area
		entities = items / single_yield
		suggestions[item] = power_used / entities * 100
	
	quick_print('POWER SUGGESTIONS:', suggestions)
	return suggestions


def get_maze_substance_cost(maze_size):
	return maze_size * get_bonus(Unlocks.Mazes)


def get_area_yield(item, farm_size):
	area = farm_size ** 2
	unlock_type = item_unlock_map[item]
	if unlock_type == None:
		return area
	
	if unlock_type == Entities.Hedge:
		# weird subs farm's columns are equal to usable drones if less than farm size
		usable_area = min(farm_size, max_drones()) * farm_size
		tree_bonus_mul = get_bonus(Unlocks.Trees)
		grass_bonus_mul = get_bonus(Unlocks.Grass)
		
		# half the area are trees, other half are grass
		# base trees give 5 wood, and weird substance take up half the yield
		return (usable_area / 2 * 5 * tree_bonus_mul / 2) + (usable_area / 2 * grass_bonus_mul / 2)
		#return area * 3 * tree_bonus_mul / 2
	
	bonus_mul = get_bonus(unlock_type)
	
	if item == Items.Gold:
		maze_size = get_multi_maze_size(farm_size)		
		return maze_size ** 2 * bonus_mul
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
				#subs_per_area = farm_size * 2**(num_unlocked(Unlocks.Mazes) - 1)
				#preqs[single_item] = actual_costs[item] / area_yield * subs_per_area * substance_mul
				#preqs[single_item] = single_costs[single_item] * entities_req * substance_mul
				#preqs[single_item] = single_costs[single_item] * entities_req
				bonus_mul = get_bonus(Unlocks.Mazes)
				maze_size = get_multi_maze_size(farm_size)
				gold_per_maze = (maze_size ** 2) * bonus_mul
				num_mazes = common.ceil(actual_costs[item] / gold_per_maze)
				subs_per_maze = get_maze_substance_cost(maze_size)
				preqs[single_item] = num_mazes * subs_per_maze
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
			
			# weird substance is pre-quantized
			if preq_item == Items.Weird_Substance:
				quantized_cost = req_cost
			else:
				quantized_cost = get_quantized_cost(req_cost, preq_item, farm_size)
			#quick_print('quantizing:', preq_item, ':', req_cost, '->', quantized_cost)
			
				
			if preq_item in actual_costs:
				actual_costs[preq_item] += quantized_cost * buffer_mul
			else:
				actual_costs[preq_item] = quantized_cost * buffer_mul
			
		
	return actual_costs


def get_actual_costs(costs, farm_size, buffer_mul = 1):
	actual_costs = recursive_actual_costs(costs, farm_size, buffer_mul)
	
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
	c = get_actual_costs({ Items.Weird_Substance: 1000}, get_world_size(), 1)
	quick_print('c:', c)
