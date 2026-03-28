import calc_actual_costs


enabled = False

items_power_used = {}
items_farmed = {}
items_power_empty = {}

num_start = 0
power_start = 0

all_suggestions = []

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

def is_power_unlocked():
	return num_unlocked(Unlocks.Sunflowers) > 0

def start_track():
	if not enabled:
		return
	
	if not is_power_unlocked():
		return
		
	global items_power_used
	global items_farmed
	global items_power_empty
	
	items_power_used = {}
	items_farmed = {}
	items_power_empty = {}
	
def start_item(item):
	if not enabled:
		return
	
	if not is_power_unlocked():
		return
	
	global num_start
	global power_start
	num_start = num_items(item)
	power_start = num_items(Items.Power)

def end_item(item):
	if not enabled:
		return
		
	if not is_power_unlocked():
		return
	
	d_items = num_items(item) - num_start
	d_power = num_items(Items.Power) - power_start
	items_farmed[item] = d_items
	items_power_used[item] = d_power
	items_power_empty[item] = num_items(Items.Power) == 0
	
	quick_print('power used:', d_power, 'power for', d_items, item)

def end_track(actual_costs):
	if not enabled:
		return
		
	if not is_power_unlocked():
		return
	
	suggestions = calc_actual_costs.suggest_power_corrections(
		actual_costs,
		items_power_used,
		items_farmed,
		items_power_empty,
		get_world_size()
	)
	all_suggestions.append(suggestions)

def suggest():
	if not enabled:
		return
	
	suggestions_sum = {}
	suggestions_count = {}
	for suggestions in all_suggestions:
		for item in item_order:
			if item not in suggestions:
				continue
				
			if item not in suggestions_sum:
				suggestions_sum[item] = 0
			suggestions_sum[item] += suggestions[item]
		
			if item not in suggestions_count:
				suggestions_count[item] = 0
			suggestions_count[item] += 1
	
	suggestions_avg = {}
	for item in item_order:
		if item not in suggestions_sum:
			continue
		suggestions_avg[item] = suggestions_sum[item] / suggestions_count[item]
	
	quick_print('AVG POWER SUGGESTIONS:', suggestions_avg)
