import unreal
import math
import random

print("==========================================================")
print("  PhobiaVR: Injecting Realistic Physics & Horror Terrors  ")
print("==========================================================")

editor_level_subsystem = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
editor_actor_subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)

# ------------------------------------------------------------------------------
# STEP 1: IMPORT SCARY AUDIO ASSETS
# ------------------------------------------------------------------------------
wav_files = [
    ("c:/Users/sanja/OneDrive/Desktop/meta 3d/Content/PhobiaVR/Audio/A_Horror_Drone_Ominous.wav", "/Game/PhobiaVR/Audio"),
    ("c:/Users/sanja/OneDrive/Desktop/meta 3d/Content/PhobiaVR/Audio/A_Jumpscare_Violin_Shriek.wav", "/Game/PhobiaVR/Audio"),
    ("c:/Users/sanja/OneDrive/Desktop/meta 3d/Content/PhobiaVR/Audio/A_Cable_Snap_Crash.wav", "/Game/PhobiaVR/Audio"),
    ("c:/Users/sanja/OneDrive/Desktop/meta 3d/Content/PhobiaVR/Audio/A_Spider_Swarm_Frenzy.wav", "/Game/PhobiaVR/Audio"),
    ("c:/Users/sanja/OneDrive/Desktop/meta 3d/Content/PhobiaVR/Audio/A_Vertigo_Abyss_Wind.wav", "/Game/PhobiaVR/Audio"),
    ("c:/Users/sanja/OneDrive/Desktop/meta 3d/Content/PhobiaVR/Audio/A_Whispers_Paranoia_Loop.wav", "/Game/PhobiaVR/Audio"),
    ("c:/Users/sanja/OneDrive/Desktop/meta 3d/Content/PhobiaVR/Audio/A_Tachycardia_Suffocation.wav", "/Game/PhobiaVR/Audio"),
]

import_tasks = []
for filename, dest_path in wav_files:
    task = unreal.AssetImportTask()
    task.set_editor_property('filename', filename)
    task.set_editor_property('destination_path', dest_path)
    task.set_editor_property('destination_name', '')
    task.set_editor_property('replace_existing', True)
    task.set_editor_property('automated', True)
    task.set_editor_property('save', True)
    import_tasks.append(task)

unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(import_tasks)
print("[Audio] Imported all 7 horror audio tracks into /Game/PhobiaVR/Audio.")

# ------------------------------------------------------------------------------
# HELPER FUNCTIONS
# ------------------------------------------------------------------------------
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

def spawn_spot(loc, rot, intensity=25000.0, color=unreal.LinearColor(1,1,1,1), outer_angle=45.0, inner_angle=25.0, radius=3000.0, label=None):
    actor = editor_actor_subsystem.spawn_actor_from_class(unreal.SpotLight, loc, rot)
    if actor:
        if label:
            actor.set_actor_label(label)
        slc = actor.light_component
        if slc:
            slc.set_intensity(intensity)
            slc.set_light_color(color)
            slc.set_outer_cone_angle(outer_angle)
            slc.set_inner_cone_angle(inner_angle)
            slc.set_attenuation_radius(radius)
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

def spawn_ps(loc, rot=unreal.Rotator(0,0,0)):
    actor = editor_actor_subsystem.spawn_actor_from_class(unreal.PlayerStart, loc, rot)
    if actor:
        actor.set_actor_label("PlayerStart_VR")
    return actor

def spawn_grabbable(loc, label=None):
    bp_class = unreal.EditorAssetLibrary.load_blueprint_class("/Game/XRFramework/Blueprints/BP_Grabbable_SmallCube")
    if bp_class:
        actor = editor_actor_subsystem.spawn_actor_from_class(bp_class, loc, unreal.Rotator(0,0,0))
        if actor and label:
            actor.set_actor_label(label)
        return actor
    return None

