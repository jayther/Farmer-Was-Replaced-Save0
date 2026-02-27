
tracked = [
	Items.Hay,
	Items.Wood,
	Items.Carrot
]
tracked_map = {}

track_id_pool = 0
track_id_map = {}

def start():
	for item in tracked:
		tracked_map[item] = num_items(item)

def end():
	for item in tracked:
		if num_items(item) < tracked_map[item]:
			print(item, 'less')

def create_tracker(items):
	global track_id_pool
	global track_id_map
	track_id = track_id_pool
	track_id_pool += 1
	track_id_map[track_id] = {}
	
	def start_track():
		for item in items:
			track_id_map[track_id][item] = num_items(item)
	
	def end_track():
		for item in items:
			if num_items(item) < track_id_map[track_id][item]:
				print(item, 'less')
	
	return start_track, end_track
		