import cactus_section

clear()

runner = cactus_section.create_run(0, 31, True)

start_cactus = num_items(Items.Cactus)

while num_items(Items.Cactus) - start_cactus < 33554432:
	runner()
