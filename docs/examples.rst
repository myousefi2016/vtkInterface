.. _examples:

Examples
========

Mesh Reading and Writing
------------------------

Both binary and ASCII .ply, .stl, and .vtk files can be read using
vtkInterface.  The vtkInterface package contains example meshes and these can 
be loaded with:

.. code:: python

    import vtkInterface
    
    # Get the filename from the examples
    from vtkInterface import examples
    filename = examples.planefile
    
    # Load mesh
    mesh = vtkInterface.LoadMesh(filename)

This mesh can then be written to a vtk file using:

.. code:: python

    mesh.WriteMesh('plane.vtk')
    
    
These meshes are identical.

.. code:: python

    mesh_from_vtk = vtkInterface.LoadMesh('plane.vtk')
    
    import numpy as np
    np.allclose(mesh_from_vtk.GetNumpyPoints(), mesh.GetNumpyPoints())
 
    
Mesh Manipulation and Plotting
------------------------------

Meshes can be directly manipulated using numpy or with the built-in
translation and rotation routines.  This example loads two meshes and moves, 
scales, and copies them.

.. code:: python

    # Load module and examples
    import vtkInterface
    from vtkInterface import examples
    planefile = examples.planefile
    antfile = examples.antfile
    
    # load and shrink airplane
    airplane = vtkInterface.LoadMesh(planefile)
    pts = airplane.GetNumpyPoints() # gets pointer to array
    pts /= 10 # shrink by 10x
    
    # rotate and translate ant so it is on the plane
    ant = vtkInterface.LoadMesh(antfile)
    ant.RotateX(90)
    ant.Translate([90, 60, 15])
    
    # Make a copy and add another ant
    ant_copy = ant.Copy()
    ant_copy.Translate([30, 0, -10])

To plot more than one mesh a plotting class must be created to manage the 
plotting.  The following code creates the class and plots the meshes with 
various colors.

.. code:: python
    
    # Create plotting object
    plobj = vtkInterface.PlotClass()
    plobj.AddMesh(ant, 'r')
    plobj.AddMesh(ant_copy, 'b')

    # Add airplane mesh and make the color equal to the Y position.  Add a
    # scalar bar associated with this mesh
    plane_scalars = pts[:, 1]
    plobj.AddMesh(airplane, scalars=plane_scalars, stitle='Plane Y\nLocation')

    # Add annotation text
    plobj.AddText('Ants and Plane Example')
    plobj.Plot()
    
    # Close plotting object
    del plobj
    
.. image:: AntsAndPlane.png



Unstructured Grid Plotting
--------------------------

This example shows how you can load an unstructured grid from a vtk file and
create a plot and gif movie by updating the plotting object.

.. code:: python

    # Load module and example file
    import vtkInterface
    from vtkInterface import examples
    import numpy as np
    import time
    
    hexfile = examples.hexbeamfile
    
    # Load Grid
    grid = vtkInterface.LoadGrid(hexfile)
    
    # Create fiticious displacements as a function of Z location
    pts = grid.GetNumpyPoints(deep=True)
    d = np.zeros_like(pts)
    d[:, 1] = pts[:, 2]**3/250
    
    # Displace original grid
    grid.SetNumpyPoints(pts + d)

A simple plot can be created by using:

.. code:: python

    grid.Plot(scalars=d[:, 1], stitle='Y Displacement')

A more complex plot can be created using:

.. code:: python

    # Store Camera position.  This can be obtained manually by getting the
    # output of plobj.Plot()
    cpos = [(11.915126303095157, 6.11392754955802, 3.6124956735471914),
             (0.0, 0.375, 2.0),
             (-0.42546442225230097, 0.9024244135964158, -0.06789847673314177)]
    
    # plot this displaced beam
    plobj = vtkInterface.PlotClass()
    plobj.AddMesh(grid, scalars=d[:, 1], stitle='Y Displacement', 
                  rng=[-d.max(), d.max()])
    plobj.AddAxes()
    plobj.SetCameraPosition(cpos)
    
    # Don't close so we can take a screenshot
    cpos = plobj.Plot(autoclose=False)
    plobj.TakeScreenShot('beam.png')
    del plobj

.. image:: beam.png


You can animate the motion of the beam by updating the positions and scalars
of the grid copied to the plotting object.  First you have to setup the
plotting object:

