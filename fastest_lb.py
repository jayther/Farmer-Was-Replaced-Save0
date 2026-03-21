from fastest_step_map import step_map
import common
import column_farmer
import basic_plant_column
import timer
import calc_actual_costs
import pumpkin_section
import weird_section
import weird_multi_section
import sunflower_column
import dumbflower_section
import cactus_section
import cactus_brick_lb
import maze_reuse_section
import dinosaur_section
import maze_multi_reuse

step = 0

item_order = [
	Items.Hay,
	Items.Wood,
	Items.Carrot,
	Items.Pumpkin,
	Items.Cactus,
	Items.Bone,
	Items.Weird_Substance,
	Items.Gold,
	Items.Fertilizer
]

def create_farmer(item, item_count):
	size = get_world_size()
	m_drones = max_drones()
	multi = m_drones > 1 and m_drones >= size

	if multi:
		quick_print('multi enabled for ', item, '(max:', max_drones(), ')')
	
	if item == Items.Power:
		clear()
		if multi:
			return dumbflower_section.create_run(0, size - 1, item_count)
		else:
			return sunflower_column.create_run_lb(0, size - 1, item_count)
	elif item == Items.Hay:
		return column_farmer.create_farmer_lb({
			0: basic_plant_column.create_basic_plant_lb(Entities.Grass, item_count, multi)
		}, item, item_count)
	elif item == Items.Wood:
		if num_unlocked(Unlocks.Trees) > 0:
			return column_farmer.create_farmer_lb({
				0: basic_plant_column.create_basic_plant_lb(Entities.Tree, item_count, multi)
			}, item, item_count)
		else:
			return column_farmer.create_farmer_lb({
				0: basic_plant_column.create_basic_plant_lb(Entities.Bush, item_count, multi)
			}, item, item_count)
	elif item == Items.Carrot:
		return column_farmer.create_farmer_lb({
			0: basic_plant_column.create_basic_plant_lb(Entities.Carrot, item_count, multi)
		}, item, item_count)
	elif item == Items.Pumpkin:
		clear()
		return pumpkin_section.create_run(0, size - 1, multi)
	elif item == Items.Weird_Substance:
		clear()
		if multi:
			return weird_multi_section.create_run(0, size - 1)
		else:
			return weird_section.create_run(0, size - 1)
	elif item == Items.Cactus:
		clear()
		if multi:
			return cactus_brick_lb.create_run(item_count - num_items(Items.Cactus))
		else:
			return cactus_section.create_run(0, size - 1, multi)
	elif item == Items.Gold:
		# calculate maze size based on max drones
		if m_drones == 1:
			use_multi = False
		else:
			max_num_mazes_side = common.floor(m_drones ** 0.5)
			maze_size = common.floor(size / max_num_mazes_side)
			use_multi = True
		
		clear()
		if use_multi:
			quick_print('MAZE_MULTI_REUSE maze_size:', maze_size)
			return maze_multi_reuse.create_run(maze_size, item_count)
		else:
			return maze_reuse_section.create_run(0, size - 1, item_count)
	elif item == Items.Bone:
		clear()
		return dinosaur_section.create_run()
	else:
		quick_print('WARNING:', item, 'is not mapped to any farming function')
		return None
	# TODO add sunflower/power as part of step requirements?
		
def get_power_threshold():
	return 200

def get_power_goal():
	return 1200

def need_more_power():
	if num_unlocked(Unlocks.Sunflowers) == 0:
		return False
	
	if num_items(Items.Power) >= get_power_threshold():
		return False
	
	return True

def create_step_for_power():
	quick_print('INSERTING carrot step for power')
	return (None, { Items.Carrot: get_power_goal() / 4 })

def farm_power():
	clear()
	power_goal = get_power_goal()
	farmer = sunflower_column.create_run_lb(0, get_world_size(), power_goal)
	while num_items(Items.Power) < power_goal:
		farmer()

