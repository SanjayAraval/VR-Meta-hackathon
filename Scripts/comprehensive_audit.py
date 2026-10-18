import unreal
import json
import os

def log(msg):
    unreal.log(f"[AUDIT] {msg}")

log("=================================================================")
log("          STARTING COMPREHENSIVE PHOBIA VR AUDIT & FIX          ")
log("=================================================================")

audit_results = {
    "gamemode": {},
    "audio_looping": {},
    "levels": {},
    "issues_found": [],
    "fixes_applied": []
}

# 1. Check GameMode and Default Pawn Class
gm_class = unreal.EditorAssetLibrary.load_blueprint_class("/Game/XRFramework/Blueprints/BP_XRGameMode")
if gm_class:
    gm_cdo = unreal.get_default_object(gm_class)
    pawn_class = gm_cdo.get_editor_property("default_pawn_class")
    audit_results["gamemode"]["pawn_class"] = str(pawn_class)
    log(f"GameMode Default Pawn: {pawn_class}")
else:
    audit_results["issues_found"].append("BP_XRGameMode could not be loaded!")

# 2. Check Audio Assets and Looping Flags
audio_dir = "/Game/PhobiaVR/Audio"
audio_assets = unreal.EditorAssetLibrary.list_assets(audio_dir, recursive=False, include_folder=False)
ambient_tracks = [
    "A_Horror_Drone_Ominous",
    "A_Vertigo_Abyss_Wind",
    "A_Spider_Swarm_Frenzy",
    "A_Whispers_Paranoia_Loop",
    "A_Tachycardia_Suffocation",
    "A_Thalassophobia_Abyss_Sonar",
    "A_Nyctophobia_Whispering_Dark",
    "A_Automaton_MusicBox_Creep",
    "A_Megalophobia_Titan_Drone",
    "A_ZenChime_Safe"
]

log("--- AUDITING AUDIO ASSETS ---")
for asset_path in audio_assets:
    asset = unreal.EditorAssetLibrary.load_asset(asset_path)
    if isinstance(asset, unreal.SoundWave):
        track_name = asset.get_name()
        is_loop = False
        try:
            is_loop = asset.get_editor_property("looping")
        except:
            try:
                is_loop = asset.get_editor_property("b_looping")
            except:
                pass
        
        audit_results["audio_looping"][track_name] = is_loop
        log(f"Audio: {track_name} | Looping: {is_loop}")
        
        # If this is an ambient loop and looping is False, fix it!
        if track_name in ambient_tracks and not is_loop:
            try:
                asset.set_editor_property("looping", True)
                unreal.EditorAssetLibrary.save_loaded_asset(asset)
                audit_results["fixes_applied"].append(f"Set looping=True on {track_name}")
                log(f"  -> FIXED: Set {track_name} to looping=True")
            except Exception as e:
                audit_results["issues_found"].append(f"Failed to set looping on {track_name}: {e}")

# 3. Audit all 6 Maps
maps = [
    "/Game/PhobiaVR/Maps/L_PhobiaClinicHub",
    "/Game/PhobiaVR/Maps/L_Sim_Acrophobia",
    "/Game/PhobiaVR/Maps/L_Sim_Claustrophobia",
    "/Game/PhobiaVR/Maps/L_Sim_Arachnophobia",
    "/Game/PhobiaVR/Maps/L_Sim_Glossophobia",
    "/Game/PhobiaVR/Maps/L_Sim_Holochamber"
]

level_subsystem = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
editor_actor_subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)

log("--- AUDITING LEVELS ---")
for map_path in maps:
    map_name = map_path.split("/")[-1]
    loaded = level_subsystem.load_level(map_path)
    if not loaded:
        audit_results["issues_found"].append(f"Failed to load map {map_path}")
        continue
    
    actors = editor_actor_subsystem.get_all_level_actors()
    player_starts = [a for a in actors if isinstance(a, unreal.PlayerStart)]
    ambient_sounds = [a for a in actors if isinstance(a, unreal.AmbientSound)]
    static_meshes = [a for a in actors if isinstance(a, unreal.StaticMeshActor)]
    physics_actors = []
    missing_mesh_actors = []
    
    for sm_actor in static_meshes:
        smc = sm_actor.static_mesh_component
        if smc:
            mesh = smc.get_editor_property("static_mesh")
            if not mesh:
                missing_mesh_actors.append(sm_actor.get_actor_label())
            if smc.is_simulating_physics():
                physics_actors.append(sm_actor.get_actor_label())
    
    level_info = {
        "total_actors": len(actors),
        "player_start_count": len(player_starts),
        "player_start_locations": [str(ps.get_actor_location()) for ps in player_starts],
        "ambient_sounds": [f"{s.get_actor_label()} (Sound: {s.audio_component.get_editor_property('sound').get_name() if s.audio_component and s.audio_component.get_editor_property('sound') else 'None'})" for s in ambient_sounds],
        "physics_actors_count": len(physics_actors),
        "missing_mesh_count": len(missing_mesh_actors),
        "missing_mesh_actors": missing_mesh_actors
    }
    audit_results["levels"][map_name] = level_info
    log(f"[MAP: {map_name}] Actors: {len(actors)} | PlayerStarts: {len(player_starts)} | Physics Actors: {len(physics_actors)}")
    log(f"  Sounds: {len(ambient_sounds)} | Missing Meshes: {len(missing_mesh_actors)}")
    
    if len(player_starts) == 0:
        issue = f"{map_name} has NO PlayerStart!"
        audit_results["issues_found"].append(issue)
        log(f"  CRITICAL ISSUE: {issue}")
    
    if len(missing_mesh_actors) > 0:
        issue = f"{map_name} has {len(missing_mesh_actors)} actors with None static mesh: {missing_mesh_actors}"
        audit_results["issues_found"].append(issue)
        log(f"  WARNING: {issue}")

# Save report to absolute JSON path
report_dir = r"c:\Users\sanja\OneDrive\Desktop\meta 3d\Content\PhobiaVR\Data"
os.makedirs(report_dir, exist_ok=True)
report_path = os.path.join(report_dir, "AuditReport.json")

with open(report_path, "w") as f:
    json.dump(audit_results, f, indent=2)

log("=================================================================")
log(f"AUDIT SCRIPT FINISHED. Report saved to: {report_path}")
log(f"Total Issues Found: {len(audit_results['issues_found'])}")
log(f"Total Fixes Applied: {len(audit_results['fixes_applied'])}")
log("=================================================================")
