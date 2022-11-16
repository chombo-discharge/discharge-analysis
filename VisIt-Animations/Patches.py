'''
This script lets VisIt generate an animation of the current grid (for making a movie or GIF). 

This should work for 3D input data. 2D has not been tested (nor does it make any sense in the context of this script).
'''

dim          = 3
basename     = "simulation"
step         = 20
directory    = "/home/robertm/Projects/chombo-discharge/Exec/Examples/ItoPlasma/plt"
framename    = "patches"
do_eb        = True
do_grid      = True
do_iso       = True

# For drawing the isosurface
color_field  = "Electric field_magnitude"
slice_field  = "Electron phi"
slice_value  = 1.E18

stripCoord = "x"
prune_frames = 10
transition_frames = 10
minLevel = 1
maxLevel = 4
transLevel = 3

'''
Colors to use when plotting levels
'''
opacity = 220
level_colors = [(255,0,0,opacity),
                (0,255,0,opacity),
                (0,0,255,opacity),
                (125,125,0,opacity),
                (0,125,125,opacity),
                (125,0,125,opacity),
                (125,0,125,opacity),
                (125,0,125,opacity)]

# First view that we use
ResetView()
view1 = View3DAttributes()
view1.focus      = (0.05, 0.05, 0.05)
view1.viewUp     = (0, 0, 1)
view1.viewNormal = (-0.5, 1, 0.1);
view1.imageZoom  = 5.0
view1.imagePan   = (0, 0.0)

# Second view that we use
view2 = View3DAttributes()
view2.focus      = (0.05, 0.05, 0.04)
view2.viewUp     = (0, 0, 1)
view2.viewNormal = (-0.5, -0.5, 0.1);
view2.imageZoom  = 40.0
view2.imagePan   = (0, 0.0)

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
    satts.outputDirectory = "./Patches-frames"
    SetSaveWindowAttributes(satts)

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
    ratts.specularCoeff = 0.3
    ratts.specularPower = 5
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

def draw_patch_level(lvl):
    '''
    Draw AMR grid patches
    '''

    AddPlot("Subset", "patches")
    satts = SubsetAttributes()
    satts.colorType = 0
    satts.singleColor = level_colors[lvl]
    satts.wireframe = 0
    satts.legendFlag = 0
    satts.drawInternal = 0
    SetPlotOptions(satts)

    # Turn off everything except the input level. 
    silr = SILRestriction()
    silr.TurnOffAll();
    silr.TurnOnSet(lvl+1)
    SetPlotSILRestriction(silr,0)

def draw_grid_level(lvl):
    '''
    Draw AMR grid patch boundaries
    '''

    # Add plot subset
    AddPlot("Subset", "patches")
    satts = SubsetAttributes()
    satts.colorType = 0
    satts.singleColor = (123,123,123,255)
    satts.wireframe = 1
    satts.drawInternal = 1
    satts.legendFlag = 0
    SetPlotOptions(satts)

    # Turn off everything except the input level.
    silr = SILRestriction()
    silr.TurnOffAll();
    silr.TurnOnSet(lvl+1)
    SetPlotSILRestriction(silr,0)

def get_spatial_extensions(lvl):
    '''
    Get the spatial extensions of the input level
    '''
    
    AddPlot("Pseudocolor", color_field)
    silr = SILRestriction()
    silr.TurnOffAll();
    silr.TurnOnSet(lvl+1)
    SetPlotSILRestriction(silr,0)
    DrawPlots()
    Query('SpatialExtents', use_actual_data=1)
    SetActivePlots(GetNumPlots()-1)
    DeleteActivePlots()

    return GetQueryOutputValue()

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
    p.centering = 1
    p.smoothingLevel=1
    SetPlotOptions(p)

    # Slice by isosurface
    AddOperator("Isosurface");
    s = IsosurfaceAttributes()
    s.contourNLevels = 1
    s.variable = surface_variable
    s.minFlag = 1
    s.min = slice_val

    SetOperatorOptions(s)

# Default things like view, annotation, render, slider, etc.
set_annotation()
set_render_attributes()

