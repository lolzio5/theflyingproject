// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Engine/GameInstance.h"
#include "IWebSocket.h"
#include "FlightTutorialGameInstance.generated.h"

/**
 *
 */
UCLASS()
class FLIGHTTUTORIAL_API UFlightTutorialGameInstance : public UGameInstance
{
	GENERATED_BODY()

public:
	virtual void Init() override;
	virtual void Shutdown() override;
	TSharedPtr<IWebSocket> WebSocket;

	//UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "WebSocket") // Expose ServerURL to Blueprints
	//FString InstanceServerURL;

	UPROPERTY(VisibleAnywhere, BlueprintReadWrite, Category = "WebSocket")
	FString ServerMessage;

	void updateServerMessage(const FString& MessageString);

	//UFUNCTION(BlueprintPure, Category = "WebSocket")
	// FString GetServerURL() const { return InstanceServerURL; }

	void SendServerMessage(const FString& Message);

	FString GetServerURL() const;

	void SendPing();

	FTimerHandle PingTimerHandle;

};
