import unreal

el = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)

maps = [
    "/Game/PhobiaVR/Maps/L_PhobiaClinicHub",
    "/Game/PhobiaVR/Maps/L_Sim_Acrophobia",
    "/Game/PhobiaVR/Maps/L_Sim_Arachnophobia",
    "/Game/PhobiaVR/Maps/L_Sim_Claustrophobia",
    "/Game/PhobiaVR/Maps/L_Sim_Glossophobia"
]

print("\n================== LEVEL ACTOR REPORT ==================")
for m in maps:
    try:
        el.load_level(m)
        actors = eas.get_all_level_actors()
        print(f"Map: {m}")
        print(f"  Total Actors: {len(actors)}")
        for a in actors[:5]:
            print(f"   - {a.get_actor_label()} ({a.get_class().get_name()})")
        if len(actors) > 5:
            print(f"   ... and {len(actors)-5} more actors")
    except Exception as e:
        print(f"Error loading {m}: {e}")
print("========================================================\n")
