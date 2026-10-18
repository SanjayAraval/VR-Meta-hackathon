import unreal

imc = unreal.EditorAssetLibrary.load_asset("/Game/XRFramework/Input/IMC_Default")
if not imc:
    print("Could not load IMC_Default")
    quit()

mappings = imc.get_editor_property("mappings")
print(f"Total mappings in IMC_Default: {len(mappings)}")

for m in mappings:
    action = m.get_editor_property("action")
    key = m.get_editor_property("key")
    modifiers = m.get_editor_property("modifiers")
    action_name = action.get_name() if action else "None"
    key_name = key.get_editor_property("key_name") if key else "None"
    mod_names = [mod.get_class().get_name() for mod in modifiers] if modifiers else []
    print(f"Action: {action_name} | Key: {key_name} | Modifiers: {mod_names}")
