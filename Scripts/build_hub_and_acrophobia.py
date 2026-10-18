import unreal
import os

print("=== Building Clinic Hub & Checking Acrophobia ===")

editor_level_subsystem = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
editor_actor_subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)

# First check Acrophobia
try:
    editor_level_subsystem.load_level("/Game/PhobiaVR/Maps/L_Sim_Acrophobia")
    acro_actors = editor_actor_subsystem.get_all_level_actors()
    print(f"L_Sim_Acrophobia Actor count: {len(acro_actors)}")
    for a in acro_actors[:6]:
        print(f" - {a.get_actor_label()} ({a.get_class().get_name()})")
except Exception as e:
    print(f"Acrophobia check error: {e}")

# Helper functions
def spawn_sm(mesh_path, loc, rot=unreal.Rotator(0,0,0), scale=unreal.Vector(1,1,1), mat=None, label=None):
    ma = unreal.EditorAssetLibrary.load_asset(mesh_path)
    if not ma:
        print("Mesh not found:", mesh_path)
        return None
    actor = editor_actor_subsystem.spawn_actor_from_class(unreal.StaticMeshActor, loc, rot)
    if actor:
        if label:
            actor.set_actor_label(label)
        smc = actor.static_mesh_component
        smc.set_static_mesh(ma)
        smc.set_world_scale3d(scale)
        if mat:
            mata = unreal.EditorAssetLibrary.load_asset(mat)
            if mata:
                smc.set_material(0, mata)
    return actor

def spawn_pl(loc, intensity=5000.0, color=unreal.LinearColor(1,1,1,1), radius=1000.0, label=None):
    actor = editor_actor_subsystem.spawn_actor_from_class(unreal.PointLight, loc, unreal.Rotator(0,0,0))
    if actor:
        if label:
            actor.set_actor_label(label)
        plc = actor.light_component
        if plc:
            plc.set_intensity(intensity)
            plc.set_light_color(color)
            plc.set_attenuation_radius(radius)
    return actor

def spawn_snd(sound_path, loc, vol=1.0, label=None):
    sa = unreal.EditorAssetLibrary.load_asset(sound_path)
    if not sa:
        return None
    actor = editor_actor_subsystem.spawn_actor_from_class(unreal.AmbientSound, loc, unreal.Rotator(0,0,0))
    if actor:
        if label:
            actor.set_actor_label(label)
        asc = actor.audio_component
        if asc:
            asc.set_sound(sa)
            asc.set_volume_multiplier(vol)
            asc.play()
    return actor

# Rebuild L_PhobiaClinicHub
hub_umap = r"c:\Users\sanja\OneDrive\Desktop\meta 3d\Content\PhobiaVR\Maps\L_PhobiaClinicHub.umap"
if os.path.exists(hub_umap):
    try:
        os.remove(hub_umap)
        print("Removed empty L_PhobiaClinicHub.umap")
    except Exception as e:
        print("Could not remove file:", e)

editor_level_subsystem.new_level("/Game/PhobiaVR/Maps/L_PhobiaClinicHub")

# Sky & Sun
sun_actor = editor_actor_subsystem.spawn_actor_from_class(unreal.DirectionalLight, unreal.Vector(0,0,500), unreal.Rotator(-35, 120, 0))
if sun_actor:
    sun_actor.set_actor_label("Sun_DirectionalLight")
    dlc = sun_actor.light_component
    if dlc:
        dlc.set_intensity(15000.0)
        dlc.set_light_color(unreal.LinearColor(1.0, 0.95, 0.88, 1.0))
        dlc.set_atmosphere_sun_light(True)

editor_actor_subsystem.spawn_actor_from_class(unreal.SkyAtmosphere, unreal.Vector(0,0,0), unreal.Rotator(0,0,0))
editor_actor_subsystem.spawn_actor_from_class(unreal.SkyLight, unreal.Vector(0,0,100), unreal.Rotator(0,0,0))
editor_actor_subsystem.spawn_actor_from_class(unreal.ExponentialHeightFog, unreal.Vector(0,0,0), unreal.Rotator(0,0,0))

# Room geometry
spawn_sm("/Game/Geometry/Meshes/TemplateFloor", unreal.Vector(0, 0, 0), scale=unreal.Vector(2.8, 2.8, 1.0), mat="/Game/Building/Materials/MI_StdOpaque_Concrete", label="Sanctuary_Floor")
spawn_sm("/Game/Building/Geometry/SM_Wall", unreal.Vector(0, 700, 150), scale=unreal.Vector(3.5, 1.0, 1.5), label="Wall_Back")
spawn_sm("/Game/Building/Geometry/SM_Wall", unreal.Vector(-700, 0, 150), rot=unreal.Rotator(0, 90, 0), scale=unreal.Vector(3.5, 1.0, 1.5), label="Wall_Left")
spawn_sm("/Game/Building/Geometry/SM_Wall", unreal.Vector(700, 0, 150), rot=unreal.Rotator(0, -90, 0), scale=unreal.Vector(3.5, 1.0, 1.5), label="Wall_Right")
spawn_sm("/Game/Building/Geometry/SM_FrameWindow", unreal.Vector(0, -700, 150), scale=unreal.Vector(3.5, 1.0, 1.5), mat="/Game/Building/Materials/MI_Simple_Glass_Inst", label="Window_Panorama")