# Open the HDF5 file.
f = directory + "/" + basename + ".step" + str(step).rjust(7,'0') + "." + str(dim) + "d.hdf5"
OpenDatabase(f)

# Draw the plots. This includes the EB, isosurface, and volume plot
if(do_eb):
    draw_boundaries()
if(do_iso):
    draw_isosurface(color_field, slice_field, slice_value)

prePlots = GetNumPlots()

# Now do the patch plots
for lvl in range(minLevel,maxLevel+1):

    draw_patch_level(lvl)
    if (do_grid):
        draw_grid_level(lvl)
        
        gridPlot  = GetNumPlots()-1
        patchPlot = gridPlot - 1
        SetActivePlots((patchPlot,gridPlot))

    AddOperator("Box")
    batts = BoxAttributes()
    batts.minx = -100
    batts.maxx = 100
    batts.miny = -100
    batts.maxy = 100
    batts.minz = -100
    batts.maxz = 100
    batts.amount = 0
    SetOperatorOptions(batts)

# Make frames using the first view. This removes level up to but not including transLevel
fidx = 0

for lvl in range(minLevel, transLevel, 1):
    # Get spatial extensions for the pruning on this level. 
    s = get_spatial_extensions(lvl)

    if(do_grid):
        patchPlot = prePlots + 2 * (lvl - minLevel)
        gridPlot  = patchPlot + 1

        SetActivePlots((patchPlot,gridPlot))
    else:
        SetActivePlots(prePlots + lvl - minLevel)
        
    for istep in range(0, prune_frames, 1):
        batts = GetOperatorOptions(0)
        if(stripCoord == "x"):
            batts.minx = s[0] + float(istep) * (s[1]-s[0])/float(prune_frames-1)
            batts.maxx = s[1]
        elif(stripCoord == "y"):
            batts.miny = s[2] + float(istep) * (s[3]-s[2])/float(prune_frames-1)
            batts.maxy = s[3]
        elif(stripCoord == "z"):
            batts.minz = s[4] + float(istep) * (s[5]-s[4])/float(prune_frames-1)
            batts.maxz = s[4]
        SetOperatorOptions(batts)

        # Draw and save
        DrawPlots()
        SetView3D(view1)        
        
        # Set name and save window
        set_output(framename, fidx)        
        SaveWindow()

        fidx += 1

    # Don't need these any longer.
    HideActivePlots()

# Gradually transition to second view on the transLevel.
for i in range(0, transition_frames):
    t = float(i) / float(transition_frames-1)
    v = EvalLinear(t, view1, view2)
    SetView3D(v)    
        
    # Set name and save window
    set_output(framename, fidx)        
    SaveWindow()

    fidx += 1

# Turn off the bounding box now
atts = GetAnnotationAttributes()
atts.axes3D.bboxFlag = 0
SetAnnotationAttributes(atts)    

# Strip off the remaining levels now
for lvl in range(transLevel, maxLevel+1, 1):
    s = get_spatial_extensions(lvl)

    if(do_grid):
        patchPlot = 2 + 2 * (lvl - minLevel)
        gridPlot  = patchPlot + 1

        SetActivePlots((patchPlot,gridPlot))
    else:
        SetActivePlots(2 + lvl - minLevel)
    
    for istep in range(0, prune_frames, 1):
        batts = GetOperatorOptions(0)
        if(stripCoord == "x"):
            batts.minx = s[0] + istep * (s[1]-s[0])/(prune_frames-1)
            batts.maxx = s[1]
        elif(stripCoord == "y"):
            batts.miny = s[2] + istep * (s[3]-s[2])/(prune_frames-1)
            batts.maxy = s[3]
        elif(stripCoord == "z"):
            batts.minz = s[4] + istep * (s[5]-s[4])/(prune_frames-1)
            batts.maxz = s[4]
        SetOperatorOptions(batts)

        # Draw and save
        DrawPlots()

        SetView3D(view2)        
        
        # Set name and save window
        set_output(framename, fidx)        
        SaveWindow()

        fidx += 1

    # Don't need this one anymore
    HideActivePlots()

# Close DB and exit.
DeleteAllPlots()
CloseDatabase(f)

exit()

