'''
This script lets VisIt generate frames of an isosurface (for making a movie or GIF).

Parameters:
dim         (int)    : Dimension
basename    (string) : Plot file name prefix
directory   (string) : Path to plot files
framename   (string) : Prefix for frame names
variable    (string) : Variable to plot
firstframe  (int)    : First plot file to use
lastframe   (int)    : Last plot file to use
framestep   (int)    : Increment between plot files
'''

import os



dim          = 3
basename     = "simulation"
directory    = "/home/robertm/Projects/chombo-discharge/Exec/Examples/ItoPlasma/plt"
framename    = "frame"
variable     = "Electron phi"
firstframe   = 0
lastframe    = 20
framestep    = 1
do_volume    = True
do_eb        = True
dark_bg      = True
outdir       = "Volume-frames"

if not os.path.exists(outdir):
    os.mkdir(outdir)

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
    satts.width    = 2048
    satts.height   = 1024
    satts.fileName = str(prefix) + str(format(frame, "05d"))
    satts.outputToCurrentDirectory = 0
    satts.outputDirectory = "./Volume-frames"
    SetSaveWindowAttributes(satts)

def set_view():
    '''
    Set the default view.
    '''
    
    ResetView()
    view            = GetView3D()
    view.focus      = (0.05, 0.05, 0.05)
    view.viewUp     = (0, 0, 1)
    view.viewNormal = (-0.5, 1, 0.1);
    view.imageZoom  = 7.0
    view.imagePan   = (0, 0.0)    
    SetView3D(view)

def set_annotation():
    '''
    Set annotation attributes
    '''
    
    atts = AnnotationAttributes()
    atts.databaseInfoTimeScale  = 1E9
    atts.axes2D.visible         = 0
    atts.axes3D.visible         = 1
    atts.axes3D.setBBoxLocation = 0
    atts.userInfoFlag           = 0
    atts.databaseInfoFlag       = 1
    atts.legendInfoFlag         = 1
    atts.axes3D.triadFlag       = 1
    atts.axes3D.bboxFlag        = 1

    if(dark_bg):
        atts.backgroundColor = (0,0,0,255)
        atts.foregroundColor = (255,255,255,255)    
    
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

def draw_volume(var):
    AddPlot("Volume", var)

    # For turning off levels
    # silr = SILRestriction()
    # silr.TurnOffSet(5);   
    # silr.TurnOffSet(6);
    # SetPlotSILRestriction(silr,0)    

    vatts = VolumeAttributes()
    vatts.legendFlag     = 0
    vatts.samplesPerRay  = 5000
    vatts.rendererType   = vatts.RayCastingOSPRay
    vatts.useColorVarMin = 1
    vatts.useColorVarMax = 1
    vatts.colorVarMin    = 0.0
    vatts.colorVarMax    = 1.0
    vatts.scaling        = vatts.Linear
    vatts.smoothData     = 1
    vatts.lightingFlag   = 1
    vatts.materialProperties = (0.8, 0.8, 0.05, 30)        
    vatts.opacityAttenuation = 0.5
    vatts.lowGradientLightingReduction = vatts.Lower
    vatts.rendererSamples = 2
    vatts.gradientType = 1

    # Monkey with opacity
    # opacity = vatts.freeformOpacity
    # y = list(opacity)
    # for i in range(1,len(opacity)):
    #     y[i] = 250
    # vatts.freeformOpacity = tuple(y)

    vatts.ospraySpp = 1
    vatts.osprayMinContribution=0.0001
    vatts.osprayAoDistance=0.01
    vatts.osprayAoSamples=5
    vatts.osprayOneSidedLightingFlag = 1
    vatts.ospraySingleShadeFlag=0
    vatts.osprayAoTransparencyEnabledFlag = 1
    vatts.osprayShadowsEnabledFlag = 0
    vatts.osprayUseGridAcceleratorFlag = 0
    
    SetPlotOptions(vatts)
    
def set_slider():
    ''' 
    Set time slider
    '''
    slider = CreateAnnotationObject("TimeSlider")
    slider.text = "Time = $time ns"
    slider.shaded=0
    slider.timeFormatString = "%.2f"
    slider.startColor = (0, 255, 255, 0)
    slider.endColor = (255, 255, 255, 0)    
    print(slider)

# Default things like view, annotation, render, slider, etc. 
set_view()
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
    if(do_eb):
        draw_boundaries()
    if(do_volume):
        DefineScalarExpression("scaled_variable", "<" + variable + ">" + "* 1E-20")
        draw_volume("scaled_variable")    

    # Draw and save
    DrawPlots()

    # Modify the label if there is one. 
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

