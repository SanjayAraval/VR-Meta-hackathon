// Copyright (c) 2026 PhobiaVR Team. Meta Quest VR Competition.

#include "PhobiaHandTrackingComponent.h"
#include "Features/IModularFeatures.h"
#include "IHandTracker.h"
#include "DrawDebugHelpers.h"
#include "Engine/World.h"
#include "Engine/Engine.h"
#include "GameFramework/PlayerController.h"
#include "Kismet/GameplayStatics.h"
#include "HAL/IConsoleManager.h"

// Console variable to toggle debug rendering in runtime
static TAutoConsoleVariable<int32> CVarPhobiaDebugHands(
	TEXT("phobia.HandTracking.Debug"),
	1,
	TEXT("Controls PhobiaVR Hand Tracking debug visualization (0 = off, 1 = on)"),
	ECVF_Cheat
);

UPhobiaHandTrackingComponent::UPhobiaHandTrackingComponent()
{
	PrimaryComponentTick.bCanEverTick = true;
	PrimaryComponentTick.TickGroup = TG_PrePhysics;

	// Pre-allocate joint arrays for 26 keypoints
	LeftHandState.JointPositions.SetNumZeroed(EHandKeypointCount);
	LeftHandState.JointRotations.SetNumZeroed(EHandKeypointCount);
	LeftHandState.JointRadii.SetNumZeroed(EHandKeypointCount);

	RightHandState.JointPositions.SetNumZeroed(EHandKeypointCount);
	RightHandState.JointRotations.SetNumZeroed(EHandKeypointCount);
	RightHandState.JointRadii.SetNumZeroed(EHandKeypointCount);
}

void UPhobiaHandTrackingComponent::BeginPlay()
{
	Super::BeginPlay();

	// Broadcast initial mode
	OnInputModeChanged.Broadcast(CurrentInputMode);
}

void UPhobiaHandTrackingComponent::TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction)
{
	Super::TickComponent(DeltaTime, TickType, ThisTickFunction);

	// Decrement poke cooldowns
	if (LeftHandState.PokeCooldownTimer > 0.0f)
	{
		LeftHandState.PokeCooldownTimer = FMath::Max(0.0f, LeftHandState.PokeCooldownTimer - DeltaTime);
	}
	if (RightHandState.PokeCooldownTimer > 0.0f)
	{
		RightHandState.PokeCooldownTimer = FMath::Max(0.0f, RightHandState.PokeCooldownTimer - DeltaTime);
	}

	// 1. Query joint poses for both hands
	UpdateHandJoints(EControllerHand::Left, LeftHandState, DeltaTime);
	UpdateHandJoints(EControllerHand::Right, RightHandState, DeltaTime);

	// 2. Manage runtime input mode auto-switching
	ProcessInputModeSwitching(DeltaTime);

	// 3. Process gestures if hands are tracked
	if (LeftHandState.bIsTracked)
	{
		ProcessPinchGesture(EControllerHand::Left, LeftHandState);
		ProcessPokeGesture(EControllerHand::Left, LeftHandState, DeltaTime);
		ProcessPalmUpGesture(EControllerHand::Left, LeftHandState);
	}
	else
	{
		if (LeftHandState.bIsPinching)
		{
			LeftHandState.bIsPinching = false;
			OnPinchEnded.Broadcast(EControllerHand::Left, LeftHandState.PinchLocation);
		}
		if (LeftHandState.bIsPalmUp)
		{
			LeftHandState.bIsPalmUp = false;
			OnPalmUpStateChanged.Broadcast(EControllerHand::Left, false, LeftHandState.PalmLocation);
		}
		LeftHandState.bIsPoking = false;
	}

	if (RightHandState.bIsTracked)
	{
		ProcessPinchGesture(EControllerHand::Right, RightHandState);
		ProcessPokeGesture(EControllerHand::Right, RightHandState, DeltaTime);
		ProcessPalmUpGesture(EControllerHand::Right, RightHandState);
	}
	else
	{
		if (RightHandState.bIsPinching)
		{
			RightHandState.bIsPinching = false;
			OnPinchEnded.Broadcast(EControllerHand::Right, RightHandState.PinchLocation);
		}
		if (RightHandState.bIsPalmUp)
		{
			RightHandState.bIsPalmUp = false;
			OnPalmUpStateChanged.Broadcast(EControllerHand::Right, false, RightHandState.PalmLocation);
		}
		RightHandState.bIsPoking = false;
	}

	// 4. Desktop fallback simulation when active
	if (CurrentInputMode == EPhobiaInputMode::DesktopKeyboardMouse)
	{
		ProcessDesktopFallbackSimulation();
	}

	// 5. Debug rendering
	if (bEnableDebugDraw && CVarPhobiaDebugHands.GetValueOnGameThread() != 0)
	{
		DrawDebugVisualization();
	}
}

