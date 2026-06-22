import os
from visit import *
import shutil

# Set up directory and retrieve sorted list of .vtk files
gw_data_dir = "/data/codyolson/memory_effect/GW_VTK_CODE/VTKdata/2D"
#bh_data_dir = "/anvil/scratch/x-colson1/n_body/bh_locations_shell_xyPlane"
#pseudocolor_xml = "/anvil/scratch/x-colson1/n_body/xml/Pseudocolor.xml"
output_dir = "/data/codyolson/memory_effect/GW_VTK_CODE/6_20_movie"

# Clean and create the output directory
if os.path.exists(output_dir):
    shutil.rmtree(output_dir)
os.makedirs(output_dir)

# Collect and sort data files
data_files_gw = [f for f in os.listdir(gw_data_dir) if f.endswith('.vtk')]
data_files_sorted_gw = sorted(data_files_gw, key=lambda x: int(x.split('_')[1].split('.')[0]))

# Create a 2D clock annotation object
clock_text = CreateAnnotationObject("Text2D")
clock_text.position = (0.75, 0.95) 
clock_text.useForegroundForTextColor = 0
clock_text.textColor = (255, 255, 255, 255)
clock_text.fontBold = 1
clock_text.fontFamily = clock_text.Times


for i, filename in enumerate(data_files_sorted_gw):
    gw_filepath = os.path.join(gw_data_dir, filename)
    #bh_filepath = os.path.join(bh_data_dir, "timestep_{}.3d".format(i))
    ActivateDatabase(gw_filepath)

    # Annotations, background, colorbar
    Ann = AnnotationAttributes()
    Ann.backgroundMode = Ann.Solid
    Ann.backgroundColor = (56, 140, 180, 255) 
    Ann.legendInfoFlag = 0
    Ann.databaseInfoFlag = 0
    Ann.userInfoFlag = 0
    Ann.axes3D.visible = 0
    Ann.axes3D.triadFlag = 0
    Ann.axes3D.bboxFlag = 0
    SetAnnotationAttributes(Ann)

    # Add pseudocolor plot for gravitational wave field
    # Pseudocolor plot for GW field
    AddPlot("Pseudocolor", "GW-MEM")
    pseudo_atts = PseudocolorAttributes()
    pseudo_atts.colorTableName = "gw_mem" #gw_mem_purple  gw_mem_red
    pseudo_atts.minFlag = 1
    pseudo_atts.min = 0.1
    pseudo_atts.maxFlag = 1
    pseudo_atts.max = 1000
    pseudo_atts.smoothingLevel = 2  # 0=NONE, 1=Fast, 2=High
    pseudo_atts.legendFlag = 0
    SetPlotOptions(pseudo_atts)

    # Resample just the pseudocolor to 2000×2000
    AddOperator("Resample")
    resample_pc = ResampleAttributes()
    resample_pc.is3D = 0
    resample_pc.samplesX = 2000
    resample_pc.samplesY = 2000
    SetOperatorOptions(resample_pc)

    # (Optional) Elevate and Cylinder on the pseudocolor
    AddOperator("Elevate")
    elevate_atts = ElevateAttributes()
    elevate_atts.variable = "GW-FIELD"
    elevate_atts.useXYLimits = elevate_atts.Never
    SetOperatorOptions(elevate_atts)

    AddOperator("Cylinder")
    cyl_atts = CylinderAttributes()
    cyl_atts.point1 = (0, 0, 10000)
    cyl_atts.point2 = (0, 0, -10000)
    cyl_atts.radius = 15 * 2.7
    cyl_atts.inverse = 1
    SetOperatorOptions(cyl_atts)

    # Mesh plot
    AddPlot("Mesh", "mesh")
    mesh_atts = MeshAttributes()
    mesh_atts.legendFlag = 0
    mesh_atts.smoothingLevel = mesh_atts.High
    SetPlotOptions(mesh_atts)

    # Resample just the mesh to 400×400
    AddOperator("Resample")
    resample_mesh = ResampleAttributes()
    resample_mesh.is3D = 0
    resample_mesh.samplesX = 400
    resample_mesh.samplesY = 400
    SetOperatorOptions(resample_mesh)

    AddOperator("Elevate")
    elevate_mesh = ElevateAttributes()
    elevate_mesh.variable = "GW-FIELD"
    elevate_mesh.useXYLimits = elevate_mesh.Never
    SetOperatorOptions(elevate_mesh)

    # Cylinder cutout on the mesh
    AddOperator("Cylinder")
    cyl_mesh = CylinderAttributes()
    cyl_mesh.point1 = (0, 0, 10000)
    cyl_mesh.point2 = (0, 0, -10000)
    cyl_mesh.radius = 15 * 2.7
    cyl_mesh.inverse = 1
    SetOperatorOptions(cyl_mesh)

    # Finally, make sure both plots are active
    SetActivePlots((0, 1))
    # Black hole data
    #OpenDatabase(bh_filepath)
    #AddPlot("Pseudocolor", "test")
    #p = PseudocolorAttributes()
    #LoadAttribute(pseudocolor_xml, p)
    #SetPlotOptions(p)
    DrawPlots()

    # Update clock text
    time = i * 3.5303225806 / 2.7  # Adjusted time calculation
    clock_text.text = "t/M = {:.0f}".format(time)

    # Configure 3D view attributes

    c0 = View3DAttributes()
    c0.viewNormal = (0, 1.2, 1)
    # c0.viewNormal = (0, 0.5, 1)
    c0.focus = (15,10,0)
    # c0.focus = (150, 50, 0)
    c0.viewUp = (-0.2, -1.2, 1)
    # c0.viewUp = (-0.25, 0, 1)
    c0.viewAngle = 30
    c0.parallelScale = 129.904 #200
    c0.nearPlane = -698.12
    c0.farPlane = 698.12
    c0.imagePan = (0, 0)
    c0.imageZoom = 0.7 #1.0 #3.2 #2.2
    c0.perspective = 1
    c0.eyeAngle = 2
    c0.centerOfRotationSet = 0
    c0.centerOfRotation = (7.2533, 7.2533, 0)
    c0.axis3DScaleFlag = 0
    c0.axis3DScales = (1, 1, 5000)
    c0.shear = (0, 0, 1)
    SetView3D(c0)
   
    output_filename = os.path.join(output_dir, "plot_timestep_{:04d}".format(i))

    # Save plot
    swa = SaveWindowAttributes()
    swa.fileName = output_filename
    swa.family = 0 
    swa.format = swa.PNG  
    swa.width = 1920  
    swa.height = 1080  
    #swa.screenCapture = 0
    #s.stereo = 0 #Setting for 3D movie
    swa.resConstraint = swa.NoConstraint
    SetSaveWindowAttributes(swa)
    SaveWindow()

    print("Saved plot for timestep {} as {}.png".format(i, output_filename))

    DeleteAllPlots()
    CloseDatabase(gw_filepath)
    #CloseDatabase(bh_filepath)
    # Finalize and print confirmation
    print("Processed file: {}".format(filename))
