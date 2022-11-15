'''
This script lets VisIt generate an animation of the current grid (for making a movie or GIF). 

This should work for 3D input data. 2D has not been tested (nor does it make any sense in the context of this script).
'''

dim          = 3
basename     = "simulation"
step         = 20
directory    = "/home/robertm/Projects/chombo-discharge/Exec/Examples/ItoPlasma/plt"
framename    = "patches"
minLevel     = 1
maxLevel     = 4
dmin         = 0.0
dmax         = 0.08
stripCoord   = "x"
nsteps       = 5

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

def set_default_view():
    '''
    Set the default view.
    '''
    
    ResetView()
    view            = GetView3D()
    view.focus      = (0.05, 0.05, 0.05)
    view.viewUp     = (0, 0, 1)
    view.viewNormal = (-0.5, 1, 0);
    view.imageZoom  = 1
    view.imagePan   = (0, 0.00)
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

def set_box(xmin, xmax, ymin, ymax, zmin, zmax):
    '''
    Add a box operator to the input operator. 
    '''
    AddOperator("Box")
    batts = BoxAttributes()
    batts.minx = xmin
    batts.maxx = xmax
    batts.miny = ymin
    batts.maxy = ymax
    batts.minz = zmin
    batts.maxz = zmax
    SetOperatorOptions(batts)    

def draw_patches(lvl):
    '''
    Draw AMR grid patches
    '''

    AddPlot("Subset", "patches")
    satts = SubsetAttributes()
    satts.colorType = 0
    satts.singleColor = (255, 0.0, 0.0, 255)
    satts.wireframe = 0
    SetPlotOptions(satts)

    # Turn off everything except the input level. 
    silr = SILRestriction()
    for l in range(0, maxLevel+1, 1):
        silr.TurnOffSet(l)
    silr.TurnOnSet(l)
    SetPlotSILRestriction(silr)

def draw_patches2(lvl):
    '''
    Draw AMR grid patches
    '''

    AddPlot("Subset", "patches")
    satts = SubsetAttributes()
    satts.colorType = 0
    satts.singleColor = (0, 255, 0.0, 255)
    satts.wireframe = 0
    SetPlotOptions(satts)

    # Turn off everything except the input level. 
    silr = SILRestriction()
    for l in range(0, maxLevel+1, 1):
        if(l != lvl):
            silr.TurnOffSet(l)
    SetPlotSILRestriction(silr)        

def draw_grid(lvl):
    '''
    Draw AMR grid patch boundaries
    '''

    # Add plot subset
    AddPlot("Subset", "patches")
    satts = SubsetAttributes()
    satts.colorType = 0
    satts.singleColor = (0, 0, 0, 255)
    satts.wireframe = 1
    SetPlotOptions(satts)

    # Turn off everything except the input level. 
    silr = SILRestriction()
    for l in range(0, maxLevel+1, 1):
        if(l != lvl):
            silr.TurnOffSet(l)
    SetPlotSILRestriction(silr)        

# Default things like view, annotation, render, slider, etc. 
set_default_view()
set_annotation()
set_render_attributes()

# Level loop -- we will "remove" a section of 
fidx = 0
for stripLevel in range(minLevel, maxLevel+1, 1):
    for istep in range(0, nsteps, 1):
        # Open the data base. 
        DeleteAllPlots()
        f = directory + "/" + basename + ".step" + str(step).rjust(7,'0') + "." + str(dim) + "d.hdf5"
        OpenDatabase(f)
    
        # Set name
        set_output(framename, fidx)

        # Draw embedded boundary
        draw_boundaries()

        # Determine the subset box
        xmin = -100.
        xmax =  100.
        ymin = -100.
        ymax =  100.
        zmin = -100.
        zmax =  100.
        
        if(stripCoord == "x"):
            xmin = dmin + istep * (dmax-dmin)/(nsteps-1)
            xmax = dmax
        elif(stripCoord == "y"):
            ymin = dmin + istep * (dmax-dmin)/(nsteps-1)
            ymax = dmax
        elif(stripCoord == "z"):
            zmin = dmin + istep * (dmax-dmin)/(nsteps-1)
            zmax = dmax
            
        # Draw finer-level grid patches.
        # for l in range(maxLevel, stripLevel, -1):
        #     draw_patches(l)
        #     draw_grid(l);

        # Draw patches and grids on this level. 
        draw_patches(stripLevel)
        set_box(xmin, xmax, ymin, ymax, zmin, zmax)

        # draw_grid(stripLevel)
        # set_box(xmin, xmax, ymin, ymax, zmin, zmax)

        # # Add in all the other patches
        # for otherLevel in range(stripLevel+1, maxLevel+1, 1):
        #     draw_patches2(otherLevel)
        #     draw_grid(otherLevel)            

        # for l in range(minLevel, maxLevel, 1):
        #     draw_grid(l)
        #     if(l == stripLevel):
        #         set_box(xmin, xmax, ymin, ymax, zmin, zmax)    
        
        # Draw and save
        DrawPlots()
        
        # Save window.
        SaveWindow()

        # Clean up stuff
        DeleteAllPlots()
        CloseDatabase(f)
        ClearCacheForAllEngines()

        # Go to next frame. 
        fidx += 1

exit()

