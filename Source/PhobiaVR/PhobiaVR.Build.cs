// Copyright (c) 2026 PhobiaVR Team. Meta Quest VR Competition.

using UnrealBuildTool;

public class PhobiaVR : ModuleRules
{
	public PhobiaVR(ReadOnlyTargetRules Target) : base(Target)
	{
		PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;

		PublicDependencyModuleNames.AddRange(new string[] {
			"Core",
			"CoreUObject",
			"Engine",
			"InputCore",
			"HeadMountedDisplay",
			"EnhancedInput"
		});

		PrivateDependencyModuleNames.AddRange(new string[] {
		});
	}
}
