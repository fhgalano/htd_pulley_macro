import sys

sys.path
sys.path.append("C:\\Users\\fhgal\\AppData\\Local\\Programs\\FreeCAD 0.19\\bin")

import FreeCAD

def get_active_sketch():
	return FreeCAD.getDocument(FreeCAD.ActiveDocument.Name).getObject(FreeCAD.ActiveDocument.ActiveObject.Name)


def draw_circle(active_sketch, radius: float, is_construction: bool):
	circle = active_sketch.addGeometry(Part.Circle(App.Vector(0,0,0), App.Vector(0,0,1), radius), is_construction)
	update_drawing()
	return circle


def draw_line(active_sketch, start, end, is_construction):
	line = active_sketch.addGeometry(Part.LineSegment(App.Vector(start[0], start[1], 0), App.Vector(end[0], end[1], 0)), is_construction)
	update_drawing()
	return line

def draw_arc(active_sketch, center, radius, start_deg, end_deg, is_construction):
	arc = active_sketch.addGeometry(Part.ArcOfCircle(Part.Circle(App.Vector(center[0], center[1],0), App.Vector(0,0,1), radius), deg_to_rads(start_deg), deg_to_rads(end_deg)), is_construction)
	update_drawing()
	return arc


def update_drawing():
	App.ActiveDocument.recompute()