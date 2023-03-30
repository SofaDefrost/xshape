import xshape

def cavity(gmshctx, numCavities: int):
    id = gmshctx.model.add("Cavity")
    for i in range(0, numCavities):
        gmshctx.model.occ.addSphere(xc=i*1.5, yc=0.0, zc=0.0, radius=1.0)
    return id

def finger(gmshctx, numPhalanges: int):
    cavities_id = cavity(gmshctx, numCavities=numPhalanges)
    
    finger_id = gmshctx.model.add("Finger")
    L, B, H, r = 2.5, 0.41, 0.41, 0.05
    channel = gmshctx.model.occ.addBox(0, 0, 0, L, B, H)    
    return finger_id

xshape.set_cache_mode("persistant")

print(xshape.get_volume_filename(cavity, numCavities=3))
print(xshape.get_volume_filename(cavity, numCavities=2))
print(xshape.get_volume_filename(finger, numPhalanges=2))
print(xshape.get_surface_filename(finger, numPhalanges=2))

#def createScene(root):
#    root.addObject("MeshMSHLoader", filename=get_volume_filename(cavity, numCavities=3))

