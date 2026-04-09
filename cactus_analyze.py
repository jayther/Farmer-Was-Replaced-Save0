tests_per_config = 10

seed = -1
filename = 'cactus_analyze_sim'
speedup = 1000

items = {
	Items.Pumpkin: 1000000000,
	Items.Power: 1000000
}

expand_size_map = {
	6: 12,
	7: 16,
	8: 22
}

def get_cactus_yield(size):
	return (size ** 2) ** 2

def create_unlock_map(expand_level):
	return {
		Unlocks.Cactus: 1,
		Unlocks.Plant: 1,
		Unlocks.Megafarm: 5,
		Unlocks.Speed: 5,
		Unlocks.Expand: expand_level
	}

def run_sim(expand_level, brick, presort):
	size = expand_size_map[expand_level]
	yield = get_cactus_yield(size)
	unlocks = create_unlock_map(expand_level)
	globals = {
		'sim_goal': yield,
		'sim_presort': presort,
		'sim_brick': brick
	}
	sum_duration = 0
	for test_num in range(tests_per_config):
		duration = simulate(filename, unlocks, items, globals, seed, speedup)
		quick_print(
			'brick', brick,
			', size', size,
			', presort', presort,
			', test', test_num,
			':', duration, 's'
		)
		sum_duration += duration
	avg_duration = sum_duration / tests_per_config
	quick_print('Tests finished. Avg:', avg_duration, 's')
	
# no brick
for expand_level in range(6, 9):
	run_sim(expand_level, False, False)
	run_sim(expand_level, False, True)

# brick, presort
for expand_level in range(6, 9):
	run_sim(expand_level, True, False)
	run_sim(expand_level, True, True)
