
unlocks = {
	Unlocks.Plant: 1,
	Unlocks.Sunflowers: 1,
	Unlocks.Expand: 8,
	Unlocks.Mazes: 6
}
items = {
	Items.Weird_Substance: 1000000000,
	Items.Power: 1000000000
}
seed = -1
filename = 'maze_reuse_section'
speedup = 1000
for target_size in range(2, 9):
	globals = {
		'target_size': target_size,
		'sim_max_runs': 50
	}
	simulate(filename, unlocks, items, globals, seed, speedup)
