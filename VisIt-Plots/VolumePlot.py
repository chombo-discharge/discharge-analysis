'''
This script lets VisIt generate a volume plot.
'''

dim          = 3
basename     = "simulation"
step         = 1250
directory    = "/home/robertm/Projects/chombo-discharge/Exec/Examples/ItoPlasma/plt"
do_eb        = True
do_volume    = True

# For drawing the isosurface
variable  = "Electron phi"

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
    atts.legendInfoFlag         = 0
    atts.axes3D.triadFlag       = 0
    atts.axes3D.bboxFlag        = 1
    atts.backgroundColor        = (0,0,0,255)
    atts.foregroundColor        = (255,255,255,255)    
    SetAnnotationAttributes(atts)

def set_render_attributes():
    ''' 
    Set rendering attributes (like specular reflection) 
    '''
    
    ratts = RenderingAttributes()
    ratts.antialiasing  = 0
    ratts.specularFlag  = 1
    ratts.specularCoeff = 0.6
    ratts.specularPower = 10
    ratts.specularColor = (255, 255, 255, 255)
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

    silr = SILRestriction()
    silr.TurnOffAll();
    silr.TurnOnSet(0)
    silr.TurnOnSet(1)
    SetPlotSILRestriction(silr,0)    
    
    vatts = VolumeAttributes()
    vatts.legendFlag     = 0
    vatts.samplesPerRay  = 50
    vatts.rendererType   = vatts.RayCastingOSPRay
    vatts.useColorVarMin = 1
    vatts.useColorVarMax = 1
    vatts.colorVarMin    = 1E10
    vatts.colorVarMax    = 1E20
    vatts.scaling        = vatts.Linear    
    vatts.smoothData     = 1
    vatts.lightingFlag   = 1
    vatts.materialProperties = (0.1, 0.5, 0.05, 10)        
    vatts.opacityAttenuation = 1.0
    vatts.lowGradientLightingReduction = vatts.Medium

    # Monkey with opacity
    opacity = vatts.freeformOpacity
    y = list(opacity)
    for i in range(len(opacity)):
        y[i] = 254
    vatts.freeformOpacity = tuple(y)
    
    vatts.useOpacityVarMin = 0
    vatts.opacityVarMin=1E14
    vatts.useOpacityVarMax = 0
    vatts.opacityVarMin=1E20
    vatts.ospraySpp = 5
    vatts.osprayOneSidedLightingFlag = 0
    vatts.osprayMinContribution=0.0000
    vatts.ospraySingleShadeFlag=1
    vatts.osprayAoDistance=0.001
    vatts.osprayAoSamples=0
    vatts.osprayAoTransparencyEnabledFlag = 0
    
    print(vatts)
    SetPlotOptions(vatts)        

    AddOperator("Box")
    batts = BoxAttributes()
    batts.minx = 0.04
    batts.maxx = 0.06
    batts.miny = 0.04
    batts.maxy = 0.06
    batts.minz = 0.04
    batts.maxz = 0.052
    batts.amount = 0
    SetOperatorOptions(batts)    



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
    draw_volume(variable)

DrawPlots()

ResetView()
view = View3DAttributes()
view.focus      = (0.05, 0.05, 0.05)
view.viewUp     = (0, 0, 1)
view.viewNormal = (0, 1, 0);
view.imageZoom  = 40
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

