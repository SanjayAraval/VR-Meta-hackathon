@echo off
title Launch PhobiaVR - Meta Quest VR Exposure Therapy
echo =====================================================================
echo           PhobiaVR: Immersive 3D Phobia Simulator for Meta VR
echo =====================================================================
echo.
echo Launching Unreal Engine 5.8 Editor with PhobiaVR project...
echo Target Platform: Meta Quest 2 / Quest 3 / Quest 3S / Quest Pro
echo.

set "UE_EDITOR=C:\Documents\UE_5.8\Engine\Binaries\Win64\UnrealEditor.exe"
set "UPROJECT=%~dp0PhobiaVR.uproject"

if not exist "%UE_EDITOR%" (
    echo [ERROR] UnrealEditor.exe not found at %UE_EDITOR%
    pause
    exit /b 1
)

start "" "%UE_EDITOR%" "%UPROJECT%"
echo Unreal Editor launched successfully.
echo.
echo Once Unreal Editor opens:
echo  1. Put on your Meta Quest headset (with Quest Link or Air Link active).
echo  2. Click the Play button dropdown in the toolbar and select 'VR Preview'.
echo  3. You will immediately enter the Zen Sanctuary Clinic and can begin any phobia simulation!
echo.
pause
