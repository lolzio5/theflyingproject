// Fill out your copyright notice in the Description page of Project Settings.


#include "JetPlayer2.h"
#include "FlightTutorialGameInstance.h"
#include "Dom/JsonObject.h"
#include "Serialization/JsonSerializer.h"

// Sets default values
AJetPlayer2::AJetPlayer2()
{
	// Set this pawn to call Tick() every frame.  You can turn this off to improve performance if you don't need it.
	PrimaryActorTick.bCanEverTick = true;

}

// Called when the game starts or when spawned
void AJetPlayer2::BeginPlay()
{
	Super::BeginPlay();
}

// Called every frame
void AJetPlayer2::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);
	//UFlightTutorialGameInstance* GameInstance = Cast<UFlightTutorialGameInstance>(GetGameInstance());
	//updatePosture(GameInstance);
	//NotifyServer();
}

void AJetPlayer2::NotifyServer()
{
	UFlightTutorialGameInstance* GameInstance = Cast<UFlightTutorialGameInstance>(GetGameInstance());
	FString message="";

	if (start_time != -1.0)
	{
		message = "{\"leaderboard\": 1, \"player\" = \"player2\", \"StartTime\" = " + FString::SanitizeFloat(start_time) + "}";
		
	}
	if (TimeAtTriggerBox1 != -1.0)
	{
		message = "{\"leaderboard\": 1, \"player\" = \"player2\", \"TimeAtTriggerBox1\" = " + FString::SanitizeFloat(TimeAtTriggerBox1) + "}";
		
	}
	if (TimeAtTriggerBox2 != -1.0)
	{
		message = "{\"leaderboard\": 1, \"player\" = \"player2\", \"TimeAtTriggerBox2\" = " + FString::SanitizeFloat(TimeAtTriggerBox2) + "}";
		
	}
	if (TimeAtTriggerBox3 != -1.0)
	{
		message = "{\"leaderboard\": 1, \"player\" = \"player2\", \"TimeAtTriggerBox3\" = " + FString::SanitizeFloat(TimeAtTriggerBox3) + "}";
		
	}

	if (GameInstance)
	{
		if (GameInstance->WebSocket->IsConnected())
		{
			GameInstance->WebSocket->Send(message);
		}
	}
}

// Called to bind functionality to input
void AJetPlayer2::SetupPlayerInputComponent(UInputComponent* PlayerInputComponent)
{
	Super::SetupPlayerInputComponent(PlayerInputComponent);
	PlayerInputComponent->BindAction("NotifyServer", IE_Pressed, this, &AJetPlayer2::NotifyServer);
}

float AJetPlayer2::getYawIn2()
{
	return yaw_in_2;
}
float AJetPlayer2::getPitchIn2()
{
	return pitch_in_2;
}
float AJetPlayer2::getRollIn2()
{
	return roll_in_2;
}

float AJetPlayer2::getThrustIn2()
{
	return thrust_in_2;
}
float AJetPlayer2::getFlapPitchIn2()
{
	return flap_pitch_in_2;
}
float AJetPlayer2::getElevatorPitchIn2()
{
	return elevator_pitch_in_2;
}
float AJetPlayer2::getLeftAileronYawIn2()
{
	return left_aileron_yaw_in_2;
}
float AJetPlayer2::getRightAileronYawIn2()
{
	return right_aileron_yaw_in_2;
}
float AJetPlayer2::getRudderYawIn2()
{
	return rudder_yaw_in_2;
}

void AJetPlayer2::setYawIn2(float data)
{
	yaw_in_2 = data;
}
void AJetPlayer2::setPitchIn2(float data)
{
	pitch_in_2 = data;
}
void AJetPlayer2::setRollIn2(float data)
{
	roll_in_2 = data;
}

void AJetPlayer2::setThrustIn2(float data)
{
	thrust_in_2 = data;
}
void AJetPlayer2::setFlapPitchIn2(float data)
{
	flap_pitch_in_2 = data;
}
void AJetPlayer2::setElevatorPitchIn2(float data)
{
	elevator_pitch_in_2 = data;
}
void AJetPlayer2::setLeftAileronYawIn2(float data)
{
	left_aileron_yaw_in_2 = data;
}
void AJetPlayer2::setRightAileronYawIn2(float data)
{
	right_aileron_yaw_in_2 = data;
}
void AJetPlayer2::setRudderYawIn2(float data)
{
	rudder_yaw_in_2 = data;
}

