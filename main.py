import basic_plant_column
import pumpkin_section
import cactus_section
import column_farmer

change_hat(Hats.Traffic_Cone)

main_farmer = column_farmer.create_multi({
	0: column_farmer.do_nothing_column,
	1: column_farmer.do_nothing_column,
	2: basic_plant_column.create_basic_plant(Entities.Grass, False, None, False, (2, 9)),
	10: basic_plant_column.create_basic_plant(Entities.Tree, False, basic_plant_column.plant_tree, False, (10, 17)),
	18: basic_plant_column.create_basic_plant(Entities.Carrot, True, None, False, (18, 21)),
	22: pumpkin_section.create_run(22, 27, True),
	28: cactus_section.create_run(28, 31, True)
}, (0, 1))
	
main_farmer()
