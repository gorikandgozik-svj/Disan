"""Small, deterministic, explicitly BLOCKOUT-tier procedural assets.

This module uses real triangle meshes and named movable parts rather than
images masquerading as 3D. It does not claim CAD dimensional accuracy, PBR
texture authoring, aerodynamic simulation, or photographic fidelity.
"""
from __future__ import annotations

import math
import json
from pathlib import Path


def _loft(rings, sides=16):
    import numpy as np
    import trimesh
    vertices=[]
    for x, yr, zr, zc in rings:
        for i in range(sides):
            angle=2*math.pi*i/sides
            vertices.append([x, math.cos(angle)*yr, zc+math.sin(angle)*zr])
    faces=[]
    for j in range(len(rings)-1):
        for i in range(sides):
            a=j*sides+i; b=j*sides+(i+1)%sides
            c=(j+1)*sides+i; d=(j+1)*sides+(i+1)%sides
            faces.extend([[a,b,d],[a,d,c]])
    vertices += [[rings[0][0],0,rings[0][3]], [rings[-1][0],0,rings[-1][3]]]
    front=len(vertices)-2; back=len(vertices)-1
    for i in range(sides):
        faces.extend([[front,(i+1)%sides,i],
                      [back,(len(rings)-1)*sides+i,(len(rings)-1)*sides+(i+1)%sides]])
    mesh=trimesh.Trimesh(vertices=np.array(vertices),faces=np.array(faces),process=True)
    return mesh


def _wedge(corners, thickness):
    """Four XY corners, extruded in Z, producing an actual closed mesh."""
    import trimesh
    n=len(corners)
    vertices=[[x,y,-thickness/2] for x,y in corners]+[[x,y,thickness/2] for x,y in corners]
    faces=[]
    for i in range(1,n-1):
        faces.extend([[0,i,i+1],[n,n+i+1,n+i]])
    for i in range(n):
        j=(i+1)%n
        faces.extend([[i,j,j+n],[i,j+n,i+n]])
    return trimesh.Trimesh(vertices=vertices,faces=faces,process=True)


