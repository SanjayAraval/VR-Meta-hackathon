import unreal

map_path = "/Game/PhobiaVR/Maps/L_PhobiaClinicHub"
level_subsystem = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
level_subsystem.load_level(map_path)

eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
actors = eas.get_all_level_actors()
portals = [a.get_actor_label() for a in actors if "Portal" in a.get_actor_label() or "Console" in a.get_actor_label()]
print("=== Clinic Hub Portals & Consoles ===")
for p in sorted(portals):
    print(" -", p)
print(f"Total Actors in Hub: {len(actors)}")
