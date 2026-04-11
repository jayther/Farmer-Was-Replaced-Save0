import timer
import carrot_poly_farmer

goal = 200000000 # 200000000

farmer = carrot_poly_farmer.create_run(0, 31, num_items(Items.Carrot) + goal)

clear()
timer.start('carrot')
farmer()
duration = timer.end('carrot')
quick_print('time to', goal, 'carrots:', duration, 's')