# Meta Quest Deployment & Packaging Guide for PhobiaVR

This guide walks you through playing PhobiaVR either **via Meta Quest Link (PCVR)** or **packaging as a standalone Android APK for Meta Quest 2 / 3 / 3S / Pro**.

---

## Part 1: Playing via Meta Quest Link / Air Link (Fastest & Highest Fidelity)

This method renders using your PC's GPU, delivering maximum graphical fidelity, full dynamic shadows, and high-resolution textures.

### Prerequisites:
1. Meta Quest Headset (Quest 2, Quest 3, Quest 3S, or Quest Pro).
2. [Meta Quest PC Software](https://www.meta.com/quest/setup/) installed on your PC.
3. USB 3.0 Type-C Cable (for Wired Link) OR a 5GHz Wi-Fi 6 Router (for Air Link).

### Steps:
1. Open the **Meta Quest PC software** on your computer.
2. Put on the Quest headset and enable **Quest Link** or **Air Link** from the Quick Settings menu.
3. Verify that your Oculus OpenXR Runtime is active:
   - In the Meta Quest PC app: Go to **Settings** -> **General** -> Under **OpenXR Runtime**, ensure it says *"Meta Quest Link is set as the active OpenXR runtime"*.
4. Launch `Launch_PhobiaVR.bat` or open `PhobiaVR.uproject` in Unreal Editor 5.8.
5. In the Unreal Editor toolbar, click the three vertical dots next to the green **Play** button and select **VR Preview** (Shortcut: `Alt + P` when VR preview is selected).
6. You will instantly be inside the VR experience in 90/120 Hz!

---

## Part 2: Packaging Standalone Android APK for Meta Quest

To package PhobiaVR to run untethered directly on the Meta Quest headset:

### Prerequisites:
1. **Android Studio** (Koala / Iguana or later) with Android SDK API Level 32 / 34 and NDK r25b installed.
2. **Meta XR Plugin** / OpenXR runtime configured (already integrated in `PhobiaVR.uproject` and `Config/DefaultEngine.ini`).

### Project Configuration (Pre-configured in this project):
- `AndroidEngine.ini` & `DefaultEngine.ini` are already customized with:
  ```ini
  [/Script/AndroidRuntimeSettings.AndroidRuntimeSettings]
  bBuildForES31=False
  ExtraApplicationSettings=<meta-data android:name="com.oculus.supportedDevices" android:value="quest2|questpro|quest3|quest3s" />\n<uses-native-library android:name="libopenxr.google.so" android:required="false" />
  bPackageForMetaQuest=True
  bPackageForOpenXRImmersive=True
  MinSDKVersion=32
  TargetSDKVersion=32
  ```

### Packaging Steps in Unreal Editor:
1. Open Unreal Editor 5.8 with `PhobiaVR.uproject`.
2. Go to **Platforms** dropdown in the top bar -> **Android** -> **Package Project**.
3. Choose a destination folder (e.g., `Builds/Android`).
4. Unreal Engine will compile the shaders and package `PhobiaVR-Android-Shipping-arm64.apk`.
5. Connect your Quest via USB-C and run the generated `Install_PhobiaVR-Android-Shipping-arm64.bat` script, or drag and drop the `.apk` using **SideQuest** or **Meta Quest Developer Hub (MQDH)**.
6. Inside the Quest headset, open your **App Library** -> Filter by **Unknown Sources** -> Launch **PhobiaVR**.

---

## Part 3: Clinical & Comfort Recommendations

- **Session Length**: We recommend 10 to 15 minute sessions per exposure tier.
- **SUDS Tracking**: Check the user's Subjective Units of Distress Scale (0-100) before and after each tier.
- **Panic Egress**: Remind users that pressing the **Menu button** (Left hand) or **B button** (Right hand) immediately returns them to the serene Zen Sanctuary.
- **Locomotion Choice**: For users prone to motion discomfort, use **Teleport Locomotion** (Left stick point-and-release) and **Snap Turn** (Right stick flick). Smooth locomotion can be toggled on demand.
