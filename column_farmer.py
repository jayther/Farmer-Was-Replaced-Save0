import sunflower_column
import tracker
import common

def do_nothing_column():
	pass

def create_farmer(config, sun_collect_first = False, sun_cols = (0,0)):
	def run():		
		clear()
		
		# setup sunflower column
		sunflower_column.setup(sun_cols[0], sun_cols[1])
		if sun_collect_first:
			sunflower_column.wait_until_grown()
			sunflower_column.check_get_power(True)

		first_run = True
		loops = 0		

		current_runner = None
		
		while True:
			x = get_pos_x()
			if x == 0 and not first_run:
				tracker.start()
			
			if x in config:
				current_runner = config[x]	
			current_runner()
			
			if get_pos_x() == get_world_size() - 1:
				if not first_run:
					tracker.end()
				loops += 1
				if loops == 1:
					first_run = False
					
			sunflower_column.check_get_power()
			move(East)
	return run

def create_multi(config, sun_cols = (0,0)):
	def spawn(col_start, col_end, runner):
		def spawn_runner():
			common.go_to_pos(col_start, 0)
			while True:
				runner()
				x = get_pos_x()
				if x < col_end:
					move(East)
				else:
					common.go_to_pos(col_start, 0)
		spawn_drone(spawn_runner)
	
	def run():
		clear()
		
		dedicated_runner = sunflower_column.create_dedicated_runner(sun_cols[0], sun_cols[1])
		
		config_start = -1
		current_config = None
		for i in range(get_world_size()):
			if i in config:
				if current_config and config_start != -1:
					spawn(config_start, i - 1, current_config)
					config_start = -1
				if config[i] == do_nothing_column:
					current_config = None
				else:
					current_config = config[i]
				config_start = i
		
		if current_config and config_start != -1:
			spawn(config_start, i - 1, current_config)
		
		while True:
			dedicated_runner()
			
	return run