import common
import point
import timer
import rect

dirs = [North, East, South, West]
dir_delta_map = {
	North: (0, 1),
	East: (1, 0),
	South: (0, -1),
	West: (-1, 0)
}

opp_dir_map = {
	North: South,
	East: West,
	South: North,
	West: East
}

quad_multipliers = [
	(1, 1, False),
	(1, -1, True),
	(-1, -1, False),
	(-1, 1, True)
]

max_runs = 300

prefind_path_id = 'prefind'
move_path_id = 'move'

path_time_map = {
	prefind_path_id: [],
	move_path_id: []
}

timer_enabled = False

def prefind_timer_start():
	if not timer_enabled:
		return
	timer.start(prefind_path_id)

def prefind_timer_end():
	if not timer_enabled:
		return
	t = timer.end(prefind_path_id)
	add_time(prefind_path_id, t)

def move_timer_start():
	if not timer_enabled:
		return
	timer.start(move_path_id)

def move_timer_end():
	if not timer_enabled:
		return
	t = timer.end(move_path_id)
	add_time(move_path_id, t)

def add_time(id, t):
	path_time_map[id].append(t)
	count = len(path_time_map[id])
	sum = 0
	for path_time in path_time_map[id]:
		sum += path_time
	avg = sum / count
	quick_print(id, 'time avg:', avg, 's; recorded count:', count)	

def create_node(x, y, score = -1):
	return {
		'x': x,
		'y': y,
		'score': score,
		'eph_score': -1,
		'path_parent': None,
		North: None,
		East: None,
		South: None,
		West: None
	}

def sort_eph_score_fn(a, b):
	return b['eph_score'] - a['eph_score']

def create_score(node, end_node):
	return (end_node['x'] - node['x'])**2 + (end_node['y'] - node['y'])**2

def assign_eph_score(node, end_node):
	if node['eph_score'] != -1:
		return
	score = create_score(node, end_node)
	node['eph_score'] = score

def assign_score(node, end_node):
	if node['score'] != -1:
		return
	score = create_score(node, end_node)
	node['score'] = score
		
def get_neighbors(node):
	neighbors = []
	for dir in dirs:
		if node[dir] != None:
			neighbors.append(node[dir])
	return neighbors

def is_in_node(node):
	return get_pos_x() == node['x'] and get_pos_y() == node['y']

def get_neighbor_dir(node, neighbor):
	neighbor_coords = get_point(neighbor)
	for dir in dirs:
		if node[dir] == None:
			continue
		n_coords = node[dir]
		if n_coords == neighbor_coords:
			return dir
	return None

def get_point(node):
	return (node['x'], node['y'])

