
import numpy as np
def dBm_to_vpp( dBm, r_load=50 ):
    power = 10**(dBm/10) # mW
    signal_Vrms = np.sqrt(power/1000*r_load) # V
    signal_V = signal_Vrms*np.sqrt(2) # V
    return signal_V

def powerdB_to_vRatio( dB ):
    return 10**(dB/20)