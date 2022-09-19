OpenDatabase("/cluster/work/users/marskar/nn9453k/shaft3d_low_pressure3/simulation.step0000000.3d.hdf5")

DeleteAllPlots()

view = GetView3D()
view.viewNormal = (-0.5, 0.25, -0.5)
view.focus = (2.E-2, 2.E-2, 2.E-2)
view.viewUp = (0, 1, 0)
view.imageZoom = 1.5
SetView3D(view)

satts = SaveWindowAttributes()
satts.family = 0
satts.width = 1024
satts.height = 1024
satts.fileName = "mechshaft_charge"
SetSaveWindowAttributes(satts)

AnnotationAtts = AnnotationAttributes()
AnnotationAtts.axes3D.visible = 0
AnnotationAtts.axes3D.setBBoxLocation = 0
AnnotationAtts.userInfoFlag = 1
AnnotationAtts.databaseInfoFlag = 1
AnnotationAtts.legendInfoFlag = 1
AnnotationAtts.axes3D.triadFlag = 0
AnnotationAtts.axes3D.bboxFlag = 0
SetAnnotationAttributes(AnnotationAtts)

RenderingAtts = RenderingAttributes()
RenderingAtts.antialiasing = 0
RenderingAtts.specularFlag = 1
RenderingAtts.specularCoeff = 1.5
RenderingAtts.specularPower = 5.0
RenderingAtts.specularColor = (255, 255, 255, 255)
SetRenderingAttributes(RenderingAtts)

AddPlot("Pseudocolor", "Electric field_magnitude")
patts=PseudocolorAttributes()
patts.minFlag=0
patts.maxFlag=0
patts.min=0.0
patts.max=1.E-9
SetPlotOptions(patts)

AddOperator("BoundaryOp")
DrawPlots()

objatts = GetAnnotationObject("Plot0000")
objatts.numberFormat = "%# -9.2G"
objatts.fontFamily = objatts.Times  # Arial, Courier, Times
objatts.fontHeight = 0.05
objatts.drawTitle = 0
objatts.drawMinMax = 0


SaveWindow()
