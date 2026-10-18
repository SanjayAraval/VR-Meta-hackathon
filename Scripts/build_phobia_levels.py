import unreal
import math
import random

print("==================================================")
print("  PhobiaVR: Building Immersive Meta VR Simulators ")
print("==================================================")

editor_level_subsystem = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
editor_actor_subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)

def create_or_clean_level(level_path):
    if unreal.EditorAssetLibrary.does_asset_exist(level_path):
        unreal.EditorAssetLibrary.delete_asset(level_path)
    return editor_level_subsystem.new_level(level_path)

def save_current_level():
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)

# Helper function to spawn static mesh actor
def spawn_static_mesh(mesh_path, location, rotation=unreal.Rotator(0, 0, 0), scale=unreal.Vector(1, 1, 1), material_path=None, label=None):
    mesh_asset = unreal.EditorAssetLibrary.load_asset(mesh_path)
    if not mesh_asset:
        print(f"Warning: Mesh not found: {mesh_path}")
        return None
    actor = editor_actor_subsystem.spawn_actor_from_class(unreal.StaticMeshActor, location, rotation)
    if actor:
        if label:
            actor.set_actor_label(label)
        smc = actor.static_mesh_component
        smc.set_static_mesh(mesh_asset)
        smc.set_world_scale3d(scale)
        if material_path:
            mat_asset = unreal.EditorAssetLibrary.load_asset(material_path)
            if mat_asset:
                smc.set_material(0, mat_asset)
    return actor

# Helper function to spawn Point/Spot light
def spawn_point_light(location, intensity=5000.0, color=unreal.LinearColor(1, 1, 1, 1), radius=1000.0, label=None):
    actor = editor_actor_subsystem.spawn_actor_from_class(unreal.PointLight, location, unreal.Rotator(0,0,0))
    if actor:
        if label:
            actor.set_actor_label(label)
        plc = actor.light_component
        if plc:
            plc.set_intensity(intensity)
            plc.set_light_color(color)
            plc.set_attenuation_radius(radius)
    return actor

def spawn_spot_light(location, rotation, intensity=25000.0, color=unreal.LinearColor(1, 1, 1, 1), outer_angle=45.0, inner_angle=25.0, radius=3000.0, label=None):
    actor = editor_actor_subsystem.spawn_actor_from_class(unreal.SpotLight, location, rotation)
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

# Helper to spawn ambient audio
def spawn_ambient_sound(sound_path, location, volume=1.0, is_ui=False, label=None):
    sound_asset = unreal.EditorAssetLibrary.load_asset(sound_path)
    if not sound_asset:
        print(f"Warning: Sound not found: {sound_path}")
        return None
    actor = editor_actor_subsystem.spawn_actor_from_class(unreal.AmbientSound, location, unreal.Rotator(0,0,0))
    if actor:
        if label:
            actor.set_actor_label(label)
        asc = actor.audio_component
        if asc:
            asc.set_sound(sound_asset)
            asc.set_volume_multiplier(volume)
            asc.set_ui_sound(is_ui)
            asc.play()
    return actor

# Helper to spawn player start
def spawn_player_start(location, rotation=unreal.Rotator(0, 0, 0)):
    actor = editor_actor_subsystem.spawn_actor_from_class(unreal.PlayerStart, location, rotation)
    if actor:
        actor.set_actor_label("PlayerStart_VR")
    return actor

