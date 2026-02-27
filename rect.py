import point

def create_from_bounds(lower_bound, upper_bound):
	# normalize lower and upper bounds so lower bounds is always bottom left and
	# upper bounds is always upper right
	return (
		(min(lower_bound[0], upper_bound[0]), min(lower_bound[1], upper_bound[1])),
		(max(lower_bound[0], upper_bound[0]), max(lower_bound[1], upper_bound[1]))
	)

def is_in_rect(rect, point):
	return (
		point[0] >= rect[0][0] and
		point[0] <= rect[1][0] and
		point[1] >= rect[0][1] and
		point[1] <= rect[1][1]
	)

def grow_rect(rect, amount):
	return create_from_bounds(
		point.translate(rect[0], -amount, -amount),
		point.translate(rect[1], amount, amount)
	)
