// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Blueprint/UserWidget.h"
#include "FlightTutorialGameInstance.h"
#include "connectParent.generated.h"


/**
 * 
 */
UCLASS()
class FLIGHTTUTORIAL_API UconnectParent : public UUserWidget
{
	GENERATED_BODY()

public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "WebSocket") // Expose ServerURL to Blueprints
	FString WidgetServerURL = "ws://127.0.0.1:12000";
	
	UFUNCTION(BlueprintCallable)
	void GetURL();

};
