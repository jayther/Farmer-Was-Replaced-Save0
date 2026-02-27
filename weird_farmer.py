import weird_section
import basic_plant_column
import column_farmer

change_hat(Hats.Wizard_Hat)

weird_farmer = column_farmer.create_farmer({
	0: column_farmer.do_nothing_column,
	1: column_farmer.do_nothing_column,
	2: weird_section.create_run(2,4),
	5: column_farmer.do_nothing_column,
})

weird_farmer()

