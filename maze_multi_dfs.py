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

def wait_for_any_drone():
	while num_drones() >= max_drones():
		pass

def wait_for_all_drones():
	while num_drones() > 1:
		pass

def create_run(col_start, col_end):
	maze_size = col_end - col_start + 1
	def setup():
		mid = maze_size / 2
		common.go_to_pos(mid, mid)
		plant(Entities.Bush)
		substance = maze_size * 2**(num_unlocked(Unlocks.Mazes) - 1)
		use_item(Items.Weird_Substance, substance)

	def find_treasure():
		cur = create_node(get_pos_x(), get_pos_y())
		visited_nodes = set()
		spent_nodes = set()
		node_map = {
			(cur['x'], cur['y']): cur
		}
		path = [cur]
		treasure_coords = measure()
		
		# TODO turn this into a function somehow so we can spawn
		
		def has_ended():
			new_coords = measure()
			return treasure_coords != new_coords
		
		def traverse():
			while len(path) > 0:
				node = path[len(path) - 1]
				
				if get_entity_type() == Entities.Treasure:
					harvest()
					break
				
				if has_ended():
					break
					
				if common.is_in(node, dirs):
					move(node)
					path.pop()
					continue
				
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
						node[dir] = neighbor_coords
						neighbor[opp_dir_map[dir]] = coords
						neighbor['path_parent'] = opp_dir_map[dir]
						node_map[neighbor_coords] = neighbor
					neighbors.append(neighbor)
				
				def applicable_neighbors(item, _):
					return (item['x'], item['y']) not in visited_nodes
				
				a_neighbors = common.filter(neighbors, applicable_neighbors)
				
				a_neighbors_len = len(a_neighbors)
				if a_neighbors_len == 0:
					spent_nodes.add(coords)
					break
					# path.pop()
					#if node['path_parent'] != None:
					#	move(node['path_parent'])
					#continue
				
				if a_neighbors_len == 1:
					last_neighbor = a_neighbors[0]
					last_neighbor_dir = get_neighbor_dir(node, last_neighbor)
					move(last_neighbor_dir)
					path.append(last_neighbor)
					spent_nodes.add(coords)
					continue
				
				for i in range(a_neighbors_len - 1):
					neighbor = a_neighbors[i]
					neighbor_dir = get_neighbor_dir(node, neighbor)
					path.append(neighbor)
					path.append(neighbor_dir)
					wait_for_any_drone()
					spawn_drone(traverse)
					path.pop()
					path.pop()
				
				neighbor = a_neighbors[a_neighbors_len - 1]
				neighbor_dir = get_neighbor_dir(node, neighbor)
				move(neighbor_dir)
				path.append(neighbor)
		
		spawn_drone(traverse)
		wait_for_all_drones()
		# harvesting nothing will clear the maze
		harvest()
		
	def end():
		mid = maze_size / 2
		common.go_to_pos(mid, mid)
	
	def run():
		setup()
		find_treasure()
		end()
		
	return run
	
if __name__ == "__main__":
	clear()
	farmer = create_run(0, 31)
	while True:
		farmer()