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

	UE_LOG(LogTemp, Warning, TEXT("Server URL: %s"), *InstanceServerURL);
	UE_LOG(LogTemp, Warning, TEXT("Before AddOnScreenDebugMessage"));
	GEngine->AddOnScreenDebugMessage(-1, 15.0f, FColor::Yellow, FString::Printf(TEXT("Server URL: %s"), *InstanceServerURL));
	UE_LOG(LogTemp, Warning, TEXT("After AddOnScreenDebugMessage"));

	WebSocket = FWebSocketsModule::Get().CreateWebSocket(InstanceServerURL);

	WebSocket->OnConnected().AddLambda([]()
		{
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

	if (WebSocket->IsConnected())
	{
		WebSocket->Close();
	}

	Super::Shutdown();
}

void UFlightTutorialGameInstance::updateServerMessage(const FString& MessageString)
{
	GEngine->AddOnScreenDebugMessage(-1, 0.05, FColor::Yellow, "get Message1: " + MessageString);
	ServerMessage = MessageString;
	GEngine->AddOnScreenDebugMessage(-1, 0.05, FColor::Yellow, "get Message2: " + ServerMessage);
}

