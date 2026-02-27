import common
import rect
import point

clear()
size = 32
set_world_size(size)

dirs = [West, North, East, South]
min_circle_radius = size / 4
perimeter_threshold = 3

def gen_squiggle():
	down = True
	gen_path = []
	for x in range(size):
		if x == 0:
			gen_path.append((x, 0))
			gen_path.append((x, size - 1))
		elif x == size - 1:
			gen_path.append((x, size - 1))
			gen_path.append((x, 0))
		elif down:
			gen_path.append((x, size - 1))
			gen_path.append((x, 1))
			down = False
		else:
			gen_path.append((x, 1))
			gen_path.append((x, size - 1))
			down = True
	return gen_path

squiggle_path = gen_squiggle()

def can_move_anywhere():
	for dir in dirs:
		if can_move(dir):
			return True
	return False
		
def on_move(x, y):
	global next_apple
	global snake
	if next_apple != None and x == next_apple[0] and y == next_apple[1]:
		snake += 1
		next_apple = measure()
		quick_print(snake, next_apple)
		
def create_circle(snake):
	max_circle_radius = size / 2
	mid_axis = size / 2
	for radius in range(min_circle_radius, max_circle_radius + 1):
		max_perim = (radius * 2 - 1) * 4
		if snake < max_perim - perimeter_threshold:
			lower_bound = mid_axis - radius
			upper_bound = mid_axis + radius - 1
			return {
				South: (lower_bound, lower_bound),
				West: (lower_bound, upper_bound),
				North: (upper_bound, upper_bound),
				East: (upper_bound, lower_bound)
			}, max_perim - perimeter_threshold
	return None, 0

def create_inner_rects(path_side_map):
	mid_axis = size / 2
	# create_from_bounds normalizes the points so its fine if it's not the right points
	return {
		West: rect.create_from_bounds(
			point.translate(path_side_map[West], 1, -1),
			(mid_axis - 1, mid_axis)
		),
		North: rect.create_from_bounds(
			point.translate(path_side_map[North], -1, -1),
			(mid_axis, mid_axis)
		),
		East: rect.create_from_bounds(
			point.translate(path_side_map[East], -1, 1),
			(mid_axis, mid_axis - 1)
		),
		South: rect.create_from_bounds(
			point.translate(path_side_map[South], 1, 1),
			(mid_axis - 1, mid_axis - 1)
		)
	}
	

def create_outer_rects(path_side_map):
	# create_from_bounds normalizes the points so its fine if it's not the right points
	return {
		West: rect.create_from_bounds(
			point.translate(path_side_map[South], -1, 0),
			(0, size - 1)
		),
		North: rect.create_from_bounds(
			point.translate(path_side_map[West], 0, 1),
			(size - 1, size - 1)
		),
		East: rect.create_from_bounds(
			point.translate(path_side_map[North], 1, 0),
			(size - 1, 0)
		),
		South: rect.create_from_bounds(
			point.translate(path_side_map[East], 0, -1),
			(0, 0)
		)
	}

def create_circle_map(snake):
	path_side_map, max_snake = create_circle(snake)
	if path_side_map == None:
		return None, 0, None, None
	inner_rect_map = create_inner_rects(path_side_map)
	if path_side_map[South] == (0,0):
		return path_side_map, max_snake, inner_rect_map, None
	
	outer_rect_map = create_outer_rects(path_side_map)
	return path_side_map, max_snake, inner_rect_map, outer_rect_map
	
def create_outer_detour(side, final_point):
	x = get_pos_x()
	y = get_pos_y()
	
	if side == West:
		second_y = max(next_apple[1], y + 1)
		if next_apple[1] > final_point[1]:
			first_x = max(0, next_apple[0] - 1)
			return [
				(first_x, y),
				(first_x, second_y),
				(x - 1, second_y),
				(x - 1, final_point[1])
			]
		return [
			(next_apple[0], y),
			(next_apple[0], second_y),
			(x, second_y)
		]
			
	if side == North:
		second_x = max(next_apple[0], x + 1)
		if next_apple[0] > final_point[0]:
			first_y = min(size - 1, next_apple[1] + 1)
			return [
				(x, first_y),
				(second_x, first_y),
				(second_x, y + 1),
				(final_point[0], y + 1)
			]
		return [
			(x, next_apple[1]),
			(second_x, next_apple[1]),
			(second_x, y)
		]
	
	if side == East:
		second_y = min(next_apple[1], y - 1)
		if next_apple[1] < final_point[1]:
			first_x = min(size - 1, next_apple[0] + 1)
			return [
				(first_x, y),
				(first_x, second_y),
				(x + 1, second_y),
				(x + 1, final_point[1])
			]
		return [
			(next_apple[0], y),
			(next_apple[0], second_y),
			(x, second_y)
		]
		
	# South
	second_x = min(next_apple[0], x - 1)
	if next_apple[0] < final_point[0]:
		first_y = max(0, next_apple[1] - 1)
		return [
			(x, first_y),
			(second_x, first_y),
			(second_x, y - 1),
			(final_point[0], y - 1)
		]
	return [
		(x, next_apple[1]),
		(second_x, next_apple[1]),
		(second_x, y)
	]

