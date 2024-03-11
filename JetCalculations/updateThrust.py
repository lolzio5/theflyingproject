def updateThrust(CurrentThrust, TargetThrust, DeltaSeconds, ThrustMultiplier=2500, MaxThrustSpeed=10000):
    CurrentThrust = TargetThrust * DeltaSeconds * ThrustMultiplier + CurrentThrust

    if CurrentThrust > MaxThrustSpeed:
        CurrentThrust = MaxThrustSpeed
        
    return CurrentThrust

def thrust(InputValue, CurrentSpeed, DeltaSeconds, ThrustMultiplier=2500, MaxThrustSpeed=10000):
    
    # calculates the target speed setpoint
    TargetSpeed = InputValue * DeltaSeconds * ThrustMultiplier
    
    # check that the target speed does not exceed the maximum speed
    if TargetSpeed + CurrentSpeed < MaxThrustSpeed:
        return TargetSpeed + CurrentSpeed
    else:
        return MaxThrustSpeed