def create_run(maze_size, max_gold = -1, timer_enabled_arg = False):
	global timer_enabled
	timer_enabled = timer_enabled_arg
	
	start_gold = num_items(Items.Gold)
	start_point = (0,0)
	maze_rect = rect.create_from_bounds((0, 0), (maze_size - 1, maze_size - 1))
	
	def need_more_gold():
		if max_gold == -1:
			return True
		return num_items(Items.Gold) - start_gold < max_gold
	
	def resetup():
		substance = maze_size * 2**(num_unlocked(Unlocks.Mazes) - 1)
		use_item(Items.Weird_Substance, substance)
		
	def setup():
		plant(Entities.Bush)
		substance = maze_size * 2**(num_unlocked(Unlocks.Mazes) - 1)
		use_item(Items.Weird_Substance, substance)
	
	def find_path(start_node, end_node, node_map):
		ended = False
		next_nodes = [start_node]
		next_nodes_set = set([get_point(start_node)])
		visited_nodes = set()
		explored_nodes = set()
		end_coords = get_point(end_node)
		
		while not ended and len(next_nodes) > 0:
			node = next_nodes.pop()
			coords = get_point(node)
			next_nodes_set.remove(coords)
			
			if coords == end_coords:
				ended = True
				break
			
			visited_nodes.add(coords)
			explored_nodes.add(coords)
			
			neighbors_coords = get_neighbors(node)
			def applicable_neighbors(n_coords, arr):
				return n_coords not in visited_nodes and n_coords in node_map and n_coords not in next_nodes_set
				
			a_neighbors_coords = common.filter(neighbors_coords, applicable_neighbors)
			if len(a_neighbors_coords) == 0:
				continue
			
			sorted_neighbors = []
			for n_coords in a_neighbors_coords:
				neighbor = node_map[n_coords]
				neighbor_dir = get_neighbor_dir(node, neighbor)
				neighbor['path_parent'] = opp_dir_map[neighbor_dir]
				explored_nodes.add(n_coords)
				assign_eph_score(neighbor, end_node)
				sorted_neighbors.append(neighbor)
			
			common.sort_by_fn(sorted_neighbors, sort_eph_score_fn)
			
			for neighbor in sorted_neighbors:
				next_nodes.append(neighbor)
				n_coords = get_point(neighbor)
				next_nodes_set.add(n_coords)
		
		if not ended:
			# no path found
			return None
		
		# create path of directions
		reversed_path = []
		cur = end_node
		cur_coords = get_point(end_node)
		start_coords = get_point(start_node)
		while cur_coords != start_coords:
			parent = cur['path_parent']
			reversed_path.append(opp_dir_map[parent])
			delta = dir_delta_map[parent]
			cur_coords = (cur['x'] + delta[0], cur['y'] + delta[1])
			cur = node_map[cur_coords]
			
		path = common.reverse(reversed_path)
		
		# reset eph scores
		for c in explored_nodes:
			n = node_map[c]
			n['eph_score'] = -1
			n['path_parent'] = None
		
		return path
	
	def find_closest_known_coords(treasure_coords, node_map):
		max_size = maze_size * 2 - 1
		for dist in range(1, max_size):
			for mult in quad_multipliers:
				swap = mult[2]
				if not swap:
					x_start = 0
					x_end = dist
					x_step = 1
					y_start = dist
					y_end = 0
					y_step = -1
				else:
					x_start = dist
					x_end = 0
					x_step = -1
					y_start = 0
					y_end = dist
					y_step = 1
				
				for i in range(dist):
					if not swap:
						x = i
						y = dist - i
					else:
						x = dist - i
						y = i
					delta = point.multiply((x, y), mult)
					check_point = point.translate_from_delta(treasure_coords, delta)
					if check_point in node_map:
						return check_point
		
		return None
						

	def find_treasure():
		cur = create_node(get_pos_x(), get_pos_y())
		visited_nodes = set()
		spent_nodes = set()
		node_map = {
			(cur['x'], cur['y']): cur
		}
		path = [cur]
		treasure_coords = measure()
		runs = 0
		first_try = False
		normal_try_interval = 5
		started_move_timer = False
		prefind_used = False

		def reset_scores():
			for c in node_map:
				node_map[c]['score'] = -1
				node_map[c]['path_parent'] = None
		
		def update_neighbors(exclude_dirs = []):
			c = (get_pos_x(),get_pos_y())
			node = node_map[c]
			for dir in dirs:
				if common.is_in(dir, exclude_dirs):
					continue
				if not can_move(dir):
					continue
				
				neighbor_coords = point.translate_from_delta(c, dir_delta_map[dir])
				node[dir] = neighbor_coords
				
				if neighbor_coords in node_map:
					neighbor = node_map[neighbor_coords]
				else:
					neighbor = create_node(neighbor_coords[0], neighbor_coords[1])
					score = common.dist_sq(neighbor_coords, treasure_coords)
					node_map[neighbor_coords] = neighbor
				
				neighbor[opp_dir_map[dir]] = c
				
		
		while len(path) > 0:
			node = path[len(path) - 1]
			
			if get_entity_type() == Entities.Treasure:
				if started_move_timer and not prefind_used:
					move_timer_end()
					started_move_timer = False
				runs += 1
				if runs > max_runs or not need_more_gold():
					harvest()
					break
				else:
					# reset
					resetup()
					reset_scores()
					visited_nodes = set()
					spent_nodes = set()
					path = [node]
					treasure_coords = measure()
					prefind_used = False
					# occasionally don't use find_path so we can update node_map via default pathfinding
					#first_try = (runs % normal_try_interval) != 0
					first_try = True
					continue
			
			if first_try:
				prefind_timer_start()
				first_try = False
				first_path = None
				if treasure_coords in node_map:
					first_path = find_path(node, node_map[treasure_coords], node_map)					
				else:
					closest_coords = find_closest_known_coords(treasure_coords, node_map)
					if closest_coords != None:
						first_path = find_path(node, node_map[closest_coords], node_map)
				
				if first_path != None:
					prev_p = None
					for p in first_path:
						update_neighbors([prev_p, p])
						prev_p = p
						if can_move(p):
							move(p)
						else:
							break
					first_coords = (get_pos_x(), get_pos_y())
					path = [node_map[first_coords]]
					prefind_used = True
					
				# only count when we actually find the treasure
				if first_coords == treasure_coords:
					prefind_timer_end()
				continue
			elif not started_move_timer:
				move_timer_start()
				started_move_timer = True
			
			coords = (get_pos_x(), get_pos_y())
			if coords[0] != node['x'] or coords[1] != node['y']:
				quick_print('mismatch coords', coords, get_point(node))
			visited_nodes.add(coords)
			
			if coords in spent_nodes:
				path.pop()
				if node['path_parent'] != None:
					move(node['path_parent'])
				if len(path) == 0:
					quick_print('empty path on spent nodes check')
				continue
			
			neighbors = []
			for dir in dirs:
				if not can_move(dir):
					if node[dir] != None:
						node[dir] = None
						quick_print('update dir', coords, dir)
					continue
					
				delta = dir_delta_map[dir]
				dir_coords = (node['x'] + delta[0], node['y'] + delta[1])
				if not rect.is_in_rect(maze_rect, dir_coords):
					continue
				
				if node[dir] != None:
					neighbor = node_map[dir_coords]
						
				elif dir_coords in node_map:
					node[dir] = dir_coords
					neighbor = node_map[dir_coords]
									
				else:
					neighbor = create_node(dir_coords[0], dir_coords[1])
					score = common.dist_sq(dir_coords, treasure_coords)
					node[dir] = dir_coords
					neighbor[opp_dir_map[dir]] = coords
					node_map[dir_coords] = neighbor
				
				if neighbor['score'] == -1:
					score = common.dist_sq(dir_coords, treasure_coords)
					neighbor['score'] = score
				
				neighbors.append(neighbor)
			
			def applicable_neighbors(item, _):
				return (item['x'], item['y']) not in visited_nodes
			
			a_neighbors = common.filter(neighbors, applicable_neighbors)
			
			a_neighbors_len = len(a_neighbors)
			if a_neighbors_len == 0:
				spent_nodes.add(coords)
				path.pop()
				if node['path_parent'] != None:
					move(node['path_parent'])
				if len(path) == 0:
					quick_print('empty path on no more neighbors')
				continue
			
			if a_neighbors_len == 1:
				last_neighbor = a_neighbors[0]
				last_neighbor_dir = get_neighbor_dir(node, last_neighbor)
				last_neighbor['path_parent'] = opp_dir_map[last_neighbor_dir]
				move(last_neighbor_dir)
				path.append(last_neighbor)
				spent_nodes.add(coords)
				continue
			
			# lowest score
			lowest_neighbor = a_neighbors[0]
			for neighbor in a_neighbors:
				if neighbor['score'] < lowest_neighbor['score']:
					lowest_neighbor = neighbor
			
			lowest_neighbor_dir = get_neighbor_dir(node, lowest_neighbor)
			lowest_neighbor['path_parent'] = opp_dir_map[lowest_neighbor_dir]
			move(lowest_neighbor_dir)
			path.append(lowest_neighbor)
				
		# harvesting nothing will clear the maze
		harvest()
		
	def end():
		pass
	
	def child_run():
		first_run = True
		while need_more_gold():
			common.go_to_pos(start_point[0], start_point[1])
			if first_run:
				common.wait(1.5)
				first_run = False
			setup()
			find_treasure()
			end()
	
	def run():
		global start_point
		global maze_rect
		world_size = get_world_size()
		world_rect = rect.create_from_bounds((0, 0), (world_size - 1, world_size - 1))
		num_mazes = common.floor(world_size / maze_size) ** 2
		while need_more_gold():
			maze_count = 0
			for x in range(0, world_size, maze_size):
				for y in range(0, world_size, maze_size):
					maze_rect_t = rect.create_from_bounds((x, y), (x + maze_size - 1, y + maze_size - 1))
					if not rect.rect_in_rect(world_rect, maze_rect_t):
						continue
					maze_rect = maze_rect_t
					start_point = (x + maze_size // 2, y + maze_size // 2)
					if (maze_count < num_mazes - 1):
						spawn_drone(child_run)
					maze_count += 1
				
			child_run()
			common.wait_for_all_drones()
		
	return run
	
if __name__ == "__main__":
	clear()
	runner = create_run(6)
	runner()
