
def create(x, y):
	return (x, y)

def translate(point, x, y):
	return (point[0] + x, point[1] + y)

def translate_from_delta(point, delta):
	return (point[0] + delta[0], point[1] + delta[1])

def multiply(point, mult):
	return (point[0] * mult[0], point[1] * mult[1])

