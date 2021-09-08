import FreeCAD


def setup_test_env():
    FreeCAD.openDocument('/home/fidel/FreeCAD/testing_grounds.FCStd')


def get_active_sketch():
    return FreeCAD.getDocument(FreeCAD.ActiveDocument.Name).getObject(FreeCAD.ActiveDocument.ActiveObject.Name)


def draw_circle(active_sketch, radius: float, is_construction: bool):
    active_sketch.addGeometry(Part.Circle(App.Vector(0,0,0), App.Vector(0,0,1), radius), is_construction)
    update_drawing()


def update_drawing():
    App.ActiveDocument.recompute()

setup_test_env()
act = get_active_sketch()
print(act.Name)
draw_circle(act, 100.0, True)
update_drawing()