void AJetPlayer2::updatePosture(UFlightTutorialGameInstance* TheGameInstance)
{
	TheGameInstance = Cast<UFlightTutorialGameInstance>(GetGameInstance());
	float current_yaw = getYawIn2();
	float current_pitch = getPitchIn2();
	float current_roll = getRollIn2();
	float current_thrust = getThrustIn2();
	float current_flap_pitch = getFlapPitchIn2();
	float current_elevator_pitch = getElevatorPitchIn2();
	float current_left_aileron_yaw = getLeftAileronYawIn2();
	float current_right_aileron_yaw = getRightAileronYawIn2();
	float current_rudder_yaw = getRudderYawIn2();

	/*GEngine->AddOnScreenDebugMessage(-1, 0.005, FColor::Green, "yaw: " + FString::SanitizeFloat(current_yaw));
	GEngine->AddOnScreenDebugMessage(-1, 0.005, FColor::Green, "pitch: " + FString::SanitizeFloat(current_pitch));
	GEngine->AddOnScreenDebugMessage(-1, 0.005, FColor::Green, "roll: " + FString::SanitizeFloat(current_roll));
	GEngine->AddOnScreenDebugMessage(-1, 0.005, FColor::Green, "thrust: " + FString::SanitizeFloat(current_thrust));
	GEngine->AddOnScreenDebugMessage(-1, 0.005, FColor::Green, "flap_pitch: " + FString::SanitizeFloat(current_flap_pitch));
	GEngine->AddOnScreenDebugMessage(-1, 0.005, FColor::Green, "elevator_pitch: " + FString::SanitizeFloat(current_elevator_pitch));
	GEngine->AddOnScreenDebugMessage(-1, 0.005, FColor::Green, "left_aileron_yaw: " + FString::SanitizeFloat(current_left_aileron_yaw));
	GEngine->AddOnScreenDebugMessage(-1, 0.005, FColor::Green, "right_aileron_yaw: " + FString::SanitizeFloat(current_right_aileron_yaw));
	GEngine->AddOnScreenDebugMessage(-1, 0.005, FColor::Green, "rudder_yaw: " + FString::SanitizeFloat(current_rudder_yaw));*/

	float new_yaw = current_yaw;
	float new_pitch = current_pitch;
	float new_roll = current_roll;
	float new_thrust = current_thrust;
	float new_flap_pitch = current_flap_pitch;
	float new_elevator_pitch = current_elevator_pitch;
	float new_left_aileron_yaw = current_left_aileron_yaw;
	float new_right_aileron_yaw = current_right_aileron_yaw;
	float new_rudder_yaw = current_rudder_yaw;

	GEngine->AddOnScreenDebugMessage(-1, 0.005, FColor::Cyan, TheGameInstance->ServerMessage);
	TSharedPtr<FJsonObject> json_data;
	if (FJsonSerializer::Deserialize(TJsonReaderFactory<>::Create(*TheGameInstance->ServerMessage), json_data) && json_data.IsValid())
	{
		if ((FString)json_data->GetStringField("Name") == "Player 2")
		{
			new_yaw = (float)json_data->GetNumberField("JetYaw");
			new_pitch = (float)json_data->GetNumberField("JetPitch");
			new_roll = (float)json_data->GetNumberField("JetRoll");
			new_thrust = (float)json_data->GetNumberField("Thrust");
			new_flap_pitch = (float)json_data->GetNumberField("FlapPitch");
			new_elevator_pitch = (float)json_data->GetNumberField("ElevatorPitch");
			new_right_aileron_yaw = (float)json_data->GetNumberField("RightAileronYaw");
			new_left_aileron_yaw = -new_right_aileron_yaw;
			new_rudder_yaw = (float)json_data->GetNumberField("RudderYaw");
		}
	}

	setYawIn2(new_yaw);
	setPitchIn2(new_pitch);
	setRollIn2(new_roll);
	setThrustIn2(new_thrust);
	setFlapPitchIn2(new_flap_pitch);
	setElevatorPitchIn2(new_elevator_pitch);
	setLeftAileronYawIn2(new_left_aileron_yaw);
	setRightAileronYawIn2(new_right_aileron_yaw);
	setRudderYawIn2(new_rudder_yaw);

}