IHandTracker* UPhobiaHandTrackingComponent::GetHandTracker() const
{
	if (IModularFeatures::Get().IsModularFeatureAvailable(IHandTracker::GetModularFeatureName()))
	{
		TArray<IHandTracker*> Trackers = IModularFeatures::Get().GetModularFeatureImplementations<IHandTracker>(IHandTracker::GetModularFeatureName());
		for (IHandTracker* Tracker : Trackers)
		{
			if (Tracker && Tracker->IsHandTrackingStateValid())
			{
				return Tracker;
			}
		}
		if (Trackers.Num() > 0)
		{
			return Trackers[0];
		}
	}
	return nullptr;
}

void UPhobiaHandTrackingComponent::UpdateHandJoints(EControllerHand Hand, FPhobiaHandState& State, float DeltaTime)
{
	IHandTracker* Tracker = GetHandTracker();
	if (!Tracker)
	{
		State.bIsTracked = false;
		return;
	}

	bool bTracked = false;
	bool bSuccess = Tracker->GetAllKeypointStates(Hand, State.JointPositions, State.JointRotations, State.JointRadii, bTracked);

	// Fallback to individual keypoint query if GetAllKeypointStates failed or returned incomplete array
	if (!bSuccess || State.JointPositions.Num() < EHandKeypointCount)
	{
		State.JointPositions.SetNumZeroed(EHandKeypointCount);
		State.JointRotations.SetNumZeroed(EHandKeypointCount);
		State.JointRadii.SetNumZeroed(EHandKeypointCount);

		bool bAnyKeypointValid = false;
		for (int32 i = 0; i < EHandKeypointCount; ++i)
		{
			FTransform OutTransform;
			float OutRadius = 0.8f;
			if (Tracker->GetKeypointState(Hand, static_cast<EHandKeypoint>(i), OutTransform, OutRadius))
			{
				State.JointPositions[i] = OutTransform.GetLocation();
				State.JointRotations[i] = OutTransform.GetRotation();
				State.JointRadii[i] = OutRadius;
				bAnyKeypointValid = true;
			}
		}
		State.bIsTracked = bAnyKeypointValid;
	}
	else
	{
		State.bIsTracked = bTracked;
	}

	if (State.bIsTracked && State.JointPositions.Num() >= EHandKeypointCount)
	{
		State.PalmLocation = State.JointPositions[(int32)EHandKeypoint::Palm];
	}
}

void UPhobiaHandTrackingComponent::ProcessPinchGesture(EControllerHand Hand, FPhobiaHandState& State)
{
	const FVector& ThumbTip = State.JointPositions[(int32)EHandKeypoint::ThumbTip];
	const FVector& IndexTip = State.JointPositions[(int32)EHandKeypoint::IndexTip];

	float Distance = FVector::Dist(ThumbTip, IndexTip);
	State.PinchDistance = Distance;
	State.PinchLocation = (ThumbTip + IndexTip) * 0.5f;

	if (!State.bIsPinching)
	{
		// Pinch Started: distance dropped below entry threshold
		if (Distance <= PinchEnterDistance)
		{
			State.bIsPinching = true;
			OnPinchStarted.Broadcast(Hand, State.PinchLocation);
		}
	}
	else
	{
		// Pinch Ended: distance opened past hysteresis exit threshold
		if (Distance >= PinchExitDistance)
		{
			State.bIsPinching = false;
			OnPinchEnded.Broadcast(Hand, State.PinchLocation);
		}
	}
}