# ==============================================================================
# 1. ACROPHOBIA: NIGHT STORM & REALISTIC GRAVITY DROP PHYSICS (200M DROP)
# ==============================================================================
def upgrade_acrophobia():
    level_path = "/Game/PhobiaVR/Maps/L_Sim_Acrophobia"
    print(f"\n---> Upgrading Acrophobia: Physics Tumbling & Vertigo Abyss ({level_path})")
    create_or_clean_level(level_path)

    tower_z = 20000.0 # 200 meters elevation
    
    # Night Storm Directional Light (Blood moon / stormy moonlight)
    sun_actor = editor_actor_subsystem.spawn_actor_from_class(unreal.DirectionalLight, unreal.Vector(0,0,tower_z + 1000), unreal.Rotator(-40.0, 190.0, 0))
    if sun_actor:
        sun_actor.set_actor_label("Storm_Moonlight")
        dlc = sun_actor.light_component
        if dlc:
            dlc.set_intensity(1800.0)
            dlc.set_light_color(unreal.LinearColor(0.2, 0.25, 0.45, 1.0))
            dlc.set_atmosphere_sun_light(True)

    editor_actor_subsystem.spawn_actor_from_class(unreal.SkyAtmosphere, unreal.Vector(0,0,0), unreal.Rotator(0,0,0))
    editor_actor_subsystem.spawn_actor_from_class(unreal.SkyLight, unreal.Vector(0,0,tower_z), unreal.Rotator(0,0,0))
    
    # Sinister dark blue / purple abyssal fog
    fog = editor_actor_subsystem.spawn_actor_from_class(unreal.ExponentialHeightFog, unreal.Vector(0,0,0), unreal.Rotator(0,0,0))
    if fog:
        fog.set_actor_label("Abyss_HeightFog")
        fc = fog.get_component_by_class(unreal.ExponentialHeightFogComponent)
        if fc:
            fc.set_editor_property("fog_density", 0.04)

    # 1. Tower Core
    spawn_sm("/Game/Building/Geometry/SM_Land", unreal.Vector(0, 0, tower_z / 2), scale=unreal.Vector(2.0, 2.0, 40.0), mat="/Game/Building/Materials/MI_StdOpaque_Concrete", label="Skyscraper_Core")

    # 2. Rooftop Platform & Dilapidated Wall
    spawn_sm("/Game/Geometry/Meshes/TemplateFloor", unreal.Vector(0, 300, tower_z), scale=unreal.Vector(1.5, 1.5, 1.0), mat="/Game/Building/Materials/MI_StdOpaque_Concrete_Ground", label="Rooftop_Floor")
    spawn_sm("/Game/Building/Geometry/SM_Wall", unreal.Vector(0, 600, tower_z + 150), scale=unreal.Vector(2.5, 1.0, 1.5), label="Rooftop_BackWall")
    spawn_sm("/Game/Building/Geometry/SM_Wall", unreal.Vector(-350, 300, tower_z + 150), rot=unreal.Rotator(0, 90, 0), scale=unreal.Vector(2.0, 1.0, 1.5), label="Rooftop_LeftWall")
    spawn_sm("/Game/Building/Geometry/SM_Wall", unreal.Vector(350, 300, tower_z + 150), rot=unreal.Rotator(0, -90, 0), scale=unreal.Vector(2.0, 1.0, 1.5), label="Rooftop_RightWall")

    # 3. Observation Railings
    spawn_sm("/Game/ArchVis/SampleScene/Building/Meshes/Railing_001", unreal.Vector(-180, 0, tower_z + 50), scale=unreal.Vector(1.0, 1.0, 1.0), label="Railing_Left")
    spawn_sm("/Game/ArchVis/SampleScene/Building/Meshes/Railing_001", unreal.Vector(180, 0, tower_z + 50), scale=unreal.Vector(1.0, 1.0, 1.0), label="Railing_Right")

    # 4. THE NARROW VERTIGO PLANK (Extending 6 meters into the black void)
    spawn_sm("/Game/Geometry/Meshes/1M_Cube", unreal.Vector(0, -300, tower_z - 5), scale=unreal.Vector(0.36, 6.0, 0.1), mat="/Game/Building/Materials/MI_StdOpaque_Brushed", label="The_Vertigo_Plank")
    spawn_sm("/Game/Geometry/Meshes/1M_Cube_Chamfer", unreal.Vector(0, -600, tower_z), scale=unreal.Vector(0.5, 0.5, 0.1), mat="/Game/XRFramework/Materials/MI_Grid_Accent", label="Plank_Tip_Platform")

    # 5. REAL PHYSICS DROP PROPS (Physics enabled, gravity enabled, high mass)
    # The user can push, grab, or kick these off the rooftop and watch them plummet 200m!
    drop_props = [
        # Paint cans on the edge
        ("/Game/Geometry/Meshes/1M_Cube_Chamfer", unreal.Vector(-50, 20, tower_z + 20), unreal.Vector(0.25, 0.25, 0.35), 4.5, "Phys_PaintCan_Edge1"),
        ("/Game/Geometry/Meshes/1M_Cube_Chamfer", unreal.Vector(50, 15, tower_z + 20), unreal.Vector(0.25, 0.25, 0.35), 4.5, "Phys_PaintCan_Edge2"),
        # Steel toolboxes
        ("/Game/Geometry/Meshes/1M_Cube", unreal.Vector(-120, 100, tower_z + 20), unreal.Vector(0.4, 0.25, 0.2), 12.0, "Phys_SteelToolbox"),
        # Loose concrete cinderblocks balanced on the plank and edge
        ("/Game/Geometry/Meshes/1M_Cube", unreal.Vector(0, -100, tower_z + 15), unreal.Vector(0.2, 0.35, 0.15), 18.0, "Phys_CinderBlock_Plank"),
        ("/Game/Geometry/Meshes/1M_Cube", unreal.Vector(-15, -450, tower_z + 15), unreal.Vector(0.15, 0.25, 0.12), 14.0, "Phys_CinderBlock_PlankTip"),
        # Rolling physics pipes/spheres that roll into the void when touched
        ("/Game/Building/Geometry/SM_SphereSky", unreal.Vector(-30, 50, tower_z + 25), unreal.Vector(0.0004, 0.0004, 0.0004), 2.0, "Phys_RollingSphere_Edge1"),
        ("/Game/Building/Geometry/SM_SphereSky", unreal.Vector(30, -50, tower_z + 25), unreal.Vector(0.0003, 0.0003, 0.0003), 1.5, "Phys_RollingSphere_Edge2"),
        # Scaffolding Timber Plank balanced over the abyss
        ("/Game/Geometry/Meshes/1M_Cube", unreal.Vector(-80, -50, tower_z + 10), unreal.Vector(0.25, 2.2, 0.06), 9.0, "Phys_TeeteringPlank_Edge")
    ]
    for mesh_p, loc, scl, mass, lbl in drop_props:
        spawn_sm(mesh_p, loc, scale=scl, mat="/Game/Building/Materials/MI_StdOpaque_Brushed", label=lbl, sim_physics=True, mass_kg=mass)

    # 6. Grabbable VR cubes
    spawn_grabbable(unreal.Vector(0, 50, tower_z + 30), label="Grabbable_Edge_Cube")
    spawn_grabbable(unreal.Vector(0, -580, tower_z + 30), label="Grabbable_PlankTip_Cube")

    # 7. Red Beacon Lights on Rooftop Corners
    spawn_pl(unreal.Vector(-340, 580, tower_z + 300), intensity=6000.0, color=unreal.LinearColor(1.0, 0.05, 0.02, 1.0), radius=500.0, label="AviationBeacon_Left")
    spawn_pl(unreal.Vector(340, 580, tower_z + 300), intensity=6000.0, color=unreal.LinearColor(1.0, 0.05, 0.02, 1.0), radius=500.0, label="AviationBeacon_Right")

    # 8. Distant Cityscape with eerie dark silhouettes
    spawn_sm("/Game/Building/Geometry/SM_Land", unreal.Vector(0, -1000, 0), scale=unreal.Vector(30.0, 30.0, 1.0), mat="/Game/Building/Materials/MI_Road", label="City_Ground_Plane")
    tower_coords = [
        (-2500, -2000, 12000), (2800, -2400, 14000),
        (-3500, 1500, 16000), (3200, 2000, 11000),
        (-1500, -4500, 9000), (1200, -5000, 13000),
    ]
    for idx, (tx, ty, tz) in enumerate(tower_coords):
        spawn_sm("/Game/Building/Geometry/SM_Land", unreal.Vector(tx, ty, tz / 2), scale=unreal.Vector(1.2, 1.2, tz / 1000.0), mat="/Game/Building/Materials/MI_StdOpaque_Concrete", label=f"Distant_Tower_{idx+1}")

    # 9. Terrifying Eerie Audio Suite (Shepard Vertigo Wind + Horror Drone + Shock Stinger)
    spawn_snd("/Game/PhobiaVR/Audio/A_Vertigo_Abyss_Wind", unreal.Vector(0, -300, tower_z + 100), vol=1.0, label="Audio_VertigoAbyssWind")
    spawn_snd("/Game/PhobiaVR/Audio/A_Horror_Drone_Ominous", unreal.Vector(0, 0, tower_z + 50), vol=0.85, label="Audio_HorrorDrone")
    spawn_snd("/Game/PhobiaVR/Audio/A_Jumpscare_Violin_Shriek", unreal.Vector(0, -600, tower_z + 50), vol=0.75, label="Audio_PlankEdgeStinger")

    spawn_ps(unreal.Vector(0, 250, tower_z + 20), unreal.Rotator(0, -90, 0))
    save_current_level()
    print("Acrophobia level rebuilt with tumbling physics & eerie terror ambiance.")

