# Run this with
# Normal job:
# > salloc --account=nn9453k --time=12:00:00 --nodes=1 --qos=preproc
# 
# Bigmem job:
# > salloc --account=nn9453k --time=00:30:00 --nodes=2 --partition=bigmem --ntasks-per-node=32 --cpus-per-task=1 --mem-per-cpu=32G
#
# To execute:
# > visit -nn 1 -np 32 -cli -nowin -s multiscale.py
basename     = "15kv_pub_hiQuench"
directory    = "/cluster/work/users/marskar/nn9453k/air7_stephens/plt"
database     = "/cluster/work/users/marskar/nn9453k/air7_stephens/plt/15kv_pub_hiQuench.step*.3d.hdf5 database"
framename    = "frame"
firstframe   = 0
lastframe    = 27000
fidx         = 0
framestep    = 100
nclear_cache = 10
degrees_rot  = 360
rotation_inc = 1

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
    satts.width    = 2048
    satts.height   = 2048
    satts.fileName = str(prefix) + str(format(frame, "05d"))
    satts.outputDirectory = "../frames"
    SetSaveWindowAttributes(satts)

def set_default_view():
    ResetView()
    view            = GetView3D()
    view.focus      = (1.0E-2, 1.0E-2, 1.0E-2)
    view.viewUp     = (0, 0, 1)
    view.viewNormal = (0, 1, 0);
    view.imageZoom  = 2.3
    view.imagePan   = (0, 0)
    SetView3D(view)

def rotate_view(axis,angle):
    v = GetView3D()
    v.RotateAxis(axis, angle)
    SetView3D(v)

def set_annotation_attributes():
    atts = AnnotationAttributes()
    atts.databaseInfoTimeScale  = 1E9
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
    ratts.antialiasing  = 1
    ratts.specularFlag  = 1
#    ratts.specularCoeff = 0.3
#    ratts.specularPower = 5
#    ratts.specularColor = (255, 255, 255, 255)
#    ratts.scalableActivationMode = ratts.Always
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
    vatts.samplesPerRay  = 15000
    vatts.rendererType   = vatts.RayCasting
    vatts.useColorVarMin = 0
    vatts.useColorVarMax = 1
    vatts.colorVarMin    = 0.0
    vatts.colorVarMax    = 3.E20
    vatts.smoothData     = 1
    vatts.lightingFlag   = 1
    vatts.scaling        = vatts.Linear
    SetPlotOptions(vatts)

def set_bbox():
    AddOperator("Box")
    batts = BoxAttributes()
    batts.minx = 0.6E-2
    batts.maxx = 1.6E-2
    batts.miny = 0.6E-2
    batts.maxy = 1.6E-2
    batts.minz = 0.1E-2
    batts.maxz = 1.55E-2
    SetOperatorOptions(batts)

def set_rotate(degrees):
    AddOperator("Transform")
    t = TransformAttributes()
    t.doRotate     = 1
    t.rotateOrigin = (1E-2, 1E-2, 1E-2)
    t.rotateAmount = degrees
    SetOperatorOptions(t)

def set_timeSlider():
    slider = CreateAnnotationObject("TimeSlider")
    slider.text = "Time = $time ns"
    slider.shaded=0
    slider.timeFormatString = "%.2f"

# Set default settings
set_default_view()
set_annotation_attributes()
set_render_attributes()
set_timeSlider()

InvertBackgroundColor()

# Draw fixed view frames
for ts in range(firstframe, lastframe+framestep, framestep):
    DeleteAllPlots()
    f = directory + "/" + basename + ".step" + str(ts).rjust(7,'0') + ".3d.hdf5"
    OpenDatabase(f)
    
    # Set name
    set_framename(framename, fidx)

    # Boundary
    draw_boundary()
    turn_off_level(6)

    draw_volume()
    turn_off_level(6)

    set_bbox()
    set_rotate(1);

    # Draw and save
    DrawPlots()
    SaveWindow()

    # Clean up stuff
    DeleteAllPlots()
    CloseDatabase(f)
    ClearCacheForAllEngines()

    fidx += 1

# Do the rotation frames
f = directory + "/" + basename + ".step" + str(lastframe).rjust(7,'0') + ".3d.hdf5"
for rot in range(1+rotation_inc, degrees_rot + rotation_inc, rotation_inc):

    OpenDatabase(f)

    # Replot
    set_default_view()
    rotate_view(1, rot)
    draw_boundary()
    draw_volume()
    turn_off_level(6)
    set_bbox()
    set_rotate(1)

    # Set name
    set_framename(framename, fidx)

    # Draw and save
    DrawPlots()
    SaveWindow()
    DeleteAllPlots()
    ClearCacheForAllEngines()

    fidx += 1

    CloseDatabase(f)

exit()

