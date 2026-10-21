import unreal
import os
import json

print("==========================================================")
print("  PhobiaVR: Building Universal Phobia Holochamber Matrix  ")
print("==========================================================")

editor_level_subsystem = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
editor_actor_subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)

# 1. Import new audio assets
wav_files = [
    ("c:/Users/sanja/OneDrive/Desktop/meta 3d/Content/PhobiaVR/Audio/A_Thalassophobia_Abyss_Sonar.wav", "/Game/PhobiaVR/Audio"),
    ("c:/Users/sanja/OneDrive/Desktop/meta 3d/Content/PhobiaVR/Audio/A_Nyctophobia_Whispering_Dark.wav", "/Game/PhobiaVR/Audio"),
    ("c:/Users/sanja/OneDrive/Desktop/meta 3d/Content/PhobiaVR/Audio/A_Automaton_MusicBox_Creep.wav", "/Game/PhobiaVR/Audio"),
    ("c:/Users/sanja/OneDrive/Desktop/meta 3d/Content/PhobiaVR/Audio/A_Megalophobia_Titan_Drone.wav", "/Game/PhobiaVR/Audio"),
]

tasks = []
for filename, dest_path in wav_files:
    task = unreal.AssetImportTask()
    task.set_editor_property('filename', filename)
    task.set_editor_property('destination_path', dest_path)
    task.set_editor_property('destination_name', '')
    task.set_editor_property('replace_existing', True)
    task.set_editor_property('automated', True)
    task.set_editor_property('save', True)
    tasks.append(task)

unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)
print("[Audio] Imported Thalassophobia, Nyctophobia, Automatonophobia, Megalophobia cues.")

# Helper functions
def create_or_clean_level(level_path):
    if unreal.EditorAssetLibrary.does_asset_exist(level_path):
        editor_level_subsystem.load_level(level_path)
        actors = editor_actor_subsystem.get_all_level_actors()
        for a in actors:
            editor_actor_subsystem.destroy_actor(a)
    else:
        editor_level_subsystem.new_level(level_path)

def save_current_level():
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)

def spawn_sm(mesh_path, loc, rot=unreal.Rotator(0,0,0), scale=unreal.Vector(1,1,1), mat=None, label=None, sim_physics=False, mass_kg=0.0):
    mesh_asset = unreal.EditorAssetLibrary.load_asset(mesh_path)
    if not mesh_asset:
        return None
    actor = editor_actor_subsystem.spawn_actor_from_class(unreal.StaticMeshActor, loc, rot)
    if actor:
        if label:
            actor.set_actor_label(label)
        smc = actor.static_mesh_component
        smc.set_static_mesh(mesh_asset)
        smc.set_world_scale3d(scale)
        if mat:
            mat_asset = unreal.EditorAssetLibrary.load_asset(mat)
            if mat_asset:
                smc.set_material(0, mat_asset)
        if sim_physics:
            smc.set_mobility(unreal.ComponentMobility.MOVABLE)
            smc.set_simulate_physics(True)
            smc.set_enable_gravity(True)
            smc.set_collision_profile_name("PhysicsActor")
            if mass_kg > 0:
                smc.set_mass_override_in_kg(unreal.Name(), mass_kg, True)
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

def spawn_snd(sound_path, loc, vol=1.0, is_ui=False, label=None):
    sound_asset = unreal.EditorAssetLibrary.load_asset(sound_path)
    if not sound_asset:
        return None
    actor = editor_actor_subsystem.spawn_actor_from_class(unreal.AmbientSound, loc, unreal.Rotator(0,0,0))
    if actor:
        if label:
            actor.set_actor_label(label)
        asc = actor.audio_component
        if asc:
            asc.set_sound(sound_asset)
            asc.set_volume_multiplier(vol)
            asc.set_ui_sound(is_ui)
            asc.play()
    return actor

# ------------------------------------------------------------------------------
# BUILD L_Sim_Holochamber
# ------------------------------------------------------------------------------
level_path = "/Game/PhobiaVR/Maps/L_Sim_Holochamber"
print(f"---> Building Universal Holochamber: {level_path}")
create_or_clean_level(level_path)

