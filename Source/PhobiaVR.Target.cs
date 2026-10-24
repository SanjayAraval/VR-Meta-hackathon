// Copyright (c) 2026 PhobiaVR Team. Meta Quest VR Competition.

using UnrealBuildTool;
using System.Collections.Generic;

public class PhobiaVRTarget : TargetRules
{
	public PhobiaVRTarget(TargetInfo Target) : base(Target)
	{
		Type = TargetType.Game;
		DefaultBuildSettings = BuildSettingsVersion.Latest;
		IncludeOrderVersion = EngineIncludeOrderVersion.Latest;
		ExtraModuleNames.Add("PhobiaVR");
	}
}
