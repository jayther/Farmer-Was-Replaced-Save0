
timer_map = {}

def start(id):
	timer_map[id] = get_time()
	return timer_map[id]

def end(id):
	if id not in timer_map:
		return -1
	
	return get_time() - timer_map[id]
