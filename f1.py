import common

maze_size = 32
drone_square = maze_size ** 0.5
local_mid = drone_square / 2
drone_points = []

# find most square rectangle dimensions with whole numbers
most_square_dims = (1, maze_size)
most_square_dim_diff = abs(maze_size - 1)
for i in range(1, maze_size / 2 + 1):
	if (maze_size % i) == 0:
		w = maze_size / i
		h = i
		dim_diff = abs(w - h)
		if dim_diff < most_square_dim_diff:
			most_square_dims = (w, h)
			most_square_dim_diff = dim_diff

quick_print(most_square_dims)

w, h = most_square_dims
for i in range(0, maze_size, w):
	x = i + w / 2
	for j in range(0, maze_size, h):
		y = j + h / 2
		drone_points.append((x, y))

quick_print(drone_square, local_mid)
quick_print(len(drone_points))
quick_print(drone_points)