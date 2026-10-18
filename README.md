# PhobiaVR: Immersive 3D Exposure Therapy Simulator for Meta Quest VR
*Engineered in Unreal Engine 5.8 with Native OpenXR and Meta Quest Touch Architecture*

---

## 📌 Project Overview
**PhobiaVR** is a clinical-grade Virtual Reality Exposure Therapy (VRET) simulation platform developed for Meta Quest headsets (Quest 2, Quest 3, Quest 3S, and Quest Pro). 

It bridges therapeutic exposure methodologies with high-immersion 3D environments, spatialized audio, haptic feedback, and biofeedback monitoring. Users navigate a calm sanctuary hub and enter graduated exposure tiers for four high-prevalence phobias.

---

## 🏛️ Simulation Environments & Maps

### 1. `L_PhobiaClinicHub` — The Zen Decompression Sanctuary
- **Design Philosophy**: A tranquil, Scandinavian-Japanese clinical sanctuary designed to lower baseline cortisol levels and provide grounding between exposure sessions.
- **Atmospheric Design**: Floor-to-ceiling glass panorama overlooking an outdoor nature garden with trees (`HillTree_02`) and a peaceful reflecting water pond (`SM_Water`).
- **Audio Cue**: 528 Hz Solfeggio harmonized meditation chime (`A_ZenChime_Safe.wav`) spatialized in the chamber.
- **Interactive Elements**:
  - Central circular therapy dais (`Central_Therapy_Platform`).
  - 4 Holographic Scenario Portals leading directly into the phobia environments.
  - Grabbable stress-relief cubes (`BP_Grabbable_SmallCube`) on a polished treatment table.
- **Safety Lifeline**: Anytime during any simulation, triggering the **Panic Lifeline** instantly returns the user to this room.

---

### 2. `L_Sim_Acrophobia` — The Skyscraper Vertigo Plank (Night Storm & Abyss)
- **Elevation**: 200 meters (20,000 Unreal Units) above street level on an 80th-floor skyscraper rooftop during a dark night storm.
- **Physics Simulation (Gravity Tumbling)**:
  - 8 real-time physics objects (`Phys_PaintCan_Edge1..2`, `Phys_SteelToolbox`, `Phys_CinderBlock_Plank`, `Phys_RollingSphere_Edge1..2`, `Phys_TeeteringPlank_Edge`).
  - Players can push, grab, and toss heavy steel toolboxes, concrete blocks, and rolling spheres off the plank edge to watch them plummet 200m down with true gravitational acceleration.
- **Eerie Audio & Psychological Terror**:
  - `A_Vertigo_Abyss_Wind.wav`: Desolate gale-force wind infused with descending Shepard vertigo tones creating dizzying depth illusions.
  - `A_Horror_Drone_Ominous.wav`: Sub-bass (38Hz) dread drone with dissonant tritones.
  - `A_Jumpscare_Violin_Shriek.wav`: Sudden microtonal screech stinger near the edge of the plank.

---

### 3. `L_Sim_Claustrophobia` — The Stalled Service Elevator (Cable Snap & Suffocation)
- **Dimensions**: Tightly constrained 2.0m x 2.0m x 2.3m metal freight elevator cabin.
- **Physics Simulation (Violent Shudders & Falling Debris)**:
  - Dislodged falling ceiling panel (`Phys_CeilingPanel_Loose`) crashing down to the floor.
  - Physics props tossed around the floor (`Phys_HeavyWrench`, `Phys_EmergencyFlashlight`, `Phys_Clipboard_Dropped`, `Phys_RollingSodaCan`).
- **Eerie Audio & Psychological Terror**:
  - `A_Cable_Snap_Crash.wav`: Groaning metal tension that suddenly snaps with an explosive whip-crack, rushing freefall wind, brake squeals, and cabin impact.
  - `A_Tachycardia_Suffocation.wav`: Frantic 150 BPM tachycardia heartbeat with choking, gasping hyperventilation.
  - `A_Whispers_Paranoia_Loop.wav`: Disembodied, creepy whispering voices echoing through the dark shaft.
  - Blood-red emergency strobe beacon casting violent moving shadows.

---

