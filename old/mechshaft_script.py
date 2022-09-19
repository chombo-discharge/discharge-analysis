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
satts.fileName = "test"
SetSaveWindowAttributes(satts)

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

AddPlot("Volume", "Space charge density")
AddOperator("Box")

vatts = VolumeAttributes()
vatts.legendFlag = 1
vatts.samplesPerRay = 1000
vatts.rendererType = vatts.RayCasting
vatts.useColorVarMin = 1
vatts.useColorVarMax = 1
vatts.colorVarMin = 0
vatts.colorVarMax = 1
vatts.smoothData = 1
#vatts.scaling = vatts.Log
vatts.lightingFlag = 0

objatts = GetAnnotationObject("Plot0002")
objatts.numberFormat = "%# -9.2G"
objatts.fontFamily = objatts.Times  # Arial, Courier, Times
objatts.fontHeight = 0.05
objatts.drawTitle = 0
objatts.drawMinMax = 0

boxatts = BoxAttributes()
boxatts.minx = 0.5E-2
boxatts.maxx = 3.5E-2
boxatts.miny = 0.5E-2
boxatts.maxy = 3.5E-2
boxatts.minz = 2.7E-2
boxatts.maxz = 3.1E-2
SetOperatorOptions(boxatts)
SetPlotOptions(vatts)

DrawPlots()
SaveWindow()