# ==============================================================================
# 2. CLAUSTROPHOBIA: VIOLENT CABLE SNAP, SHAKING CABIN & SUFFOCATION PANIC
# ==============================================================================
def upgrade_claustrophobia():
    level_path = "/Game/PhobiaVR/Maps/L_Sim_Claustrophobia"
    print(f"\n---> Upgrading Claustrophobia: Elevator Cable Snap & Severe Panic ({level_path})")
    create_or_clean_level(level_path)

    # 1. Enclosed Claustrophobic Elevator Cabin (2m x 2m x 2.4m)
    spawn_sm("/Game/Geometry/Meshes/TemplateFloor", unreal.Vector(0, 0, 0), scale=unreal.Vector(0.45, 0.45, 1.0), mat="/Game/Building/Materials/MI_StdOpaque_Brushed", label="Elevator_Floor")
    spawn_sm("/Game/Building/Geometry/SM_Wall", unreal.Vector(0, 110, 120), scale=unreal.Vector(0.55, 0.5, 1.2), mat="/Game/Building/Materials/MI_StdOpaque_Brushed", label="Elevator_Wall_Back")
    spawn_sm("/Game/Building/Geometry/SM_Wall", unreal.Vector(0, -110, 120), scale=unreal.Vector(0.55, 0.5, 1.2), mat="/Game/Building/Materials/MI_StdOpaque_Brushed", label="Elevator_Wall_Door")
    spawn_sm("/Game/Building/Geometry/SM_Wall", unreal.Vector(-110, 0, 120), rot=unreal.Rotator(0, 90, 0), scale=unreal.Vector(0.55, 0.5, 1.2), mat="/Game/Building/Materials/MI_StdOpaque_Brushed", label="Elevator_Wall_Left")
    spawn_sm("/Game/Building/Geometry/SM_Wall", unreal.Vector(110, 0, 120), rot=unreal.Rotator(0, -90, 0), scale=unreal.Vector(0.55, 0.5, 1.2), mat="/Game/Building/Materials/MI_StdOpaque_Brushed", label="Elevator_Wall_Right")
    spawn_sm("/Game/Geometry/Meshes/TemplateFloor", unreal.Vector(0, 0, 230), scale=unreal.Vector(0.45, 0.45, 0.2), mat="/Game/Building/Materials/MI_StdOpaque_Brushed", label="Elevator_Ceiling")

    # 2. Control Panel with jammed buttons
    spawn_sm("/Game/Geometry/Meshes/1M_Cube_Chamfer", unreal.Vector(95, -20, 110), scale=unreal.Vector(0.05, 0.2, 0.5), mat="/Game/XRFramework/Materials/MI_Grid_Accent", label="Elevator_Control_Panel")

    # 3. REAL PHYSICS LOOSE ITEMS INSIDE CABIN
    # When the elevator drops or shudders, these items get kicked and bounce on the floor!
    spawn_sm("/Game/Geometry/Meshes/1M_Cube", unreal.Vector(30, 40, 15), scale=unreal.Vector(0.12, 0.35, 0.08), mat="/Game/Building/Materials/MI_Simple_Chrome", label="Phys_HeavyWrench", sim_physics=True, mass_kg=3.0)
    spawn_sm("/Game/Geometry/Meshes/1M_Cube_Chamfer", unreal.Vector(-40, 30, 15), scale=unreal.Vector(0.15, 0.15, 0.25), mat="/Game/Building/Materials/MI_StdOpaque_Brushed", label="Phys_EmergencyFlashlight", sim_physics=True, mass_kg=1.2)
    spawn_sm("/Game/Geometry/Meshes/1M_Cube", unreal.Vector(50, -40, 10), scale=unreal.Vector(0.25, 0.35, 0.02), mat="/Game/Building/Materials/MI_StdOpaque_Concrete", label="Phys_Clipboard_Dropped", sim_physics=True, mass_kg=0.6)
    spawn_sm("/Game/Building/Geometry/SM_SphereSky", unreal.Vector(-30, -30, 15), scale=unreal.Vector(0.0002, 0.0002, 0.0002), mat="/Game/Building/Materials/MI_Simple_Chrome", label="Phys_RollingSodaCan", sim_physics=True, mass_kg=0.35)

    # 4. Falling Ceiling Grates & Debris (Dislodged when cable snaps)
    spawn_sm("/Game/Geometry/Meshes/1M_Cube", unreal.Vector(0, 10, 215), scale=unreal.Vector(0.35, 0.35, 0.04), mat="/Game/Building/Materials/MI_StdOpaque_Brushed", label="Phys_CeilingPanel_Loose", sim_physics=True, mass_kg=5.0)

    # 5. Terrifying Emergency Strobe & Pitch Black Shaft
    spawn_point_light = spawn_pl
    spawn_point_light(unreal.Vector(0, 0, 215), intensity=300.0, color=unreal.LinearColor(0.2, 0.2, 0.2, 1.0), radius=200.0, label="Light_FailingOverhead")
    # Blood-red flashing emergency beacon
    spawn_point_light(unreal.Vector(70, -20, 205), intensity=5000.0, color=unreal.LinearColor(1.0, 0.02, 0.01, 1.0), radius=350.0, label="Light_EmergencyBeacon_BloodRed")

    # Shaft below and above
    spawn_sm("/Game/Building/Geometry/SM_Land", unreal.Vector(0, 0, -800), scale=unreal.Vector(1.0, 1.0, 25.0), mat="/Game/Building/Materials/MI_StdOpaque_Concrete", label="Elevator_Shaft_Void")

    # 6. Eerie Horror Audio Suite: Catastrophic Cable Snap, Freefall Crash & Tachycardia Suffocation
    spawn_snd("/Game/PhobiaVR/Audio/A_Cable_Snap_Crash", unreal.Vector(0, 0, 225), vol=1.0, label="Audio_CableSnapCrash")
    spawn_snd("/Game/PhobiaVR/Audio/A_Tachycardia_Suffocation", unreal.Vector(0, 0, 120), vol=0.95, label="Audio_PanicSuffocation")
    spawn_snd("/Game/PhobiaVR/Audio/A_Whispers_Paranoia_Loop", unreal.Vector(0, -110, 120), vol=0.6, label="Audio_ShaftWhispers")

    spawn_ps(unreal.Vector(0, 0, 20), unreal.Rotator(0, -90, 0))
    save_current_level()
    print("Claustrophobia level rebuilt with violent cable snap physics & suffocation audio.")