# 1. Sky & Void
editor_actor_subsystem.spawn_actor_from_class(unreal.SkyAtmosphere, unreal.Vector(0,0,0), unreal.Rotator(0,0,0))
fog = editor_actor_subsystem.spawn_actor_from_class(unreal.ExponentialHeightFog, unreal.Vector(0,0,0), unreal.Rotator(0,0,0))
if fog:
    fc = fog.get_component_by_class(unreal.ExponentialHeightFogComponent)
    if fc:
        fc.set_editor_property("fog_density", 0.03)

# 2. Hexagonal Modular Holodeck Chamber
spawn_sm("/Game/Geometry/Meshes/TemplateFloor", unreal.Vector(0, 0, 0), scale=unreal.Vector(3.0, 3.0, 1.0), mat="/Game/XRFramework/Materials/MI_Grid_Accent", label="Holodeck_Matrix_Floor")
spawn_sm("/Game/Building/Geometry/SM_Wall", unreal.Vector(0, 800, 200), scale=unreal.Vector(4.0, 1.0, 2.0), mat="/Game/Building/Materials/MI_StdOpaque_Concrete", label="Holodeck_Wall_North")
spawn_sm("/Game/Building/Geometry/SM_Wall", unreal.Vector(0, -800, 200), scale=unreal.Vector(4.0, 1.0, 2.0), mat="/Game/Building/Materials/MI_StdOpaque_Concrete", label="Holodeck_Wall_South")
spawn_sm("/Game/Building/Geometry/SM_Wall", unreal.Vector(-800, 0, 200), rot=unreal.Rotator(0, 90, 0), scale=unreal.Vector(4.0, 1.0, 2.0), mat="/Game/Building/Materials/MI_StdOpaque_Concrete", label="Holodeck_Wall_West")
spawn_sm("/Game/Building/Geometry/SM_Wall", unreal.Vector(800, 0, 200), rot=unreal.Rotator(0, -90, 0), scale=unreal.Vector(4.0, 1.0, 2.0), mat="/Game/Building/Materials/MI_StdOpaque_Concrete", label="Holodeck_Wall_East")
spawn_sm("/Game/Geometry/Meshes/TemplateFloor", unreal.Vector(0, 0, 500), scale=unreal.Vector(3.0, 3.0, 0.5), mat="/Game/Building/Materials/MI_StdOpaque_Concrete", label="Holodeck_Ceiling")

# 3. Master Phobia Registry Terminal Console
spawn_sm("/Game/Geometry/Meshes/1M_Cube_Chamfer", unreal.Vector(0, 350, 50), scale=unreal.Vector(1.2, 0.8, 1.0), mat="/Game/Building/Materials/MI_StdOpaque_Brushed", label="Holodeck_Console_Base")
spawn_sm("/Game/Building/Geometry/SM_FrameWindow", unreal.Vector(0, 350, 130), rot=unreal.Rotator(-30, 0, 0), scale=unreal.Vector(0.8, 0.8, 0.4), mat="/Game/XRFramework/Materials/MI_Grid_Accent", label="Holodeck_Hologram_Screen")
spawn_pl(unreal.Vector(0, 350, 170), intensity=6000.0, color=unreal.LinearColor(0.2, 0.8, 1.0, 1.0), radius=400.0, label="Light_Terminal_Glow")

# 4. SHOWCASE PHOBIA MODULES INSIDE HOLOCHAMBER:

# Module A: Thalassophobia (Deep Ocean Trench & Leviathan Shadow)
spawn_sm("/Game/Building/Geometry/SM_Water", unreal.Vector(-400, -200, 10), scale=unreal.Vector(1.5, 1.5, 1.0), mat="/Game/Building/Materials/MI_Water", label="Holodeck_Thalassophobia_Pool")
spawn_sm("/Game/Building/Geometry/SM_Land", unreal.Vector(-400, -200, -300), scale=unreal.Vector(0.8, 0.8, 10.0), mat="/Game/Building/Materials/MI_Silhouette", label="Leviathan_Deep_Silhouette")
spawn_pl(unreal.Vector(-400, -200, 80), intensity=2500.0, color=unreal.LinearColor(0.05, 0.3, 0.6, 1.0), radius=500.0, label="Light_AbyssBlue")
spawn_snd("/Game/PhobiaVR/Audio/A_Thalassophobia_Abyss_Sonar", unreal.Vector(-400, -200, 80), vol=0.9, label="Audio_Thalassophobia")