# Garden outside
spawn_sm("/Game/ArchVis/SampleScene/Tree/HillTree_02", unreal.Vector(-400, -1200, 0), scale=unreal.Vector(0.8, 0.8, 0.8), label="Garden_Tree1")
spawn_sm("/Game/ArchVis/SampleScene/Tree/HillTree_02", unreal.Vector(350, -1350, 0), scale=unreal.Vector(0.9, 0.9, 0.9), label="Garden_Tree2")
spawn_sm("/Game/Building/Geometry/SM_Water", unreal.Vector(0, -1200, -20), scale=unreal.Vector(3.0, 3.0, 1.0), mat="/Game/Building/Materials/MI_Water", label="Garden_Water")

# Ceiling & lights
spawn_sm("/Game/Geometry/Meshes/TemplateFloor", unreal.Vector(0, 0, 450), scale=unreal.Vector(2.8, 2.8, 0.5), label="Sanctuary_Ceiling")
spawn_pl(unreal.Vector(0, 0, 400), intensity=12000.0, color=unreal.LinearColor(1.0, 0.92, 0.82, 1.0), radius=900.0, label="Light_CenterWarm")
spawn_pl(unreal.Vector(-350, 350, 380), intensity=6000.0, color=unreal.LinearColor(0.85, 0.9, 1.0, 1.0), radius=600.0, label="Light_CornerSoft1")
spawn_pl(unreal.Vector(350, 350, 380), intensity=6000.0, color=unreal.LinearColor(0.85, 0.9, 1.0, 1.0), radius=600.0, label="Light_CornerSoft2")

# Central Therapy Dais
spawn_sm("/Game/Geometry/Meshes/1M_Cube_Chamfer", unreal.Vector(0, 0, 5), scale=unreal.Vector(2.5, 2.5, 0.1), mat="/Game/XRFramework/Materials/MI_Grid_Accent", label="Central_Therapy_Platform")

# 4 Holographic Scenario Portals
spawn_sm("/Game/ArchVis/SampleScene/Building/Meshes/Door_01_L", unreal.Vector(-350, 600, 10), scale=unreal.Vector(1.2, 1.2, 1.2), label="Portal_Acrophobia_Heights")
spawn_pl(unreal.Vector(-350, 580, 220), intensity=4000.0, color=unreal.LinearColor(0.2, 0.7, 1.0, 1.0), radius=350.0, label="Light_Portal_Acrophobia")

spawn_sm("/Game/ArchVis/SampleScene/Building/Meshes/Door_01_L", unreal.Vector(-120, 600, 10), scale=unreal.Vector(1.2, 1.2, 1.2), label="Portal_Arachnophobia_Spiders")
spawn_pl(unreal.Vector(-120, 580, 220), intensity=4000.0, color=unreal.LinearColor(0.8, 0.4, 0.1, 1.0), radius=350.0, label="Light_Portal_Arachnophobia")

spawn_sm("/Game/ArchVis/SampleScene/Building/Meshes/Door_01_L", unreal.Vector(120, 600, 10), scale=unreal.Vector(1.2, 1.2, 1.2), label="Portal_Claustrophobia_Elevator")
spawn_pl(unreal.Vector(120, 580, 220), intensity=4000.0, color=unreal.LinearColor(1.0, 0.2, 0.2, 1.0), radius=350.0, label="Light_Portal_Claustrophobia")

spawn_sm("/Game/ArchVis/SampleScene/Building/Meshes/Door_01_L", unreal.Vector(350, 600, 10), scale=unreal.Vector(1.2, 1.2, 1.2), label="Portal_Glossophobia_Auditorium")
spawn_pl(unreal.Vector(350, 580, 220), intensity=4000.0, color=unreal.LinearColor(0.9, 0.8, 0.2, 1.0), radius=350.0, label="Light_Portal_Glossophobia")

# Grabbable Cubes
spawn_sm("/Game/Geometry/Meshes/1M_Cube", unreal.Vector(-200, 100, 40), scale=unreal.Vector(0.8, 1.2, 0.8), mat="/Game/Building/Materials/MI_StdOpaque_Brushed", label="Table_StressRelief")
grabbable_bp = unreal.EditorAssetLibrary.load_blueprint_class("/Game/XRFramework/Blueprints/BP_Grabbable_SmallCube")
if grabbable_bp:
    c1 = editor_actor_subsystem.spawn_actor_from_class(grabbable_bp, unreal.Vector(-200, 80, 85), unreal.Rotator(0,0,0))
    if c1:
        c1.set_actor_label("Grabbable_CalmCube1")
    c2 = editor_actor_subsystem.spawn_actor_from_class(grabbable_bp, unreal.Vector(-200, 120, 85), unreal.Rotator(0,0,0))
    if c2:
        c2.set_actor_label("Grabbable_CalmCube2")

# Ambient Zen Audio
spawn_snd("/Game/PhobiaVR/Audio/A_ZenChime_Safe", unreal.Vector(0, 0, 200), vol=0.8, label="Audio_ZenChime")

# Player Start
ps = editor_actor_subsystem.spawn_actor_from_class(unreal.PlayerStart, unreal.Vector(0, 0, 30), unreal.Rotator(0, 90, 0))
if ps:
    ps.set_actor_label("PlayerStart_VR")

unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
hub_actors = editor_actor_subsystem.get_all_level_actors()
print(f"L_PhobiaClinicHub rebuilt! Total actors: {len(hub_actors)}")
print("=== Rebuild Complete ===")