def create_vehicle_blockout(project_name, vehicle_type='sports-car'):
    import trimesh
    from core import project_dir
    if vehicle_type not in ('sports-car','airliner'):
        raise ValueError('vehicle_type must be sports-car or airliner')
    scene=trimesh.Scene()

    def add(name, mesh, color):
        mesh.visual.face_colors=color
        scene.add_geometry(mesh,geom_name=name,node_name=name)

    if vehicle_type=='sports-car':
        body=_loft([(-2.24,.42,.32,.72),(-1.85,.88,.37,.72),(-1.25,.99,.38,.72),
                    (.7,.98,.4,.72),(1.65,.88,.34,.72),(2.12,.43,.30,.72)])
        add('chassis-paint',body,(28,32,36,255))
        cabin=_loft([(-.90,.63,.05,1.01),(-.52,.70,.35,1.13),(.55,.68,.32,1.12),(.96,.63,.05,1.02)])
        add('glass-canopy',cabin,(45,78,88,200))
        for x,side in [(-1.32,-1),(-1.32,1),(1.34,-1),(1.34,1)]:
            wheel=trimesh.creation.cylinder(radius=.46,height=.23,sections=24)
            wheel.apply_transform(trimesh.transformations.rotation_matrix(math.pi/2,[1,0,0]))
            wheel.apply_translation([x,side*1.03,.48])
            add(('front' if x>0 else 'rear')+'-'+('right' if side>0 else 'left')+'-wheel',wheel,(19,21,23,255))
            rim=trimesh.creation.cylinder(radius=.26,height=.235,sections=16)
            rim.apply_transform(trimesh.transformations.rotation_matrix(math.pi/2,[1,0,0]))
            rim.apply_translation([x,side*1.03,.48])
            add(('front' if x>0 else 'rear')+'-'+('right' if side>0 else 'left')+'-rim',rim,(165,166,166,255))
        for side in [-1,1]:
            lamp=trimesh.creation.box([.065,.40,.12]);lamp.apply_translation([2.02,side*.44,.94])
            add(('right' if side>0 else 'left')+'-headlamp',lamp,(255,236,173,255))
        spoiler=trimesh.creation.box([.23,1.80,.10]);spoiler.apply_translation([-1.84,0,1.19]);add('rear-spoiler',spoiler,(24,28,30,255))
    else:
        # Generic widebody four-engine airliner silhouette, not a model of any airline's aircraft.
        add('fuselage',_loft([(-15,.12,.16,2.9),(-13,1.4,1.55,2.9),(-10,2.1,2.25,2.9),
                            (8,2.15,2.27,2.9),(12,1.6,1.78,2.9),(18,.07,.09,3.5)],20),(224,230,234,255))
        wing=_wedge([(-4,0),(-1,0),(6,17),(2,20)],.26);wing.apply_translation([0,0,2.75])
        add('left-main-wing',wing,(171,180,185,255))
        wing2=wing.copy();wing2.apply_transform(trimesh.transformations.reflection_matrix([0,0,0],[0,1,0]));add('right-main-wing',wing2,(171,180,185,255))
        htail=_wedge([(-12,0),(-10,0),(-10.5,6),(-12.9,7)],.18);htail.apply_translation([0,0,3.15]);add('left-stabilizer',htail,(180,188,193,255))
        ht2=htail.copy();ht2.apply_transform(trimesh.transformations.reflection_matrix([0,0,0],[0,1,0]));add('right-stabilizer',ht2,(180,188,193,255))
        vert=trimesh.creation.box([4.8,.20,5]);vert.apply_translation([-12.7,0,5.45]);add('vertical-stabilizer',vert,(205,216,223,255))
        for side in [-1,1]:
            for offset in [5.4,11.8]:
                engine=trimesh.creation.cylinder(radius=.83,height=3.3,sections=24)
                engine.apply_transform(trimesh.transformations.rotation_matrix(math.pi/2,[0,1,0]))
                engine.apply_translation([.20,side*offset,1.56])
                tag=f'{"right" if side>0 else "left"}-{int(offset)}'
                add('engine-'+tag,engine,(109,121,130,255))
                fan=trimesh.creation.cylinder(radius=.68,height=.025,sections=24)
                fan.apply_transform(trimesh.transformations.rotation_matrix(math.pi/2,[0,1,0]))
                fan.apply_translation([1.87,side*offset,1.56]);add('fan-'+tag,fan,(26,33,38,255))

    out=project_dir(project_name)
    path=out/(vehicle_type+'-blockout.glb')
    path.write_bytes(scene.export(file_type='glb'))
    import json
    info={'file':str(path),'vehicle_type':vehicle_type,'part_count':len(scene.geometry),
          'tier':'BLOCKOUT','accuracy':'silhouette only; not reference-verified CAD',
          'animations':'separate named components; NOT rigged or animated',
          'pbr_textures':False,'tested_in_game_engine':False}
    (out/'vehicle-report.json').write_text(json.dumps(info,indent=2),encoding='utf8')
    return info


def audit_3d(glb_path, max_size_mb=150):
    """Structural audit, not aesthetic approval or runtime profiling."""
    import numpy as np
    import trimesh
    path=Path(glb_path).expanduser().resolve()
    if not path.is_file() or path.suffix.lower()!='.glb':
        raise ValueError('A real GLB file is required')
    if path.stat().st_size>int(max_size_mb)*1024*1024 or int(max_size_mb)<1:
        raise ValueError('GLB exceeds allowed audit size')
    scene=trimesh.load(str(path),force='scene')
    geometry=list(scene.geometry.values())
    if not geometry:raise ValueError('GLB contains no geometry')
    face_count=sum(len(g.faces) for g in geometry)
    issues=[]
    for name,g in scene.geometry.items():
        if not np.isfinite(g.vertices).all():issues.append(f'{name}: non-finite vertex coordinates')
        if len(g.faces)==0:issues.append(f'{name}: empty mesh')
        if len(g.faces)>0 and (g.faces.max()>=len(g.vertices) or g.faces.min()<0):issues.append(f'{name}: invalid face indices')
        if len(g.faces)>0 and np.any(g.area_faces<1e-12):issues.append(f'{name}: degenerate triangles')
    bound=scene.bounds
    if bound is None or not np.isfinite(bound).all():issues.append('invalid global bounds')
    return {'file':str(path),'mesh_count':len(geometry),'triangles':face_count,
            'bounds_m':bound.tolist() if bound is not None else None,
            'structurally_valid':not issues,'issues':issues,
            'visual_fidelity':'NOT TESTED','runtime_fps':'NOT TESTED','collision':'NOT TESTED'}


