import math
import bpy  
import os
import random

#c=lower southwest corner, s=length of a side, i=indent
def makeCube(c, s, i, mat):
   verts = [(c[0]+i, c[1]+i, c[2]+i),
      (c[0]+s-i, c[1]+i, c[2]+i),
      (c[0]+i, c[1]+s-i, c[2]+i),
      (c[0]+s-i, c[1]+s-i, c[2]+i),
      (c[0]+i, c[1]+i, c[2]+s-i),
      (c[0]+s-i, c[1]+i, c[2]+s-i),
      (c[0]+i, c[1]+s-i, c[2]+s-i),
      (c[0]+s-i, c[1]+s-i, c[2]+s-i)]

   faces = [(0, 1, 3, 2),
   (4, 5, 7, 6),
   (0, 1, 5, 4),
   (3 ,2 ,6 ,7 ),
   (0 ,2 ,6, 4 ),
   (1, 3, 7 ,5 ),]  
  
   mesh_data = bpy.data.meshes.new("cube_mesh_data")  
   mesh_data.from_pydata(verts, [], faces)  
   mesh_data.update() # (calc_edges=True) not needed here  
  
   cube_object = bpy.data.objects.new("Cube_Object", mesh_data)  
  
   scene = bpy.context.scene
   scene.objects.link(cube_object)
   cube_object.select = True
   cube_object.data.materials.append(mat)
   bpy.context.scene.objects.active = cube_object
   return cube_object
   #image = bpy.data.images.load(randEmojiPath())
   #for uv_face in cube_object.data.uv_textures:
   #   uv_face.image = image


def makePlane(v, f, mat):
    p = bpy.data.meshes.new("plane_data")
    p.from_pydata(v, [], f)
    p.update()
    pob = bpy.data.objects.load("plane_object", p)
    scene = bpy.context.scene
    scene.objects.link(pob)
    pob.select = True
    pob.data.materials.append(mat)
   

#ts = total side length
#ss = small side length
#cps = cubesPerSide
#i = indent
def makeCubeGrid(ts, cps, i, c):
   objs = []
   ss = ts/(1.0*cps)
   print('ss:'+str(ss))
   for x in range(cps):
       for y in range(cps):
           for z in range(cps):
               mat = makeMat(randEmojiPath('/home/brink/photo-mosaic-video-generator/win/'))
               cube = makeCube((c[0] + x*ss, c[1] + y*ss, c[2] + z*ss), ss, i, mat) 
               objs.append(cube)
   return objs


def makeMat(imgName = None):
   tex = bpy.data.textures.new('tiny_icon', type = 'IMAGE')
   if (imgName != None):
      img = bpy.data.images.load(imgName)
      tex.image = img
   mat = bpy.data.materials.new('MatName')
   mtex = mat.texture_slots.add()
   mtex.texture = tex
   mtex.texture_coords = 'UV'
   mtex.use_map_color_diffuse = True 
   mtex.diffuse_color_factor = 1.0
   mtex.blend_type = 'MULTIPLY'
   return mat

def randEmojiPath(path = '/home/brink/photo-mosaic-video-generator/emoji/'):
   return path + random.choice(os.listdir(path))


def stackCubeGrids(ts, cps, i, c, cubes, d = (0, 0, 1)):
   objs = []
   for n in range(cubes):
      nc = (c[0] + (ts*n)*d[0], c[1] + (ts*n)*d[1], c[2] + (ts*n)*d[2])
      grid = makeCubeGrid(ts, cps, i, nc)
      for cube in grid:
         objs.append(cube)
   return objs

def move(objs, d = (0, 0, 1)):
   for obj in objs:
   #obj = bpy.context.object
      obj.location[2] = 0.0
      obj.keyframe_insert(data_path="location", frame=0.0, index=2)
      obj.location[2] = 40.0
      obj.keyframe_insert(data_path="location", frame=3000.0, index=2)
   
def main():
   objs = stackCubeGrids(10, 12, .25, (-6, -4, -5), 5, d = (0, 0, -1))
   move(objs)
    
main()
#file_path = StringProperty(name = "/home/brink/Desktop/tiny_icon.png", subtype = "FILE_PATH")
#img = bpy.data.images.load(file_path) #most of the time you will have to do self.file_path
#console.log(img)