import unreal

print("=== Verifying Generated PhobiaVR Maps ===")
maps = [
    "/Game/PhobiaVR/Maps/L_PhobiaClinicHub",
    "/Game/PhobiaVR/Maps/L_Sim_Acrophobia",
    "/Game/PhobiaVR/Maps/L_Sim_Claustrophobia",
    "/Game/PhobiaVR/Maps/L_Sim_Arachnophobia",
    "/Game/PhobiaVR/Maps/L_Sim_Glossophobia"
]

asset_reg = unreal.AssetRegistryHelpers.get_asset_registry()
for m in maps:
    exists = unreal.EditorAssetLibrary.does_asset_exist(m)
    print(f"Map {m}: {'EXISTS' if exists else 'NOT FOUND'}")

print("=== Check Complete ===")
