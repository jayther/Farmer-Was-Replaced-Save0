import sunflower_column
import common

def plant_tree(x, y):
	if (x + y) % 2 == 0:
		plant(Entities.Tree)
	# else, grass

def fertilize_pattern(x, y):
	if ((x * 3) + y) % 5 == 0:
	#	print(x, y)
		if num_items(Items.Weird_Substance) == 0:
			common.wait_for_item(Items.Fertilizer, 1)
			use_item(Items.Fertilizer)
		else:
			common.wait_for_item(Items.Fertilizer, 2)
			use_item(Items.Fertilizer)
			use_item(Items.Weird_Substance)
			use_item(Items.Fertilizer)

def create_run(col_start, col_end):
	first_run = True
	def run():
		global first_run
		if first_run:
			# plant
			for i in range(col_start, col_end + 1):
				for j in range(get_world_size()):
					plant_tree(i, j)
					move(North)
				move(East)
			first_run = False
				
		common.go_to_pos(col_start, 0)
		
		# fertilize
		for i in range(col_start, col_end + 1):
			for j in range(get_world_size()):
				fertilize_pattern(i, j)
				move(North)
			move(East)
				
		common.go_to_pos(col_start, 0)		
		
		# harvest
		for i in range(col_start, col_end + 1):
			for j in range(get_world_size()):
				while not can_harvest():
					pass
				harvest()
				plant_tree(i, j)
				move(North)
			move(East)
				
		common.go_to_pos(col_start, 0)	
	return run
	
if __name__ == '__main__':
	clear()
	set_world_size(10)
	runner = create_run(0, 9)
	while True:
		runner()