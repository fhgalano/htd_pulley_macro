from math import pi


def pitch_diameter(tooth_count, tooth_pitch):
    return tooth_count * tooth_pitch / pi


active_sketch.addGeometry(Part.ArcOfCircle(Part.Circle(App.Vector(center[0], center[1],0), App.Vector(0,0,1), radius), deg_to_rads(start_deg), deg_to_rads(end_deg)), is_construction)