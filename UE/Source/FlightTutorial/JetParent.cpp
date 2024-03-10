// Fill out your copyright notice in the Description page of Project Settings.


#include "JetParent.h"
#include "FlightTutorialGameInstance.h"
#include "Dom/JsonObject.h"
#include "Serialization/JsonSerializer.h"

// Sets default values
AJetParent::AJetParent()
{
 	// Set this pawn to call Tick() every frame.  You can turn this off to improve performance if you don't need it.
	PrimaryActorTick.bCanEverTick = true;

}

// Called when the game starts or when spawned
void AJetParent::BeginPlay()
{
	Super::BeginPlay();
}

// Called every frame
void AJetParent::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);
	//UFlightTutorialGameInstance* GameInstance = Cast<UFlightTutorialGameInstance>(GetGameInstance());
	//updatePosture(GameInstance);
	//NotifyServer();
}

void AJetParent::NotifyServer()
{
	//UFlightTutorialGameInstance* GameInstance = Cast<UFlightTutorialGameInstance>(GetGameInstance());
	if (GameInstance)
	{
		if (GameInstance->WebSocket->IsConnected())
		{
			GameInstance->WebSocket->Send("get");
		}
	}
}

// Called to bind functionality to input
void AJetParent::SetupPlayerInputComponent(UInputComponent* PlayerInputComponent)
{
	Super::SetupPlayerInputComponent(PlayerInputComponent);
	PlayerInputComponent->BindAction("NotifyServer", IE_Pressed, this, &AJetParent::NotifyServer);
}

float AJetParent::getYawIn()
{
	return yaw_in;
}
float AJetParent::getPitchIn()
{
	return pitch_in;
}
float AJetParent::getRollIn()
{
	return roll_in;
}

float AJetParent::getThrustIn()
{
	return thrust_in;
}
float AJetParent::getFlapPitchIn()
{
	return flap_pitch_in;
}
float AJetParent::getElevatorPitchIn()
{
	return elevator_pitch_in;
}
float AJetParent::getLeftAileronYawIn()
{
	return left_aileron_yaw_in;
}
float AJetParent::getRightAileronYawIn()
{
	return right_aileron_yaw_in;
}
float AJetParent::getRudderYawIn()
{
	return rudder_yaw_in;
}
float AJetParent::getXPositionIn()
{
	return x_position_in;
}
float AJetParent::getYPositionIn()
{
	return y_position_in;
}
float AJetParent::getZPositionIn() 
{
	return z_position_in;
}

void AJetParent::setYawIn(float data)
{
	yaw_in = data;
}
void AJetParent::setPitchIn(float data)
{
	pitch_in = data;
}
void AJetParent::setRollIn(float data)
{
	roll_in = data;
}

void AJetParent::setThrustIn(float data)
{
	 thrust_in = data;
}
void AJetParent::setFlapPitchIn(float data)
{
	flap_pitch_in = data;
}
void AJetParent::setElevatorPitchIn(float data)
{
	elevator_pitch_in = data;
}
void AJetParent::setLeftAileronYawIn(float data)
{
	left_aileron_yaw_in = data;
}
void AJetParent::setRightAileronYawIn(float data)
{
	right_aileron_yaw_in = data;
}
void AJetParent::setRudderYawIn(float data)
{
	rudder_yaw_in  = data;
}
void AJetParent::setXPositionIn(float data)
{
	x_position_in = data;
}
void AJetParent::setYPositionIn(float data)
{
	y_position_in = data;
}
void AJetParent::setZPositionIn(float data)
{
	z_position_in = data;
}