### 4. `L_Sim_Arachnophobia` — The Infested Specimen Lab (Chitinous Swarm Frenzy)
- **Setting**: Dilapidated, dark entomological research laboratory.
- **Physics Simulation (Knockdown Chemistry & Terrarium Lid)**:
  - Interactive physics terrarium lid (`Phys_TerrariumLid`) that flips and clatters when nudged.
  - Laboratory glassware (`Phys_ChemicalFlask_Left`, `Phys_ChemicalFlask_Front`), metal specimen tray, and heavy medical books that tumble across the table.
- **Arachnid Hierarchy & Hanging Spiders**:
  - Ceiling spider suspended directly at head height on a silk thread, swinging towards the player.
  - Escaped tabletop arachnids, giant wall-crawling specimens, and terrarium inhabitant.
- **Eerie Audio & Psychological Terror**:
  - `A_Spider_Swarm_Frenzy.wav`: Over 120 wet chitinous foot clicks, mandibles tapping, and venomous hissing directly inside the player's ears.
  - `A_Jumpscare_Violin_Shriek.wav`: Razor-sharp violin stinger when approaching the specimen.

---

### 5. `L_Sim_Glossophobia` — The Nightmare Auditorium (Paranoia Whispers & Blinding Glare)
- **Setting**: Pitch black amphitheater viewed from the speaker's podium.
- **Physics Simulation (Fluttering Speech Notes)**:
  - 4 loose paper speech cue cards (`Phys_SpeechPage_1..4`) with low mass that flutter, scatter, and slide off the podium if brushed.
  - Physics water tumbler (`Phys_WaterGlass_Podium`) that spills and tumbles.
- **Menacing Audience Silhouettes**:
  - 35 sinister shadow silhouettes sitting motionlessly in the darkness, staring directly at the presenter under 65,000-lux glaring spotlights.
- **Eerie Audio & Psychological Terror**:
  - `A_Whispers_Paranoia_Loop.wav`: Layered creeping whispers and murmurs ("they're judging you...", "run away...").
  - `A_Tachycardia_Suffocation.wav`: Suffocating panic breathing and chest-pounding heartbeat.
  - `A_Horror_Drone_Ominous.wav`: Ambient nightmare drone.

---

## 🎮 Controller Layout (Meta Quest Touch / Touch Plus / Quest Pro)

| Controller | Input Action | Function in Simulator |
|---|---|---|
| **Left Thumbstick** | Movement Axis (X/Y) | Smooth locomotion or Teleportation arc |
| **Right Thumbstick** | Snap / Smooth Turn | 45-degree comfort snap turning |
| **Left Grip / Right Grip** | Grab Pressed | Grab stress cubes, physics drop items, flashlight, bell |
| **Left Trigger / Right Trigger** | Trigger Click | Interact with UI buttons / confirm portal destination |
| **Left Menu / B Button** | Panic Lifeline | **Instant Egress**: Emergency return to Zen Sanctuary |

---

## 🚀 How to Launch & Play

### Option 1: One-Click Quick Launch
Double-click `Launch_PhobiaVR.bat` located in the project root:
```bat
c:\Users\sanja\OneDrive\Desktop\meta 3d\Launch_PhobiaVR.bat
```

### Option 2: Through Unreal Engine 5.8 Editor
1. Connect your Meta Quest to your PC via **Meta Quest Link cable** (USB 3.0) or **Air Link** (5GHz Wi-Fi).
2. Ensure the **Meta Quest PC app** is open and device status shows **Connected**.
3. Launch Unreal Engine 5.8 and open `PhobiaVR.uproject`.
4. In the main editor toolbar, click the dropdown next to the **Play** button and choose **VR Preview**.
5. Put on your headset. You will spawn directly in `L_PhobiaClinicHub`!

---

## 📦 Technical Specifications
- **Engine**: Unreal Engine 5.8
- **XR Pipeline**: OpenXR (Standard XR runtime for Meta Quest, OpenXRHandTracking, OpenXREyeTracker)
- **Render Settings**: Forward Shading (`r.ForwardShading=True`), MSAA 4x, Instanced Stereo (`vr.InstancedStereo=True`), Mobile Multi-View (`vr.MobileMultiView=True`)
- **Target Hardware**: Meta Quest 2 / Quest 3 / Quest 3S / Quest Pro / PCVR Link
