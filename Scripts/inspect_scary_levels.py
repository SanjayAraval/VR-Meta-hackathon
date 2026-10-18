import unreal

maps = [
    "/Game/PhobiaVR/Maps/L_PhobiaClinicHub",
    "/Game/PhobiaVR/Maps/L_Sim_Acrophobia",
    "/Game/PhobiaVR/Maps/L_Sim_Claustrophobia",
    "/Game/PhobiaVR/Maps/L_Sim_Arachnophobia",
    "/Game/PhobiaVR/Maps/L_Sim_Glossophobia"
]

editor_level_subsystem = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
editor_actor_subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)

print("\n=== Inspecting Upgraded Physics & Horror Levels ===")
for m in maps:
    editor_level_subsystem.load_level(m)
    actors = editor_actor_subsystem.get_all_level_actors()
    physics_actors = []
    sound_actors = []
    for a in actors:
        if isinstance(a, unreal.StaticMeshActor):
            if a.get_actor_label().startswith("Phys_"):
                physics_actors.append(a.get_actor_label())
        elif isinstance(a, unreal.AmbientSound):
            asc = a.audio_component
            s_name = asc.sound.get_name() if asc and asc.sound else "None"
            sound_actors.append(f"{a.get_actor_label()} [{s_name}]")
            
    print(f"\nMap: {m}")
    print(f" - Total Actors: {len(actors)}")
    print(f" - Physics Simulating Props ({len(physics_actors)}): {', '.join(physics_actors[:6])}...")
    print(f" - Audio Ambience Cues ({len(sound_actors)}): {', '.join(sound_actors)}")

print("\n=== Inspection Complete ===")