void UPhobiaHandTrackingComponent::ProcessPokeGesture(EControllerHand Hand, FPhobiaHandState& State, float DeltaTime)
{
	const FVector& IndexProximal = State.JointPositions[(int32)EHandKeypoint::IndexProximal];
	const FVector& IndexIntermediate = State.JointPositions[(int32)EHandKeypoint::IndexIntermediate];
	const FVector& IndexDistal = State.JointPositions[(int32)EHandKeypoint::IndexDistal];
	const FVector& IndexTip = State.JointPositions[(int32)EHandKeypoint::IndexTip];

	State.PokeLocation = IndexTip;
	State.PokeDirection = (IndexTip - IndexDistal).GetSafeNormal();

	// Check finger extension: segments must align closely (straight index finger)
	FVector Seg1 = (IndexIntermediate - IndexProximal).GetSafeNormal();
	FVector Seg2 = (IndexDistal - IndexIntermediate).GetSafeNormal();
	FVector Seg3 = State.PokeDirection;

	bool bIsExtended = (FVector::DotProduct(Seg1, Seg2) > 0.65f) && (FVector::DotProduct(Seg2, Seg3) > 0.65f);

	if (DeltaTime > 0.0001f && !State.PrevIndexTipLocation.IsZero())
	{
		FVector TipVelocity = (IndexTip - State.PrevIndexTipLocation) / DeltaTime;
		float ForwardSpeed = FVector::DotProduct(TipVelocity, State.PokeDirection);

		if (bIsExtended && ForwardSpeed >= PokeVelocityThreshold && State.PokeCooldownTimer <= 0.0f)
		{
			State.bIsPoking = true;
			State.PokeCooldownTimer = PokeCooldown;
			OnPoke.Broadcast(Hand, State.PokeLocation, State.PokeDirection);
		}
		else if (State.PokeCooldownTimer <= (PokeCooldown * 0.5f))
		{
			State.bIsPoking = false;
		}
	}

	State.PrevIndexTipLocation = IndexTip;
}

void UPhobiaHandTrackingComponent::ProcessPalmUpGesture(EControllerHand Hand, FPhobiaHandState& State)
{
	const FVector& Wrist = State.JointPositions[(int32)EHandKeypoint::Wrist];
	const FVector& MiddleKnuckle = State.JointPositions[(int32)EHandKeypoint::MiddleProximal];
	const FVector& IndexKnuckle = State.JointPositions[(int32)EHandKeypoint::IndexProximal];
	const FVector& LittleKnuckle = State.JointPositions[(int32)EHandKeypoint::LittleProximal];

	FVector Forward = (MiddleKnuckle - Wrist).GetSafeNormal();
	FVector Across = (LittleKnuckle - IndexKnuckle).GetSafeNormal();

	FVector Normal;
	if (Hand == EControllerHand::Right)
	{
		Normal = FVector::CrossProduct(Forward, Across).GetSafeNormal();
	}
	else
	{
		Normal = FVector::CrossProduct(Across, Forward).GetSafeNormal();
	}

	State.PalmNormal = Normal;
	float UpDot = FVector::DotProduct(Normal, FVector::UpVector);

	if (!State.bIsPalmUp)
	{
		if (UpDot >= PalmUpEnterThreshold)
		{
			State.bIsPalmUp = true;
			OnPalmUpStateChanged.Broadcast(Hand, true, State.PalmLocation);
		}
	}
	else
	{
		if (UpDot < PalmUpExitThreshold)
		{
			State.bIsPalmUp = false;
			OnPalmUpStateChanged.Broadcast(Hand, false, State.PalmLocation);
		}
	}
}

