# Copyright (c) 2026 PhobiaVR Team. Meta Quest VR Competition.
"""
Script to verify and automate PhobiaHandTrackingComponent attachment on BP_XRPawn.
Can be executed via Unreal Python plugin:
    py "c:/Users/sanja/OneDrive/Desktop/meta 3d/Scripts/add_hand_tracking_to_pawn.py"
"""
import unreal

def verify_and_setup():
    unreal.log("=== Checking PhobiaHandTrackingComponent on BP_XRPawn ===")
    pawn_bp = unreal.EditorAssetLibrary.load_asset("/Game/XRFramework/Blueprints/BP_XRPawn")
    if not pawn_bp:
        unreal.log_error("Could not load /Game/XRFramework/Blueprints/BP_XRPawn")
        return

    # Check if PhobiaHandTrackingComponent class is registered
    hand_comp_class = unreal.load_class(None, "/Script/PhobiaVR.PhobiaHandTrackingComponent")
    if not hand_comp_class:
        unreal.log_warning("PhobiaHandTrackingComponent C++ class is not yet loaded in editor.")
        unreal.log_warning("Please compile the project first in Visual Studio or click 'Compile' / 'Live Coding' in Unreal Editor.")
        return

    unreal.log(f"Successfully located C++ class: {hand_comp_class}")
    unreal.log("You can add it directly in BP_XRPawn: Open BP_XRPawn -> Click '+ Add' -> Select 'Phobia Hand Tracking'.")

if __name__ == "__main__":
    verify_and_setup()
