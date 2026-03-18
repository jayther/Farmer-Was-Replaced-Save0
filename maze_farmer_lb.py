import maze_multi_reuse
import common

target_gold = 9863168

clear()
runner = maze_multi_reuse.create_run(6, target_gold)

start_gold = num_items(Items.Gold)
while num_items(Items.Gold) - start_gold < target_gold:
	runner()