def create_inner_detour(side):
	x = get_pos_x()
	y = get_pos_y()
	
	if side == West:
		first_y = max(y + 1, next_apple[1] - 1)
		return [
			(x, first_y),
			(next_apple[0], first_y),
			(next_apple[0], first_y + 1),
			(x, first_y + 1)
		]
	
	if side == North:
		first_x = max(x + 1, next_apple[0] - 1)
		return [
			(first_x, y),
			(first_x, next_apple[1]),
			(first_x + 1, next_apple[1]),
			(first_x + 1, y)
		]
	
	if side == East:
		first_y = min(y - 1, next_apple[1] + 1)
		return [
			(x, first_y),
			(next_apple[0], first_y),
			(next_apple[0], first_y - 1),
			(x, first_y - 1)
		]
	
	# South
	first_x = min(x - 1, next_apple[0] + 1)
	return [
		(first_x, y),
		(first_x, next_apple[1]),
		(first_x - 1, next_apple[1]),
		(first_x - 1, y)
	]
		

def run_circle():
	# assume we start at 0,0
	
	path_side_map, max_snake, inner_rect_map, outer_rect_map = create_circle_map(snake)
	dir_index = 0
	common.go_to_pos(path_side_map[South][0], path_side_map[South][1], True)
	
	while True:
		path = []
		found = False
		cur_side = dirs[dir_index]
		ignore = False
		final_point = path_side_map[cur_side]
		
		if not ignore:
			# check if outside of snake circle 
			if outer_rect_map != None:
				outer_rect = outer_rect_map[cur_side]
				if rect.is_in_rect(outer_rect, next_apple):
					# create the outer detour path
					detour = create_outer_detour(cur_side, final_point)
					for p in detour:
						path.append(p)
					found = True
			
			# check if inside of snake circle (if not found outside)
			if not found:
				inner_rect = inner_rect_map[cur_side]
				if rect.is_in_rect(inner_rect, next_apple):
					# create the outer detour path
					detour = create_inner_detour(cur_side)
					for p in detour:
						path.append(p)
					found = True
				
			# else, do nothing bc already created detour or it's in the snake's default path
		
		path.append(path_side_map[cur_side])
		for p in path:
			common.go_to_pos(p[0], p[1], True, on_move)
		
		if snake >= max_snake:
			ignore = True
			if cur_side == East:
				path_side_map, max_snake, inner_rect_map, outer_rect_map = create_circle_map(snake)
				ignore = False
				quick_print('grow perimeter')
				if path_side_map == None:
					break
				move(East)
				move(South)
		
		dir_index = (dir_index + 1) % len(dirs)
	
	common.go_to_pos(0, 0, True, on_move)
	
	return False


		
def run_column_squiggle():
	# assume we start at 0,0
	
	top_row = size - 1
	squiggle_row = size - 2
	bottom_row = 1
	final_row = size / 2 - 1
	
	squiggle_column_rects = []
	squiggle_column_index = 0
	num_squiggle_columns = size / 2 - 1 # excluding sides for the return trip
	
	for col in range(num_squiggle_columns):
		left = col * 2 + 1
		right = left + 1
		squiggle_column_rects.append(rect.create_from_bounds((left, bottom_row), (right, squiggle_row)))
	
	return_trip_path = [
		(size - 1, size - 1),
		(size - 1, 0),
		(0, 0),
		(0, size - 1),
	]
	
	final_path = [
		(size - 1, size - 1),
		(size - 1, 0),
		(0, 0)
	]
	
	common.go_to_pos(0, size - 1, True, on_move)
	
	while True:
		start_x = squiggle_column_index * 2 + 1
		start_y = top_row
		end_x = start_x + 1
		end_y = start_y
		
		squiggle_column_rect = squiggle_column_rects[squiggle_column_index]
		if next_apple[1] < squiggle_row:
			if rect.is_in_rect(squiggle_column_rect, next_apple):
				turn_y = next_apple[1]
			else:
				turn_y = squiggle_row
		
		path = [
			(start_x, start_y),
			(start_x, turn_y),
			(end_x, turn_y),
			(end_x, end_y)
		]
		
		for p in path:
			common.go_to_pos(p[0], p[1], True, on_move)
			
		if not can_move_anywhere():
			return False
		
		squiggle_column_index = (squiggle_column_index + 1) % len(squiggle_column_rects)
		
		# if wrapped around, do return path
		if squiggle_column_index == 0:
			if squiggle_row <= final_row:
				break
			for p in return_trip_path:
				common.go_to_pos(p[0], p[1], True, on_move)
				
		if not can_move_anywhere():
			return False
		
		if squiggle_row > bottom_row:
			# determine if we need to lower the squiggle row
			# empty space = (right - left) * (top - bottom)
			empty_space_area = (size - 1 - 1) * (squiggle_row + 1 - 1)
			# max snake size = map size - empty space
			max_snake_size = size * size - empty_space_area
			if snake >= max_snake_size - perimeter_threshold:
				squiggle_row -= 1
	
	for p in final_path:
		common.go_to_pos(p[0], p[1], True, on_move)
		
	return False
	
def run_squiggle():
	for (x, y) in squiggle_path:
		common.go_to_pos(x, y, True, on_move)
		if not can_move_anywhere():
			return False
	return True

algos = [
	run_circle,
	run_column_squiggle,
	run_squiggle
]
algo_length = len(algos)

snake = 1
next_apple = None

while True:
	common.go_to_pos(0, 0)
	change_hat(Hats.Dinosaur_Hat)
	can_still_move = True
	algo = algos[0]
	algo_index = 0
	snake = 1
	next_apple = measure()
	while algo_index < algo_length:
		repeat = algo()
		if not repeat:
			algo_index += 1
			if algo_index < algo_length:
				algo = algos[algo_index]
			else:
				algo = None
	
	# commit bones by changing hats
	change_hat(Hats.Traffic_Cone)