# Helper to spawn sky sphere & sun
def setup_sky_and_sun(sun_pitch=-45.0, sun_yaw=60.0, sun_lux=20000.0, sun_color=unreal.LinearColor(1.0, 0.95, 0.88, 1.0)):
    # Directional Light (Sun)
    sun_rot = unreal.Rotator(sun_pitch, sun_yaw, 0)
    sun_actor = editor_actor_subsystem.spawn_actor_from_class(unreal.DirectionalLight, unreal.Vector(0,0,500), sun_rot)
    if sun_actor:
        sun_actor.set_actor_label("Sun_DirectionalLight")
        dlc = sun_actor.light_component
        if dlc:
            dlc.set_intensity(sun_lux)
            dlc.set_light_color(sun_color)
            dlc.set_atmosphere_sun_light(True)
    # Sky Atmosphere
    sky_atm = editor_actor_subsystem.spawn_actor_from_class(unreal.SkyAtmosphere, unreal.Vector(0,0,0), unreal.Rotator(0,0,0))
    if sky_atm:
        sky_atm.set_actor_label("SkyAtmosphere")
    # Sky Light
    sky_light = editor_actor_subsystem.spawn_actor_from_class(unreal.SkyLight, unreal.Vector(0,0,100), unreal.Rotator(0,0,0))
    if sky_light:
        sky_light.set_actor_label("SkyLight")
    # Exponential Height Fog
    fog = editor_actor_subsystem.spawn_actor_from_class(unreal.ExponentialHeightFog, unreal.Vector(0,0,0), unreal.Rotator(0,0,0))
    if fog:
        fog.set_actor_label("HeightFog")

# Helper to spawn grabbable physics cubes (from XRFramework)
def spawn_grabbable_item(location, label=None):
    bp_class = unreal.EditorAssetLibrary.load_blueprint_class("/Game/XRFramework/Blueprints/BP_Grabbable_SmallCube")
    if bp_class:
        actor = editor_actor_subsystem.spawn_actor_from_class(bp_class, location, unreal.Rotator(0,0,0))
        if actor and label:
            actor.set_actor_label(label)
        return actor
    return None

