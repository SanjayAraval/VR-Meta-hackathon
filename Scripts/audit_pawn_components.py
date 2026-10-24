import unreal

bp = unreal.EditorAssetLibrary.load_asset("/Game/XRFramework/Blueprints/BP_XRPawn")
gen_class = unreal.EditorAssetLibrary.load_blueprint_class("/Game/XRFramework/Blueprints/BP_XRPawn")
cdo = unreal.get_default_object(gen_class)

print("=== BP_XRPawn Class ===", gen_class)

# Inspect subobject components in Blueprint generated class
for prop_name in dir(cdo):
    try:
        val = getattr(cdo, prop_name)
        if isinstance(val, unreal.ActorComponent):
            print(f"Component: {prop_name} -> {val.get_class().get_name()}")
    except:
        pass
