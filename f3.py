unlocks = {
	Unlocks.Pumpkins: 2,
	Unlocks.Carrots: 2,
	Unlocks.Cactus: 2,
	Unlocks.Expand: 6,
	Unlocks.Dinosaurs: 4,
	Unlocks.Trees: 3
}
items = {
	Items.Cactus: 1000000,
	Items.Power: 1000000
}
globals = {}
filename = 'dinosaur_section'
speedup = 4
simulate(filename, unlocks, items, globals, 16, speedup)
#for seed in range(1,200):
#	quick_print('dinosaur seed', seed)
#	simulate(filename, unlocks, items, globals, seed, speedup)