import pumpkin_section

runner = pumpkin_section.create_run(0, 31, True)

while num_items(Items.Pumpkin) < 200000000:
	runner()