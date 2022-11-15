'''
This script lets VisIt generate an animation of the current grid (for making a movie or GIF). 

This should work for 3D input data. 2D has not been tested (nor does it make any sense in the context of this script).
'''

dim          = 3
basename     = "simulation"
step         = 20
directory    = "/home/robertm/Projects/chombo-discharge/Exec/Examples/ItoPlasma/plt"
framename    = "patches"

stripCoord   = "x"
nsteps       = 11
zoom1        = 1.0
zoom2        = 5.0
nzooms       = 10

level_colors = [(255,0,0,255),
                (0,255,0,255),
                (0,0,255,255),
                (125,125,0,255),
                (0,125,125,255),
                (125,0,125,255)]

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
    view.viewNormal = (-0.5, 1, 0.1);
    view.imageZoom  = zoom1
    view.imagePan   = (0, 0.00)
    SetView3D(view)

def set_zoom(zoom):
    '''
    Zoom 
    '''
    view = GetView3D()
    view.imageZoom = zoom
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
    batts.amount = 0
    SetOperatorOptions(batts)    

def draw_patches(lvl):
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
    satts.drawInternal = 1
    satts.legendFlag = 0
    SetPlotOptions(satts)

    # Turn off everything except the input level.
    silr = SILRestriction()
    silr.TurnOffAll();
    silr.TurnOnSet(lvl+1)
    SetPlotSILRestriction(silr,0)

def make_frames(frame_index, minLevel, maxLevel):
    ''' 
    Create frames
    '''
    for stripLevel in range(minLevel, maxLevel+1, 1):
        for istep in range(0, nsteps, 1):
            # Open the data base. 
            DeleteAllPlots()
            f = directory + "/" + basename + ".step" + str(step).rjust(7,'0') + "." + str(dim) + "d.hdf5"
            OpenDatabase(f)
            
            # Add a ghost plot for getting extensions of current level being plotted. This plot
            # is deleted afterwards.
            AddPlot("Pseudocolor", "Electric field_magnitude")
            silr = SILRestriction()
            silr.TurnOffAll();
            silr.TurnOnSet(stripLevel+1)
            SetPlotSILRestriction(silr,0)
            DrawPlots()
            Query('SpatialExtents', use_actual_data=1)
            s = GetQueryOutputValue()
            DeleteAllPlots()

            # Determine the subset box
            xmin = -100.
            xmax =  100.
            ymin = -100.
            ymax =  100.
            zmin = -100.
            zmax =  100.        
        
            if(stripCoord == "x"):
                xmin = s[0] + istep * (s[1]-s[0])/(nsteps-1)
                xmax = s[1]
            elif(stripCoord == "y"):
                ymin = s[2] + istep * (s[3]-s[2])/(nsteps-1)
                ymax = s[3]
            elif(stripCoord == "z"):
                zmin = s[4] + istep * (s[5]-s[4])/(nsteps-1)
                zmax = s[4]

            # Draw embedded boundary
            draw_boundaries()            

            # Strip this level
            draw_patches(stripLevel)
            set_box(xmin, xmax, ymin, ymax, zmin, zmax)
        
            draw_grid(stripLevel)
            set_box(xmin, xmax, ymin, ymax, zmin, zmax)

            # Add in the finer level
            if(stripLevel < maxLevel):
                draw_patches(stripLevel+1)

                # Transform by some tiny amount to prevent surfaces from overlapping
                AddOperator("Transform")
                t = TransformAttributes()
                t.doScale= 1
                t.scaleX = 1.0001
                t.scaleY = 1.0001
                t.scaleZ = 1.0001
                SetOperatorOptions(t)                    

                draw_grid(stripLevel+1)                        

            # Draw and save
            DrawPlots()
        
            # Set name and save window
            set_output(framename, frame_index)        
            SaveWindow()

            # Clean up stuff
            DeleteAllPlots()
            CloseDatabase(f)
            ClearCacheForAllEngines()

            # Go to next frame. 
            frame_index += 1

    return frame_index

# Default things like view, annotation, render, slider, etc. 
set_default_view()
set_annotation()
set_render_attributes()

# Make frames using the first view.
fidx = 0
fidx = make_frames(fidx,1,3)

# Make frames using the second view
set_zoom(zoom2)
fidx = make_frames(fidx,3,4)

exit()

