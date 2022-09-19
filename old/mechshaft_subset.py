OpenDatabase("/cluster/work/users/marskar/nn9453k/shaft3d_low_pressure2/simulation.step0000400.3d.hdf5")

InvertBackgroundColor()

DeleteAllPlots()

AddPlot("Boundary", "materials")
AddOperator("Cylinder")
batts = BoundaryAttributes()
batts.legendFlag = 0
batts.colorType = batts.ColorByMultipleColors
batts.SetMultiColor(0, (255, 0, 0, 255))
batts.SetMultiColor(1, (176, 176, 176, 255))

cylatts = CylinderAttributes()
cylatts.point1 = (2E-2, 2E-2, -1)
cylatts.point2 = (2E-2, 2E-2, 1)
cylatts.radius = 5.5E-3
SetPlotOptions(batts)
SetOperatorOptions(cylatts)
DrawPlots()


AddPlot("Boundary", "materials")
AddOperator("Cylinder")
batts = BoundaryAttributes()
batts.legendFlag = 0
batts.colorType = batts.ColorByMultipleColors
batts.SetMultiColor(0, (123, 123, 123, 255))
batts.SetMultiColor(1, (123, 123, 123, 255))

cylatts = CylinderAttributes()
cylatts.point1 = (2E-2, 2E-2, -1)
cylatts.point2 = (2E-2, 2E-2, 1)
cylatts.radius = 5.5E-3
cylatts.inverse = 1
SetPlotOptions(batts)
SetOperatorOptions(cylatts)
DrawPlots()

AddPlot("Subset", "levels")
subatts = SubsetAttributes()
subatts.singleColor = (0, 0, 0, 255)
subatts.SetMultiColor(0, (255, 0, 0, 0))
subatts.SetMultiColor(1, (0, 255, 0, 0))
subatts.SetMultiColor(2, (0, 0, 255, 0))
subatts.SetMultiColor(3, (0, 255, 255, 0))
subatts.SetMultiColor(4, (0, 255, 0, 0))
subatts.SetMultiColor(5, (138, 43, 226, 128))
subatts.legendFlag = 0
subatts.drawInternal = 1
SetPlotOptions(subatts)
DrawPlots()

view = GetView3D()
view.viewNormal = (-0.5, 0.25, -0.5)
view.focus = (2.E-2, 2.E-2, 3.E-2)
view.viewUp = (0, 1, 0)
view.imageZoom = 2.3
SetView3D(view)

satts = SaveWindowAttributes()
satts.family = 0
satts.width = 1024
satts.height = 1024
satts.fileName = "subset"
SetSaveWindowAttributes(satts)

AnnotationAtts = AnnotationAttributes()
AnnotationAtts.axes3D.visible = 0
AnnotationAtts.axes3D.setBBoxLocation = 0
AnnotationAtts.userInfoFlag = 0
AnnotationAtts.databaseInfoFlag = 0
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

DrawPlots()
SaveWindow()
