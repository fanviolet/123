import os, math, json
from PIL import Image, ImageDraw
import trimesh
from trimesh.visual.material import PBRMaterial

ROOT=os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
MODEL=os.path.join(ROOT,'assets','models')
ICON=os.path.join(ROOT,'assets','icons')
os.makedirs(MODEL,exist_ok=True); os.makedirs(ICON,exist_ok=True)

def mat(name, rgba, metallic=0.0, rough=0.45):
    return PBRMaterial(name=name, baseColorFactor=list(rgba), metallicFactor=metallic, roughnessFactor=rough)

def add(scene, mesh, color, name, transform=None, metallic=0.0, rough=0.45):
    mesh.visual.material=mat(name,color,metallic,rough)
    scene.add_geometry(mesh,node_name=name,geom_name=name,transform=transform)

def box(ext,pos=(0,0,0),color=(190,120,60,255),name='box',scene=None,metallic=0,rough=.45):
    mesh=trimesh.creation.box(extents=ext)
    add(scene,mesh,color,name,trimesh.transformations.translation_matrix(pos),metallic,rough)

def cyl(radius,height,pos=(0,0,0),color=(180,180,190,255),name='cyl',scene=None,metallic=.2,rough=.3,sections=32,axis='z'):
    mesh=trimesh.creation.cylinder(radius=radius,height=height,sections=sections)
    transform=trimesh.transformations.translation_matrix(pos)
    if axis=='y': transform=transform@trimesh.transformations.rotation_matrix(math.pi/2,[1,0,0])
    elif axis=='x': transform=transform@trimesh.transformations.rotation_matrix(math.pi/2,[0,1,0])
    add(scene,mesh,color,name,transform,metallic,rough)

def sphere(radius,pos,color,name,scene,metallic=0,rough=.35):
    mesh=trimesh.creation.icosphere(subdivisions=3,radius=radius)
    add(scene,mesh,color,name,trimesh.transformations.translation_matrix(pos),metallic,rough)

def export(scene,name): scene.export(os.path.join(MODEL,name+'.glb'))

s=trimesh.Scene(); box((1.15,.95,.9),(0,0,0),(191,118,58,255),'crate_body',s,rough=.62)
for x in (-.51,.51):
    for z in (-.38,.38): box((.09,1.01,.09),(x,0,z),(111,66,34,255),'corner',s,rough=.65)
for y in (-.37,0,.37): box((1.2,.08,.08),(0,y,.44),(223,151,77,255),'slat',s,rough=.55)
export(s,'crate')

s=trimesh.Scene(); box((1.45,.26,.92),(0,0,0),(247,225,180,255),'pages',s,rough=.78); box((1.52,.055,.98),(0,.157,0),(241,74,87,255),'cover_top',s,rough=.34); box((1.52,.055,.98),(0,-.157,0),(224,48,70,255),'cover_bottom',s,rough=.34); box((.09,.37,.98),(-.715,0,0),(184,32,55,255),'spine',s,rough=.36); export(s,'book')

s=trimesh.Scene(); box((1.18,.52,.66),(0,0,0),(221,87,64,255),'brick',s,rough=.68)
for x in (-.34,.34): box((.035,.535,.68),(x,.01,0),(158,56,45,255),'groove',s,rough=.8)
export(s,'brick')

s=trimesh.Scene(); box((1.9,.23,.5),(0,0,0),(202,132,67,255),'plank',s,rough=.66)
for x in (-.6,.35,.7): cyl(.045,.012,(x,.122,.12),(115,72,42,255),'knot',s,metallic=0,rough=.8,sections=20,axis='y')
export(s,'plank')

s=trimesh.Scene(); cyl(.37,.86,(0,0,0),(99,190,224,255),'can_body',s,metallic=.58,rough=.22,sections=40,axis='y')
for y in (-.43,.43): cyl(.39,.035,(0,y,0),(220,225,232,255),'rim',s,metallic=.8,rough=.15,sections=40,axis='y')
export(s,'can')

s=trimesh.Scene(); cyl(.48,.92,(0,0,0),(168,99,48,255),'barrel_body',s,metallic=0,rough=.6,sections=32,axis='y')
for y in (-.32,0,.32): cyl(.495,.055,(0,y,0),(72,82,94,255),'band',s,metallic=.7,rough=.25,sections=32,axis='y')
export(s,'barrel')

