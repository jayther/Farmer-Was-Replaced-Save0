import common

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

def create_run(col_start, col_end):
	maze_size = col_end - col_start + 1
	def setup():
		common.go_to_pos(col_start, 0)
		plant(Entities.Bush)
		substance = maze_size * 2**(num_unlocked(Unlocks.Mazes) - 1)
		use_item(Items.Weird_Substance, substance)
	
	def find_path(start_node, end_node, node_map):
		ended = False
		next_nodes = [start_node]
		visited_nodes = set()
		explored_nodes = set()
		end_coords = get_point(end_node)
		
		while not ended and len(next_nodes) > 0:
			node = next_nodes.pop()
			coords = get_point(node)
			
			if coords == end_coords:
				ended = True
				break
			
			visited_nodes.add(coords)
			explored_nodes.add(coords)
			
			neighbors = get_neighbors(node)
			def applicable_neighbors(item, arr):
				return get_point(item) not in visited_nodes
				
			a_neighbors = common.filter(neighbors, applicable_neighbors)
			if len(a_neighbors) == 0:
				continue
			
			for n in a_neighbors:
				n['path_parent'] = node
				n_coords = get_point(n)
				explored_nodes.add(n_coords)
				assign_eph_score(n, end_node)
				next_nodes.append(n)
			
			common.sort_by_fn(next_nodes, sort_eph_score_fn)
		
		if not ended:
			# no path found
			return None
		
		# create path of directions
		reversed_path = []
		cur = end_node
		cur_coords = get_point(cur)
		start_coords = get_point(start_node)
		while cur_coords != start_coords:
			parent = cur['path_parent']
			# purposely doing the other way because it's reversed
			reversed_path.append(get_neighbor_dir(parent, cur))
			cur = parent
			cur_coords = get_point(cur)
		path = common.reverse(reversed_path)
		
		# reset eph scores
		for c in explored_nodes:
			n = node_map[c]
			n['eph_score'] = -1
			n['path_parent'] = None
		
		return path


	def find_treasure():
		cur = create_node(get_pos_x(), get_pos_y())
		visited_nodes = set()
		spent_nodes = set()
		node_map = {
			(cur['x'], cur['y']): cur
		}
		path = [cur]
		treasure_coords = measure()
		
		while len(path) > 0:
			node = path[len(path) - 1]
			
			if get_entity_type() == Entities.Treasure:
				harvest()
				break
			
			coords = (get_pos_x(), get_pos_y())
			
			if coords in spent_nodes:
				path.pop()
				if node['path_parent'] != None:
					move(node['path_parent'])
				continue
			
			visited_nodes.add(coords)
			
			neighbors = []
			for dir in dirs:
				if not can_move(dir):
					continue
				delta = dir_delta_map[dir]
				if node[dir] != None:
					neighbor = node_map[node[dir]]
				else:
					neighbor = create_node(node['x'] + delta[0], node['y'] + delta[1])
					neighbor_coords = get_point(neighbor)
					score = common.dist_sq(neighbor_coords, treasure_coords)
					node[dir] = neighbor_coords
					neighbor[opp_dir_map[dir]] = coords
					neighbor['path_parent'] = opp_dir_map[dir]
					neighbor['score'] = score
					node_map[neighbor_coords] = neighbor
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
				continue
			
			if a_neighbors_len == 1:
				last_neighbor = a_neighbors[0]
				last_neighbor_dir = get_neighbor_dir(node, last_neighbor)
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
			move(lowest_neighbor_dir)
			path.append(lowest_neighbor)
				
		# harvesting nothing will clear the maze
		harvest()
		
	def find_treasure_old():
		cur = create_node(get_pos_x(), get_pos_y())
		next_nodes = [cur]
		visited_nodes = set()
		node_map = {
			(cur['x'], cur['y']): cur
		}
		
		while len(next_nodes) > 0:
			node = next_nodes.pop()
			if not is_in_node(node):
				path = find_path(node_map[(get_pos_x(), get_pos_y())], node, node_map)
				for p in path:
					move(p)
			
			if get_entity_type() == Entities.Treasure:
				harvest()
				break
			
			coords = (get_pos_x(), get_pos_y())
			visited_nodes.add(coords)
			
			neighbors = []
			for dir in dirs:
				if not can_move(dir):
					continue
				delta = dir_delta_map[dir]
				if node[dir] != None:
					neighbor = node[dir]
				else:
					neighbor = create_node(node['x'] + delta[0], node['y'] + delta[1])
					node[dir] = neighbor
					neighbor[opp_dir_map[dir]] = node
					node_map[get_point(neighbor)] = neighbor
				neighbors.append(neighbor)
			
			def applicable_neighbors(item, _):
				return (item['x'], item['y']) not in visited_nodes
			
			a_neighbors = common.filter(neighbors, applicable_neighbors)
			
			if len(a_neighbors) == 0:
				continue
				
			for n in a_neighbors:
				next_nodes.append(n)
			
			last_neighbor = a_neighbors[len(a_neighbors) - 1]
			last_neighbor_dir = get_neighbor_dir(node, last_neighbor)
			move(last_neighbor_dir)
				
		# harvesting nothing will clear the maze
		harvest()
		
	def end():
		common.go_to_pos(col_end, 0)
	
	def run():
		setup()
		find_treasure()
		end()
		
	return run