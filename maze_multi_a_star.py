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

def create_run(col_start, col_end, max_gold = -1):
	maze_size = col_end - col_start + 1
	child = False
	start_gold = num_items(Items.Gold)
	starting_point = (0, 0)
	
	def need_more_gold():
		if max_gold == -1:
			return True
		return num_items(Items.Gold) - start_gold < max_gold
	
	def setup():
		global starting_point
		common.go_to_pos(col_start, 0)
		
		if num_drones() == 1:
			# full setup
			drone_points = []
			
			# find most square rectangle dimensions with whole numbers
			most_square_dims = (1, maze_size)
			most_square_dim_diff = abs(maze_size - 1)
			for i in range(1, maze_size / 2 + 1):
				if (maze_size % i) == 0:
					w = maze_size / i
					h = i
					dim_diff = abs(w - h)
					if dim_diff < most_square_dim_diff:
						most_square_dims = (w, h)
						most_square_dim_diff = dim_diff
						
			w, h = most_square_dims
			
			for i in range(0, maze_size, w):
				x = i + w / 2
				for j in range(0, maze_size, h):
					y = j + h / 2
					starting_point = (x, y)
					if num_drones() < max_drones():
						spawn_drone(child_run)
		
		common.go_to_pos(starting_point[0], starting_point[1])
		
		# TODO wait for other drones to be in position
		common.wait(0.5)
		
		plant(Entities.Bush)
		substance = maze_size * 2**(num_unlocked(Unlocks.Mazes) - 1)
		use_item(Items.Weird_Substance, substance)
		
	def repeat_setup():
		plant(Entities.Bush)
		substance = maze_size * 2**(num_unlocked(Unlocks.Mazes) - 1)
		use_item(Items.Weird_Substance, substance)
	
	def child_run():
		global child
		child = True
		
		while need_more_gold():
			waiting = True
			common.go_to_pos(starting_point[0], starting_point[1])
			
			while waiting:
				if get_entity_type() != Entities.Grass:
					waiting = False
			find_treasure()

	def find_treasure():
		cur = create_node(get_pos_x(), get_pos_y())
		visited_nodes = set()
		spent_nodes = set()
		node_map = {
			(cur['x'], cur['y']): cur
		}
		path = [cur]
		treasure_coords = measure()

		# workaround for racing condition
		if treasure_coords == None:
			return
		
		while len(path) > 0:
			node = path[len(path) - 1]
			
			if get_entity_type() == Entities.Treasure:
				harvest()
				break
			
			if get_entity_type() == Entities.Grass:
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
	
	def repeat_run():
		first_run = True
		while need_more_gold():
			common.go_to_pos(starting_point[0], starting_point[1])
			common.wait(0.25)
			if first_run:
				first_run = False
			elif need_more_gold():
				repeat_setup()
			find_treasure()
		
	def end():
		common.go_to_pos(col_end, 0)
	
	def run():
		setup()
		repeat_run()
		end()
		
	return run
	
if __name__ == '__main__':
	clear()
	runner = create_run(0, 31)
	while True:
		runner()
	