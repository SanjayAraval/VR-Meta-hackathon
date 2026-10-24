import unreal

gen_class = unreal.EditorAssetLibrary.load_blueprint_class("/Game/XRFramework/Blueprints/BP_XRPawn")
bp = unreal.EditorAssetLibrary.load_asset("/Game/XRFramework/Blueprints/BP_XRPawn")

scs = bp.get_editor_property("simple_construction_script")
if scs:
    nodes = scs.get_all_nodes()
    print("=== SCS Nodes in BP_XRPawn ===")
    for n in nodes:
        c_template = n.get_editor_property("component_template")
        var_name = n.get_editor_property("variable_name")
        c_class = c_template.get_class().get_name() if c_template else "Unknown"
        print(f"Node: {var_name} ({c_class})")
