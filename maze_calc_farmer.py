import column_farmer
import maze_section
import maze_section_a_star
import common

clear()

time_start = 0
treasure_start = 0
max_runs = 50

def start_time():
	global time_start
	time_start = get_time()

def end_time():
	dt = get_time() - time_start
	return dt

def start_treasure():
	global treasure_start
	treasure_start = num_items(Items.Gold)

def end_treasure():
	dt = num_items(Items.Gold) - treasure_start
	return dt

def create_maze_section_test(size, runs):
	col_start = 0
	col_end = size - 1
	runner = maze_section.create_run(col_start, col_end)
	def maze_section_test():
		for _ in range(runs):
			runner()
			common.go_to_pos(0,0)
	return maze_section_test

def create_a_star_test(size, runs):
	col_start = 0
	col_end = size - 1
	runner = maze_section_a_star.create_run(col_start, col_end)
	def a_star_test():
		for _ in range(runs):
			runner()
			common.go_to_pos(0,0)
	return a_star_test

tests = []

for size in range(1, get_world_size() + 1):
	fn = create_maze_section_test(size, max_runs)
	tests.append(('wallhug', size, fn))

#tests.append(('wallhug', 32, create_maze_section_test(32)))

for size in range(1, get_world_size() + 1):
	fn = create_a_star_test(size, max_runs)
	tests.append(('astar', size, fn))

highest_settings = tests[0]
highest_rate = 0
for (test_name, test_size, test) in tests:
	start_time()
	start_treasure()
	test()
	time = end_time()
	treasure = end_treasure()
	treasure_rate = treasure / time
	quick_print(test_name, test_size, '; time:', time, 's; treasure:', treasure, '; gold/s:', treasure_rate, 'g/s')
	if treasure_rate > highest_rate:
		highest_rate = treasure_rate
		highest_settings = (test_name, test_size, test)

test_name, test_size, test = highest_settings
quick_print('USING', test_name, test_size)
while True:
	start_time()
	start_treasure()
	test()
	time = end_time()
	treasure = end_treasure()
	treasure_rate = treasure / time	
	quick_print(test_name, test_size, '; time:', time, 's; treasure:', treasure, '; gold/s:', treasure_rate, 'g/s')