void UPhobiaHandTrackingComponent::ProcessInputModeSwitching(float DeltaTime)
{
	if (!bAutoSwitchInputMode)
	{
		return;
	}

	bool bAnyHandTracked = LeftHandState.bIsTracked || RightHandState.bIsTracked;

	if (bAnyHandTracked)
	{
		TimeSinceLastHandTracking = 0.0f;
		if (CurrentInputMode != EPhobiaInputMode::HandTracking)
		{
			SetCurrentInputMode(EPhobiaInputMode::HandTracking);
		}
	}
	else
	{
		TimeSinceLastHandTracking += DeltaTime;
		if (TimeSinceLastHandTracking >= TrackingTimeout && CurrentInputMode != EPhobiaInputMode::DesktopKeyboardMouse)
		{
			SetCurrentInputMode(EPhobiaInputMode::DesktopKeyboardMouse);
		}
	}
}

void UPhobiaHandTrackingComponent::ProcessDesktopFallbackSimulation()
{
	UWorld* World = GetWorld();
	if (!World)
	{
		return;
	}

	APlayerController* PC = UGameplayStatics::GetPlayerController(World, 0);
	if (!PC)
	{
		return;
	}

	bool bLMouseDown = PC->IsInputKeyDown(EKeys::LeftMouseButton);
	bool bRMouseDown = PC->IsInputKeyDown(EKeys::RightMouseButton);

	FVector CamLoc;
	FRotator CamRot;
	PC->GetPlayerViewPoint(CamLoc, CamRot);

	FVector CenterInteractionPoint = CamLoc + (CamRot.Vector() * 75.0f);

	// Simulate Left Hand with LMB
	if (bLMouseDown && !bLeftMouseWasDown)
	{
		FVector LeftPoint = CenterInteractionPoint - CamRot.RotateVector(FVector(0.0f, 12.0f, 0.0f));
		OnPinchStarted.Broadcast(EControllerHand::Left, LeftPoint);
		OnPoke.Broadcast(EControllerHand::Left, LeftPoint, CamRot.Vector());
	}
	else if (!bLMouseDown && bLeftMouseWasDown)
	{
		FVector LeftPoint = CenterInteractionPoint - CamRot.RotateVector(FVector(0.0f, 12.0f, 0.0f));
		OnPinchEnded.Broadcast(EControllerHand::Left, LeftPoint);
	}

	// Simulate Right Hand with RMB
	if (bRMouseDown && !bRightMouseWasDown)
	{
		FVector RightPoint = CenterInteractionPoint + CamRot.RotateVector(FVector(0.0f, 12.0f, 0.0f));
		OnPinchStarted.Broadcast(EControllerHand::Right, RightPoint);
		OnPoke.Broadcast(EControllerHand::Right, RightPoint, CamRot.Vector());
	}
	else if (!bRMouseDown && bRightMouseWasDown)
	{
		FVector RightPoint = CenterInteractionPoint + CamRot.RotateVector(FVector(0.0f, 12.0f, 0.0f));
		OnPinchEnded.Broadcast(EControllerHand::Right, RightPoint);
	}

	bLeftMouseWasDown = bLMouseDown;
	bRightMouseWasDown = bRMouseDown;
}

void UPhobiaHandTrackingComponent::DrawDebugFinger(const FPhobiaHandState& State, int32 StartJoint, int32 EndJoint, const FColor& BoneColor)
{
	UWorld* World = GetWorld();
	if (!World || State.JointPositions.Num() < EHandKeypointCount)
	{
		return;
	}

	// Draw bone from Wrist (1) to Knuckle
	DrawDebugLine(World, State.JointPositions[1], State.JointPositions[StartJoint], BoneColor, false, -1.0f, 0, 0.15f);

	// Draw joint chain
	for (int32 i = StartJoint; i < EndJoint; ++i)
	{
		DrawDebugLine(World, State.JointPositions[i], State.JointPositions[i + 1], BoneColor, false, -1.0f, 0, 0.18f);

		float Radius = State.JointRadii[i + 1] > 0.1f ? State.JointRadii[i + 1] : 0.65f;
		FColor JointColor = FColor(70, 180, 255);

		// Tip highlighting
		if (i + 1 == (int32)EHandKeypoint::ThumbTip && State.bIsPinching)
		{
			JointColor = FColor::Green;
			Radius *= 1.3f;
		}
		else if (i + 1 == (int32)EHandKeypoint::IndexTip)
		{
			if (State.bIsPinching)
			{
				JointColor = FColor::Green;
				Radius *= 1.3f;
			}
			else if (State.bIsPoking)
			{
				JointColor = FColor::Yellow;
				Radius *= 1.4f;
			}
		}

		DrawDebugSphere(World, State.JointPositions[i + 1], Radius, 8, JointColor, false, -1.0f, 0, 0.1f);
	}
}

