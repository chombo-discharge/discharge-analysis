OpenDatabase("/cluster/work/users/marskar/nn9453k/rod3d_branch_1E15/simulation.step0000800.3d.hdf5")

InvertBackgroundColor()

DeleteAllPlots()

AddPlot("Boundary", "materials")
batts = BoundaryAttributes()
batts.legendFlag = 0
batts.colorType = batts.ColorByMultipleColors
batts.SetMultiColor(0, (123, 123, 123, 255))
batts.SetMultiColor(1, (123, 123, 123, 255))
SetPlotOptions(batts)

view = GetView3D()
view.focus = (1.35E-2, 1.35E-2, 1.675E-2)
view.viewUp = (0, 0, -1)
view.viewNormal = (0.5, 1, -0.5)
view.imageZoom = 20
SetView3D(view)

satts = SaveWindowAttributes()
satts.family = 0
satts.width = 1024
satts.height = 1024
satts.fileName = "test"
SetSaveWindowAttributes(satts)

AnnotationAtts = AnnotationAttributes()
AnnotationAtts.axes3D.visible = 0
AnnotationAtts.axes3D.setBBoxLocation = 0
AnnotationAtts.userInfoFlag = 0
AnnotationAtts.databaseInfoFlag = 0
AnnotationAtts.legendInfoFlag = 0
AnnotationAtts.axes3D.triadFlag = 0
AnnotationAtts.axes3D.bboxFlag = 0
SetAnnotationAttributes(AnnotationAtts)

RenderingAtts = RenderingAttributes()
RenderingAtts.antialiasing = 1
RenderingAtts.specularFlag = 1
RenderingAtts.specularCoeff = 0.5
RenderingAtts.specularPower = 10
RenderingAtts.specularColor = (255, 255, 255, 255)
SetRenderingAttributes(RenderingAtts)

AddPlot("Volume", "Space charge density")
AddOperator("Box")

vatts = VolumeAttributes()
vatts.legendFlag = 0
vatts.samplesPerRay = 700
vatts.rendererType = vatts.RayCasting
vatts.useColorVarMin = 1
vatts.useColorVarMax = 1
vatts.colorVarMin = 0
vatts.colorVarMax = 10
vatts.smoothData = 1
#vatts.scaling = vatts.Log
vatts.lightingFlag = 1

boxatts = BoxAttributes()
boxatts.minx = 1.1E-2
boxatts.maxx = 1.5E-2
boxatts.miny = 1.1E-2
boxatts.maxy = 1.5E-2
boxatts.minz = 1.6E-2
boxatts.maxz = 1.8E-2
SetOperatorOptions(boxatts)
SetPlotOptions(vatts)

# AddPlot("Mesh", "Mesh")
# AddOperator("Slice")
# sliceatts = SliceAttributes()
# sliceatts.originType = sliceatts.Point
# sliceatts.originPoint = (1.35E-2, 1.35E-2, 1.7E-2)
# sliceatts.project2d = 0
# SetOperatorOptions(sliceatts)

DrawPlots()
SaveWindow()