# Module B: Automatonophobia / Coulrophobia (The Staring Mannequins)
spawn_sm("/Game/Building/Geometry/SM_SilhouetteWomen", unreal.Vector(400, -200, 30), rot=unreal.Rotator(0, 135, 0), scale=unreal.Vector(1.1, 1.1, 1.1), mat="/Game/Building/Materials/MI_StdOpaque_Concrete", label="Mannequin_Watcher_1")
spawn_sm("/Game/Building/Geometry/SM_SilhouetteWomen", unreal.Vector(480, -120, 30), rot=unreal.Rotator(0, 150, 0), scale=unreal.Vector(1.1, 1.1, 1.1), mat="/Game/Building/Materials/MI_StdOpaque_Concrete", label="Mannequin_Watcher_2")
spawn_pl(unreal.Vector(400, -200, 150), intensity=3000.0, color=unreal.LinearColor(1.0, 0.85, 0.6, 1.0), radius=450.0, label="Light_Mannequin_Spot")
spawn_snd("/Game/PhobiaVR/Audio/A_Automaton_MusicBox_Creep", unreal.Vector(400, -200, 100), vol=0.85, label="Audio_MusicBox")

# Module C: Megalophobia (Colossal Monolithic Titan Pillar)
spawn_sm("/Game/Geometry/Meshes/1M_Cube", unreal.Vector(0, -550, 200), scale=unreal.Vector(1.0, 1.0, 8.0), mat="/Game/Building/Materials/MI_Silhouette", label="Megalophobia_Colossal_Monolith")
spawn_snd("/Game/PhobiaVR/Audio/A_Megalophobia_Titan_Drone", unreal.Vector(0, -550, 200), vol=0.8, label="Audio_TitanDrone")

# Module D: Nyctophobia (Sensory Deprivation Darkness Alcove)
spawn_sm("/Game/Geometry/Meshes/1M_Cube", unreal.Vector(-650, 200, 150), scale=unreal.Vector(2.0, 2.0, 3.0), mat="/Game/Building/Materials/MI_Silhouette", label="Nyctophobia_Blackout_Booth")
spawn_snd("/Game/PhobiaVR/Audio/A_Nyctophobia_Whispering_Dark", unreal.Vector(-650, 200, 100), vol=0.85, label="Audio_DarknessWhispers")

# 5. Physics Interactive Props inside the Holochamber
holodeck_props = [
    ("/Game/Geometry/Meshes/1M_Cube_Chamfer", unreal.Vector(-150, 200, 30), unreal.Vector(0.3, 0.3, 0.3), 5.0, "Phys_Holodeck_Cube1"),
    ("/Game/Geometry/Meshes/1M_Cube_Chamfer", unreal.Vector(150, 200, 30), unreal.Vector(0.3, 0.3, 0.3), 5.0, "Phys_Holodeck_Cube2"),
    ("/Engine/BasicShapes/Sphere", unreal.Vector(0, 100, 30), unreal.Vector(0.35, 0.35, 0.35), 2.0, "Phys_Holodeck_Sphere"),
    ("/Game/Geometry/Meshes/1M_Cube", unreal.Vector(250, 100, 20), unreal.Vector(0.2, 0.6, 0.1), 8.0, "Phys_Holodeck_Barricade")
]
for m, loc, scl, mass, lbl in holodeck_props:
    spawn_sm(m, loc, scale=scl, mat="/Game/XRFramework/Materials/MI_Grid_Accent", label=lbl, sim_physics=True, mass_kg=mass)

# 6. General Lighting & Ambience
spawn_pl(unreal.Vector(0, 0, 420), intensity=8000.0, color=unreal.LinearColor(0.8, 0.9, 1.0, 1.0), radius=900.0, label="Light_Holodeck_Ambient")
spawn_snd("/Game/PhobiaVR/Audio/A_Horror_Drone_Ominous", unreal.Vector(0, 0, 200), vol=0.6, label="Audio_Matrix_Background")

# Player Start
ps = editor_actor_subsystem.spawn_actor_from_class(unreal.PlayerStart, unreal.Vector(0, 0, 30), unreal.Rotator(0, 90, 0))
if ps:
    ps.set_actor_label("PlayerStart_VR")

save_current_level()
print("Universal Phobia Holochamber level built successfully!")
