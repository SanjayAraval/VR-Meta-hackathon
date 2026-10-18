import unreal

print("=== Unreal Engine 5.8 Python API Test ===")
print(f"Engine Version: {unreal.SystemLibrary.get_engine_version()}")

# Test importing audio wav files into /Game/PhobiaVR/Audio/
wav_files = [
    ("c:/Users/sanja/OneDrive/Desktop/meta 3d/Content/PhobiaVR/Audio/A_ZenChime_Safe.wav", "/Game/PhobiaVR/Audio"),
    ("c:/Users/sanja/OneDrive/Desktop/meta 3d/Content/PhobiaVR/Audio/A_Wind_HighAltitude_Loop.wav", "/Game/PhobiaVR/Audio"),
    ("c:/Users/sanja/OneDrive/Desktop/meta 3d/Content/PhobiaVR/Audio/A_Elevator_Stall_Groan.wav", "/Game/PhobiaVR/Audio"),
    ("c:/Users/sanja/OneDrive/Desktop/meta 3d/Content/PhobiaVR/Audio/A_Spider_Skitter_Cue.wav", "/Game/PhobiaVR/Audio"),
    ("c:/Users/sanja/OneDrive/Desktop/meta 3d/Content/PhobiaVR/Audio/A_Audience_Murmur_Loop.wav", "/Game/PhobiaVR/Audio"),
    ("c:/Users/sanja/OneDrive/Desktop/meta 3d/Content/PhobiaVR/Audio/A_Heartbeat_Pulse_Cue.wav", "/Game/PhobiaVR/Audio"),
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
print("Imported audio tasks complete.")

# Verify imported sound waves
asset_reg = unreal.AssetRegistryHelpers.get_asset_registry()
assets = asset_reg.get_assets_by_path("/Game/PhobiaVR/Audio", recursive=True)
print(f"Total audio assets found in /Game/PhobiaVR/Audio: {len(assets)}")
for a in assets:
    print(f" - {a.asset_name} ({a.asset_class_path.asset_name})")

print("=== Test Complete ===")
