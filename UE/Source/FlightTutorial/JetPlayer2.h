// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
#include "GameFramework/Pawn.h"
#include "JetPlayer2.generated.h"

UCLASS()
class FLIGHTTUTORIAL_API AJetPlayer2 : public APawn
{
	GENERATED_BODY()

public:
	// Sets default values for this pawn's properties
	AJetPlayer2();
	UFlightTutorialGameInstance* GameInstance;

private:

	UPROPERTY(BlueprintReadWrite, meta = (AllowPrivateAccess = "true"))
	float yaw_in_2 = 0.0;

	UPROPERTY(BlueprintReadWrite, meta = (AllowPrivateAccess = "true"))
	float pitch_in_2 = 0.0;

	UPROPERTY(BlueprintReadWrite, meta = (AllowPrivateAccess = "true"))
	float roll_in_2 = 0.0;

	UPROPERTY(BlueprintReadWrite, meta = (AllowPrivateAccess = "true"))
	float thrust_in_2 = 4000.0;

	UPROPERTY(BlueprintReadWrite, meta = (AllowPrivateAccess = "true"))
	float flap_pitch_in_2 = 0.0;

	UPROPERTY(BlueprintReadWrite, meta = (AllowPrivateAccess = "true"))
	float elevator_pitch_in_2 = 0.0;

	UPROPERTY(BlueprintReadWrite, meta = (AllowPrivateAccess = "true"))
	float left_aileron_yaw_in_2 = 0.0;

	UPROPERTY(BlueprintReadWrite, meta = (AllowPrivateAccess = "true"))
	float right_aileron_yaw_in_2 = 0.0;

	UPROPERTY(BlueprintReadWrite, meta = (AllowPrivateAccess = "true"))
	float rudder_yaw_in_2 = 0.0;

public:
	float getYawIn2();
	float getPitchIn2();
	float getRollIn2();
	float getThrustIn2();
	float getFlapPitchIn2();
	float getElevatorPitchIn2();
	float getLeftAileronYawIn2();
	float getRightAileronYawIn2();
	float getRudderYawIn2();

	void setYawIn2(float data);
	void setPitchIn2(float data);
	void setRollIn2(float data);
	void setThrustIn2(float data);
	void setFlapPitchIn2(float data);
	void setElevatorPitchIn2(float data);
	void setLeftAileronYawIn2(float data);
	void setRightAileronYawIn2(float data);
	void setRudderYawIn2(float data);

	UFUNCTION(BlueprintCallable)
	void updatePosture(UFlightTutorialGameInstance* GameInstance);
	void NotifyServer();

protected:
	// Called when the game starts or when spawned
	virtual void BeginPlay() override;

public:
	// Called every frame
	virtual void Tick(float DeltaTime) override;

	// Called to bind functionality to input
	virtual void SetupPlayerInputComponent(class UInputComponent* PlayerInputComponent) override;

};
