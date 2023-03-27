from temp.resonator_response import * 
from temp.noise_analysis import *
import matplotlib.pyplot as plt
from temp.unit_conversion import *
PLANCK = 6.626e-34

qubitCavityCouplingInfo = {
        "q_i": 40e3,
        "q_c": 20e3,
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
n_c = cavityParas["n_crit"]

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
print(f"n_c: {n_c}")

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

# calcuate maximum input power
power_trans_gnd = np.abs(s21_r_gnd)**2
power_reflect_gnd = np.abs(s21_r_gnd-1)**2
power_abs_gnd = 1-(power_trans_gnd+power_reflect_gnd)

power_trans_exc = np.abs(s21_r_exc)**2
power_reflect_exc = np.abs(s21_r_exc-1)**2
power_abs_exc = 1-(power_trans_exc+power_reflect_exc)

max_power_abs = np.maximum(power_abs_gnd,power_abs_exc)
# Plot max_power_abs

plt.figure(10)
plt.plot(f_ratio,power_abs_gnd,label='gnd')
plt.plot(f_ratio,power_abs_exc,label='exc')
plt.plot(f_ratio,max_power_abs,label='max(gnd,exc)')
plt.legend()

plt.figure(11)
plt.plot(f_ratio,power_abs_gnd/max_power_abs,label='gnd')
plt.plot(f_ratio,power_abs_exc/max_power_abs,label='exc')
plt.legend()


k_c = qubitCavityCouplingInfo["f_r_bare"]/qubitCavityCouplingInfo["q_c"]
k_i = qubitCavityCouplingInfo["f_r_bare"]/qubitCavityCouplingInfo["q_i"]
s21_r_gnd = notch_resonator(f,cavityParas["gnd"])

r_abs = absorption(s21_r_gnd,k_i)*k_i # Energy ratio
r_df = d_formula(f, f_r_gnd, k_c, k_i) # Energy ratio
er_res = 4.*k_c/((k_c+k_i)**2) # Energy ratio
p_crit = n_c*PLANCK*f_r_gnd/er_res
print(f"p_crit = {10*np.log10(p_crit*1000)} dBm")
plt.figure(14)
plt.plot(f,r_abs,label='abs')
# plt.plot(f,r_df,label='df')
plt.legend()

# plt.figure(13)
# plt.plot(f_ratio,np.abs(s21_r_exc-s21_r_gnd)*(power_abs_gnd/max_power_abs+power_abs_exc/max_power_abs-1),label='gnd')
# plt.legend()
plt.show()
sim_point = int(1000)
dt = 2e-9
bandwidth = 1/dt/2
signal_temp = 0.2
resistance_load = 50

time = np.linspace(0.0, sim_point*dt, sim_point, endpoint=False)
s21_r_gnd = notch_resonator(f_r_effBare,cavityParas["gnd"])
s21_r_exc = notch_resonator(f_r_effBare,cavityParas["exc"])

amp_g = dBm_to_vpp(10*np.log10(p_crit*1000))*np.abs(s21_r_gnd)
pha_g = np.angle(s21_r_gnd)
amp_e = dBm_to_vpp(10*np.log10(p_crit*1000))*np.abs(s21_r_exc)
pha_e = np.angle(s21_r_exc)

v_noise = thermal_noise(f_r_effBare,signal_temp,bandwidth,resistance_load)
plt.figure(15)
shots_g = acc_shot(1000,time,amp_g,f_r_effBare,pha_g,v_noise)
shots_e = acc_shot(1000,time,amp_e,f_r_effBare,pha_e,v_noise)
nosig_shots = 0
plt.plot(shots_g.real,shots_g.imag,"o",label='g')
plt.plot(shots_e.real,shots_e.imag,"o",label='e')
# plt.plot(nosig_shots.real,nosig_shots.imag,"o",label='no sig')
plt.show()

rt_ref_psd = thermal_PSD(f_r_effBare,290)
rt_ref_noise = thermal_noise(f_r_effBare,290,bandwidth,resistance_load)


G_JPA = 0
NT_JPA = 0
f_hemt = (290+NT_JPA)/290
np_in = (f_hemt-1)*rt_ref_noise**2
jpa_noise = np.sqrt(v_noise**2+np_in)
print(f"JPA noise :{jpa_noise*1e6} uV {rt_ref_noise**2/v_noise**2} ,{np_in/v_noise**2}")
a_jpa = powerdB_to_vRatio(G_JPA)
g_jpa = 10**(G_JPA/10)
print(f"JPA gain {g_jpa} {a_jpa}")
shots_g = acc_shot(1000,time,amp_g*a_jpa,f_r_effBare,pha_g,jpa_noise*a_jpa)
shots_e = acc_shot(1000,time,amp_e*a_jpa,f_r_effBare,pha_e,jpa_noise*a_jpa) 
nosig_shots = 0
plt.figure(16)

plt.plot(shots_g.real,shots_g.imag,"o",label='g')
plt.plot(shots_e.real,shots_e.imag,"o",label='e')
# plt.plot(nosig_shots.real,nosig_shots.imag,"o",label='no sig')
plt.show()




G_HEMT = 40
NF_HEMT = 0.022
f_hemt = 10**(0.022/10)
np_in = (f_hemt-1)*rt_ref_noise**2
hemt_noise = np.sqrt((jpa_noise*a_jpa)**2+np_in)
print(f"HEMT noise :{hemt_noise*1e6} uV {rt_ref_noise**2/v_noise**2} ,{np_in/v_noise**2}")
a_hemt = powerdB_to_vRatio(G_HEMT)
shots_g = acc_shot(1000,time,amp_g*a_jpa*a_hemt,f_r_effBare,pha_g,hemt_noise*a_hemt)
shots_e = acc_shot(1000,time,amp_e*a_jpa*a_hemt,f_r_effBare,pha_e,hemt_noise*a_hemt) 
nosig_shots = 0
plt.figure(16)

plt.plot(shots_g.real,shots_g.imag,"o",label='g')
plt.plot(shots_e.real,shots_e.imag,"o",label='e')
# plt.plot(nosig_shots.real,nosig_shots.imag,"o",label='no sig')
plt.show()