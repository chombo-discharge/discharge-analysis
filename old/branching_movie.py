# Run this with
# > salloc --account=nn9453k --time=02:00:00 --nodes=64
# > visit -nn 64 -np 2048 -cli -nowin -s branching_movie.py
basename     = "15kv_pub_hiQuench"
directory    = "/cluster/work/users/marskar/nn9453k/air7/stephens/plt"
database     = "/cluster/work/users/marskar/nn9453k/air7_stephens/plt/15kv_pub_hiQuench.step*.3d.hdf5 database"
framename    = "frame"
firstframe   = 1000
lastframe    = 1100
fidx         = 0
framestep    = 100
nclear_cache = 10
degrees_rot  = 720
rotation_inc = 10

def turn_off_level(L):
    silr = SILRestriction()
    silr.TurnOffSet(L)
    SetPlotSILRestriction(silr)

def turn_on_level(L):
    silr = SILRestriction()
    silr.TurnOnSet(L)
    SetPlotSILRestriction(silr)

def set_framename(prefix, frame):
    satts = SaveWindowAttributes()
    satts.family   = 0
    satts.width    = 1024
    satts.height   = 1024
    satts.fileName = str(prefix) + str(format(frame, "05d"))
    satts.outputDirectory = "../frames"
    SetSaveWindowAttributes(satts)

def set_default_view():
    ResetView()
    view = GetView3D()
    view.focus      = (1.0E-2, 1.0E-2, 1.0E-2)
    view.viewUp     = (0, 0, 1)
    view.viewNormal = (0.25, 1, 0);
    view.imageZoom  = 1.0
    SetView3D(view)

def rotate_view(axis,angle):
    v = GetView3D()
    v.RotateAxis(axis, angle)
    SetView3D(v)

def set_annotation_attributes():
    atts = AnnotationAttributes()
    atts.axes2D.visible         = 0
    atts.axes3D.visible         = 0
    atts.axes3D.setBBoxLocation = 0
    atts.userInfoFlag           = 0
    atts.databaseInfoFlag       = 0
    atts.legendInfoFlag         = 0
    atts.axes3D.triadFlag       = 0
    atts.axes3D.bboxFlag        = 0
    SetAnnotationAttributes(atts)

def set_render_attributes():
    ratts = RenderingAttributes()
    ratts.antialiasing  = 0
    ratts.specularFlag  = 1
    ratts.specularCoeff = 0.5
    ratts.specularPower = 10
    ratts.specularColor = (255, 255, 255, 255)
    ratts.scalableActivationMode = ratts.Always
    SetRenderingAttributes(ratts)

def draw_boundary():
    AddPlot("Boundary", "materials")
    batts = BoundaryAttributes()
    batts.legendFlag = 0
    batts.colorType  = batts.ColorByMultipleColors
    batts.SetMultiColor(0, (123, 123, 123, 255))
    batts.SetMultiColor(1, (123, 123, 123, 255))
    SetPlotOptions(batts)

def draw_volume():
    AddPlot("Volume", "electron phi")
    vatts = VolumeAttributes()
    vatts.legendFlag     = 0
    vatts.samplesPerRay  = 50
    vatts.rendererType   = vatts.RayCasting
    vatts.useColorVarMin = 1
    vatts.useColorVarMax = 1
    vatts.colorVarMin    = 0.0
    vatts.colorVarMax    = 1.E20
    vatts.smoothData     = 0
    vatts.lightingFlag   = 0
    vatts.scaling        = vatts.Linear
    SetPlotOptions(vatts)

def set_bbox():
    AddOperator("Box")
    batts = BoxAttributes()
    batts.minx = 0.6E-2
    batts.maxx = 1.4E-2
    batts.miny = 0.6E-2
    batts.maxy = 1.4E-2
    batts.minz = 0.2E-2
    batts.maxz = 1.6E-2
    SetOperatorOptions(batts)

# Open database    
OpenDatabase(database, 0)

# Get number of states
nts    = TimeSliderGetNStates()
fidx   = 0

# Draw boundary
draw_boundary()
turn_off_level(6)
turn_off_level(5)
turn_off_level(4)

# Draw volume
# draw_volume()
# turn_off_level(6)
# turn_off_level(5)
# turn_off_level(4)
# set_bbox()

# Draw plots
DrawPlots()

# Set view and attributes
set_default_view()
set_annotation_attributes()
set_render_attributes()
InvertBackgroundColor()

# Draw fixed view frames
for ts in range(firstframe, nts, framestep):
    print "doing ts = ", ts, "fidx = ", fidx
    # Save frame
    TimeSliderSetState(ts)
    set_framename(framename, fidx)
    SaveWindow()
    fidx += 1
    if fidx % nclear_cache == 0:
        ClearCacheForAllEngines() # Clear cache every 10

print "fidx after linear frames = ", fidx

# Draw ''rotation'' frames around the z-axis
# for deg in range(rotation_inc, degrees_rot + rotation_inc, rotation_inc):
#     set_default_view()
#     rotate_view(1,deg)
#     set_framename(framename, fidx)
#     SaveWindow()
#     fidx += 1

# print "fidx after first rotation = ", fidx

# # Tilt the camera
# for deg in range(rotation_inc, degrees_rot + rotation_inc, rotation_inc):
#     rotate_view(0,deg)
#     set_framename(framename, fidx)
#     SaveWindow()
#     fidx += 1

# print "fidx after last rotation = ", fidx

# exit()


# AddPlot("Volume", "Space charge density")
# AddOperator("Box")

# vatts = VolumeAttributes()
# vatts.legendFlag = 0
# vatts.samplesPerRay = 700
# vatts.rendererType = vatts.RayCasting
# vatts.useColorVarMin = 1
# vatts.useColorVarMax = 1
# vatts.colorVarMin = 0
# vatts.colorVarMax = 10
# vatts.smoothData = 1
# #vatts.scaling = vatts.Log
# vatts.lightingFlag = 1

# boxatts = BoxAttributes()
# boxatts.minx = 1.1E-2
# boxatts.maxx = 1.5E-2
# boxatts.miny = 1.1E-2
# boxatts.maxy = 1.5E-2
# boxatts.minz = 1.6E-2
# boxatts.maxz = 1.8E-2
# SetOperatorOptions(boxatts)
# SetPlotOptions(vatts)

# AddPlot("Mesh", "Mesh")
# AddOperator("Slice")
# sliceatts = SliceAttributes()
# sliceatts.originType = sliceatts.Point
# sliceatts.originPoint = (1.35E-2, 1.35E-2, 1.7E-2)
# sliceatts.project2d = 0
# SetOperatorOptions(sliceatts)

