import unreal

print("=== Importing Terrifying Horror Soundscapes into UE 5.8 ===")

wav_files = [
    ("c:/Users/sanja/OneDrive/Desktop/meta 3d/Content/PhobiaVR/Audio/A_Horror_Drone_Ominous.wav", "/Game/PhobiaVR/Audio"),
    ("c:/Users/sanja/OneDrive/Desktop/meta 3d/Content/PhobiaVR/Audio/A_Jumpscare_Violin_Shriek.wav", "/Game/PhobiaVR/Audio"),
    ("c:/Users/sanja/OneDrive/Desktop/meta 3d/Content/PhobiaVR/Audio/A_Cable_Snap_Crash.wav", "/Game/PhobiaVR/Audio"),
    ("c:/Users/sanja/OneDrive/Desktop/meta 3d/Content/PhobiaVR/Audio/A_Spider_Swarm_Frenzy.wav", "/Game/PhobiaVR/Audio"),
    ("c:/Users/sanja/OneDrive/Desktop/meta 3d/Content/PhobiaVR/Audio/A_Vertigo_Abyss_Wind.wav", "/Game/PhobiaVR/Audio"),
    ("c:/Users/sanja/OneDrive/Desktop/meta 3d/Content/PhobiaVR/Audio/A_Whispers_Paranoia_Loop.wav", "/Game/PhobiaVR/Audio"),
    ("c:/Users/sanja/OneDrive/Desktop/meta 3d/Content/PhobiaVR/Audio/A_Tachycardia_Suffocation.wav", "/Game/PhobiaVR/Audio"),
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
print("Import of horror audio cues completed successfully.")
