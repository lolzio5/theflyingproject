import numpy as np

# Run using Epic installed python: 
# C:/Program Files/Epic Games/UE_4.27/Engine/Binaries/ThirdParty/Python3/Win64/python.exe

# To install new packages, pip has wrong path, manual install:
# cd C:/"Program Files"/"Epic Games"/UE_4.27/Engine/Binaries/ThirdParty/Python3/Win64 
# ./python.exe -m pip install --target . <PACKAGENAME>

# Variables to be retained:
# DeltaSeconds <- time elapsed since last frame (since last packet of information sent)
# CurrentPosition, CurrentThrust, CurrentPitch, CurrentRoll, CurrentYaw <- retained from previous tick
# TargetThrust, TargetPitch, TargetRoll, TargetYaw <- Given by FPGA controller

def interpolate_to(current_value, target_value, delta_time, interpolation_speed):
    interpolation_factor = 1.0 - np.exp(-interpolation_speed * delta_time)
    interpolated_value = current_value + interpolation_factor * (target_value - current_value)
    return interpolated_value

def normalize_vector(vector):
    length = np.linalg.norm(vector)

    if length != 0:
        normalized_vector = vector / length
    else:
        normalized_vector = vector

    return normalized_vector

def updateThrust(CurrentThrust, TargetThrust, DeltaSeconds, ThrustMultiplier=2500, MaxThrustSpeed=10000):
    CurrentThrust = TargetThrust * DeltaSeconds * ThrustMultiplier + CurrentThrust

    if CurrentThrust > MaxThrustSpeed:
        CurrentThrust = MaxThrustSpeed
        
    return CurrentThrust

def updatePitch(CurrentPitch, TargetPitch, DeltaSeconds, MaxFlapPitch=10, MaxElevatorPitch=25):

    CurrentPitch = interpolate_to(CurrentPitch, TargetPitch, DeltaSeconds, 10)
    
    JetPitch = CurrentPitch * DeltaSeconds * 20
    
    FlapPitch = np.interp(CurrentPitch, [-1, 1], [-MaxFlapPitch, MaxFlapPitch])
    
    ElevatorPitch = np.interp(CurrentPitch, [-1, 1], [-MaxElevatorPitch, MaxElevatorPitch])
    
    return [JetPitch, -FlapPitch, -ElevatorPitch]

def updateRoll(CurrentRoll, TargetRoll, DeltaSeconds, MaxAileronYaw=45):
    
    CurrentRoll = interpolate_to(CurrentRoll, TargetRoll, DeltaSeconds, 10)
    
    JetRoll = CurrentRoll * DeltaSeconds * 20
    
    AileronYaw = np.interp(CurrentRoll, [-1, 1], [-MaxAileronYaw, MaxAileronYaw])
    
    # JET, LEFT AILERON, RIGHT AILERON
    return [JetRoll, -AileronYaw, AileronYaw]

def updateYaw(CurrentYaw, TargetYaw, DeltaSeconds, MaxRudderYaw=45):
    
    CurrentYaw = interpolate_to(CurrentYaw, TargetYaw, DeltaSeconds, 10)
    
    JetYaw = CurrentYaw * DeltaSeconds * 20
    
    RudderYaw = np.interp(CurrentYaw, [-1, 1], [-MaxRudderYaw, MaxRudderYaw])

    return [JetYaw, RudderYaw]

def updatePosition(CurrentPosition, CurrentThrust, TargetThrust, DeltaSeconds, Drag=0.25, MinThrust=4000, Gravity=981):
    
    # Get direction vectors by normalizing CurrentPosition
    CurrentForwardPosition = normalize_vector(CurrentPosition)
    # Smooth deceleration
    if TargetThrust < CurrentThrust:
        CurrentThrust = interpolate_to(CurrentThrust, TargetThrust, DeltaSeconds, Drag)
    else:
        CurrentThrust = TargetThrust
    
    # Calculate New Position
    NewPosition = [i * CurrentThrust * DeltaSeconds for i in CurrentForwardPosition]
    
    # Calculate Applied Gravity
    AppliedGravity = np.interp(CurrentThrust, [0, MinThrust], [-Gravity, 0])
    
    # Update Position
    NewPosition[2] -= AppliedGravity * DeltaSeconds

    return NewPosition