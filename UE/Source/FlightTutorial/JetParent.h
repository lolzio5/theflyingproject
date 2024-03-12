// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
#include "GameFramework/Pawn.h"
#include "JetParent.generated.h"

UCLASS()
class FLIGHTTUTORIAL_API AJetParent : public APawn
{
	GENERATED_BODY()

public:
	// Sets default values for this pawn's properties
	AJetParent();
	UFlightTutorialGameInstance* GameInstance;

private:

	UPROPERTY(BlueprintReadWrite, meta = (AllowPrivateAccess = "true"))
	float yaw_in = 0.0;

	UPROPERTY(BlueprintReadWrite, meta = (AllowPrivateAccess = "true"))
	float pitch_in = 0.0;

	UPROPERTY(BlueprintReadWrite, meta = (AllowPrivateAccess = "true"))
	float roll_in = 0.0;

	UPROPERTY(BlueprintReadWrite, meta = (AllowPrivateAccess = "true"))
	float thrust_in = 4000.0;

	UPROPERTY(BlueprintReadWrite, meta = (AllowPrivateAccess = "true"))
	float flap_pitch_in = 0.0;

	UPROPERTY(BlueprintReadWrite, meta = (AllowPrivateAccess = "true"))
	float elevator_pitch_in = 0.0;

	UPROPERTY(BlueprintReadWrite, meta = (AllowPrivateAccess = "true"))
	float left_aileron_yaw_in = 0.0;

	UPROPERTY(BlueprintReadWrite, meta = (AllowPrivateAccess = "true"))
	float right_aileron_yaw_in = 0.0;

	UPROPERTY(BlueprintReadWrite, meta = (AllowPrivateAccess = "true"))
	float rudder_yaw_in = 0.0;

public:
	float getYawIn();
	float getPitchIn();
	float getRollIn();
	float getThrustIn();
	float getFlapPitchIn();
	float getElevatorPitchIn();
	float getLeftAileronYawIn();
	float getRightAileronYawIn();
	float getRudderYawIn();

	void setYawIn(float data);
	void setPitchIn(float data);
	void setRollIn(float data);
	void setThrustIn(float data);
	void setFlapPitchIn(float data);
	void setElevatorPitchIn(float data);
	void setLeftAileronYawIn(float data);
	void setRightAileronYawIn(float data);
	void setRudderYawIn(float data);

	UFUNCTION(BlueprintCallable)
	void updatePosture(UFlightTutorialGameInstance* GameInstance);
	void NotifyServer();

	UPROPERTY(BlueprintReadWrite, meta = (AllowPrivateAccess = "true"))
	float TimeAtTriggerBox1;
	UPROPERTY(BlueprintReadWrite, meta = (AllowPrivateAccess = "true"))
	float TimeAtTriggerBox2;
	UPROPERTY(BlueprintReadWrite, meta = (AllowPrivateAccess = "true"))
	float TimeAtTriggerBox3;
protected:
	// Called when the game starts or when spawned
	virtual void BeginPlay() override;

public:
	// Called every frame
	virtual void Tick(float DeltaTime) override;

	// Called to bind functionality to input
	virtual void SetupPlayerInputComponent(class UInputComponent* PlayerInputComponent) override;

};
