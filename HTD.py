import os
import sys
from math import pi
from time import sleep

import FreeCAD
import FreeCADGui as Gui
import Draft
from PySide import QtGui


source_dir = os.path.dirname(__file__)
helper_dir = os.path.join(source_dir, 'helpers')
sys.path
sys.path.append(helper_dir)

import helpers.math_helpers as mh

# constants
# TODO: have num teeth given as an input
# TODO: have constants defined by HTD 3M/5M/8M etc. possibly from a reference file
radius_small_arc = 0.43
radius_large_arc = 1.49
num_teeth = 12
pitch = 5
tooth_size = 2.06
max_arc_percent = 0.35

# freecad helpers
def get_active_sketch():
	return FreeCAD.getDocument(FreeCAD.ActiveDocument.Name).getObject(FreeCAD.ActiveDocument.ActiveObject.Name)


def create_new_sketch():
	doc = FreeCAD.ActiveDocument
	obj = FreeCAD.ActiveDocument.addObject("Sketcher::SketchObject", "GearSketch")
	return obj, doc


def clean_up(doc, sketch):
	FreeCAD.getDocument(doc.Name).removeObject(sketch.Name)
	update_drawing()


def draw_circle(active_sketch, radius: float, is_construction: bool):
	circle = active_sketch.addGeometry(Part.Circle(App.Vector(0,0,0), App.Vector(0,0,1), radius), is_construction)
	update_drawing()
	return circle


def draw_line(active_sketch, start, end, is_construction):
	line = active_sketch.addGeometry(Part.LineSegment(App.Vector(start[0], start[1], 0), App.Vector(end[0], end[1], 0)), is_construction)
	update_drawing()
	return line


def draw_arc(active_sketch, center, radius, start_deg, end_deg, is_construction):
	arc = active_sketch.addGeometry(Part.ArcOfCircle(Part.Circle(App.Vector(center[0], center[1],0), App.Vector(0,0,1), radius), mh.deg_to_rads(start_deg), mh.deg_to_rads(end_deg)), is_construction)
	update_drawing()
	return arc


def create_arc(active_sketch, is_construction, start_deg, end_deg):
	arc = active_sketch.addGeometry(Part.ArcOfCircle(Part.Circle(App.Vector(0,0,0), App.Vector(0,0,1), 1), mh.deg_to_rads(start_deg), mh.deg_to_rads(end_deg)), is_construction)
	return arc


def get_edge_size(active_doc, active_sketch, edge):
	edge_str = 'Edge' + str(int(edge)+1)
	Gui.Selection.addSelection(str(active_doc.Name), str(active_sketch.Name), edge_str)
	update_drawing()
	sleep(0.1)
	edge_size = Gui.Selection.getSelectionEx()[0].SubObjects[0].Length
	Gui.Selection.clearSelection()
	return edge_size

def create_polar_array(sketch):
	_obj_ = Draft.make_polar_array(
		sketch,
		number=num_teeth,
		angle=360.0,
		center=FreeCAD.Vector(0.0, 0.0, 0.0),
		use_link=False)
	_obj_.Fuse = True
	Draft.autogroup(_obj_)
	update_drawing()

	return _obj_


def update_drawing():
	App.ActiveDocument.recompute()


