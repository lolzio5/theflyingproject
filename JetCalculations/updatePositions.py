import numpy as np
import unreal as un

# Run using Epic installed python: 
# C:/Program Files/Epic Games/UE_4.27/Engine/Binaries/ThirdParty/Python3/Win64/python.exe

# To install new packages, pip has wrong path, manual install:
# cd C:/Program Files/Epic Games/UE_4.27/Engine/Binaries/ThirdParty/Python3/Win64 
# ./python.exe -m pip install --target . <PACKAGENAME>

# Variables to be retained:
# DeltaSeconds <- time elapsed since last frame (since last packet of information sent)
# CurrentThrust, CurrentPitch, CurrentRoll, CurrentYaw <- retained from previous tick
# TargetThrust, TargetPitch, TargetRoll, TargetYaw <- Given by FPGA controller

def interpolate_to(current_value, target_value, delta_time, interpolation_speed):
    interpolation_factor = 1.0 - np.exp(-interpolation_speed * delta_time)
    interpolated_value = current_value + interpolation_factor * (target_value - current_value)
    return interpolated_value

def updateThrust(CurrentThrust, TargetThrust, DeltaSeconds, ThrustMultiplier=2500, MaxThrustSpeed=10000):
    CurrentThrust = TargetThrust * DeltaSeconds * ThrustMultiplier + CurrentThrust;

    if CurrentThrust > MaxThrustSpeed:
        CurrentThrust = MaxThrustSpeed
        
    return CurrentThrust

def updatePitch(CurrentPitch, TargetPitch, DeltaSeconds, MaxFlapPitch=10, MaxElevatorPitch=25):

    CurrentPitch = interpolate_to(CurrentPitch, TargetPitch, DeltaSeconds, 10)
    
    JetPitch = CurrentPitch * DeltaSeconds
    
    if -MaxFlapPitch <= CurrentPitch <= MaxFlapPitch:
        FlapPitch = CurrentPitch
    elif CurrentPitch > MaxFlapPitch:
        FlapPitch = MaxFlapPitch
    else:
        FlapPitch=-MaxFlapPitch
    
    if -MaxElevatorPitch <= CurrentPitch <= MaxElevatorPitch:
        ElevatorPitch = CurrentPitch
    elif CurrentPitch > MaxElevatorPitch:
        ElevatorPitch = MaxElevatorPitch
    else:
        ElevatorPitch=-MaxElevatorPitch
    
    return [JetPitch, FlapPitch, ElevatorPitch]

def updateRoll(CurrentRoll, TargetRoll, DeltaSeconds, MaxAileronYaw=45):
    
    CurrentRoll = interpolate_to(CurrentRoll, TargetRoll, DeltaSeconds, 10)
    
    JetRoll = CurrentRoll * DeltaSeconds
    
    if -MaxAileronYaw <= CurrentRoll <= MaxAileronYaw:
        AileronYaw = CurrentRoll
    elif CurrentRoll > MaxAileronYaw:
        AileronYaw = MaxAileronYaw
    else:
        AileronYaw=-MaxAileronYaw
    
    return [JetRoll, AileronYaw]

def updateYaw(CurrentYaw, TargetYaw, DeltaSeconds, MaxRudderYaw=45):
    
    CurrentYaw = interpolate_to(CurrentYaw, TargetYaw, DeltaSeconds, 10)
    
    JetYaw = CurrentYaw * DeltaSeconds
    
    if -MaxRudderYaw <= CurrentYaw <= MaxRudderYaw:
        RudderYaw = CurrentYaw
    elif CurrentYaw > MaxRudderYaw:
        RudderYaw = MaxRudderYaw
    else:
        RudderYaw=-MaxRudderYaw
    
    return [JetYaw, RudderYaw]

# needs fixing, currently unreal package broken..
def updatePosition(CurrentThrust, TargetThrust, DeltaSeconds, Drag=0.25, Gravity=981.0, MinThrust=4000):
    
    # Calculate CurrentThrust (Interpolate if slowdown, instant if speed up)
    if TargetThrust < CurrentThrust:
        CurrentThrust = interpolate_to(CurrentThrust, TargetThrust, DeltaSeconds, Drag)
    else:
        CurrentThrust = TargetThrust
        
    # Calculate NewPosition
    XPosition = un.get_actor_forward_vector()
    NewPosition = XPosition * CurrentThrust * DeltaSeconds
    
    # Calculate Applied Gravity
    AppliedGravity = un.map_range_clamped(CurrentThrust, 0.0, MinThrust, Gravity, 0.0)
    
    # Update Position
    NewPosition[2] = NewPosition[2] - (AppliedGravity * DeltaSeconds)
    
    return NewPosition