.. code:: python

    # Animate plot
    plobj = vtkInterface.PlotClass()
    plobj.AddMesh(grid, scalars=d[:, 1], stitle='Y Displacement', 
                  showedges=True, rng=[-d.max(), d.max()], 
                  interpolatebeforemap=True)
    plobj.AddAxes()
    plobj.SetCameraPosition(cpos)
    
You then open the render window by plotting before opening movie file.
Set autoclose to False so
the plobj doesn't close automatically.  Disabling interactive means 
the plot will automatically continue without waiting for the user to
exit the window.

.. code:: python

    plobj.Plot(interactive=False, autoclose=False, window_size=[800, 600])
    
    # open movie file.  A mp4 file can be written instead.  Requires moviepy
    #plobj.OpenMovie('beam.mp4')
    plobj.OpenGif('beam.gif')
    
    # Modify position of the beam cyclically
    for phase in np.linspace(0, 2*np.pi, 20):
        plobj.UpdateCoordinates(pts + d*np.cos(phase), render=False)
        plobj.UpdateScalars(d[:, 1]*np.cos(phase), render=False)
        plobj.Render()
        plobj.WriteFrame()
    
    # Close the movie
    plobj.Close()
    del plobj
    
.. image:: beam.gif

You can also render the beam as as a wireframe object:

.. code:: python

    # Animate plot as a wireframe
    plobj = vtkInterface.PlotClass()
    plobj.AddMesh(grid, scalars=d[:, 1], stitle='Y Displacement', showedges=True,
                  rng=[-d.max(), d.max()], interpolatebeforemap=True,
                  style='wireframe')
    plobj.AddAxes()
    plobj.SetCameraPosition(cpos)
    plobj.Plot(interactive=False, autoclose=False, window_size=[800, 600])
    
    #plobj.OpenMovie('beam.mp4')
    plobj.OpenGif('beam_wireframe.gif')
    for phase in np.linspace(0, 2*np.pi, 20):
        plobj.UpdateCoordinates(pts + d*np.cos(phase), render=False)
        plobj.UpdateScalars(d[:, 1]*np.cos(phase), render=False)
        plobj.Render()
        plobj.WriteFrame()
        time.sleep(0.01)
    
    plobj.Close()
    del plobj
    
.. image:: beam_wireframe.gif


Adding Labels to a Plot
-----------------------

Labels can be added to a plot using the ``AddPointLabels`` function within the 
``PlotClass`` object.  The following example loads the included example beam, generates a plotting class, and subselects points along the y-z plane and labels their coordinates.  ``AddPointLabels`` requires that the number of labels matches the number of points, and that labels is a list containing one entry per point.  The code automatically converts each item in the list to a string.

.. code:: python

    # Load module and example file
    import vtkInterface
    from vtkInterface import examples

    hexfile = examples.hexbeamfile

    # Load Grid
    grid = vtkInterface.LoadGrid(hexfile)

    # Create plotting class and add the unstructured grid
    plobj = vtkInterface.PlotClass()
    plobj.AddMesh(grid)

    # Add labels to points on the yz plane (where x == 0)
    points = grid.GetNumpyPoints()
    mask = points[:, 0] == 0
    plobj.AddPointLabels(points[mask], points[mask].tolist())

    # plot and then close plot
    plobj.Plot(); del plobj

.. image:: labels0.png

This example is similar and shows how labels can be combined with a scalar bar to show the exact value of certain points.

.. code:: python

    # Load module and example file
    import vtkInterface
    from vtkInterface import examples

    hexfile = examples.hexbeamfile

    # get a numpy array of the points from  the unstructured grid
    points = grid.GetNumpyPoints()
    values = points[:, 2]

    # Create plotting class and add the unstructured grid
    plobj = vtkInterface.PlotClass()
    plobj.AddMesh(grid, scalars=values) # color mesh according to z value
    plobj.AddScalarBar(title='Z Position')

    # Add labels to points on the yz plane (where x == 0)
    mask = points[:, 0] == 0
    plobj.AddPointLabels(points[mask], values.tolist(), fontsize=24)

    # add some text to the plot
    plobj.AddText('Example showing plot labels')

    # plot and then close plot
    plobj.Plot(); del plobj

.. image:: labels1.png
