def maybe_water():
	if get_water() < 0.5:
		use_item(Items.Water)


def should_harvest():
	if can_harvest() or get_entity_type() == Entities.Dead_Pumpkin:
		harvest()

def do_nothing(x, y):
	pass

def go_to_pos(x, y, stay_within = False, cb = do_nothing):
	world_size = get_world_size()
	half_world_size = world_size / 2
	cur_x = get_pos_x()
	cur_y = get_pos_y()
	
	dx = x - cur_x
	if not stay_within:
		# if delta is more than half the world size
		# it's faster to go the other way
		if dx >= half_world_size:
			dx -= world_size
		elif dx < -half_world_size:
			dx += world_size
	
	dy = y - cur_y
	if not stay_within:
		# if delta is more than half the world size
		# it's faster to go the other way
		if dy >= half_world_size:
			dy -= world_size
		elif dy < -half_world_size:
			dy += world_size
	
	step = 0
	direction = East
	if dx > 0:
		step = 1
		direction = East
	elif dx < 0:
		step = -1
		direction = West
	else:
		step = 0
	
	if step != 0:
		for i in range(0, dx, step):
			move(direction)
			cb(get_pos_x(), get_pos_y())
	
	if dy > 0:
		step = 1
		direction = North
	elif dy < 0:
		step = -1
		direction = South
	else:
		step = 0
	
	if step != 0:
		for i in range(0, dy, step):
			move(direction)
			cb(get_pos_x(), get_pos_y())
			
def asc_fn(a, b):
	return a - b
	
def desc_fn(a, b):
	return b - a

def rand_fn(a, b):
	return random() * 2 - 1

def sort_by_fn(arr, fn):
	for i in range(len(arr) - 1):
		for j in range(i + 1, len(arr)):
			a = arr[i]
			b = arr[j]
			if fn(a, b) > 0:
				arr[i] = b
				arr[j] = a

hat_map = {
	Entities.Grass: Hats.The_Farmers_Remains,
	Entities.Tree: Hats.Tree_Hat,
	Entities.Bush: Hats.Tree_Hat,
	Entities.Carrot: Hats.Carrot_Hat,
	Entities.Pumpkin: Hats.Pumpkin_Hat,
	Entities.Cactus: Hats.Cactus_Hat
}
def get_hat_from_entity(entity):
	if not entity in hat_map:
		return Hats.Gold_Hat
	return hat_map[entity]
	
def filter(arr, fn):
	new_arr = []
	for item in arr:
		if fn(item, arr):
			new_arr.append(item)
	return new_arr

def reverse(arr):
	new_arr = []
	for i in range(len(arr) - 1, -1, -1):
		new_arr.append(arr[i])
	return new_arr

def dist_sq(a, b):
	return (b[0] - a[0])**2 + (b[1] - a[1])**2
