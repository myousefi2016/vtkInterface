import os
import vtkInterface
import numpy as np
import time

# get location of this folder and the example files
dir_path = os.path.dirname(os.path.realpath(__file__))
antfile = os.path.join(dir_path, 'ant.ply')
planefile = os.path.join(dir_path, 'airplane.ply')
hexbeamfile = os.path.join(dir_path, 'hexbeam.vtk')
spherefile = os.path.join(dir_path, 'sphere.vtk')


# get location of this folder
dir_path = os.path.dirname(os.path.realpath(__file__))


def LoadAnt():
    """ Load ply ant mesh """
    return vtkInterface.LoadMesh(antfile)
   
    
def LoadAirplane():
    """ Load ply airplane mesh """
    return vtkInterface.LoadMesh(planefile)
    

def LoadSphere():
    """ Loads sphere ply mesh """
    return vtkInterface.LoadMesh(spherefile)


def PlotAirplane():
    """ Plot a white airplane """
    airplane = vtkInterface.LoadMesh(planefile)
    airplane.Plot()
    
    
def PlotAnt():
    """ Plot a red ant in wireframe"""
    ant = vtkInterface.LoadMesh(antfile)
    ant.Plot(color='r', style='wireframe')
    

def PlotAntsPlane():
    """ 
    DESCRIPTION
    Demonstrate how to create a plot class to plot multiple meshes while 
    adding scalars and text.
    Plot two ants and airplane
    
    """
    
    # load and shrink airplane
    airplane = vtkInterface.LoadMesh(planefile)
    pts = airplane.GetNumpyPoints() # gets pointer to array
    pts /= 10 # shrink
    
    # rotate and translate ant so it is on the plane
    ant = vtkInterface.LoadMesh(antfile)
    ant.RotateX(90)
    ant.Translate([90, 60, 15])
    
    # Make a copy and add another ant
    ant_copy = ant.Copy()
    ant_copy.Translate([30, 0, -10])
    
    # Create plotting object
    plobj = vtkInterface.PlotClass()
    plobj.AddMesh(ant, 'r')
    plobj.AddMesh(ant_copy, 'b')
    
    # Add airplane mesh and make the color equal to the Y position
    plane_scalars = pts[:, 1]
    plobj.AddMesh(airplane, scalars=plane_scalars, stitle='Plane Y\nLocation')
    plobj.AddText('Ants and Plane Example')
    plobj.Plot(); del plobj


def BeamExample():
    # Load module and example file
    
    hexfile = hexbeamfile
    
    # Load Grid
    grid = vtkInterface.LoadGrid(hexfile)
    
    # Create fiticious displacements as a function of Z location
    pts = grid.GetNumpyPoints(deep=True)
    d = np.zeros_like(pts)
    d[:, 1] = pts[:, 2]**3/250
    
    # Displace original grid
    grid.SetNumpyPoints(pts + d)
    
    # Camera position
    cpos = [(11.915126303095157, 6.11392754955802, 3.6124956735471914),
             (0.0, 0.375, 2.0),
             (-0.42546442225230097, 0.9024244135964158, -0.06789847673314177)]
    
    # plot this displaced beam
    plobj = vtkInterface.PlotClass()
    plobj.AddMesh(grid, scalars=d[:, 1], stitle='Y Displacement', 
                  rng=[-d.max(), d.max()])
    plobj.AddAxes()
    plobj.SetCameraPosition(cpos)
    plobj.AddText('Static Beam Example')
    cpos = plobj.Plot(autoclose=False) # store camera position
#    plobj.TakeScreenShot('beam.png')
    del plobj
    
    
    # Animate plot
    plobj = vtkInterface.PlotClass()
    plobj.AddMesh(grid, scalars=d[:, 1], stitle='Y Displacement', showedges=True,
                  rng=[-d.max(), d.max()], interpolatebeforemap=True)
    plobj.AddAxes()
    plobj.SetCameraPosition(cpos)
    plobj.AddText('Beam Animation Example')
    plobj.Plot(interactive=False, autoclose=False, window_size=[800, 600])

    #plobj.OpenMovie('beam.mp4')
#    plobj.OpenGif('beam.gif')
    for phase in np.linspace(0, 4*np.pi, 100):
        plobj.UpdateCoordinates(pts + d*np.cos(phase), render=False)
        plobj.UpdateScalars(d[:, 1]*np.cos(phase), render=False)
        plobj.Render()
#        plobj.WriteFrame()
        time.sleep(0.01)
    
    plobj.Close()
    del plobj
    
    
    # Animate plot as a wireframe
    plobj = vtkInterface.PlotClass()
    plobj.AddMesh(grid, scalars=d[:, 1], stitle='Y Displacement', showedges=True,
                  rng=[-d.max(), d.max()], interpolatebeforemap=True,
                  style='wireframe')
    plobj.AddAxes()
    plobj.SetCameraPosition(cpos)
    plobj.AddText('Beam Animation Example 2')
    plobj.Plot(interactive=False, autoclose=False, window_size=[800, 600])
    
    #plobj.OpenMovie('beam.mp4')
#    plobj.OpenGif('beam_wireframe.gif')
    for phase in np.linspace(0, 4*np.pi, 100):
        plobj.UpdateCoordinates(pts + d*np.cos(phase), render=False)
        plobj.UpdateScalars(d[:, 1]*np.cos(phase), render=False)
        plobj.Render()
#        plobj.WriteFrame()
        time.sleep(0.01)
    
    plobj.Close()
    del plobj