

target_unlocks = [
	Unlocks.Grass,
	Unlocks.Speed,
	Unlocks.Expand,
	Unlocks.Plant,
	Unlocks.Carrots,
	Unlocks.Pumpkins,
	Unlocks.Cactus,
	Unlocks.Dinosaurs,
	Unlocks.Fertilizer,
	Unlocks.Mazes,
	Unlocks.Megafarm,
	Unlocks.Watering,
	Unlocks.Sunflowers,
	Unlocks.Trees,
	Unlocks.Leaderboard
]

quick_print('unlock_map = {')
for upgrade in target_unlocks:
	upgrade_level = 0
	run_time = 0
	quick_print('\t', upgrade, ': [')
	while run_time < 0.2:
		unlocks = {
			upgrade: upgrade_level
		}
		items = {}
		globals = {
			'upgrade_type': upgrade
		}
		seed = -1
		filename = 'unlocks_mapper_out'
		speedup = 1
		run_time = simulate(filename, unlocks, items, globals, seed, speedup)
		upgrade_level += 1
	
	quick_print('\t]')

quick_print('}')