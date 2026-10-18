import unreal

def log(msg):
    unreal.log(f"[PAWN_AUDIT] {msg}")

pawn_class = unreal.EditorAssetLibrary.load_blueprint_class("/Game/XRFramework/Blueprints/BP_XRPawn")
log(f"Loaded pawn class: {pawn_class}")

cdo = unreal.get_default_object(pawn_class)
log(f"CDO: {cdo}")

# Inspect components
subsystems = unreal.get_editor_subsystem(unreal.SubsystemBlueprintLibrary)
# List components on the pawn class
for prop in dir(cdo):
    if any(k in prop.lower() for k in ["camera", "movement", "input", "collision", "root"]):
        log(f"Pawn property: {prop}")