# ==============================================================================
# LEVEL 1: CLINIC / ZEN HUB (L_PhobiaClinicHub)
# ==============================================================================
def build_clinic_hub():
    level_path = "/Game/PhobiaVR/Maps/L_PhobiaClinicHub"
    print(f"\n---> Building Zen Clinic Hub: {level_path}")
    create_or_clean_level(level_path)
    
    setup_sky_and_sun(sun_pitch=-30.0, sun_yaw=120.0, sun_lux=15000.0)
    
    # 1. Main Room Floor
    spawn_static_mesh("/Game/Geometry/Meshes/TemplateFloor", unreal.Vector(0, 0, 0), scale=unreal.Vector(2.8, 2.8, 1.0), material_path="/Game/Building/Materials/MI_StdOpaque_Concrete", label="Sanctuary_Floor")
    
    # 2. Back and Side Walls
    spawn_static_mesh("/Game/Building/Geometry/SM_Wall", unreal.Vector(0, 700, 150), scale=unreal.Vector(3.5, 1.0, 1.5), label="Wall_Back")
    spawn_static_mesh("/Game/Building/Geometry/SM_Wall", unreal.Vector(-700, 0, 150), rotation=unreal.Rotator(0, 90, 0), scale=unreal.Vector(3.5, 1.0, 1.5), label="Wall_Left")
    spawn_static_mesh("/Game/Building/Geometry/SM_Wall", unreal.Vector(700, 0, 150), rotation=unreal.Rotator(0, -90, 0), scale=unreal.Vector(3.5, 1.0, 1.5), label="Wall_Right")
    
    # 3. Floor-to-ceiling glass panorama window
    spawn_static_mesh("/Game/Building/Geometry/SM_FrameWindow", unreal.Vector(0, -700, 150), scale=unreal.Vector(3.5, 1.0, 1.5), material_path="/Game/Building/Materials/MI_Simple_Glass_Inst", label="Window_Panorama")
    
    # 4. Garden Outside
    spawn_static_mesh("/Game/ArchVis/SampleScene/Tree/HillTree_02", unreal.Vector(-400, -1200, 0), scale=unreal.Vector(0.8, 0.8, 0.8), label="Garden_Tree1")
    spawn_static_mesh("/Game/ArchVis/SampleScene/Tree/HillTree_02", unreal.Vector(350, -1350, 0), scale=unreal.Vector(0.9, 0.9, 0.9), label="Garden_Tree2")
    spawn_static_mesh("/Game/Building/Geometry/SM_Water", unreal.Vector(0, -1200, -20), scale=unreal.Vector(3.0, 3.0, 1.0), material_path="/Game/Building/Materials/MI_Water", label="Garden_Water")
    
    # 5. Ceiling with soft lighting
    spawn_static_mesh("/Game/Geometry/Meshes/TemplateFloor", unreal.Vector(0, 0, 450), scale=unreal.Vector(2.8, 2.8, 0.5), label="Sanctuary_Ceiling")
    spawn_point_light(unreal.Vector(0, 0, 400), intensity=12000.0, color=unreal.LinearColor(1.0, 0.92, 0.82, 1.0), radius=900.0, label="Light_CenterWarm")
    spawn_point_light(unreal.Vector(-350, 350, 380), intensity=6000.0, color=unreal.LinearColor(0.85, 0.9, 1.0, 1.0), radius=600.0, label="Light_CornerSoft1")
    spawn_point_light(unreal.Vector(350, 350, 380), intensity=6000.0, color=unreal.LinearColor(0.85, 0.9, 1.0, 1.0), radius=600.0, label="Light_CornerSoft2")

    # 6. Central Therapy Dais
    spawn_static_mesh("/Game/Geometry/Meshes/1M_Cube_Chamfer", unreal.Vector(0, 0, 5), scale=unreal.Vector(2.5, 2.5, 0.1), material_path="/Game/XRFramework/Materials/MI_Grid_Accent", label="Central_Therapy_Platform")
    
    # 7. Holographic Scenario Portals
    spawn_static_mesh("/Game/ArchVis/SampleScene/Building/Meshes/Door_01_L", unreal.Vector(-350, 600, 10), scale=unreal.Vector(1.2, 1.2, 1.2), label="Portal_Acrophobia_Heights")
    spawn_point_light(unreal.Vector(-350, 580, 220), intensity=4000.0, color=unreal.LinearColor(0.2, 0.7, 1.0, 1.0), radius=350.0, label="Light_Portal_Acrophobia")
    
    spawn_static_mesh("/Game/ArchVis/SampleScene/Building/Meshes/Door_01_L", unreal.Vector(-120, 600, 10), scale=unreal.Vector(1.2, 1.2, 1.2), label="Portal_Arachnophobia_Spiders")
    spawn_point_light(unreal.Vector(-120, 580, 220), intensity=4000.0, color=unreal.LinearColor(0.8, 0.4, 0.1, 1.0), radius=350.0, label="Light_Portal_Arachnophobia")
    
    spawn_static_mesh("/Game/ArchVis/SampleScene/Building/Meshes/Door_01_L", unreal.Vector(120, 600, 10), scale=unreal.Vector(1.2, 1.2, 1.2), label="Portal_Claustrophobia_Elevator")
    spawn_point_light(unreal.Vector(120, 580, 220), intensity=4000.0, color=unreal.LinearColor(1.0, 0.2, 0.2, 1.0), radius=350.0, label="Light_Portal_Claustrophobia")
    
    spawn_static_mesh("/Game/ArchVis/SampleScene/Building/Meshes/Door_01_L", unreal.Vector(350, 600, 10), scale=unreal.Vector(1.2, 1.2, 1.2), label="Portal_Glossophobia_Auditorium")
    spawn_point_light(unreal.Vector(350, 580, 220), intensity=4000.0, color=unreal.LinearColor(0.9, 0.8, 0.2, 1.0), radius=350.0, label="Light_Portal_Glossophobia")

    # 8. Grabbable Objects
    spawn_static_mesh("/Game/Geometry/Meshes/1M_Cube", unreal.Vector(-200, 100, 40), scale=unreal.Vector(0.8, 1.2, 0.8), material_path="/Game/Building/Materials/MI_StdOpaque_Brushed", label="Table_StressRelief")
    spawn_grabbable_item(unreal.Vector(-200, 80, 85), label="Grabbable_CalmCube1")
    spawn_grabbable_item(unreal.Vector(-200, 120, 85), label="Grabbable_CalmCube2")

    # 9. Ambient Zen Sound & Player Start
    spawn_ambient_sound("/Game/PhobiaVR/Audio/A_ZenChime_Safe", unreal.Vector(0, 0, 200), volume=0.8, label="Audio_ZenChime")
    spawn_player_start(unreal.Vector(0, 0, 30), unreal.Rotator(0, 90, 0))
    
    save_current_level()
    print(f"Saved: {level_path}")

