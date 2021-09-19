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

pitch_map = {
	3: "3M",
	5: "5M"
}

source_dir = os.path.dirname(__file__)
helper_dir = os.path.join(source_dir, 'helpers')
sys.path
sys.path.append(helper_dir)

import helpers.math_helpers as mh
import helpers.freecad_helpers as fh
importlib.reload(fh)
import helpers.htd as htd
importlib.reload(htd)


# main functions
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


def main():
	# inputs
	num_teeth, pitch = get_user_inputs()

	# create pulley object
	gear = htd.HTD(pitch_map[pitch], pitch, num_teeth)

	# create gear
	gear.create_gear()

	# end
	FreeCAD.Console.PrintMessage("End\n")

if __name__ == "__main__":
	main()