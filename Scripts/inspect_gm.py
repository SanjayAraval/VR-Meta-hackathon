import unreal

gm_class = unreal.EditorAssetLibrary.load_blueprint_class("/Game/XRFramework/Blueprints/BP_XRGameMode")
pawn_class = unreal.EditorAssetLibrary.load_blueprint_class("/Game/XRFramework/Blueprints/BP_XRPawn")

print(f"GameMode Class: {gm_class}")
print(f"Pawn Class: {pawn_class}")

# Inspect BP_XRGameMode default pawn class
gm_cdo = unreal.get_default_object(gm_class)
print(f"Default Pawn Class in GameMode: {gm_cdo.get_editor_property('default_pawn_class')}")
