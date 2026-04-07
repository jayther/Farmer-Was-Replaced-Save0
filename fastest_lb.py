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
import suggester
import hay_poly_farmer
import carrot_poly_farmer
import tree_poly_farmer

step = 0
prev_item = None

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
	multi = m_drones > 1
	
	if item == Items.Power:
		clear()
		if m_drones == 1:
			quick_print('using smartflower farm')
			return sunflower_column.create_run_lb(0, size - 1, item_count)
		else:
			quick_print('using dumbflower farm (', m_drones, 'drones,', size, 'size)')
			return dumbflower_section.create_run(0, m_drones - 1, item_count)
	elif item == Items.Hay:
		if m_drones >= 4 and num_unlocked(Unlocks.Polyculture) > 0:
			clear()
			return hay_poly_farmer.create_run(0, m_drones - 1, item_count)
		else:
			return column_farmer.create_farmer_lb({
				0: basic_plant_column.create_basic_plant_lb(Entities.Grass, item_count, multi)
			}, item, item_count)
	elif item == Items.Wood:
		if num_unlocked(Unlocks.Trees) > 0:
			if m_drones >= 4 and num_unlocked(Unlocks.Polyculture) > 0:
				clear()
				return tree_poly_farmer.create_run(0, m_drones - 1, item_count)
			else:
				return column_farmer.create_farmer_lb({
					0: basic_plant_column.create_basic_plant_lb(Entities.Tree, item_count, multi)
				}, item, item_count)
		else:
			return column_farmer.create_farmer_lb({
				0: basic_plant_column.create_basic_plant_lb(Entities.Bush, item_count, multi)
			}, item, item_count)
	elif item == Items.Carrot:
		if m_drones >= 4 and num_unlocked(Unlocks.Polyculture) > 0:
			clear()
			return carrot_poly_farmer.create_run(0, m_drones - 1, item_count)
		else:
			return column_farmer.create_farmer_lb({
				0: basic_plant_column.create_basic_plant_lb(Entities.Carrot, item_count, multi)
			}, item, item_count)
	elif item == Items.Pumpkin:
		clear()
		return pumpkin_section.create_run(0, size - 1, m_drones >= size)
	elif item == Items.Weird_Substance:
		clear()
		if multi:
			return weird_multi_section.create_run(0, size - 1, item_count)
		else:
			return weird_section.create_run(0, size - 1, item_count)
	elif item == Items.Cactus:
		if prev_item == item:
			common.go_to_pos(0, 0)
		else:
			clear()
		if m_drones >= size:
			return cactus_brick_lb.create_run(item_count - num_items(Items.Cactus))
		else:
			return cactus_section.create_run(0, size - 1)
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
			return maze_multi_reuse.create_run(maze_size, item_count)
		else:
			return maze_reuse_section.create_run(0, size - 1, item_count)
		
	elif item == Items.Bone:
		clear()
		return dinosaur_section.create_run(item_count)
	
	else:
		quick_print('WARNING:', item, 'is not mapped to any farming function')
		return None

		
def maybe_farm_power(actual_costs):
	global prev_item
	
	if num_unlocked(Unlocks.Sunflowers) == 0:
		return
		
	if Items.Power not in actual_costs:
		return
	
	world_size = get_world_size()
	
	power_req = actual_costs[Items.Power]
	
	if num_items(Items.Power) >= power_req:
		quick_print('have enough power:', num_items(Items.Power), '/', power_req, '. Skipping power farm.')
		return
	
	sunflower_goal = max(power_req / 4, world_size ** 2)
	
	start_power = num_items(Items.Power)
	
	quick_print('Farming for', power_req, 'power...')
	
	# farm for sunflower prereqs
	sunflower_costs = calc_actual_costs.get_actual_costs({ Items.Carrot: sunflower_goal }, world_size, 1)
	quick_print('sunflower costs:', sunflower_costs)
	for item in item_order:
		if item not in sunflower_costs:
			continue
		cost = sunflower_costs[item]
		farmer = create_farmer(item, cost)
		prev_item = item
		
		while num_items(item) < cost:
			farmer()

	pre_sun_power = num_items(Items.Power)
			
	# farm actual sunflowers
	farmer = create_farmer(Items.Power, power_req)
	prev_item = Items.Power
	while num_items(Items.Power) < power_req:
		farmer()
	
	current_power = num_items(Items.Power)
	net_power = current_power - start_power
	power_farmed = current_power - pre_sun_power
	quick_print(
		net_power, 'net power;',
		power_farmed , '/', power_req, 'power farmed (', current_power , 'current);',
		'Resume normal farming'
	)


while num_unlocked(Unlocks.Leaderboard) == 0:
	world_size = get_world_size()
	power_unlocked = num_unlocked(Unlocks.Sunflowers) > 0
	timer.start('unlock')
	unlock_type, costs = step_map[step]
	actual_costs = calc_actual_costs.get_actual_costs(costs, world_size, 1)
	unlock_lvl = num_unlocked(unlock_type)
	quick_print('unlocking', unlock_type, unlock_lvl, '->', unlock_lvl + 1, '... (', actual_costs, ')')
	reruns = 0
	unlocked = False
	
	while not unlocked:
		
		# farm for power
		maybe_farm_power(actual_costs)
		
		suggester.start_track()
		
		# farm the required stuff
		for item in item_order:
			if item not in actual_costs:
				continue
			
			cost = actual_costs[item]
			farmer = create_farmer(item, cost)
			prev_item = item
			
			suggester.start_item(item)
			starting_count = num_items(item)
			iterations = 0
			while num_items(item) < cost:
				# run farm
				farmer()
				if power_unlocked and num_items(Items.Power) == 0:
					quick_print('NO POWER at step', step, 'after gathering', cost, item)
				iterations += 1
			ending_count = num_items(item)
			diff_count = ending_count - starting_count
			if item == Items.Weird_Substance:
				quick_print(
					'SUBS farm actual cost:', cost,
					'; starting:', starting_count,
					'; farmed:', diff_count,
					'; ending:', ending_count,
					'; iters:', iterations
				)
			
			suggester.end_item(item)
		
		suggester.end_track(actual_costs)
			
		if unlock_type == None:
			unlocked = True
		else:
			unlocked = unlock(unlock_type)
		
		if not unlocked:
			reruns += 1
			if reruns < 5:
				quick_print('COSTS NOT MET FOR', unlock_type, '; rerunning...')
			
	if unlocked:
		quick_print('unlocked', unlock_type, '(', timer.end('unlock'), 's)')
	else:
		quick_print('NOT unlocked', unlock_type, '(', timer.end('unlock'), 's)')
	
	step += 1

suggester.suggest()
