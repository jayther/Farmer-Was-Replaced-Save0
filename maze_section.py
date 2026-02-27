
import common

dirs = [North, East, South, West]

def create_run(col_start, col_end):
	maze_size = col_end - col_start + 1
	def setup():
		plant(Entities.Bush)
		substance = maze_size * 2**(num_unlocked(Unlocks.Mazes) - 1)
		use_item(Items.Weird_Substance, substance)
		
	def find_treasure():
		dir_index = 0
		found = False
		while not found:
			if get_entity_type() == Entities.Treasure:
				harvest()
				found = True
				break
			
			left_index = (dir_index - 1) % 4
			if can_move(dirs[left_index]):
				dir_index = left_index
				move(dirs[dir_index])
			elif can_move(dirs[dir_index]):
				move(dirs[dir_index])
			else:
				dir_index = (dir_index + 1) % 4
				move(dirs[dir_index])
				
		# harvesting nothing will clear the maze
		harvest()
		
	def end():
		common.go_to_pos(col_end, 0)
		
	def run():
		setup()
		find_treasure()
		end()
	return run