while num_unlocked(Unlocks.Leaderboard) == 0:
	world_size = get_world_size()
	timer.start('unlock')
	power_needed = False
	if power_needed:
		unlock_type, costs = create_step_for_power()
	else:
		unlock_type, costs = step_map[step]
	actual_costs = calc_actual_costs.get_actual_costs(costs, world_size, 1)
	unlock_lvl = num_unlocked(unlock_type)
	quick_print('unlocking', unlock_type, unlock_lvl, '->', unlock_lvl + 1, '... (', actual_costs, ')')
	reruns = 0
	unlocked = False
	while not unlocked:
		
		# farm for power
		if num_unlocked(Unlocks.Sunflowers) > 0 and Items.Power in actual_costs:
			# minimum 10 power
			power_req = actual_costs[Items.Power]
			sunflower_goal = max(power_req / 4, world_size ** 2)
			
			quick_print('Farming for', power_req, 'power...')
			
			# farm for sunflower prereqs
			sunflower_costs = calc_actual_costs.get_actual_costs({ Items.Carrot: sunflower_goal }, world_size, 1)
			quick_print('sunflower costs:', sunflower_costs)
			for item in item_order:
				if item not in sunflower_costs:
					continue
				cost = sunflower_costs[item]
				farmer = create_farmer(item, cost)
				
				while num_items(item) < cost:
					farmer()
					
			# farm actual sunflowers
			farmer = create_farmer(Items.Power, sunflower_goal)
			while num_items(Items.Power) < sunflower_goal:
				farmer()
			
			quick_print('Resume normal farming')
		
		# farm the required stuff
		for item in item_order:
			if item not in actual_costs:
				continue
			
			cost = actual_costs[item]
			farmer = create_farmer(item, cost)
			
			#start_tick = get_tick_count()
			#start_items = num_items(item)
			
			#if item in calc_actual_costs.item_entity_map:
			#	area = world_size ** 2
			#	entity = calc_actual_costs.item_entity_map[item]
			#	if entity != None:
			#		proj_unlock_type = calc_actual_costs.entity_unlock_map[entity]
			#		area_yield = 2 ** (num_unlocked(proj_unlock_type) - 1) * area
			#		if entity == Entities.Cactus:
			#			area_yield *= area ** 2
			#		elif entity == Entities.Pumpkin:
			#			pumpkin_mul = min(world_size, 6)
			#			area_yield = area * pumpkin_mul * 0.6 * 2 ** (num_unlocked(proj_unlock_type) - 1)
			#		elif entity == Entities.Bush:
			#			area_yield *= 3
			#		quick_print(item, 'expected iters:', (cost - num_items(item)) / area_yield)
			
			#iters = 0
			while num_items(item) < cost:
				# run farm
				farmer()
				if num_unlocked(Unlocks.Sunflowers) > 0 and num_items(Items.Power) == 0:
					quick_print('NO POWER at step', step, 'after gathering', cost, item)
			#	iters += 1
				
			#quick_print(item, 'actual iters:', iters)
			
			# d_tick = get_tick_count() - start_tick
			# d_items = num_items(item) - start_items
			#if item == Items.Weird_Substance:
			#	entity_unlock = Unlocks.Trees
			#	yield_mul = 0.5
			#elif item == Items.Bone:
			#	entity_unlock = Unlocks.Dinosaurs
			#	yield_mul = 1
			#else:
			#	entity = calc_actual_costs.item_entity_map[item]
			#	entity_unlock = calc_actual_costs.entity_unlock_map[entity]
			#	yield_mul = 1
			#yield = yield_mul * 2 ** (num_unlocked(entity_unlock) - 1)
			#power_per_tick = 1 / (30 * 200)
			#quick_print('TICK COUNT:', d_tick, 'for', d_items, item, '(', (d_items / yield) / d_tick * 100, '100-tile/tick)')
			#quick_print('POWER REQ for total:', d_tick * power_per_tick, 'power')
			
			
		if unlock_type == None:
			unlocked = True
		else:
			unlocked = unlock(unlock_type)
		
		if not unlocked:
			reruns += 1
			if reruns < 5:
				quick_print('COSTS NOT MET FOR', unlock_type, '; rerunning...')
	
	if power_needed:
		farm_power()
			
	if unlocked:
		quick_print('unlocked', unlock_type, '(', timer.end('unlock'), 's)')
	else:
		quick_print('NOT unlocked', unlock_type, '(', timer.end('unlock'), 's)')
	
	if not power_needed:
		step += 1
