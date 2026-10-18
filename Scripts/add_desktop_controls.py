import unreal

print("=== Adding Desktop Keyboard & Mouse Mappings to IMC_Default ===")

imc = unreal.EditorAssetLibrary.load_asset("/Game/XRFramework/Input/IMC_Default")
if not imc:
    print("Error: Could not load IMC_Default")
    exit(1)

# Helper to create Key
def make_key(name):
    k = unreal.Key()
    k.import_text(name)
    return k

# Load Actions
ia_move = unreal.EditorAssetLibrary.load_asset("/Game/XRFramework/Input/Actions/IA_Move")
ia_turn = unreal.EditorAssetLibrary.load_asset("/Game/XRFramework/Input/Actions/IA_Turn")
ia_grab_r = unreal.EditorAssetLibrary.load_asset("/Game/XRFramework/Input/Actions/IA_Grab_Right_Pressed")
ia_grab_l = unreal.EditorAssetLibrary.load_asset("/Game/XRFramework/Input/Actions/IA_Grab_Left_Pressed")
ia_menu = unreal.EditorAssetLibrary.load_asset("/Game/XRFramework/Input/Actions/IA_Menu_Toggle_Left")

keys_to_map = [
    (ia_move, "W"),
    (ia_move, "S"),
    (ia_move, "A"),
    (ia_move, "D"),
    (ia_turn, "MouseX"),
    (ia_turn, "Q"),
    (ia_turn, "E"),
    (ia_grab_r, "RightMouseButton"),
    (ia_grab_r, "F"),
    (ia_grab_l, "LeftMouseButton"),
    (ia_menu, "M"),
    (ia_menu, "Tab"),
]

for action, key_name in keys_to_map:
    if action:
        try:
            k = make_key(key_name)
            imc.map_key(action, k)
            print(f"Mapped {key_name} to {action.get_name()}")
        except Exception as e:
            print(f"Error mapping {key_name}: {e}")

unreal.EditorAssetLibrary.save_asset("/Game/XRFramework/Input/IMC_Default")
print("Saved IMC_Default with Desktop Keyboard/Mouse controls.")
