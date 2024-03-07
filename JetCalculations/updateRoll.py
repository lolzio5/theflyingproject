import numpy as np
from updatePositions import interpolate_to

# REMEMBER one aileron needs to have reversed polarity to the other
def updateRoll(CurrentRoll, TargetRoll, DeltaSeconds, MaxAileronYaw=45):
    
    CurrentRoll = interpolate_to(CurrentRoll, TargetRoll, DeltaSeconds, 10)
    
    JetRoll = CurrentRoll * DeltaSeconds * 20
    
    AileronYaw = np.interp(CurrentRoll, [-1, 1], [-MaxAileronYaw, MaxAileronYaw])
    
    # JET, LEFT AILERON, RIGHT AILERON
    return [JetRoll, -AileronYaw, AileronYaw]