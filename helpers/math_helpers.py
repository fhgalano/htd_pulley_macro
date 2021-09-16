from math import pi

def pitch_diameter(tooth_count, tooth_pitch):
	return tooth_count * tooth_pitch / pi

def tooth_separation_angles(teeth: float):
	return 360.0 / teeth

def outside_diameter(pd):
	pd_to_tooth = (3.81 - 2.08) / 2
	return pd - (2 * pd_to_tooth)

def deg_to_rads(deg):
	return deg * pi / 180


