import unreal

print("=== Adding Holochamber Universal Matrix Portal to L_PhobiaClinicHub ===")

level_subsystem = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
editor_actor_subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)

map_path = "/Game/PhobiaVR/Maps/L_PhobiaClinicHub"
success = level_subsystem.load_level(map_path)
if not success:
    print(f"Failed to load {map_path}")
    quit()

world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()

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

# Check existing actors to avoid duplicates
existing_labels = {a.get_actor_label() for a in editor_actor_subsystem.get_all_level_actors()}

# Grand Archway / Portal for Holochamber Matrix on the East Wall (X=650, Y=0, Z=0) facing inward
if "Portal_Holochamber_UniversalMatrix" not in existing_labels:
    # Portal Door Frame
    spawn_sm("/Game/ArchVis/SampleScene/Building/Meshes/Door_01_L",
             unreal.Vector(650, 0, 10),
             rot=unreal.Rotator(0, 180, 0),
             scale=unreal.Vector(1.6, 1.6, 1.5),
             label="Portal_Holochamber_UniversalMatrix")

    # Cybernetic / Mystical Violet Aura Light
    spawn_pl(unreal.Vector(620, 0, 220),
             intensity=8000.0,
             color=unreal.LinearColor(0.65, 0.15, 1.0, 1.0),
             radius=500.0,
             label="Light_Portal_Holochamber")

    # Portal Pedestal Platform
    spawn_sm("/Game/Geometry/Meshes/1M_Cube_Chamfer",
             unreal.Vector(620, 0, 5),
             rot=unreal.Rotator(0, 0, 0),
             scale=unreal.Vector(1.4, 2.2, 0.12),
             mat="/Game/XRFramework/Materials/MI_Grid_Accent",
             label="Platform_Holochamber_Dais")

    # Holographic Terminal Console in front of the Holochamber Portal
    spawn_sm("/Game/Geometry/Meshes/1M_Cube",
             unreal.Vector(550, 0, 45),
             rot=unreal.Rotator(0, 180, 0),
             scale=unreal.Vector(0.5, 1.0, 0.9),
             mat="/Game/Building/Materials/MI_Dark_Metal",
             label="Console_86Phobia_Index")

    # Terminal Hologram Screen
    spawn_sm("/Game/Geometry/Meshes/1M_Cube",
             unreal.Vector(540, 0, 105),
             rot=unreal.Rotator(-25, 180, 0),
             scale=unreal.Vector(0.05, 0.8, 0.5),
             mat="/Game/XRFramework/Materials/MI_Grid_Accent",
             label="Screen_86Phobias_Hologram")

    # Hologram Glow Light
    spawn_pl(unreal.Vector(525, 0, 110),
             intensity=3500.0,
             color=unreal.LinearColor(0.3, 0.8, 1.0, 1.0),
             radius=250.0,
             label="Light_Console_HoloGlow")

    print("Spawned Holochamber Gateway and 86-Phobia Terminal Console successfully.")
else:
    print("Portal_Holochamber_UniversalMatrix already present.")

saved = unreal.EditorLoadingAndSavingUtils.save_map(world, map_path)
print(f"L_PhobiaClinicHub saved! Success: {saved}")
