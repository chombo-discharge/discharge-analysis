'''
This script lets VisIt generate a volume plot.
'''

dim          = 3
basename     = "simulation"
step         = 1250
directory    = "/home/robertm/Projects/chombo-discharge/Exec/Examples/ItoPlasma/plt"
do_eb        = True
do_volume    = True
dark_bg      = True
variable     = "Electron phi"

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
    ratts.specularCoeff = 0.6
    ratts.specularPower = 10
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
    batts.SetMultiColor(0, (200, 200, 200, 255))
    batts.SetMultiColor(1, (200, 200, 200, 255))
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
    print(vatts)

# Default things like view, annotation, render, slider, etc.
set_annotation()
set_render_attributes()

# Open the HDF5 file.
f = directory + "/" + basename + ".step" + str(step).rjust(7,'0') + "." + str(dim) + "d.hdf5"
OpenDatabase(f)

# Draw the EB and volume plot
if(do_eb):
    draw_boundaries()
if(do_volume):
    # Scaling because VisIt-OSPRay can't handle huge floating point numbers. Thanks to the VisIt
    # folks for not telling anyone about this.
    DefineScalarExpression("scaled_variable", "<" + variable + ">" + "* 1E-20")
    draw_volume("scaled_variable")

DrawPlots()

ResetView()
view = View3DAttributes()
view.focus      = (0.05, 0.05, 0.05)
view.viewUp     = (0, 0, 1)
view.viewNormal = (-0.5, 1, 0.1);
view.imageZoom  = 7.0
view.imagePan   = (0, 0.0)
SetView3D(view)

# Save plot
satts          = SaveWindowAttributes()
satts.family   = 0
satts.width    = 1024
satts.height   = 1024
satts.fileName = "volume_plot"
satts.outputToCurrentDirectory = 1
SetSaveWindowAttributes(satts)
SaveWindow()

# Close DB and exit.
DeleteAllPlots()
CloseDatabase(f)

exit()

