Xshape 
------

A small python library to ease the use procedural geometry in Sofa. The geometry is generated once
and then saved in a cache for future use. It is possible to control hoz the cache is working.


'''python
import xshape

def finger(gmshctx, numPhalanges: int):
    '''Defines a procedural geometry using gmesh'''  
    cavities_id = cavity(gmshctx, numCavities=numPhalanges)

    cube1 = gmshctx.model.occ.addBox(0, 0, 0, 1, 1, 1)
    cutid = gmshctx.model.occ.cut([(3, cube1)], [(3, cavities_id)])
    return cutid

def createScene(root):
    root.addObject('MeshMSHLoader', filename=xshape.get_volume_filename(cavity, numCavities=1) )
    root.addObject('MeshMSHLoader', filename=xshape.get_volume_filename(cavity, numCavities=2) )
'''