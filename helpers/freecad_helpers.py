import os
import sys
from time import sleep
from math import pi

import FreeCAD
import Part
import FreeCADGui as Gui
import Draft
from PySide import QtGui
import math_helpers as mh

# constants

max_arc_percent = 0.35

def update_drawing():
    FreeCAD.ActiveDocument.recompute()
    return


def get_working_dir():
    print(os.getcwd())
    return

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
    circle = active_sketch.addGeometry(Part.Circle(FreeCAD.Vector(0,0,0), FreeCAD.Vector(0,0,1), radius), is_construction)
    update_drawing()
    return circle


def draw_line(active_sketch, start, end, is_construction):
    print("hi\n")
    get_working_dir()
    line = active_sketch.addGeometry(Part.LineSegment(FreeCAD.Vector(start[0], start[1], 0), FreeCAD.Vector(end[0], end[1], 0)), is_construction)
    update_drawing()
    return line


def draw_arc(active_sketch, center, radius, start_deg, end_deg, is_construction):
    arc = active_sketch.addGeometry(Part.ArcOfCircle(Part.Circle(FreeCAD.Vector(center[0], center[1],0), FreeCAD.Vector(0,0,1), radius), mh.deg_to_rads(start_deg), mh.deg_to_rads(end_deg)), is_construction)
    update_drawing()
    return arc


def create_arc(active_sketch, is_construction, start_deg, end_deg):
    arc = active_sketch.addGeometry(Part.ArcOfCircle(Part.Circle(FreeCAD.Vector(0,0,0), FreeCAD.Vector(0,0,1), 1), mh.deg_to_rads(start_deg), mh.deg_to_rads(end_deg)), is_construction)
    return arc


def get_edge_size(active_doc, active_sketch, edge):
    edge_str = 'Edge' + str(int(edge)+1)
    Gui.Selection.addSelection(str(active_doc.Name), str(active_sketch.Name), edge_str)
    update_drawing()
    sleep(0.1)
    edge_size = Gui.Selection.getSelectionEx()[0].SubObjects[0].Length
    Gui.Selection.clearSelection()
    return edge_size

def create_polar_array(sketch, num_teeth):
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


def arc_too_big(arc_edge, arc_radius):
    max_arc = 2 * pi * arc_radius * max_arc_percent
    if arc_edge < max_arc:
        return False
    return True