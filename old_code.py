
	
def get_actual_costs_old(costs, farm_size, buffer_mul = 1):
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
	