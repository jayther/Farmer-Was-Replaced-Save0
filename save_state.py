
unlock_types = [
	Unlocks.Grass,
	Unlocks.Speed,
	Unlocks.Expand,
	Unlocks.Plant,
	Unlocks.Carrots,
	Unlocks.Pumpkins,
	Unlocks.Cactus,
	Unlocks.Dinosaurs,
	Unlocks.Fertilizer,
	Unlocks.Mazes,
	Unlocks.Megafarm,
	Unlocks.Watering,
	Unlocks.Sunflowers,
	Unlocks.Trees,
	Unlocks.Leaderboard
]

item_types = [
	Items.Hay,
	Items.Wood,
	Items.Carrot,
	Items.Pumpkin,
	Items.Bone,
	Items.Weird_Substance,
	Items.Gold,
	Items.Water,
	Items.Fertilizer,
	Items.Power
]


def export_unlock_state():
	unlocks = {}
	for type in unlock_types:
		unlocks[type] = num_unlocked(type)
	return unlocks
	

def export_item_state():
	items = {}
	for type in item_types:
		items[type] = num_items(type)
	return items
	

def print_state():
	item_state = export_item_state()
	unlock_state = export_unlock_state()
	
	quick_print('unlock state:')
	quick_print(unlock_state)
	
	quick_print('item state:')
	quick_print(item_state)
