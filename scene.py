import xshape

def cavity(gmshctx, numCavities: int):
    list_of_sphere = []
    for i in range(0, numCavities):
        sid = gmshctx.model.occ.addSphere(xc=i, yc=0.5, zc=0.5, radius=0.6)
        list_of_sphere.append((3, sid))
    
    id = gmshctx.model.occ.fuse(list_of_sphere[:1], list_of_sphere[1:], )
    return id[0][0][1]

def finger(gmshctx, numPhalanges: int):
    cavities_id = cavity(gmshctx, numCavities=numPhalanges)

    cube1 = gmshctx.model.occ.addBox(0, 0, 0, 1, 1, 1)
    cutid = gmshctx.model.occ.cut([(3, cube1)], [(3, cavities_id)])
    return cutid

#xshape.set_cache_mode("single-time")
#xshape.set_cache_mode("persistant")

print(xshape.get_volume_filename(cavity, numCavities=3))
print(xshape.get_volume_filename(cavity, numCavities=2))
print(xshape.get_volume_filename(finger, numPhalanges=2))
print(xshape.get_surface_filename(finger, numPhalanges=2))

xshape.save(xshape.get_surface_filename(finger, numPhalanges=2), 'myfile.msh')

#xshape.show(cavity, numCavities=10)
xshape.show(finger, numPhalanges=2)

#def createScene(root):
#    root.addObject("MeshMSHLoader", filename=get_volume_filename(cavity, numCavities=3))

