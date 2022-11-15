# Run this with
#
# Normal job:
# -----------
# > salloc --account=nn9453k --time=3:00:00 --nodes=4
# > visit -nn 4 -np 128 -cli -nowin -s electrons.py
#
# Devel job:
# -----------
# > salloc --account=nn9453k --time=0:30:00 --nodes=4 --qos=devel
# > visit -nn 4 -np 128 -cli -nowin -s electrons.py
#
# Preproc job:
# -----------
# > salloc --account=nn9453k --time=0:30:00 --nodes=1 --qos=preproc
# > visit -nn 1 -np 32 -cli -nowin -s electrons.py
#

dim          = 3
basename     = "simulation"
directory    = "/home/robertm/Projects/chombo-discharge/Exec/Examples/ItoPlasma/plt"
framename    = "electrons"
color_field  = "Electric field_magnitude"
slice_field  = "Electron phi"
slice_value  = 1.E10
firstframe   = 0
lastframe    = 20
framestep    = 1

def turn_off_level(L):
    ''' 
    Turn off a mesh level 

    Parameters: 
    L (int): Level to turn off

    '''
    silr = SILRestriction()
    silr.TurnOffSet(L)
    SetPlotSILRestriction(silr)

def turn_on_level(L):
    ''' 
    Turn on a mesh level 

    Parameters: 
    L (int): Level to turn on

    '''    
    silr = SILRestriction()
    silr.TurnOnSet(L)
    SetPlotSILRestriction(silr)

def set_output(prefix, frame):
    '''
    Set save window attributes. Sets save file name as prefix<frame>.png

    Parameters:
    prefix (string): File name prefix
    frame  (int)   : Frame number
    '''
    satts          = SaveWindowAttributes()
    satts.family   = 0
    satts.width    = 1024
    satts.height   = 1024
    satts.fileName = str(prefix) + str(format(frame, "05d"))
    satts.outputToCurrentDirectory = 0
    satts.outputDirectory = "./Isosurface-frames"
    SetSaveWindowAttributes(satts)

def set_default_view():
    '''
    Set the default view.
    '''
    
    ResetView()
    view            = GetView3D()
    view.focus      = (1.0E-2, 1.0E-2, 1.0E-2)
    view.viewUp     = (0, 0, 1)
    view.viewNormal = (0, 1, 0);
    view.imageZoom  = 2.3
    view.imagePan   = (0, 0)
    SetView3D(view)

def set_annotation():
    '''
    Set annotation attributes
    '''
    
    atts = AnnotationAttributes()
    atts.databaseInfoTimeScale  = 1E9
    atts.axes2D.visible         = 0
    atts.axes3D.visible         = 0
    atts.axes3D.setBBoxLocation = 0
    atts.userInfoFlag           = 0
    atts.databaseInfoFlag       = 0
    atts.legendInfoFlag         = 1
    atts.axes3D.triadFlag       = 0
    atts.axes3D.bboxFlag        = 0
    
    SetAnnotationAttributes(atts)

def set_render_attributes():
    ''' 
    Set rendering attributes (like specular reflection) 
    '''
    
    ratts = RenderingAttributes()
    ratts.antialiasing  = 1
    ratts.specularFlag  = 1
    ratts.specularCoeff = 0.3
    ratts.specularPower = 5
    ratts.specularColor = (255, 255, 255, 255)
    ratts.scalableActivationMode = ratts.Always
    
    SetRenderingAttributes(ratts)

def draw_boundaries():
    '''
    Draw material surfaces
    '''
    
    AddPlot("Boundary", "materials")
    batts = BoundaryAttributes()
    batts.legendFlag = 0
    batts.colorType  = batts.ColorByMultipleColors
    batts.SetMultiColor(0, (123, 123, 123, 255))
    batts.SetMultiColor(1, (123, 123, 123, 255))
    
    SetPlotOptions(batts)

def draw_isosurface(color_variable, surface_variable, slice_val):
    ''' 
    Draw an isosurface plot of the input variable

    Parameters: 
    color_variable   (string): Variable to plot
    surface_variable (string): Variable to slice by
    slice_val        (float) : Isosurface value
    '''

    # Add pseudocolor plot
    AddPlot("Pseudocolor", color_variable)
    p = PseudocolorAttributes()
    p.min, p.minFlag = 0.0, 1
    p.max, p.maxFlag = 1E7, 1
    p.legendFlag = 0
    SetPlotOptions(p)

    # Slice by isosurface
    AddOperator("Isosurface");
    s = IsosurfaceAttributes()
    s.contourNLevels = 1
    s.variable       = surface_variable
    s.contourValue   = slice_val
    
    SetOperatorOptions(s)

    
def set_slider():
    ''' Set time slider '''
    slider = CreateAnnotationObject("TimeSlider")
    slider.text = "Time = $time ns"
    slider.shaded=0
    slider.timeFormatString = "%.2f"

# Default things like view, annotation, render, slider, etc. 
set_default_view()
set_annotation()
set_render_attributes()
set_slider()

# Draw fixed view frames
fidx = 0
for ts in range(firstframe, lastframe+framestep, framestep):

    # Open the data base. 
    DeleteAllPlots()
    f = directory + "/" + basename + ".step" + str(ts).rjust(7,'0') + "." + str(dim) + "d.hdf5"
    OpenDatabase(f)
    
    # Set name
    set_output(framename, fidx)

    # Boundary
    draw_boundaries()
    draw_isosurface(color_field, slice_field, slice_value)

    # Draw and save
    DrawPlots()

    # Modify the label.
    isoPlot  = GetAnnotationObjectNames()[2]
    isoAnnot = GetAnnotationObject(isoPlot)
    isoAnnot.drawMinMax = 0
    isoAnnot.drawTitle = 0
    isoAnnot.fontFamily = 2
    isoAnnot.fontHeight = 0.03
    isoAnnot.fontBold = 1
    isoAnnot.numberFormat = "%# -7.2G"
    isoAnnot.active = 0

    # Save window.
    SaveWindow()

    # Clean up stuff
    DeleteAllPlots()
    CloseDatabase(f)
    ClearCacheForAllEngines()

    # Go to next frame. 
    fidx += 1

exit()

