// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Engine/TriggerBox.h"
#include "MyTriggerBox.generated.h"

/**
 * 
 */
UCLASS()
class FLIGHTTUTORIAL_API AMyTriggerBox : public ATriggerBox
{
	GENERATED_BODY()

public:
    AMyTriggerBox();



protected:
    virtual void BeginPlay() override;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "GameTime")
        float StartTime;

    // Function to be called when something overlaps this trigger box
    UFUNCTION()
        void OnOverlapBegin(AActor* OverlappedActor, AActor* OtherActor);
};
