// Fill out your copyright notice in the Description page of Project Settings.


#include "FlightTutorialGameInstance.h"
#include "WebSocketsModule.h"

void UFlightTutorialGameInstance::Init() {

	Super::Init();

	ServerMessage = "Inited";

	if (!FModuleManager::Get().IsModuleLoaded("WebSockets"))
	{
		FModuleManager::Get().LoadModule("WebSockets");
	}

	FString InstanceServerURL = GetServerURL();

	UE_LOG(LogTemp, Warning, TEXT("Server URL: %s"), *InstanceServerURL);
	UE_LOG(LogTemp, Warning, TEXT("Before AddOnScreenDebugMessage"));
	GEngine->AddOnScreenDebugMessage(-1, 15.0f, FColor::Yellow, FString::Printf(TEXT("Server URL: %s"), *InstanceServerURL));
	UE_LOG(LogTemp, Warning, TEXT("After AddOnScreenDebugMessage"));

	// Set the ping timeout value
	float PingTimeout = 99999.0f;

	// Start a timer to periodically send ping messages
	GetWorld()->GetTimerManager().SetTimer(PingTimerHandle, this, &UFlightTutorialGameInstance::SendPing, PingTimeout, true);

	WebSocket = FWebSocketsModule::Get().CreateWebSocket(InstanceServerURL);

	WebSocket->OnConnected().AddLambda([this]()
		{
			SendServerMessage(TEXT("Player 1"));
			GEngine->AddOnScreenDebugMessage(-1, 0.005, FColor::Green, "Successfully Connected !");
		});

	WebSocket->OnConnectionError().AddLambda([](const FString& Error)
		{
			GEngine->AddOnScreenDebugMessage(-1, 15.0f, FColor::Red, Error);
		});

	WebSocket->OnClosed().AddLambda([](int32 StatusCode, const FString& Reason, bool bWasClean)
		{
			GEngine->AddOnScreenDebugMessage(-1, 15.0f, bWasClean ? FColor::Green : FColor::Red, "Connection Closed " + Reason);
		});

	WebSocket->OnMessage().AddUObject(this, &UFlightTutorialGameInstance::updateServerMessage);


	WebSocket->Connect();

}

void UFlightTutorialGameInstance::Shutdown() {

	GetWorld()->GetTimerManager().ClearTimer(PingTimerHandle);

	if (WebSocket->IsConnected()) {
		WebSocket->Close();
	}

	Super::Shutdown();
}

void UFlightTutorialGameInstance::SendPing() {
	if (WebSocket->IsConnected()) {
		// Send a ping message to the server
		WebSocket->Send(TEXT("Ping"));
	}
}

void UFlightTutorialGameInstance::SendServerMessage(const FString& Message)	{
	if (WebSocket->IsConnected())
	{
		// Send the specified message to the server
		WebSocket->Send(Message);
	}
}

void UFlightTutorialGameInstance::updateServerMessage(const FString& MessageString)
{
	GEngine->AddOnScreenDebugMessage(-1, 0.05, FColor::Yellow, "get Message1: " + MessageString);
	ServerMessage = MessageString;
	GEngine->AddOnScreenDebugMessage(-1, 0.05, FColor::Yellow, "get Message2: " + ServerMessage);
}

FString UFlightTutorialGameInstance::GetServerURL() const {
	// Replace this with code to dynamically retrieve the server URL
	// For example, you can read it from a configuration file or retrieve it from a server

	FString ServerURL;
	const FString ConfigFilePath = FPaths::ProjectConfigDir() / TEXT("GameConfig.ini");
	UE_LOG(LogTemp, Warning, TEXT("Config File Path: %s"), *ConfigFilePath);
	GConfig->GetString(TEXT("ServerSettings"), TEXT("ServerURL"), ServerURL, ConfigFilePath);
	return ServerURL;

}