void UPhobiaHandTrackingComponent::DrawDebugVisualization()
{
	UWorld* World = GetWorld();
	if (!World)
	{
		return;
	}

	auto DrawHandDebug = [this, World](EControllerHand Hand, const FPhobiaHandState& State, const FString& HandName)
	{
		if (!State.bIsTracked || State.JointPositions.Num() < EHandKeypointCount)
		{
			return;
		}

		// Palm & Wrist
		FColor PalmColor = State.bIsPalmUp ? FColor::Orange : FColor(80, 200, 255);
		DrawDebugSphere(World, State.JointPositions[0], 1.2f, 8, PalmColor, false, -1.0f, 0, 0.15f);
		DrawDebugSphere(World, State.JointPositions[1], 1.0f, 8, FColor(80, 140, 255), false, -1.0f, 0, 0.15f);
		DrawDebugLine(World, State.JointPositions[0], State.JointPositions[1], FColor::White, false, -1.0f, 0, 0.2f);

		// Fingers
		FColor BoneColor = State.bIsPinching ? FColor(100, 255, 100) : FColor(180, 220, 255);
		DrawDebugFinger(State, (int32)EHandKeypoint::ThumbMetacarpal, (int32)EHandKeypoint::ThumbTip, BoneColor);
		DrawDebugFinger(State, (int32)EHandKeypoint::IndexMetacarpal, (int32)EHandKeypoint::IndexTip, BoneColor);
		DrawDebugFinger(State, (int32)EHandKeypoint::MiddleMetacarpal, (int32)EHandKeypoint::MiddleTip, BoneColor);
		DrawDebugFinger(State, (int32)EHandKeypoint::RingMetacarpal, (int32)EHandKeypoint::RingTip, BoneColor);
		DrawDebugFinger(State, (int32)EHandKeypoint::LittleMetacarpal, (int32)EHandKeypoint::LittleTip, BoneColor);

		// Pinch indicator line
		FColor PinchLineColor = State.bIsPinching ? FColor::Green : FColor::Red;
		DrawDebugLine(World, State.JointPositions[(int32)EHandKeypoint::ThumbTip], State.JointPositions[(int32)EHandKeypoint::IndexTip], PinchLineColor, false, -1.0f, 0, State.bIsPinching ? 0.35f : 0.08f);

		// Palm normal arrow
		DrawDebugDirectionalArrow(World, State.PalmLocation, State.PalmLocation + State.PalmNormal * 12.0f, 2.5f, State.bIsPalmUp ? FColor::Orange : FColor::Magenta, false, -1.0f, 0, 0.2f);

		// Poke direction arrow
		if (State.bIsPoking)
		{
			DrawDebugDirectionalArrow(World, State.PokeLocation, State.PokeLocation + State.PokeDirection * 15.0f, 3.0f, FColor::Yellow, false, -1.0f, 0, 0.35f);
		}

		// Text HUD near palm
		FString HUDText = FString::Printf(TEXT("[%s Hand]\nPinch: %s (%.1f cm)\nPalmUp: %s%s"),
			*HandName,
			State.bIsPinching ? TEXT("ACTIVE") : TEXT("OPEN"),
			State.PinchDistance,
			State.bIsPalmUp ? TEXT("YES") : TEXT("NO"),
			State.bIsPoking ? TEXT("\nPOKE DETECTED!") : TEXT("")
		);
		DrawDebugString(World, State.PalmLocation + FVector(0, 0, 6.0f), HUDText, nullptr, FColor::White, 0.0f, true, 0.9f);
	};

	DrawHandDebug(EControllerHand::Left, LeftHandState, TEXT("LEFT"));
	DrawHandDebug(EControllerHand::Right, RightHandState, TEXT("RIGHT"));

	// On-screen banner indicating active mode
	if (GEngine)
	{
		FString ModeMsg = (CurrentInputMode == EPhobiaInputMode::HandTracking)
			? TEXT("[PhobiaVR] Input Mode: HAND TRACKING (OpenXR Hands Active)")
			: TEXT("[PhobiaVR] Input Mode: DESKTOP FALLBACK (WASD / Mouse Look / LMB=Left Pinch / RMB=Right Pinch)");

		FColor BannerColor = (CurrentInputMode == EPhobiaInputMode::HandTracking) ? FColor::Cyan : FColor::Yellow;
		GEngine->AddOnScreenDebugMessage(8934, 0.0f, BannerColor, ModeMsg);
	}
}