# ==============================================================================
# LEVEL 2: ACROPHOBIA (FEAR OF HEIGHTS & VERTIGO) (L_Sim_Acrophobia)
# ==============================================================================
def build_acrophobia_level():
    level_path = "/Game/PhobiaVR/Maps/L_Sim_Acrophobia"
    print(f"\n---> Building Acrophobia Skyscraper Plank: {level_path}")
    create_or_clean_level(level_path)
    
    setup_sky_and_sun(sun_pitch=-25.0, sun_yaw=210.0, sun_lux=35000.0)
    tower_z = 20000.0 # 200 meters high
    
    # 1. Skyscraper Main Core Tower
    spawn_static_mesh("/Game/Building/Geometry/SM_Land", unreal.Vector(0, 0, tower_z / 2), scale=unreal.Vector(2.0, 2.0, 40.0), material_path="/Game/Building/Materials/MI_StdOpaque_Concrete", label="Skyscraper_Tower_Body")
    
    # 2. Skyscraper Rooftop Elevator Landing Room
    spawn_static_mesh("/Game/Geometry/Meshes/TemplateFloor", unreal.Vector(0, 300, tower_z), scale=unreal.Vector(1.5, 1.5, 1.0), material_path="/Game/Building/Materials/MI_StdOpaque_Concrete_Ground", label="Rooftop_Floor")
    spawn_static_mesh("/Game/Building/Geometry/SM_Wall", unreal.Vector(0, 600, tower_z + 150), scale=unreal.Vector(2.5, 1.0, 1.5), label="Rooftop_BackWall")
    spawn_static_mesh("/Game/Building/Geometry/SM_Wall", unreal.Vector(-350, 300, tower_z + 150), rotation=unreal.Rotator(0, 90, 0), scale=unreal.Vector(2.0, 1.0, 1.5), label="Rooftop_LeftWall")
    spawn_static_mesh("/Game/Building/Geometry/SM_Wall", unreal.Vector(350, 300, tower_z + 150), rotation=unreal.Rotator(0, -90, 0), scale=unreal.Vector(2.0, 1.0, 1.5), label="Rooftop_RightWall")
    
    # 3. Observation Balcony Railing (Level 1: Safe Exposure)
    spawn_static_mesh("/Game/ArchVis/SampleScene/Building/Meshes/Railing_001", unreal.Vector(-180, 0, tower_z + 50), scale=unreal.Vector(1.0, 1.0, 1.0), label="Railing_Left")
    spawn_static_mesh("/Game/ArchVis/SampleScene/Building/Meshes/Railing_001", unreal.Vector(180, 0, tower_z + 50), scale=unreal.Vector(1.0, 1.0, 1.0), label="Railing_Right")

    # 4. THE VERTIGO PLANK (Level 3: Full Extreme Exposure)
    spawn_static_mesh("/Game/Geometry/Meshes/1M_Cube", unreal.Vector(0, -300, tower_z - 5), scale=unreal.Vector(0.36, 6.0, 0.1), material_path="/Game/Building/Materials/MI_StdOpaque_Brushed", label="The_Vertigo_Plank")
    spawn_static_mesh("/Game/Geometry/Meshes/1M_Cube_Chamfer", unreal.Vector(0, -600, tower_z), scale=unreal.Vector(0.5, 0.5, 0.1), material_path="/Game/XRFramework/Materials/MI_Grid_Accent", label="Plank_Tip_Platform")
    
    # 5. Grabbable Physics Drop Items
    spawn_grabbable_item(unreal.Vector(0, 50, tower_z + 30), label="DropItem_Cube_Edge")
    spawn_grabbable_item(unreal.Vector(0, -580, tower_z + 30), label="DropItem_Cube_PlankTip")

    # 6. Distant Ground Cityscape
    spawn_static_mesh("/Game/Building/Geometry/SM_Land", unreal.Vector(0, -1000, 0), scale=unreal.Vector(30.0, 30.0, 1.0), material_path="/Game/Building/Materials/MI_Road", label="City_Ground_Plane")
    
    tower_coords = [
        (-2500, -2000, 12000), (2800, -2400, 14000),
        (-3500, 1500, 16000), (3200, 2000, 11000),
        (-1500, -4500, 9000), (1200, -5000, 13000),
        (-4000, -4000, 10000), (4500, -3500, 15000)
    ]
    for idx, (tx, ty, tz) in enumerate(tower_coords):
        spawn_static_mesh("/Game/Building/Geometry/SM_Land", unreal.Vector(tx, ty, tz / 2), scale=unreal.Vector(1.2, 1.2, tz / 1000.0), material_path="/Game/Building/Materials/MI_StdOpaque_Concrete", label=f"Distant_Tower_{idx+1}")
        spawn_static_mesh("/Game/Building/Geometry/SM_StreetLight", unreal.Vector(tx + 200, ty + 200, 0), scale=unreal.Vector(3.0, 3.0, 3.0), label=f"StreetLight_{idx+1}")

    # 7. High Altitude Spatialized Wind Loop & Player Start
    spawn_ambient_sound("/Game/PhobiaVR/Audio/A_Wind_HighAltitude_Loop", unreal.Vector(0, -250, tower_z + 100), volume=1.0, label="Audio_HighAltitudeWind")
    spawn_player_start(unreal.Vector(0, 250, tower_z + 20), unreal.Rotator(0, -90, 0))

    save_current_level()
    print(f"Saved: {level_path}")

