import numpy as np
from updatePositions import interpolate_to

def updateYaw(CurrentYaw, TargetYaw, DeltaSeconds, MaxRudderYaw=45):
    
    CurrentYaw = interpolate_to(CurrentYaw, TargetYaw, DeltaSeconds, 10)
    
    JetYaw = CurrentYaw * DeltaSeconds * 20
    
    RudderYaw = np.interp(CurrentYaw, [-1, 1], [-MaxRudderYaw, MaxRudderYaw])

    return [JetYaw, RudderYaw]