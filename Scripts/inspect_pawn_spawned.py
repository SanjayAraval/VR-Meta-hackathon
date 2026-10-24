import unreal

sub = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
world = sub.get_editor_world()

gen_class = unreal.EditorAssetLibrary.load_blueprint_class("/Game/XRFramework/Blueprints/BP_XRPawn")
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)

actor = eas.spawn_actor_from_class(gen_class, unreal.Vector(0,0,0), unreal.Rotator(0,0,0))
if actor:
    comps = actor.get_components_by_class(unreal.ActorComponent)
    for c in comps:
        unreal.log(f"[COMP] {c.get_name()} ({c.get_class().get_name()})")
    eas.destroy_actor(actor)