// -------------------------------------------------------------
// PUBLIC QUERIES & CONTROLS
// -------------------------------------------------------------

bool UPhobiaHandTrackingComponent::IsHandTracked(EControllerHand Hand) const
{
	return (Hand == EControllerHand::Left) ? LeftHandState.bIsTracked : RightHandState.bIsTracked;
}

bool UPhobiaHandTrackingComponent::IsPinching(EControllerHand Hand) const
{
	return (Hand == EControllerHand::Left) ? LeftHandState.bIsPinching : RightHandState.bIsPinching;
}

bool UPhobiaHandTrackingComponent::IsPalmUp(EControllerHand Hand) const
{
	return (Hand == EControllerHand::Left) ? LeftHandState.bIsPalmUp : RightHandState.bIsPalmUp;
}

bool UPhobiaHandTrackingComponent::GetPinchLocation(EControllerHand Hand, FVector& OutLocation) const
{
	const FPhobiaHandState& State = (Hand == EControllerHand::Left) ? LeftHandState : RightHandState;
	if (State.bIsTracked)
	{
		OutLocation = State.PinchLocation;
		return true;
	}
	return false;
}

float UPhobiaHandTrackingComponent::GetPinchDistance(EControllerHand Hand) const
{
	const FPhobiaHandState& State = (Hand == EControllerHand::Left) ? LeftHandState : RightHandState;
	return State.PinchDistance;
}

bool UPhobiaHandTrackingComponent::GetIndexTipPose(EControllerHand Hand, FVector& OutLocation, FVector& OutDirection) const
{
	const FPhobiaHandState& State = (Hand == EControllerHand::Left) ? LeftHandState : RightHandState;
	if (State.bIsTracked)
	{
		OutLocation = State.PokeLocation;
		OutDirection = State.PokeDirection;
		return true;
	}
	return false;
}

bool UPhobiaHandTrackingComponent::GetJointTransform(EControllerHand Hand, EHandKeypoint Keypoint, FTransform& OutTransform, float& OutRadius) const
{
	const FPhobiaHandState& State = (Hand == EControllerHand::Left) ? LeftHandState : RightHandState;
	int32 Index = static_cast<int32>(Keypoint);
	if (State.bIsTracked && State.JointPositions.IsValidIndex(Index))
	{
		OutTransform = FTransform(State.JointRotations[Index], State.JointPositions[Index]);
		OutRadius = State.JointRadii[Index];
		return true;
	}
	return false;
}

void UPhobiaHandTrackingComponent::SetCurrentInputMode(EPhobiaInputMode NewMode)
{
	if (CurrentInputMode != NewMode)
	{
		CurrentInputMode = NewMode;
		OnInputModeChanged.Broadcast(CurrentInputMode);
	}
}

void UPhobiaHandTrackingComponent::ToggleDebugDraw()
{
	SetDebugDraw(!bEnableDebugDraw);
}

void UPhobiaHandTrackingComponent::SetDebugDraw(bool bEnabled)
{
	bEnableDebugDraw = bEnabled;
}