# main functions
def create_htd_pulley(active_doc, active_sketch):

	# math vars
	pitch_radius = mh.pitch_diameter(num_teeth, pitch) / 2
	outer_radius = mh.outside_diameter(pitch_radius * 2) / 2

	# drawing
	outer_radius_line = draw_line(active_sketch, (0, 0), (25, outer_radius), True)
	pitch_radius_line = draw_line(active_sketch, (0, 0), (25, pitch_radius), True)
	mid_tooth_line = draw_line(active_sketch, (0, 0), (25, pitch_radius), True)
	tooth_flat = draw_arc(active_sketch, App.Vector(0, 0, 0), outer_radius, 85, 90, False)
	tooth_small_curve = create_arc(active_sketch, False, 20, 90)
	tooth_large_curve = create_arc(active_sketch, False, -210, -90)

	# constraints
	# od line
	active_sketch.addConstraint(Sketcher.Constraint('Vertical', outer_radius_line))
	active_sketch.addConstraint(Sketcher.Constraint('Coincident', outer_radius_line, 1, -1, 1))
	active_sketch.addConstraint(Sketcher.Constraint('Distance', outer_radius_line, 1, outer_radius_line, 2, outer_radius))

	# pd line
	active_sketch.addConstraint(Sketcher.Constraint('Vertical', pitch_radius_line))
	active_sketch.addConstraint(Sketcher.Constraint('Coincident', pitch_radius_line, 1, -1, 1))
	active_sketch.addConstraint(Sketcher.Constraint('Distance', pitch_radius_line, 1, pitch_radius_line, 2, pitch_radius))

	# mid tooth line
	active_sketch.addConstraint(Sketcher.Constraint('Coincident', mid_tooth_line, 1, -1, 1))
	# active.addConstraint(Sketcher.Constraint('Coincident', mid_tooth_line, 2, tooth_guide_curve, 1))
	active_sketch.addConstraint(Sketcher.Constraint('Angle', mid_tooth_line, 2, pitch_radius_line, 2, mh.deg_to_rads(360 / (num_teeth * 2))))
	active_sketch.addConstraint(Sketcher.Constraint('Distance', mid_tooth_line, 1, mid_tooth_line, 2, pitch_radius))

	# tooth flat
	# active.addConstraint(Sketcher.Constraint('Block', tooth_flat)) # TODO: remove this once tooth size is calculated
	active_sketch.addConstraint(Sketcher.Constraint('Coincident', tooth_flat, 3, -1, 1))
	active_sketch.addConstraint(Sketcher.Constraint('Coincident', tooth_flat, 2, outer_radius_line, 2))


	# small curve
	active_sketch.addConstraint(Sketcher.Constraint('Radius', tooth_small_curve, radius_small_arc))
	# active.addConstraint(Sketcher.Constraint('Coincident', tooth_flat, 1, tooth_small_curve, 2))
	active_sketch.addConstraint(Sketcher.Constraint('Tangent', tooth_flat, 1, tooth_small_curve, 2))

	# large curve
	active_sketch.addConstraint(Sketcher.Constraint('Radius', tooth_large_curve, radius_large_arc))
	active_sketch.addConstraint(Sketcher.Constraint('Tangent', tooth_large_curve, 1, tooth_small_curve, 1))
	active_sketch.addConstraint(Sketcher.Constraint('PointOnObject', tooth_large_curve, 3, mid_tooth_line))
	active_sketch.addConstraint(Sketcher.Constraint('PointOnObject', tooth_large_curve, 2, mid_tooth_line))
	active_sketch.addConstraint(Sketcher.Constraint('Distance', tooth_large_curve, 2, -1, 1, outer_radius - tooth_size))

	# symmetry
	mirror_large, mirror_small, mirror_flat = active_sketch.addSymmetric([tooth_large_curve, tooth_small_curve, tooth_flat], mid_tooth_line)

	small_edge_size = get_edge_size(active_doc, active_sketch, tooth_small_curve)
	large_edge_size = get_edge_size(active_doc, active_sketch, tooth_large_curve)

	if not _arc_too_big(small_edge_size, radius_small_arc) \
			and not _arc_too_big(large_edge_size, radius_large_arc):
		return True

	return False


def _arc_too_big(arc_edge, arc_radius):
	max_arc = 2 * pi * arc_radius * max_arc_percent
	if arc_edge < max_arc:
		return False
	return True


## MAIN ##
# Create the Gear Tooth
while True:
	gear_sketch, gear_doc = create_new_sketch()
	if create_htd_pulley(gear_doc, gear_sketch):
		break

	clean_up(gear_doc, gear_sketch)

# Polar array of the gear tooth
polar_array = create_polar_array(gear_sketch)

# Turn polar array into a new sketch
polar_sketch = Draft.makeSketch(polar_array, autoconstraints=True)
polar_sketch.Label = "gear_sketch_" + str(num_teeth) + "_teeth"

# Clean up things that aren't needed anymore
FreeCAD.getDocument(gear_doc.Name).removeObject(polar_array.Name)
FreeCAD.getDocument(gear_doc.Name).removeObject(gear_sketch.Name)

QtGui.QInputDialog.getText(None, "Get text", "Input:")[0]

FreeCAD.Console.PrintMessage("\nEnd\n")