s=trimesh.Scene(); box((1.1,.82,.96),(0,0,0),(212,168,103,255),'carton',s,rough=.74); box((.12,.84,.98),(0,0,0),(238,210,146,255),'tape',s,rough=.45); export(s,'carton')

s=trimesh.Scene(); box((.9,.15,.85),(0,.2,0),(96,176,231,255),'seat',s,rough=.35); box((.9,.85,.14),(0,.65,.35),(72,145,214,255),'back',s,rough=.35)
for x in (-.36,.36):
    for z in (-.31,.31): box((.13,.72,.13),(x,-.23,z),(65,87,111,255),'leg',s,rough=.5)
export(s,'chair')

s=trimesh.Scene(); sphere(.48,(0,.85,0),(104,187,255,255),'head',s,metallic=.05,rough=.28); sphere(.36,(0,.18,0),(255,198,69,255),'body',s,metallic=.02,rough=.32)
for x in (-.19,.19): sphere(.075,(x,.96,.43),(35,45,63,255),'eye',s,metallic=.1,rough=.2)
sphere(.055,(0,.79,.47),(255,104,122,255),'nose',s,rough=.25)
for x in (-.42,.42): cyl(.095,.48,(x,.28,0),(255,198,69,255),'arm',s,rough=.32,sections=24,axis='y')
for x in (-.2,.2): cyl(.11,.46,(x,-.22,0),(88,158,230,255),'leg',s,rough=.3,sections=24,axis='y')
export(s,'mascot_blox')

s=trimesh.Scene(); box((.65,.25,.22),(-.2,0,0),(236,75,90,255),'mag_a',s,rough=.3); box((.65,.25,.22),(.2,0,0),(80,145,240,255),'mag_b',s,rough=.3); box((.22,.65,.22),(-.43,.2,0),(236,75,90,255),'leg_a',s,rough=.3); box((.22,.65,.22),(.43,.2,0),(80,145,240,255),'leg_b',s,rough=.3); export(s,'stabilizer')

s=trimesh.Scene(); cyl(.9,.12,(0,0,0),(71,212,190,255),'platform',s,metallic=.15,rough=.32,sections=48,axis='y'); cyl(.7,.14,(0,.02,0),(247,196,72,255),'ring',s,metallic=.1,rough=.3,sections=48,axis='y'); export(s,'safety_platform')

s=trimesh.Scene(); box((.16,1.1,.16),(0,.15,0),(246,181,64,255),'mast',s,metallic=.2,rough=.3); box((.85,.14,.14),(.34,.66,0),(246,181,64,255),'boom',s,metallic=.2,rough=.3); cyl(.06,.55,(.72,.35,0),(67,78,95,255),'cable',s,metallic=.7,rough=.2,sections=20,axis='y'); sphere(.12,(.72,.04,0),(240,91,95,255),'hook',s,metallic=.5,rough=.25); export(s,'undo_crane')

N=512; im=Image.new('RGBA',(N,N),(55,203,212,255)); d=ImageDraw.Draw(im); pix=im.load()
for y in range(N):
    t=y/(N-1); c=(int(55*(1-t)+111*t),int(203*(1-t)+113*t),int(212*(1-t)+245*t),255)
    for x in range(N): pix[x,y]=c
colors=[(255,107,107,255),(255,205,86,255),(93,204,156,255),(94,158,255,255),(180,111,255,255)]
for i,c in enumerate(colors):
    w=250-i*28; x=(N-w)//2+(i%2)*12-6; y=350-i*58; d.rounded_rectangle((x,y,x+w,y+54),radius=18,fill=c,outline=(255,255,255,100),width=3)
cx,cy=370,125; d.ellipse((cx-68,cy-68,cx+68,cy+68),fill=(255,201,70,255),outline=(255,255,255,150),width=5); d.ellipse((cx-30,cy-18,cx-14,cy-2),fill=(30,40,60,255)); d.ellipse((cx+14,cy-18,cx+30,cy-2),fill=(30,40,60,255)); d.arc((cx-30,cy-5,cx+30,cy+38),0,180,fill=(80,55,40,255),width=6)
im.save(os.path.join(ICON,'icon.png'))
manifest={f:os.path.getsize(os.path.join(MODEL,f)) for f in os.listdir(MODEL)}
with open(os.path.join(ROOT,'assets','asset_manifest.json'),'w') as fp: json.dump(manifest,fp,indent=2)
print('generated',len(manifest),'models')