# ==============================================================================
# LEVEL 3: CLAUSTROPHOBIA (ELEVATOR STALL & CONFINED SPACE) (L_Sim_Claustrophobia)
# ==============================================================================
def build_claustrophobia_level():
    level_path = "/Game/PhobiaVR/Maps/L_Sim_Claustrophobia"
    print(f"\n---> Building Claustrophobia Elevator Simulator: {level_path}")
    create_or_clean_level(level_path)

    # 1. Elevator Cabin: Enclosed 2m x 2m x 2.4m
    spawn_static_mesh("/Game/Geometry/Meshes/TemplateFloor", unreal.Vector(0, 0, 0), scale=unreal.Vector(0.45, 0.45, 1.0), material_path="/Game/Building/Materials/MI_StdOpaque_Brushed", label="Elevator_Floor")
    spawn_static_mesh("/Game/Building/Geometry/SM_Wall", unreal.Vector(0, 110, 120), scale=unreal.Vector(0.55, 0.5, 1.2), material_path="/Game/Building/Materials/MI_StdOpaque_Brushed", label="Elevator_Wall_Back")
    spawn_static_mesh("/Game/Building/Geometry/SM_Wall", unreal.Vector(0, -110, 120), scale=unreal.Vector(0.55, 0.5, 1.2), material_path="/Game/Building/Materials/MI_StdOpaque_Brushed", label="Elevator_Wall_Door")
    spawn_static_mesh("/Game/Building/Geometry/SM_Wall", unreal.Vector(-110, 0, 120), rotation=unreal.Rotator(0, 90, 0), scale=unreal.Vector(0.55, 0.5, 1.2), material_path="/Game/Building/Materials/MI_StdOpaque_Brushed", label="Elevator_Wall_Left")
    spawn_static_mesh("/Game/Building/Geometry/SM_Wall", unreal.Vector(110, 0, 120), rotation=unreal.Rotator(0, -90, 0), scale=unreal.Vector(0.55, 0.5, 1.2), material_path="/Game/Building/Materials/MI_StdOpaque_Brushed", label="Elevator_Wall_Right")
    spawn_static_mesh("/Game/Geometry/Meshes/TemplateFloor", unreal.Vector(0, 0, 230), scale=unreal.Vector(0.45, 0.45, 0.2), material_path="/Game/Building/Materials/MI_StdOpaque_Brushed", label="Elevator_Ceiling")

    # 2. Control Panel
    spawn_static_mesh("/Game/Geometry/Meshes/1M_Cube_Chamfer", unreal.Vector(95, -20, 110), scale=unreal.Vector(0.05, 0.2, 0.5), material_path="/Game/XRFramework/Materials/MI_Grid_Accent", label="Elevator_Control_Panel")
    
    # 3. Lighting
    spawn_point_light(unreal.Vector(0, 0, 220), intensity=1500.0, color=unreal.LinearColor(1.0, 0.95, 0.8, 1.0), radius=280.0, label="Light_Elevator_Main")
    spawn_point_light(unreal.Vector(80, -20, 210), intensity=2500.0, color=unreal.LinearColor(1.0, 0.05, 0.02, 1.0), radius=350.0, label="Light_Elevator_EmergencyRed")

    # 4. Elevator Shaft Outer
    spawn_static_mesh("/Game/Building/Geometry/SM_Land", unreal.Vector(0, 0, -500), scale=unreal.Vector(1.0, 1.0, 20.0), material_path="/Game/Building/Materials/MI_StdOpaque_Concrete", label="Elevator_Shaft_Outer")
    
    # 5. Audio & Player Start
    spawn_ambient_sound("/Game/PhobiaVR/Audio/A_Elevator_Stall_Groan", unreal.Vector(0, 0, 220), volume=1.0, label="Audio_ElevatorCableGroan")
    spawn_ambient_sound("/Game/PhobiaVR/Audio/A_Heartbeat_Pulse_Cue", unreal.Vector(0, 0, 150), volume=0.85, label="Audio_PatientHeartbeat")
    spawn_player_start(unreal.Vector(0, 0, 20), unreal.Rotator(0, -90, 0))

    save_current_level()
    print(f"Saved: {level_path}")

