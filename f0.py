col_size = 32
row_size = 30
section_size = col_size / row_size
section_row = 0
row_start = -1
row_end = -1

drone_count = 0

for row in range(0, col_size):
	if section_row < 1:
		row_start = row
		if drone_count == row_size - 1:
			break
			
	section_row += 1
	if section_row >= section_size:
		row_end = row
		quick_print('row', row_start, row_end)
		drone_count += 1
		section_row -= section_size

row_end = col_size - 1
quick_print('row', row_start, row_end)
drone_count += 1
quick_print('drones', drone_count)