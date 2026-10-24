// Copyright (c) 2026 PhobiaVR Team. Meta Quest VR Competition.

#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "InputCoreTypes.h"
#include "HeadMountedDisplayTypes.h"
#include "PhobiaHandTrackingComponent.generated.h"

class IHandTracker;

/** Current active input mode */
UENUM(BlueprintType)
enum class EPhobiaInputMode : uint8
{
	HandTracking          UMETA(DisplayName = "Hand Tracking (VR)"),
	DesktopKeyboardMouse  UMETA(DisplayName = "Desktop Keyboard / Mouse Fallback")
};

/** State data tracked per hand */
USTRUCT(BlueprintType)
struct FPhobiaHandState
{
	GENERATED_BODY()

	UPROPERTY(BlueprintReadOnly, Category = "Hand Tracking")
	bool bIsTracked = false;

	UPROPERTY(BlueprintReadOnly, Category = "Hand Tracking")
	bool bIsPinching = false;

	UPROPERTY(BlueprintReadOnly, Category = "Hand Tracking")
	float PinchDistance = 100.0f; // in cm

	UPROPERTY(BlueprintReadOnly, Category = "Hand Tracking")
	FVector PinchLocation = FVector::ZeroVector;

	UPROPERTY(BlueprintReadOnly, Category = "Hand Tracking")
	bool bIsPoking = false;

	UPROPERTY(BlueprintReadOnly, Category = "Hand Tracking")
	FVector PokeLocation = FVector::ZeroVector;

	UPROPERTY(BlueprintReadOnly, Category = "Hand Tracking")
	FVector PokeDirection = FVector::ForwardVector;

	UPROPERTY(BlueprintReadOnly, Category = "Hand Tracking")
	bool bIsPalmUp = false;

	UPROPERTY(BlueprintReadOnly, Category = "Hand Tracking")
	FVector PalmLocation = FVector::ZeroVector;

	UPROPERTY(BlueprintReadOnly, Category = "Hand Tracking")
	FVector PalmNormal = FVector::UpVector;

	// Internal previous positions for velocity calculations
	FVector PrevIndexTipLocation = FVector::ZeroVector;
	float PokeCooldownTimer = 0.0f;

	// Keypoint arrays (world space)
	TArray<FVector> JointPositions;
	TArray<FQuat> JointRotations;
	TArray<float> JointRadii;
};

// Delegates
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnHandPinchSignature, EControllerHand, Hand, const FVector&, PinchLocation);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_ThreeParams(FOnHandPokeSignature, EControllerHand, Hand, const FVector&, TipLocation, const FVector&, PokeDirection);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_ThreeParams(FOnPalmUpSignature, EControllerHand, Hand, bool, bIsPalmUp, const FVector&, PalmLocation);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnInputModeChangedSignature, EPhobiaInputMode, NewMode);

/**
 * UPhobiaHandTrackingComponent
 *
 * Implements an OpenXR / Meta XR hand tracking layer for VR Pawns in PhobiaVR.
 * Features:
 * - Direct interface with OpenXR/Meta XR Hand Tracking APIs (IHandTracker / EHandKeypoint).
 * - Full 26-joint skeleton pose extraction in UE world space.
 * - Robust pinch gesture detection with hysteresis (PinchEnterDistance vs PinchExitDistance).
 * - Index fingertip poke detection with extension and velocity analysis.
 * - Palm-up gesture detection with anatomical normal calculation and angle hysteresis.
 * - Dual-mode auto-switching: automatically falls back to Desktop Keyboard/Mouse when hands are not tracked.
 * - Built-in debug visualization drawing joints, bones, gesture vectors, and status HUD.
 */
UCLASS(ClassGroup=(PhobiaVR), meta=(BlueprintSpawnableComponent))
class PHOBIAVR_API UPhobiaHandTrackingComponent : public UActorComponent
{
	GENERATED_BODY()

public:
	UPhobiaHandTrackingComponent();

