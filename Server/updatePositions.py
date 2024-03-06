import numpy as np
import unreal as un

# Variables to be retained:
# DeltaSeconds <- time elapsed since last frame (since last packet of information sent)
# CurrentThrust, CurrentPitch, CurrentRoll, CurrentYaw <- retained from previous tick
# TargetThrust, TargetPitch, TargetRoll, TargetYaw <- Given by FPGA controller

def updateThrust(CurrentThrust, TargetThrust, DeltaSeconds):
    ThrustMultiplier=2500
    MaxThrustSpeed=10000

    CurrentThrust = TargetThrust * DeltaSeconds * ThrustMultiplier + CurrentThrust

    if CurrentThrust > MaxThrustSpeed:
        CurrentThrust = MaxThrustSpeed
        
    return CurrentThrust

def updatePitch(CurrentPitch, TargetPitch, DeltaSeconds):
    MaxFlapPitch=10
    MaxElevatorPitch=25

    CurrentPitch = np.interp(CurrentPitch, TargetPitch, 10)
    
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
    
    return {JetPitch, FlapPitch, ElevatorPitch}

def updateRoll(CurrentRoll, TargetRoll, DeltaSeconds):
    MaxAileronYaw=45

    CurrentRoll = np.interp(CurrentRoll, TargetRoll, 10)
    
    JetRoll = CurrentRoll * DeltaSeconds
    
    if -MaxAileronYaw <= CurrentRoll <= MaxAileronYaw:
        AileronYaw = CurrentRoll
    elif CurrentRoll > MaxAileronYaw:
        AileronYaw = MaxAileronYaw
    else:
        AileronYaw=-MaxAileronYaw
    
    return {JetRoll, AileronYaw}

def updateYaw(CurrentYaw, TargetYaw, DeltaSeconds):
    MaxRudderYaw=45

    CurrentYaw = np.interp(CurrentYaw, TargetYaw, 10)
    
    JetYaw = CurrentYaw * DeltaSeconds
    
    if -MaxRudderYaw <= CurrentYaw <= MaxRudderYaw:
        RudderYaw = CurrentYaw
    elif CurrentYaw > MaxRudderYaw:
        RudderYaw = MaxRudderYaw
    else:
        RudderYaw=-MaxRudderYaw
    
    return {JetYaw, RudderYaw}

def updatePosition(CurrentThrust, TargetThrust, DeltaSeconds):
    Drag=0.25
    Gravity=981.0
    MinThrust=4000
    
    # Calculate CurrentThrust (Interpolate if slowdown, instant if speed up)
    if TargetThrust < CurrentThrust:
        CurrentThrust = np.interp(CurrentThrust, TargetThrust, Drag)
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