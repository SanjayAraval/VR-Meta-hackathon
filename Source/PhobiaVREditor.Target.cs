// Copyright (c) 2026 PhobiaVR Team. Meta Quest VR Competition.

using UnrealBuildTool;
using System.Collections.Generic;

public class PhobiaVREditorTarget : TargetRules
{
	public PhobiaVREditorTarget(TargetInfo Target) : base(Target)
	{
		Type = TargetType.Editor;
		DefaultBuildSettings = BuildSettingsVersion.Latest;
		IncludeOrderVersion = EngineIncludeOrderVersion.Latest;
		ExtraModuleNames.Add("PhobiaVR");
	}
}