	virtual void BeginPlay() override;
	virtual void TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) override;

	// -------------------------------------------------------------
	// DELEGATES
	// -------------------------------------------------------------

	/** Fired when thumb and index finger touch / close past enter threshold */
	UPROPERTY(BlueprintAssignable, Category = "Hand Tracking|Events")
	FOnHandPinchSignature OnPinchStarted;

	/** Fired when pinched thumb and index finger release past exit threshold */
	UPROPERTY(BlueprintAssignable, Category = "Hand Tracking|Events")
	FOnHandPinchSignature OnPinchEnded;

	/** Fired when index fingertip pokes or strikes forward */
	UPROPERTY(BlueprintAssignable, Category = "Hand Tracking|Events")
	FOnHandPokeSignature OnPoke;

	/** Fired when palm transitions to/from facing upward towards the sky */
	UPROPERTY(BlueprintAssignable, Category = "Hand Tracking|Events")
	FOnPalmUpSignature OnPalmUpStateChanged;

	/** Fired when input mode changes between Hand Tracking and Desktop Fallback */
	UPROPERTY(BlueprintAssignable, Category = "Hand Tracking|Events")
	FOnInputModeChangedSignature OnInputModeChanged;

	// -------------------------------------------------------------
	// CONFIGURATION & THRESHOLDS
	// -------------------------------------------------------------

	/** Distance (in cm) between thumb and index tip to enter pinch state. Default: 2.5 cm */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Hand Tracking|Settings|Pinch")
	float PinchEnterDistance = 2.5f;

	/** Distance (in cm) between thumb and index tip to exit pinch state (hysteresis). Default: 4.0 cm */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Hand Tracking|Settings|Pinch")
	float PinchExitDistance = 4.0f;

	/** Dot product threshold with World Up (0,0,1) to trigger Palm Up (0.707 = ~45 deg). Default: 0.707 */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Hand Tracking|Settings|Palm Up")
	float PalmUpEnterThreshold = 0.707f;

	/** Dot product threshold with World Up (0,0,1) to exit Palm Up (hysteresis, 0.5 = ~60 deg). Default: 0.5 */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Hand Tracking|Settings|Palm Up")
	float PalmUpExitThreshold = 0.5f;

	/** Forward speed (cm/s) of index fingertip along poke direction required to trigger poke. Default: 30 cm/s */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Hand Tracking|Settings|Poke")
	float PokeVelocityThreshold = 30.0f;

	/** Minimum time (seconds) between consecutive poke events to prevent spamming. Default: 0.3s */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Hand Tracking|Settings|Poke")
	float PokeCooldown = 0.3f;

	/** Seconds without tracked hands before falling back to Desktop mode. Default: 1.0s */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Hand Tracking|Settings|Mode")
	float TrackingTimeout = 1.0f;

	/** Automatically switch between Hand Tracking and Desktop mode at runtime. Default: true */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Hand Tracking|Settings|Mode")
	bool bAutoSwitchInputMode = true;

	/** Whether debug visualization is currently rendered. Default: true */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Hand Tracking|Debug")
	bool bEnableDebugDraw = true;

	// -------------------------------------------------------------
	// PUBLIC API QUERIES
	// -------------------------------------------------------------

	/** Returns true if the specified hand is currently tracked */
	UFUNCTION(BlueprintPure, Category = "Hand Tracking|Queries")
	bool IsHandTracked(EControllerHand Hand) const;

	/** Returns true if the specified hand is currently pinching */
	UFUNCTION(BlueprintPure, Category = "Hand Tracking|Queries")
	bool IsPinching(EControllerHand Hand) const;

	/** Returns true if the specified hand has its palm facing upward */
	UFUNCTION(BlueprintPure, Category = "Hand Tracking|Queries")
	bool IsPalmUp(EControllerHand Hand) const;

	/** Returns the pinch location (midpoint of thumb and index) if available */
	UFUNCTION(BlueprintPure, Category = "Hand Tracking|Queries")
	bool GetPinchLocation(EControllerHand Hand, FVector& OutLocation) const;

	/** Returns distance between thumb and index tip in cm */
	UFUNCTION(BlueprintPure, Category = "Hand Tracking|Queries")
	float GetPinchDistance(EControllerHand Hand) const;

	/** Returns index fingertip position and forward poke direction */
	UFUNCTION(BlueprintPure, Category = "Hand Tracking|Queries")
	bool GetIndexTipPose(EControllerHand Hand, FVector& OutLocation, FVector& OutDirection) const;

	/** Gets the world-space transform and radius of any specific joint */
	UFUNCTION(BlueprintPure, Category = "Hand Tracking|Queries")
	bool GetJointTransform(EControllerHand Hand, EHandKeypoint Keypoint, FTransform& OutTransform, float& OutRadius) const;

	/** Returns the current input mode */
	UFUNCTION(BlueprintPure, Category = "Hand Tracking|Mode")
	EPhobiaInputMode GetCurrentInputMode() const { return CurrentInputMode; }

	/** Explicitly sets the input mode (disabling or overriding auto-switch) */
	UFUNCTION(BlueprintCallable, Category = "Hand Tracking|Mode")
	void SetCurrentInputMode(EPhobiaInputMode NewMode);

	/** Toggles debug skeleton drawing on or off */
	UFUNCTION(BlueprintCallable, Category = "Hand Tracking|Debug")
	void ToggleDebugDraw();

	/** Sets debug drawing explicitly */
	UFUNCTION(BlueprintCallable, Category = "Hand Tracking|Debug")
	void SetDebugDraw(bool bEnabled);

protected:
	/** Queries IHandTracker modular feature for current frame joint poses */
	void UpdateHandJoints(EControllerHand Hand, FPhobiaHandState& State, float DeltaTime);

	/** Computes pinch hysteresis and fires events */
	void ProcessPinchGesture(EControllerHand Hand, FPhobiaHandState& State);

	/** Computes poke extension, velocity, and fires events */
	void ProcessPokeGesture(EControllerHand Hand, FPhobiaHandState& State, float DeltaTime);

	/** Computes palm normal vector and palm-up hysteresis */
	void ProcessPalmUpGesture(EControllerHand Hand, FPhobiaHandState& State);

	/** Manages runtime mode switching between VR hand tracking and desktop fallback */
	void ProcessInputModeSwitching(float DeltaTime);

	/** Renders debug spheres, bones, gesture vectors, and text HUD */
	void DrawDebugVisualization();

	/** Helper to draw a single finger chain of joints and bones */
	void DrawDebugFinger(const FPhobiaHandState& State, int32 StartJoint, int32 EndJoint, const FColor& BoneColor);

	/** Fallback simulation of pinch when running in desktop mode */
	void ProcessDesktopFallbackSimulation();

private:
	IHandTracker* GetHandTracker() const;

	UPROPERTY(VisibleInstanceOnly, Category = "Hand Tracking")
	EPhobiaInputMode CurrentInputMode = EPhobiaInputMode::DesktopKeyboardMouse;

	FPhobiaHandState LeftHandState;
	FPhobiaHandState RightHandState;

	float TimeSinceLastHandTracking = 100.0f;
	bool bLeftMouseWasDown = false;
	bool bRightMouseWasDown = false;
};
