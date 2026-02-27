import sunflower_column
import common

def plant_tree(x, y):
	if (x + y) % 2 == 0:
		plant(Entities.Tree)
	# else, grass

def fertilize_pattern(x, y):
	if (((x / 2) % 2) + y) % 2 == 0:
		use_item(Items.Fertilizer)
		use_item(Items.Weird_Substance)
		use_item(Items.Fertilizer)

def create_run(col_start, col_end):			
	def run():
		for i in range(col_start, col_end + 1):
			for j in range(get_world_size()):
				if can_harvest():
					harvest()
				plant_tree(i, j)
				fertilize_pattern(i, j)
				move(North)
			sunflower_column.check_get_power()
			if i != col_end:
				move(East)
	return run