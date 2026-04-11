import timer
import tree_poly_farmer

goal = 1000000000 # 200000000
abs_goal = num_items(Items.Wood) + goal

farmer = tree_poly_farmer.create_run(0, 31, abs_goal)

clear()
timer.start('wood')
farmer()
duration = timer.end('wood')
quick_print('time to', goal, 'wood:', duration, 's')