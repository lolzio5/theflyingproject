// Fill out your copyright notice in the Description page of Project Settings.


#include "connectParent.h"
#include "FlightTutorialGameInstance.h"

void connectParent::GetURL() {
	
	UFlightTutorialGameInstance* GameInstance = Cast<UFlightTutorialGameInstance>(GetGameInstance());
	
}