# ==============================================================================
# LEVEL 4: ARACHNOPHOBIA (FEAR OF SPIDERS) (L_Sim_Arachnophobia)
# ==============================================================================
def build_arachnophobia_level():
    level_path = "/Game/PhobiaVR/Maps/L_Sim_Arachnophobia"
    print(f"\n---> Building Arachnophobia Exposure Lab: {level_path}")
    create_or_clean_level(level_path)

    # 1. Room
    spawn_static_mesh("/Game/Geometry/Meshes/TemplateFloor", unreal.Vector(0, 0, 0), scale=unreal.Vector(1.2, 1.2, 1.0), material_path="/Game/Building/Materials/MI_StdOpaque_Concrete", label="Lab_Floor")
    spawn_static_mesh("/Game/Building/Geometry/SM_Wall", unreal.Vector(0, 300, 150), scale=unreal.Vector(1.5, 1.0, 1.5), label="Lab_Wall_Back")
    spawn_static_mesh("/Game/Building/Geometry/SM_Wall", unreal.Vector(-300, 0, 150), rotation=unreal.Rotator(0, 90, 0), scale=unreal.Vector(1.5, 1.0, 1.5), label="Lab_Wall_Left")
    spawn_static_mesh("/Game/Building/Geometry/SM_Wall", unreal.Vector(300, 0, 150), rotation=unreal.Rotator(0, -90, 0), scale=unreal.Vector(1.5, 1.0, 1.5), label="Lab_Wall_Right")
    spawn_static_mesh("/Game/Geometry/Meshes/TemplateFloor", unreal.Vector(0, 0, 300), scale=unreal.Vector(1.2, 1.2, 0.2), label="Lab_Ceiling")

    # 2. Table
    spawn_static_mesh("/Game/Geometry/Meshes/1M_Cube", unreal.Vector(0, 110, 40), scale=unreal.Vector(1.4, 0.8, 0.8), material_path="/Game/Building/Materials/MI_StdOpaque_Brushed", label="Lab_Observation_Table")

    # 3. Terrarium
    spawn_static_mesh("/Game/Geometry/Meshes/1M_Cube_Chamfer", unreal.Vector(0, 110, 85), scale=unreal.Vector(0.5, 0.5, 0.05), material_path="/Game/Building/Materials/MI_StdOpaque_Brushed", label="Terrarium_Base")
    spawn_static_mesh("/Game/Building/Geometry/SM_FrameWindow", unreal.Vector(0, 110, 105), scale=unreal.Vector(0.25, 0.25, 0.25), material_path="/Game/Building/Materials/MI_Simple_Glass_Inst", label="Terrarium_Glass_Cover")
    
    # 4. Spiders
    def spawn_spider(loc, rot=unreal.Rotator(0,0,0), scale=1.0, name_prefix="Spider"):
        spawn_static_mesh("/Game/Building/Geometry/SM_SphereSky", loc + unreal.Vector(0, 0, 3*scale), scale=unreal.Vector(0.0004*scale, 0.0005*scale, 0.0003*scale), material_path="/Game/Building/Materials/MI_Silhouette", label=f"{name_prefix}_Abdomen")
        spawn_static_mesh("/Game/Building/Geometry/SM_SphereSky", loc + unreal.Vector(0, 3*scale, 2*scale), scale=unreal.Vector(0.00025*scale, 0.00025*scale, 0.0002*scale), material_path="/Game/Building/Materials/MI_Silhouette", label=f"{name_prefix}_Head")
        angles = [-60, -35, -15, 0, 15, 35, 60, 80]
        for leg_idx, ang in enumerate(angles):
            rad = math.radians(ang)
            lx = math.cos(rad) * 6 * scale
            ly = math.sin(rad) * 6 * scale
            spawn_static_mesh("/Game/Geometry/Meshes/1M_Cube", loc + unreal.Vector(lx, ly, 1.5*scale), rotation=unreal.Rotator(15, ang, 0), scale=unreal.Vector(0.008*scale, 0.06*scale, 0.008*scale), material_path="/Game/Building/Materials/MI_Silhouette", label=f"{name_prefix}_Leg_{leg_idx+1}")

    spawn_spider(unreal.Vector(0, 110, 88), scale=1.0, name_prefix="Spider_Terrarium")
    spawn_spider(unreal.Vector(35, 80, 81), scale=0.8, name_prefix="Spider_Table_Free")
    spawn_spider(unreal.Vector(-80, 290, 140), rot=unreal.Rotator(90, 0, 0), scale=1.5, name_prefix="Spider_Wall_Giant")
    spawn_spider(unreal.Vector(-180, 160, 5), scale=1.2, name_prefix="Spider_Floor_Corner")

    # 5. Grabbable items
    spawn_grabbable_item(unreal.Vector(-40, 80, 85), label="Lab_Grabbable_FlashlightCube")
    spawn_grabbable_item(unreal.Vector(50, 75, 85), label="Lab_Grabbable_Bell")

    # 6. Lighting & Sound
    spawn_spot_light(unreal.Vector(0, 110, 250), unreal.Rotator(-75, 0, 0), intensity=18000.0, color=unreal.LinearColor(1.0, 0.98, 0.9, 1.0), outer_angle=35.0, label="Desk_Spotlight")
    spawn_ambient_sound("/Game/PhobiaVR/Audio/A_Spider_Skitter_Cue", unreal.Vector(0, 110, 85), volume=0.9, label="Audio_SpiderSkitter")
    spawn_player_start(unreal.Vector(0, 0, 20), unreal.Rotator(0, 90, 0))

    save_current_level()
    print(f"Saved: {level_path}")

