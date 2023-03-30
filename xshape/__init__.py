# Copyright CNRS
# Licence lgpl
# contributors:
#    damien.marchal@univ-lille.fr
import hashlib
import os
import gmsh
import tempfile
import shutil

class PersistantPath():
    name = ".xshape/tmp"
    def __init__(self, filename):
        self.name = filename

xshape_path = ".xshape"
xshape_cache_mode = "persistant" #or one shot
temporary_path_name=".xshape/tmp"
temporary_path_size_limit=10
temporary_path=PersistantPath(temporary_path_name)

def set_cache_mode(mode):
    global temporary_path
    xshape_cache_mode = mode 
    if mode == "persistant":
        temporary_path=PersistantPath(temporary_path_name)
    elif mode == "single-time":
        temporary_path=tempfile.TemporaryDirectory()
    else:
        raise Exception("Invalid xshape_cache_mode, allowed value are 'persistant' or 'single-time'")    

def manage_temporary_directories():
    # Prepare the directories
    if not os.path.exists(xshape_path):
        print("Creating the {0} directory".format(xshape_path))
        os.mkdir(xshape_path)

    if not os.path.exists(temporary_path.name):
        print("Creating the {0} directory to cache mesh generation data".format(temporary_path.name))
        os.mkdir(temporary_path.name)      

    # Check that the temporary directrories are not going too big.
    size = 0
    file = 0
    for ele in os.scandir(temporary_path.name):
        size+=os.path.getsize(ele)
        file+=1
    size = size/(1024*1024)
    if size > temporary_path_size_limit:
        print("Temporary directory is in: "+temporary_path.name)
        print("                     file: "+str(file))
        print("                     size: "+str(int(size))+" Mb")
        print("The cache directory is too big...  please consider cleaning")

def get_unique_filename(generating_function, **kwargs):
    temporary_file = tempfile.NamedTemporaryFile(suffix='.geo_unrolled')
    temporary_file.close()
    gmsh.write(temporary_file.name)
    result = hashlib.md5(open(temporary_file.name).read().encode())

    md5digest=result.hexdigest()

    return generating_function.__name__+"_"+md5digest

def get_volume_filename(generating_function, **kwargs):
    manage_temporary_directories()

    gmsh.initialize()

    # Silence gmsh so by default nothing is printed
    gmsh.option.setNumber("General.Terminal", 0)
    
    id = generating_function(gmsh, **kwargs)
    gmsh.model.occ.synchronize()

    filename = get_unique_filename(generating_function, **kwargs)
    full_filename = os.path.join(temporary_path.name, filename+"_volume.msh")   
    if not os.path.exists(full_filename):
        # When we are generating the mesh, it is better to know something is happening so let's reactive the printed messages
        gmsh.option.setNumber("General.Terminal", 1)
        gmsh.model.mesh.generate(3)
        gmsh.write(full_filename)

    gmsh.finalize()
    return full_filename

def get_surface_filename(generating_function, **kwargs):
    manage_temporary_directories()

    gmsh.initialize()

    # Silence gmsh so by default nothing is printed
    gmsh.option.setNumber("General.Terminal", 0)
    
    id = generating_function(gmsh, **kwargs)
    gmsh.model.occ.synchronize()

    filename = get_unique_filename(generating_function, **kwargs)
    full_filename = os.path.join(temporary_path.name, filename+"_surface.stl")   
    if not os.path.exists(full_filename):
        # When we are generating the mesh, it is better to know something is happening so let's reactive the printed messages
        gmsh.option.setNumber("General.Terminal", 1)
        gmsh.model.mesh.generate(2)
        gmsh.write(full_filename)

    gmsh.finalize()
    return full_filename

def save(source_filename, as_filename):
    return shutil.copy(source_filename, as_filename)

def show(generating_function, **kwargs):
    manage_temporary_directories()

    gmsh.initialize()

    # Silence gmsh so by default nothing is printed
    gmsh.option.setNumber("General.Terminal", 0)
    
    id = generating_function(gmsh, **kwargs)
    gmsh.model.occ.synchronize()

    gmsh.fltk.run()

    gmsh.finalize()