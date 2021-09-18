import os
import sys
from math import pi
from time import sleep

import FreeCAD
import Part
import FreeCADGui as Gui
import Draft
from PySide import QtGui

import importlib

source_dir = os.path.dirname(__file__)
helper_dir = os.path.join(source_dir, 'helpers')
sys.path
sys.path.append(helper_dir)

import helpers.math_helpers as mh
import helpers.freecad_helpers as fh
importlib.reload(fh)

# constants
# TODO: have num teeth given as an input
# TODO: have constants defined by HTD 3M/5M/8M etc. possibly from a reference file
radius_small_arc = 0.43
radius_large_arc = 1.49
tooth_size = 2.06



# main functions
def create_htd_pulley_tooth(active_doc, active_sketch, num_teeth, pitch):

	# math vars
	pitch_radius = mh.pitch_diameter(num_teeth, pitch) / 2
	outer_radius = mh.outside_diameter(pitch_radius * 2) / 2

	# drawing
	outer_radius_line = fh.draw_line(active_sketch, (0, 0), (25, outer_radius), True)
	pitch_radius_line = fh.draw_line(active_sketch, (0, 0), (25, pitch_radius), True)
	mid_tooth_line = fh.draw_line(active_sketch, (0, 0), (25, pitch_radius), True)
	tooth_flat = fh.draw_arc(active_sketch, App.Vector(0, 0, 0), outer_radius, 85, 90, False)
	tooth_small_curve = fh.create_arc(active_sketch, False, 20, 90)
	tooth_large_curve = fh.create_arc(active_sketch, False, -210, -90)

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

	small_edge_size = fh.get_edge_size(active_doc, active_sketch, tooth_small_curve)
	large_edge_size = fh.get_edge_size(active_doc, active_sketch, tooth_large_curve)

	if not fh.arc_too_big(small_edge_size, radius_small_arc) \
			and not fh.arc_too_big(large_edge_size, radius_large_arc):
		return True

	return False
def get_user_inputs():
	# Get user inputs for settings
	input_teeth = QtGui.QInputDialog.getInt(None, "Get Teeth", "Number of Teeth:", value=12)
	input_pitch = QtGui.QInputDialog.getInt(None, "Get Pitch", "Pitch (mm):", value=5)

	if input_teeth[1] is False or input_pitch[1] is False:
		FreeCAD.Console.PrintMessage("ERROR: User Cancelled Operation\n")
		raise Exception("User Cancelled Operation")
	else:
		num_teeth = input_teeth[0]
		pitch = input_pitch[0]

	return num_teeth, pitch


def create_gear_tooth(num_teeth, pitch):
	while True:
		sketch, doc = fh.create_new_sketch()
		if create_htd_pulley_tooth(doc, sketch, num_teeth, pitch):
			break

		fh.clean_up(doc, sketch)

	return doc, sketch


def gear_tooth_revolve(doc, sketch, teeth):
	# Polar array of the gear tooth
	polar_array = fh.create_polar_array(sketch, teeth)

	# Turn polar array into a new sketch
	polar_sketch = Draft.makeSketch(polar_array, autoconstraints=True)
	polar_sketch.Label = "gear_sketch_" + str(teeth) + "_teeth"

	FreeCAD.getDocument(doc.Name).removeObject(polar_array.Name)


def main():
	# inputs
	num_teeth, pitch = get_user_inputs()

	# create gear
	gear_doc, tooth_sketch = create_gear_tooth(num_teeth, pitch)
	gear_tooth_revolve(gear_doc, tooth_sketch, num_teeth)

	# clean up
	FreeCAD.getDocument(gear_doc.Name).removeObject(tooth_sketch.Name)

	# end
	FreeCAD.Console.PrintMessage("End\n")

if __name__ == "__main__":
	main()