def create_winter_environment(project_name, tree_count=45, seed=17):
    """Export a genuinely traversable, low-poly winter environment GLB.

    Deliberately blockout tier. No skybox/photogrammetry, alpha foliage,
    collision mesh, navmesh, landscape LODs or GPU FPS assertions.
    """
    import random
    import numpy as np
    import trimesh
    from core import project_dir
    if isinstance(tree_count, bool) or not 1 <= int(tree_count) <= 150:
        raise ValueError('tree_count must be an integer between 1 and 150')
    if isinstance(seed, bool) or not -2**31 <= int(seed) < 2**31:
        raise ValueError('seed out of range')
    random_gen = random.Random(int(seed))
    scene = trimesh.Scene()

    def add(name, mesh, rgba):
        mesh.visual.face_colors = rgba
        scene.add_geometry(mesh, geom_name=name, node_name=name)

    # Wavy terrain with a gentle track corridor between two rows of conifers.
    count = 28
    extent = 54.0
    verts = []
    for iy in range(count + 1):
        y = extent * (iy / count - .5)
        for ix in range(count + 1):
            x = extent * (ix / count - .5)
            z = 0.28 * math.sin(x * .19) * math.cos(y * .15) + .12 * math.sin(x * .43 + y * .16)
            verts.append((x, y, z))
    faces = []
    for iy in range(count):
        for ix in range(count):
            a = iy * (count + 1) + ix
            faces.extend(((a, a + 1, a + count + 2), (a, a + count + 2, a + count + 1)))
    terrain = trimesh.Trimesh(vertices=np.array(verts), faces=np.array(faces), process=True)
    add('snow-terrain', terrain, (211, 224, 239, 255))

    # Raised snow track with two tire ruts; trails are geometry, not decals.
    for track_id, x in enumerate((-1.20, 1.20)):
        road = trimesh.creation.box(extents=(.42, 48.0, .055))
        road.apply_translation((x, 0, .14))
        add(f'compressed-snow-track-{track_id}', road, (160, 181, 207, 255))

    for idx in range(int(tree_count)):
        # Constrain trees outside a visible corridor; no overlap with track.
        side = -1 if idx % 2 == 0 else 1
        x = side * random_gen.uniform(5, 25)
        y = random_gen.uniform(-25, 25)
        height = random_gen.uniform(2.8, 7.3)
        base = .32 * math.sin(x * .19) * math.cos(y * .15)
        trunk = trimesh.creation.cylinder(radius=.095 * height / 5, height=height*.22, sections=8)
        trunk.apply_translation((x, y, base + height*.11))
        add(f'pine-{idx:03d}-trunk', trunk, (87, 62, 51, 255))
        for layer in range(3):
            radius = (height * (.19 - layer*.042))
            cone = trimesh.creation.cone(radius=radius, height=height*.42, sections=9)
            cone.apply_translation((x, y, base + height*(.17 + layer*.225)))
            col = (47, 86 + layer*8, 86 + layer*6, 255)
            add(f'pine-{idx:03d}-foliage-{layer}', cone, col)
            cap = trimesh.creation.cone(radius=radius*.82, height=height*.11, sections=9)
            cap.apply_translation((x, y, base + height*(.17 + layer*.225 + .25)))
            add(f'pine-{idx:03d}-snow-cap-{layer}', cap, (222, 231, 242, 255))

    directory = project_dir(project_name)
    path = directory / 'winter-environment-blockout.glb'
    path.write_bytes(scene.export(file_type='glb'))
    report = {
        'file': str(path), 'tree_count': int(tree_count), 'seed': int(seed),
        'mesh_count': len(scene.geometry), 'tier': 'BLOCKOUT',
        'weather': 'static snowy ground; no simulated snowfall',
        'game_ready': False, 'photoreal': False, 'lod_generated': False,
        'collision_verified': False, 'fps_verified': False,
    }
    (directory / 'winter-report.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    return report
