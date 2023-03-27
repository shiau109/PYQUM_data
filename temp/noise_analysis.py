import numpy as np
import matplotlib.pyplot as plt

from scipy.fft import fft, fftfreq
from scipy.interpolate import interp1d
BOLTZ = 1.38e-23
PLANCK = 6.626e-34
def thermal_qeff(f,temperature):
    er = f*PLANCK/(BOLTZ*temperature)
    # print(np.max(er),np.min(er/(np.exp(er)-1)))
    return er/(np.exp(er)-1)

def thermal_PSD(f,temperature):
    return BOLTZ*temperature*thermal_qeff(f,temperature)

def thermal_noise( f,temperature, bandwidth, r_load=50 ):
    p = thermal_PSD(f,temperature)*bandwidth
    return np.sqrt(p*r_load)*2


def complex_noise( points, sigma ):
    complex_noise = np.random.normal(0, sigma, points)+1j*np.random.normal(0, sigma, points)
    return complex_noise

def sim_RF_real( t, amp, freq, phase, sigma ):
    sig_point = len(t)
    noise = complex_noise( sig_point, sigma ).real
    return amp*np.cos( freq* 2.0*np.pi*t +phase) +noise

def sim_RF_complex( t, amp, freq, phase, sigma ):
    sig_point = len(t)
    noise = complex_noise( sig_point, sigma )
    return amp*np.exp( 1j*freq* 2.0*np.pi*t +phase) +complex_noise

def ave_exp( times, t, amp, freq, phase, sigma ):
    init_data = np.zeros(len(t),dtype=np.complex128)
    for i in range(times):
        init_data += sim_RF_real( t, amp, freq, phase, sigma )
    return init_data/times

def ddc_complex( t, signal, freq ):
    converted_data = signal*np.exp( -1j*freq* 2.0*np.pi*t )
    return converted_data

def oneshot(  t, signal, freq  ):
    shot_data = np.mean(sim_mixer_downconversion( t, signal, freq ))
    return shot_data

def acc_shot( times, t, amp, freq, phase, sigma ):
    data = []
    for i in range(times):
        single_data = sim_RF_real( t, amp, freq, phase, sigma )
        data.append(oneshot( t, single_data, freq ))
    return np.array(data)

def sim_mixer_downconversion( time, signal, m_freq ):
    """
    Ideal mixer
    """
    sig_i = signal*np.cos( m_freq*2*np.pi*time )
    sig_q = signal*np.sin( m_freq*2*np.pi*time )
    return sig_i+1j*sig_q

def sampling ( time, signal, dt ):       
    f = interp1d(time, signal)
    new_point = int( (time[-1]-time[0])//dt)
    new_time = np.linspace(time, new_point*dt, new_point, endpoint=False)
    new_signal = f(new_time)

    return new_time, new_signal




if __name__ == '__main__':
    from temp.unit_conversion import *
    signal_temp = 290
    resistance_load = 50
    dt = 2e-9

    signal_dBm = -130
    signal_freq = -25e6
    signal_V = dBm_to_vpp( signal_dBm )
    print(f"Signal voltage: {signal_V*1e6} uV")
    print(f"Signal power: {signal_dBm} (dBm)")

    sim_point = int(1e4) # Number of sample points

    mu = 0 # mean 
    bandwidth = 1/dt/2
    th_psd = thermal_PSD(signal_freq,signal_temp)
    v_noise_ref = thermal_noise(signal_freq,signal_temp,1,50)
    # print(np.sqrt(4*BOLTZ*signal_temp*50*1))
    # print(np.sqrt(th_psd*1*50)*2)
    v_noise = thermal_noise(signal_freq,signal_temp,bandwidth,50)
    v_noise_var = v_noise**2
    p_noise = th_psd*bandwidth

    mW_noise = p_noise*1e3
    dbm_noise = 10*np.log10(mW_noise)
    print(f"At {signal_temp} K")
    print(f"PSD : {10*np.log10(th_psd*1000)} dBm/Hz {v_noise_ref*1e9} nV")
    print(f"Thermal noise power : {dbm_noise} dBm")
    print(f"Thermal noise voltage (STD): {v_noise*1e6} uV")



    # sample spacing

    time = np.linspace(0.0, sim_point*dt, sim_point, endpoint=False)

    # n_uni = np.random.uniform(-sigma,sigma,sim_point)
    # y = np.sin( 0.1 * 2.0*np.pi*x) + 0.5*np.cos( 0.15 * 2.0*np.pi*x)
    

    # f_n_uni = fft(n_uni)

    xf = fftfreq(sim_point, dt)[:sim_point//2]
    import matplotlib.pyplot as plt
    # plt.plot(xf,thermal_PSD(xf,0.1,50))
    # plt.show()


    # plt.plot(xf,thermal_qeff(xf,0.1))
    # plt.show()
    # Plot raw signal before and after ave
    ave_sig = ave_exp(1000,time,signal_V,signal_freq,0,v_noise)
    raw_sig = sim_RF_real(time,signal_V,signal_freq,0,v_noise)
    f_n_nor = np.abs(fft(raw_sig)[:sim_point//2]*2.0/sim_point)
    f_np_nor = 10*np.log10(f_n_nor**2/2/resistance_load*1e3)
    # plt.plot(time,raw_sig.real,'-')
    # plt.plot(time,ave_sig.real,'-')
    # plt.show()
    # d_raw_sig = sim_mixer_downconversion( time,raw_sig,signal_freq )
    # d_ave_sig = sim_mixer_downconversion( time,ave_sig,signal_freq )
    # plt.plot(time,d_raw_sig.real)
    # plt.plot(time,d_ave_sig.real)
    # plt.show()
    shots = acc_shot(1000,time,signal_V,signal_freq,0,v_noise)
    nosig_shots = acc_shot(1000,time,0,signal_freq,0,v_noise)
    plt.plot(shots.real,shots.imag,"o")
    plt.plot(nosig_shots.real,nosig_shots.imag,"o")
    plt.show()
    # plt.plot(xf, f_n_nor )
    # plt.show()
    plt.plot(xf, f_np_nor)
    plt.show()
    # plt.plot(xf, 2.0/sim_point * np.abs(f_n_nor[0:sim_point//2])) 
    # plt.show()