void AJetParent::updatePosture(UFlightTutorialGameInstance* TheGameInstance)
{	
	TheGameInstance = Cast<UFlightTutorialGameInstance>(GetGameInstance());
	float current_yaw = getYawIn();
	float current_pitch = getPitchIn();
	float current_roll = getRollIn();
	float current_thrust = getThrustIn();
	float current_flap_pitch = getFlapPitchIn();
	float current_elevator_pitch = getElevatorPitchIn();
	float current_left_aileron_yaw = getLeftAileronYawIn();
	float current_right_aileron_yaw = getRightAileronYawIn();
	float current_rudder_yaw = getRudderYawIn();
	float current_x_position = getXPositionIn();
	float current_y_position = getYPositionIn();
	float current_z_position = getZPositionIn();

	GEngine->AddOnScreenDebugMessage(-1, 0.005, FColor::Green,"yaw: "+ FString::SanitizeFloat(current_yaw));
	GEngine->AddOnScreenDebugMessage(-1, 0.005, FColor::Green,"pitch: " + FString::SanitizeFloat(current_pitch));
	GEngine->AddOnScreenDebugMessage(-1, 0.005, FColor::Green, "roll: " + FString::SanitizeFloat(current_roll));
	GEngine->AddOnScreenDebugMessage(-1, 0.005, FColor::Green, "thrust: " + FString::SanitizeFloat(current_thrust));
	GEngine->AddOnScreenDebugMessage(-1, 0.005, FColor::Green, "flap_pitch: " + FString::SanitizeFloat(current_flap_pitch));
	GEngine->AddOnScreenDebugMessage(-1, 0.005, FColor::Green, "elevator_pitch: " + FString::SanitizeFloat(current_elevator_pitch));
	GEngine->AddOnScreenDebugMessage(-1, 0.005, FColor::Green, "left_aileron_yaw: " + FString::SanitizeFloat(current_left_aileron_yaw));
	GEngine->AddOnScreenDebugMessage(-1, 0.005, FColor::Green, "right_aileron_yaw: " + FString::SanitizeFloat(current_right_aileron_yaw));
	GEngine->AddOnScreenDebugMessage(-1, 0.005, FColor::Green, "rudder_yaw: " + FString::SanitizeFloat(current_rudder_yaw));
	GEngine->AddOnScreenDebugMessage(-1, 0.005, FColor::Green, "x_position: " + FString::SanitizeFloat(current_x_position));
	GEngine->AddOnScreenDebugMessage(-1, 0.005, FColor::Green, "y_position: " + FString::SanitizeFloat(current_y_position));
	GEngine->AddOnScreenDebugMessage(-1, 0.005, FColor::Green, "z_position: " + FString::SanitizeFloat(current_z_position));

	float new_yaw = current_yaw;
	float new_pitch = current_pitch;
	float new_roll = current_roll;
	float new_thrust = current_thrust;
	float new_flap_pitch = current_flap_pitch;
	float new_elevator_pitch = current_elevator_pitch;
	float new_left_aileron_yaw = current_left_aileron_yaw;
	float new_right_aileron_yaw = current_right_aileron_yaw;
	float new_rudder_yaw = current_rudder_yaw;
	float new_x_position = current_x_position;
	float new_y_position = current_y_position;
	float new_z_position = current_z_position;

	GEngine->AddOnScreenDebugMessage(-1, 0.005, FColor::Cyan, TheGameInstance->ServerMessage);
	TSharedPtr<FJsonObject> json_data;
	if (FJsonSerializer::Deserialize(TJsonReaderFactory<>::Create(*TheGameInstance->ServerMessage), json_data) && json_data.IsValid())
	{
		new_yaw =				(float)json_data->GetNumberField("JetYaw");
		new_pitch =				(float)json_data->GetNumberField("JetPitch");
		new_roll =				(float)json_data->GetNumberField("JetRoll");
		new_thrust =			(float)json_data->GetNumberField("Thrust");
		new_flap_pitch =		(float)json_data->GetNumberField("FlapPitch");
		new_elevator_pitch =	(float)json_data->GetNumberField("ElevatorPitch");
		new_left_aileron_yaw =	(float)json_data->GetNumberField("LeftAileronYaw");
		new_right_aileron_yaw = -new_left_aileron_yaw;
		new_rudder_yaw =		(float)json_data->GetNumberField("RudderYaw");
		new_x_position =		(float)json_data->GetNumberField("XPosition");
		new_y_position =		(float)json_data->GetNumberField("YPosition");
		new_z_position =		(float)json_data->GetNumberField("ZPosition");

	}
	

	setYawIn			(new_yaw);
	setPitchIn			(new_pitch);
	setRollIn			(new_roll);
	setThrustIn			(new_thrust);
	setFlapPitchIn		(new_flap_pitch);
	setElevatorPitchIn	(new_elevator_pitch);
	setLeftAileronYawIn	(new_left_aileron_yaw);
	setRightAileronYawIn(new_right_aileron_yaw);
	setRudderYawIn		(new_rudder_yaw);
	setXPositionIn		(new_x_position);
	setYPositionIn		(new_y_position);
	setZPositionIn		(new_z_position);

}