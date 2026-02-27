import column_farmer
import maze_section
import maze_section_a_star
import common

clear()

change_hat(Hats.Traffic_Cone)

#maze_farmer = column_farmer.create_farmer({
#	0: maze_section.create_run(0, 9),
#	10: column_farmer.do_nothing_column,
#}, True, (10, 10))

runner = maze_section_a_star.create_run(0, 31)
#runner = maze_section.create_run(0, 31)

def maze_farmer():
	while True:
		runner()
		common.go_to_pos(0, 0)

maze_farmer()