# ==============================================================================
# LEVEL 5: GLOSSOPHOBIA (FEAR OF PUBLIC SPEAKING) (L_Sim_Glossophobia)
# ==============================================================================
def build_glossophobia_level():
    level_path = "/Game/PhobiaVR/Maps/L_Sim_Glossophobia"
    print(f"\n---> Building Glossophobia Grand Auditorium: {level_path}")
    create_or_clean_level(level_path)

    # 1. Stage Floor
    spawn_static_mesh("/Game/Geometry/Meshes/TemplateFloor", unreal.Vector(0, 0, 0), scale=unreal.Vector(1.8, 1.0, 1.0), material_path="/Game/Building/Materials/MI_StdOpaque_Brushed", label="Stage_Floor")
    spawn_static_mesh("/Game/Building/Geometry/SM_Wall", unreal.Vector(0, -250, 200), scale=unreal.Vector(2.5, 1.0, 2.0), label="Stage_Backdrop_Wall")

    # 2. Presenter's Podium
    spawn_static_mesh("/Game/Geometry/Meshes/1M_Cube_Chamfer", unreal.Vector(0, 120, 60), scale=unreal.Vector(0.7, 0.5, 1.2), material_path="/Game/Building/Materials/MI_StdOpaque_Concrete", label="Podium_Base")
    spawn_static_mesh("/Game/Geometry/Meshes/1M_Cube", unreal.Vector(0, 125, 125), scale=unreal.Vector(0.04, 0.04, 0.25), material_path="/Game/Building/Materials/MI_Simple_Chrome", label="Podium_Microphone")
    spawn_static_mesh("/Game/Building/Geometry/SM_FrameWindow", unreal.Vector(0, 140, 130), rotation=unreal.Rotator(-25, 0, 0), scale=unreal.Vector(0.35, 0.35, 0.2), material_path="/Game/XRFramework/Materials/MI_Grid_Accent", label="Teleprompter_Monitor")

    # 3. Spotlights Aimed at Player
    spawn_spot_light(unreal.Vector(-200, 450, 400), unreal.Rotator(-40, -110, 0), intensity=45000.0, color=unreal.LinearColor(1.0, 0.95, 0.85, 1.0), outer_angle=30.0, inner_angle=15.0, label="Spotlight_Stage_Left")
    spawn_spot_light(unreal.Vector(200, 450, 400), unreal.Rotator(-40, -70, 0), intensity=45000.0, color=unreal.LinearColor(1.0, 0.95, 0.85, 1.0), outer_angle=30.0, inner_angle=15.0, label="Spotlight_Stage_Right")

    # 4. Auditorium Seating with Audience Avatars
    row_distances = [400, 650, 900, 1150]
    row_heights = [-50, 0, 50, 100]
    silhouette_mesh = "/Game/Building/Geometry/SM_SilhouetteWomen"
    
    seat_idx = 0
    for r_idx, (r_dist, r_height) in enumerate(zip(row_distances, row_heights)):
        num_attendees = 5 + r_idx * 2
        for a_idx in range(num_attendees):
            t = (a_idx / (num_attendees - 1)) - 0.5
            angle = t * 70.0
            rad = math.radians(angle)
            sx = math.sin(rad) * r_dist
            sy = math.cos(rad) * r_dist
            
            spawn_static_mesh("/Game/Geometry/Meshes/1M_Cube", unreal.Vector(sx, sy, r_height), scale=unreal.Vector(0.5, 0.5, 0.5), label=f"Seat_R{r_idx}_S{a_idx}")
            look_rot = unreal.Rotator(0, 180 - angle, 0)
            spawn_static_mesh(silhouette_mesh, unreal.Vector(sx, sy, r_height + 30), rotation=look_rot, scale=unreal.Vector(1.0, 1.0, 1.0), material_path="/Game/Building/Materials/MI_Silhouette", label=f"Audience_Member_{seat_idx+1}")
            seat_idx += 1

    # 5. Walls & Audio
    spawn_static_mesh("/Game/Building/Geometry/SM_Wall", unreal.Vector(-800, 600, 250), rotation=unreal.Rotator(0, 90, 0), scale=unreal.Vector(6.0, 1.0, 3.0), label="Auditorium_Wall_Left")
    spawn_static_mesh("/Game/Building/Geometry/SM_Wall", unreal.Vector(800, 600, 250), rotation=unreal.Rotator(0, -90, 0), scale=unreal.Vector(6.0, 1.0, 3.0), label="Auditorium_Wall_Right")
    spawn_ambient_sound("/Game/PhobiaVR/Audio/A_Audience_Murmur_Loop", unreal.Vector(0, 700, 50), volume=1.0, label="Audio_AudienceMurmur")

    # 6. Player Start
    spawn_player_start(unreal.Vector(0, 60, 20), unreal.Rotator(0, 90, 0))

    save_current_level()
    print(f"Saved: {level_path}")

# ==============================================================================
# MAIN EXECUTION
# ==============================================================================
if __name__ == "__main__":
    build_clinic_hub()
    build_acrophobia_level()
    build_claustrophobia_level()
    build_arachnophobia_level()
    build_glossophobia_level()
    print("\n==================================================")
    print("  ALL 5 PHOBIA LEVELS GENERATED & SAVED IN UE5!    ")
    print("==================================================")
