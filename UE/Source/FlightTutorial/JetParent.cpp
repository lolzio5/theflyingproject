// Fill out your copyright notice in the Description page of Project Settings.

#include "FlightTriggerBox.h"
#include "Kismet/GameplayStatics.h"
#include "FlightTutorialGameInstance.h"
#include "Dom/JsonObject.h"
#include "Serialization/JsonSerializer.h"

AFlightTriggerBox::AFlightTriggerBox()
{
    OnActorBeginOverlap.AddDynamic(this, &AFlightTriggerBox::OnOverlapBegin);
}

void AFlightTriggerBox::BeginPlay()
{
    Super::BeginPlay();
    StartTime = UGameplayStatics::GetTimeSeconds(GetWorld());
}

float AFlightTriggerBox::OnOverlapBegin(AActor* OverlappedActor, AActor* OtherActor)
{

    if (OtherActor->IsA(APawn::StaticClass()))
    {
        float CurrentTime = UGameplayStatics::GetTimeSeconds(GetWorld());
        float Duration = CurrentTime - StartTime;

        // Log the duration for testing
        UE_LOG(LogTemp, Warning, TEXT("Jet has finished the race! Duration: %f seconds"), Duration);

        // End the game
        //UGameplayStatics::SetGamePaused(GetWorld(), true);
        return CurrentTime;
    }

}