# ==============================================================================
# 3. ARACHNOPHOBIA: PHYSICS CHEMICAL VIALS, SHATTERING GLASS & SWARM TERROR
# ==============================================================================
def upgrade_arachnophobia():
    level_path = "/Game/PhobiaVR/Maps/L_Sim_Arachnophobia"
    print(f"\n---> Upgrading Arachnophobia: Physics Terrarium & Chitin Swarm Frenzy ({level_path})")
    create_or_clean_level(level_path)

    # 1. Abandoned Dilapidated Lab Room
    spawn_sm("/Game/Geometry/Meshes/TemplateFloor", unreal.Vector(0, 0, 0), scale=unreal.Vector(1.4, 1.4, 1.0), mat="/Game/Building/Materials/MI_StdOpaque_Concrete", label="Lab_Floor")
    spawn_sm("/Game/Building/Geometry/SM_Wall", unreal.Vector(0, 350, 150), scale=unreal.Vector(1.8, 1.0, 1.5), label="Lab_Wall_Back")
    spawn_sm("/Game/Building/Geometry/SM_Wall", unreal.Vector(-350, 0, 150), rot=unreal.Rotator(0, 90, 0), scale=unreal.Vector(1.8, 1.0, 1.5), label="Lab_Wall_Left")
    spawn_sm("/Game/Building/Geometry/SM_Wall", unreal.Vector(350, 0, 150), rot=unreal.Rotator(0, -90, 0), scale=unreal.Vector(1.8, 1.0, 1.5), label="Lab_Wall_Right")
    spawn_sm("/Game/Geometry/Meshes/TemplateFloor", unreal.Vector(0, 0, 320), scale=unreal.Vector(1.4, 1.4, 0.2), label="Lab_Ceiling")

    # 2. Central Steel Lab Table
    spawn_sm("/Game/Geometry/Meshes/1M_Cube", unreal.Vector(0, 110, 40), scale=unreal.Vector(1.4, 0.8, 0.8), mat="/Game/Building/Materials/MI_StdOpaque_Brushed", label="Lab_Examination_Table")

    # 3. Terrarium with REAL PHYSICS LID & BASE
    spawn_sm("/Game/Geometry/Meshes/1M_Cube_Chamfer", unreal.Vector(0, 110, 82), scale=unreal.Vector(0.55, 0.55, 0.04), mat="/Game/Building/Materials/MI_StdOpaque_Brushed", label="Terrarium_Base")
    spawn_sm("/Game/Building/Geometry/SM_FrameWindow", unreal.Vector(0, 110, 105), scale=unreal.Vector(0.26, 0.26, 0.26), mat="/Game/Building/Materials/MI_Simple_Glass_Inst", label="Terrarium_Glass_Cover")
    # Physics Glass Lid: Can be bumped or knocked completely off!
    spawn_sm("/Game/Geometry/Meshes/1M_Cube", unreal.Vector(0, 110, 132), scale=unreal.Vector(0.52, 0.52, 0.03), mat="/Game/Building/Materials/MI_Simple_Glass_Inst", label="Phys_TerrariumLid", sim_physics=True, mass_kg=1.8)

    # 4. PHYSICS LAB PROPS ON TABLE (Bottles, flasks, instruments that roll/spill)
    lab_phys = [
        ("/Game/Building/Geometry/SM_SphereSky", unreal.Vector(-45, 110, 85), unreal.Vector(0.0003, 0.0003, 0.0005), 0.5, "Phys_ChemicalFlask_Left"),
        ("/Game/Building/Geometry/SM_SphereSky", unreal.Vector(-30, 85, 85), unreal.Vector(0.00025, 0.00025, 0.0004), 0.4, "Phys_ChemicalFlask_Front"),
        ("/Game/Geometry/Meshes/1M_Cube", unreal.Vector(45, 110, 85), unreal.Vector(0.12, 0.25, 0.08), 1.8, "Phys_MetalSpecimenTray"),
        ("/Game/Geometry/Meshes/1M_Cube", unreal.Vector(40, 80, 85), unreal.Vector(0.2, 0.25, 0.05), 2.2, "Phys_HeavyMedicalBook")
    ]
    for m, loc, scl, mass, lbl in lab_phys:
        spawn_sm(m, loc, scale=scl, mat="/Game/Building/Materials/MI_StdOpaque_Concrete", label=lbl, sim_physics=True, mass_kg=mass)

    # 5. SPIDERS: Swarm surrounding the player
    def spawn_spider(loc, rot=unreal.Rotator(0,0,0), scale=1.0, name_prefix="Spider"):
        spawn_sm("/Game/Building/Geometry/SM_SphereSky", loc + unreal.Vector(0, 0, 3*scale), scale=unreal.Vector(0.0004*scale, 0.0005*scale, 0.0003*scale), mat="/Game/Building/Materials/MI_Silhouette", label=f"{name_prefix}_Abdomen")
        spawn_sm("/Game/Building/Geometry/SM_SphereSky", loc + unreal.Vector(0, 3*scale, 2*scale), scale=unreal.Vector(0.00025*scale, 0.00025*scale, 0.0002*scale), mat="/Game/Building/Materials/MI_Silhouette", label=f"{name_prefix}_Head")
        angles = [-60, -35, -15, 0, 15, 35, 60, 80]
        for leg_idx, ang in enumerate(angles):
            rad = math.radians(ang)
            lx = math.cos(rad) * 6 * scale
            ly = math.sin(rad) * 6 * scale
            spawn_sm("/Game/Geometry/Meshes/1M_Cube", loc + unreal.Vector(lx, ly, 1.5*scale), rot=unreal.Rotator(15, ang, 0), scale=unreal.Vector(0.008*scale, 0.06*scale, 0.008*scale), mat="/Game/Building/Materials/MI_Silhouette", label=f"{name_prefix}_Leg_{leg_idx+1}")

    # Terrarium Specimen
    spawn_spider(unreal.Vector(0, 110, 85), scale=1.0, name_prefix="Spider_Terrarium")
    # Tabletop escapee right in front of player
    spawn_spider(unreal.Vector(25, 75, 82), scale=0.85, name_prefix="Spider_Table_Escaped")
    # Giant spider crawling on back wall
    spawn_spider(unreal.Vector(-80, 340, 160), rot=unreal.Rotator(90, 0, 0), scale=2.2, name_prefix="Spider_Wall_Giant1")
    spawn_spider(unreal.Vector(120, 340, 210), rot=unreal.Rotator(90, 0, 0), scale=1.8, name_prefix="Spider_Wall_Giant2")
    # Spiders hanging down from the ceiling directly above player's head!
    spawn_spider(unreal.Vector(0, 30, 175), rot=unreal.Rotator(180, 0, 0), scale=1.5, name_prefix="Spider_Ceiling_Dangler")
    spawn_sm("/Game/Geometry/Meshes/1M_Cube", unreal.Vector(0, 30, 245), scale=unreal.Vector(0.002, 0.002, 1.4), mat="/Game/Building/Materials/MI_Simple_Chrome", label="Spider_Silk_Thread")

    # 6. Grabbables
    spawn_grabbable(unreal.Vector(-30, 80, 85), label="Lab_Flashlight_Grabbable")
    spawn_grabbable(unreal.Vector(50, 75, 85), label="Lab_PanicBell_Grabbable")

    # 7. Flickering Light & Terrifying Chitin Swarm Frenzy Audio
    spawn_spot(unreal.Vector(0, 110, 270), unreal.Rotator(-75, 0, 0), intensity=12000.0, color=unreal.LinearColor(0.85, 0.9, 0.8, 1.0), outer_angle=35.0, label="Desk_FlickerSpotlight")
    spawn_snd("/Game/PhobiaVR/Audio/A_Spider_Swarm_Frenzy", unreal.Vector(0, 110, 85), vol=1.0, label="Audio_SpiderSwarmFrenzy")
    spawn_snd("/Game/PhobiaVR/Audio/A_Horror_Drone_Ominous", unreal.Vector(0, 0, 150), vol=0.8, label="Audio_LabDreadDrone")
    spawn_snd("/Game/PhobiaVR/Audio/A_Jumpscare_Violin_Shriek", unreal.Vector(0, 110, 95), vol=0.7, label="Audio_TerrariumStinger")

    spawn_ps(unreal.Vector(0, 0, 20), unreal.Rotator(0, 90, 0))
    save_current_level()
    print("Arachnophobia level rebuilt with physics props & chitin swarm frenzy.")

