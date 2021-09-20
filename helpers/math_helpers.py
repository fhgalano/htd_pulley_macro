from math import pi

<<<<<<< HEAD

def pitch_diameter(tooth_count, tooth_pitch):
    return tooth_count * tooth_pitch / pi


active_sketch.addGeometry(Part.ArcOfCircle(Part.Circle(App.Vector(center[0], center[1],0), App.Vector(0,0,1), radius), deg_to_rads(start_deg), deg_to_rads(end_deg)), is_construction)
=======
def pitch_diameter(tooth_count, tooth_pitch):
	return tooth_count * tooth_pitch / pi

def tooth_separation_angles(teeth: float):
	return 360.0 / teeth

def outside_diameter(pd):
	pd_to_tooth = (3.81 - 2.08) / 2
	return pd - (2 * pd_to_tooth)

def deg_to_rads(deg):
	return deg * pi / 180


>>>>>>> 55390a480180ac8f542d8863ca583682e181dfdb
