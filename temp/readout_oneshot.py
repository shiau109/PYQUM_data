from temp.resonator_response import * 
from temp.noise_analysis import *
import matplotlib.pyplot as plt

signal_power = -130
qubitCavityCouplingInfo = {
        "q_i": 100e3,
        "q_c": 50e3,
        "f_r_bare": 6.0e9,#Hz
        "f_a": 4.5e9, #Hz
        "E_c": 200e6, #Hz
        "g_ra": 40e6, #Hz
    }
cavityParas = get_simulationCavityParas(qubitCavityCouplingInfo)

power_in = 1

f_r_gnd = cavityParas["gnd"][0]
f_r_exc = cavityParas["exc"][0]
chi_eff = cavityParas["chi_eff"]
q_l = cavityParas["gnd"][1]
f_r_effBare = (f_r_gnd+f_r_exc)/2
k_l = 2*np.pi*f_r_gnd/q_l

#plot frequency range setting
f_r_max = np.max([f_r_gnd,f_r_exc])+2*abs(chi_eff)
f_r_min = np.min([f_r_gnd,f_r_exc])-2*abs(chi_eff)
f = np.linspace( f_r_min, f_r_max,1000)

print(f"f_r_gnd: {f_r_gnd/1e9} GHz")
print(f"f_r_exc: {f_r_exc/1e9} GHz")
print(f"k/2chi: {k_l/(2*chi_eff)/(2*np.pi)}")
print(f"q_l: {q_l}")
print(f"chi_01: {chi_eff/1e3} kHz")
print(f"chi_eff: {chi_eff/1e3} kHz")
#r_bare = notch_resonator(f,[f_r_bare,q_l,q_c,0,0])
s21_r_gnd = notch_resonator(f,cavityParas["gnd"])
s21_r_exc = notch_resonator(f,cavityParas["exc"])

f_ratio = (f-f_r_effBare)/abs(chi_eff)
# Plot Amplitude
plt.figure(4)
plt.plot(f_ratio,np.abs(s21_r_gnd),label='gnd')
plt.plot(f_ratio,np.abs(s21_r_exc),label='exc')
plt.plot(f_ratio,abs(np.abs(s21_r_exc)-np.abs(s21_r_gnd)),label='exc-gnd')
plt.legend()

# Plot Phase
plt.figure(5)
plt.plot(f_ratio,np.arctan2(s21_r_gnd.imag,s21_r_gnd.real),label='gnd')
plt.plot(f_ratio,np.arctan2(s21_r_exc.imag,s21_r_exc.real),label='exc')
plt.plot(f_ratio,np.arctan2(s21_r_exc.imag,s21_r_exc.real)-np.arctan2(s21_r_gnd.imag,s21_r_gnd.real),label='exc-gnd')
plt.legend()

# Plot IQ plane
"""
plt.figure(6)
plt.plot(s21_r_gnd.real,s21_r_gnd.imag,'bo',label='gnd')
plt.plot(s21_r_exc.real,s21_r_exc.imag,'ro',label='exc')
plt.plot((s21_r_exc-s21_r_gnd).real,(s21_r_exc-s21_r_gnd).imag,label='exc-gnd')
plt.legend()
"""
# Plot vector
# plt.figure(7)
# plt.plot(f_ratio,np.abs(s21_r_exc-s21_r_gnd),label='exc-gnd')
# plt.legend()

# calciate maximum input power
power_trans_gnd = power_in*np.abs(s21_r_gnd)**2
power_reflect_gnd = power_in*np.abs(s21_r_gnd-1)**2
power_abs_gnd = power_in-(power_trans_gnd+power_reflect_gnd)

power_trans_exc = power_in*np.abs(s21_r_exc)**2
power_reflect_exc = power_in*np.abs(s21_r_exc-1)**2
power_abs_exc = power_in-(power_trans_exc+power_reflect_exc)

max_power_abs = np.maximum(power_abs_gnd,power_abs_exc)
# Plot max_power_abs
"""
plt.figure(10)
plt.plot(f_ratio,power_abs_gnd,label='gnd')
plt.plot(f_ratio,power_abs_exc,label='exc')
plt.plot(f_ratio,max_power_abs,label='gnd+exc')
plt.legend()

plt.figure(11)
plt.plot(f_ratio,power_abs_gnd/max_power_abs,label='gnd')
plt.plot(f_ratio,power_abs_exc/max_power_abs,label='exc')
plt.legend()
"""
s21_r_gnd = notch_resonator(f_r_effBare,cavityParas["gnd"])
s21_r_exc = notch_resonator(f_r_effBare,cavityParas["exc"])
time = np.linspace(0, 3e-6, 3000)
raw_sig = sim_RF_real(time,signal_V,signal_freq,0,v_noise_discrete)

# plt.figure(13)
# plt.plot(f_ratio,np.abs(s21_r_exc-s21_r_gnd)*(power_abs_gnd/max_power_abs+power_abs_exc/max_power_abs-1),label='gnd')
# plt.legend()
plt.show()