# ==============================================================================
# 4. GLOSSOPHOBIA: NIGHTMARE AUDITORIUM, FLUTTERING SPEECH NOTES & PARANOIA
# ==============================================================================
def upgrade_glossophobia():
    level_path = "/Game/PhobiaVR/Maps/L_Sim_Glossophobia"
    print(f"\n---> Upgrading Glossophobia: Scattering Physics Notes & Paranoia Whispers ({level_path})")
    create_or_clean_level(level_path)

    # 1. Pitch Black Nightmare Stage
    spawn_sm("/Game/Geometry/Meshes/TemplateFloor", unreal.Vector(0, 0, 0), scale=unreal.Vector(2.0, 1.2, 1.0), mat="/Game/Building/Materials/MI_StdOpaque_Brushed", label="Stage_Floor")
    spawn_sm("/Game/Building/Geometry/SM_Wall", unreal.Vector(0, -280, 200), scale=unreal.Vector(2.8, 1.0, 2.0), label="Stage_Backdrop_VoidWall")

    # 2. Presenter's Podium
    spawn_sm("/Game/Geometry/Meshes/1M_Cube_Chamfer", unreal.Vector(0, 120, 60), scale=unreal.Vector(0.7, 0.5, 1.2), mat="/Game/Building/Materials/MI_StdOpaque_Concrete", label="Podium_Base")
    spawn_sm("/Game/Geometry/Meshes/1M_Cube", unreal.Vector(0, 125, 125), scale=unreal.Vector(0.04, 0.04, 0.25), mat="/Game/Building/Materials/MI_Simple_Chrome", label="Podium_Microphone")
    spawn_sm("/Game/Building/Geometry/SM_FrameWindow", unreal.Vector(0, 140, 130), rot=unreal.Rotator(-25, 0, 0), scale=unreal.Vector(0.35, 0.35, 0.2), mat="/Game/XRFramework/Materials/MI_Grid_Accent", label="Teleprompter_Monitor")

    # 3. REAL PHYSICS FLUTTERING SPEECH CUE CARDS
    # If the user brushes past the podium, these papers scatter and slide off the edge with physics!
    paper_coords = [
        (unreal.Vector(-15, 115, 122), unreal.Rotator(0, 12, 0), "Phys_SpeechPage_1"),
        (unreal.Vector(0, 118, 123), unreal.Rotator(0, -5, 0), "Phys_SpeechPage_2"),
        (unreal.Vector(18, 114, 122), unreal.Rotator(0, 25, 0), "Phys_SpeechPage_3"),
        (unreal.Vector(-8, 125, 124), unreal.Rotator(0, -18, 0), "Phys_SpeechPage_4"),
    ]
    for loc, rot, lbl in paper_coords:
        spawn_sm("/Game/Geometry/Meshes/1M_Cube", loc, rot=rot, scale=unreal.Vector(0.18, 0.25, 0.005), mat="/Game/Building/Materials/MI_StdOpaque_Brushed", label=lbl, sim_physics=True, mass_kg=0.08)

    # Physics water cup on podium edge that can be knocked over!
    spawn_sm("/Game/Building/Geometry/SM_SphereSky", unreal.Vector(25, 130, 125), scale=unreal.Vector(0.0002, 0.0002, 0.0003), mat="/Game/Building/Materials/MI_Simple_Glass_Inst", label="Phys_WaterGlass_Podium", sim_physics=True, mass_kg=0.4)

    # 4. Blinding Glaring Stage Spotlights casting grotesque elongated shadows
    spawn_spot(unreal.Vector(-220, 500, 450), unreal.Rotator(-42, -112, 0), intensity=65000.0, color=unreal.LinearColor(1.0, 0.96, 0.9, 1.0), outer_angle=26.0, inner_angle=12.0, label="Spotlight_StageGlare_Left")
    spawn_spot(unreal.Vector(220, 500, 450), unreal.Rotator(-42, -68, 0), intensity=65000.0, color=unreal.LinearColor(1.0, 0.96, 0.9, 1.0), outer_angle=26.0, inner_angle=12.0, label="Spotlight_StageGlare_Right")

    # 5. Sinister Audience Silhouettes in the Pitch Black Theater
    row_distances = [420, 680, 940, 1200]
    row_heights = [-40, 10, 65, 120]
    silhouette_mesh = "/Game/Building/Geometry/SM_SilhouetteWomen"
    
    seat_idx = 0
    for r_idx, (r_dist, r_height) in enumerate(zip(row_distances, row_heights)):
        num_attendees = 6 + r_idx * 2
        for a_idx in range(num_attendees):
            t = (a_idx / (num_attendees - 1)) - 0.5
            angle = t * 75.0
            rad = math.radians(angle)
            sx = math.sin(rad) * r_dist
            sy = math.cos(rad) * r_dist
            
            spawn_sm("/Game/Geometry/Meshes/1M_Cube", unreal.Vector(sx, sy, r_height), scale=unreal.Vector(0.5, 0.5, 0.5), label=f"Seat_R{r_idx}_S{a_idx}")
            look_rot = unreal.Rotator(0, 180 - angle, 0)
            spawn_sm(silhouette_mesh, unreal.Vector(sx, sy, r_height + 30), rot=look_rot, scale=unreal.Vector(1.0, 1.0, 1.0), mat="/Game/Building/Materials/MI_Silhouette", label=f"ShadowAudience_{seat_idx+1}")
            seat_idx += 1

    # 6. Eerie Paranoia Whispers & Tachycardia Panic Audio
    spawn_snd("/Game/PhobiaVR/Audio/A_Whispers_Paranoia_Loop", unreal.Vector(0, 700, 50), vol=1.0, label="Audio_ParanoiaWhispers")
    spawn_snd("/Game/PhobiaVR/Audio/A_Tachycardia_Suffocation", unreal.Vector(0, 60, 120), vol=0.9, label="Audio_StagePanicHeartbeat")
    spawn_snd("/Game/PhobiaVR/Audio/A_Horror_Drone_Ominous", unreal.Vector(0, 300, 150), vol=0.75, label="Audio_NightmareDrone")

    spawn_ps(unreal.Vector(0, 60, 20), unreal.Rotator(0, 90, 0))
    save_current_level()
    print("Glossophobia level rebuilt with scattering physics cue cards & paranoia whispers.")

if __name__ == "__main__":
    upgrade_acrophobia()
    upgrade_claustrophobia()
    upgrade_arachnophobia()
    upgrade_glossophobia()
    print("\n==========================================================")
    print("  ALL PHOBIA LEVELS UPGRADED WITH PHYSICS & HORROR AUDIO!  ")
    print("==========================================================")
