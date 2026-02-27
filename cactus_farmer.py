import basic_plant_column
import pumpkin_section
import cactus_section
import column_farmer

change_hat(Hats.Traffic_Cone)

main_farmer = column_farmer.create_multi({
	0: column_farmer.do_nothing_column,
	1: column_farmer.do_nothing_column,
	28: cactus_section.create_run(2, 31, True)
}, (0, 1))
	
main_farmer()
