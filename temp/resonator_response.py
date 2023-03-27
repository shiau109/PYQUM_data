import numpy as np

def ideal_notch_resonator( f, p ):
    """
    fr=p[0] resonant frequency
    ql=p[1] loaded quality factor
    qc=p[2] coupling quality factor
    phi=p[3] asymmetry 
    """
    fr=p[0]
    ql=p[1] 
    qc=p[2] 
    phi=p[3] 
    return 1- ql/np.abs(qc) *np.exp(1j*phi)/(1+2j*ql*(f/fr-1))
def notch_resonator( f, p ):
    return np.exp(1j*p[4])*ideal_notch_resonator(f,p[0:4])

def get_simulationCavityParas(qubitCavityCouplingInfo = None):
    defaultInfo = {
            "q_i": 1000e3,
            "q_c": 50e3,
            "f_r_bare": 7e9,#Hz
            "f_a": 5e9, #Hz
            "E_c": 200e6, #Hz
            "g_ra": 40e6, #Hz
        }
    if qubitCavityCouplingInfo == None:
        qubitCavityCouplingInfo = defaultInfo

    q_i = qubitCavityCouplingInfo["q_i"]
    q_c = qubitCavityCouplingInfo["q_c"]
    f_r_bare = qubitCavityCouplingInfo["f_r_bare"] #Hz
    f_a = qubitCavityCouplingInfo["f_a"] #Hz
    E_c = qubitCavityCouplingInfo["E_c"]  #Hz
    g_ra = qubitCavityCouplingInfo["g_ra"]  #Hz
    anharmonicity = -E_c
    q_l = q_c*q_i/(q_c+q_i)
    detuning = f_a-f_r_bare
    chi_01 = -g_ra**2/detuning
    beta_eff = anharmonicity/(detuning-anharmonicity)
    chi_eff = chi_01*beta_eff
    f_r_gnd = f_r_bare +chi_01
    f_r_exc = f_r_gnd -2*chi_eff
    n_crit = (detuning/g_ra)**2/4
    cavityPara = {
        "gnd": [f_r_gnd,q_l,q_c,0,0],
        "exc": [f_r_exc,q_l,q_c,0,0],
        "chi_eff": chi_eff,
        "n_crit": n_crit
    }
    return cavityPara

def absorption( s21, k_i ):
    """
    photon number calculation method
    """
    trans = np.abs(s21)**2
    reflect = np.abs(1-s21)**2
    absorb = 1-(trans+reflect)
    return absorb/k_i

def d_formula(  f, fr, k_c, k_i ):
    """
    photon number calculation method
    """

    return k_c/((k_i+k_c)**2+(f-fr)**2)

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    f_r = 6e9
    f_win = 2e6
    f = np.linspace( f_r-f_win/2, f_r+f_win/2, 200 )
    s21_ideal = ideal_notch_resonator(f,(f_r+0.05*f_win,40e3, 40e3 ,0))
    s21_ideal_2 = ideal_notch_resonator(f,(f_r-0.05*f_win,40e3, 40e3 ,0))

    d1_pt = ideal_notch_resonator(f_r+0.05*f_win,(f_r+0.05*f_win,40e3, 40e3 ,0))
    d2_pt = ideal_notch_resonator(f_r+0.05*f_win,(f_r-0.05*f_win,40e3, 40e3 ,0))

    s21_ki = ideal_notch_resonator(f,(f_r,20e3, 40e3 ,0))
    plt.plot(f-f_r,np.abs(s21_ideal),label="fr=fq_0")
    plt.plot(f-f_r,np.abs(s21_ideal_2),label="fr=fq_1")
    plt.plot(0.05*f_win,np.abs(d1_pt),'o',label="fr=fq_0")
    plt.plot(0.05*f_win,np.abs(d2_pt),'o',label="fr=fq_1")
    plt.legend()
    plt.show()
    plt.plot(f-f_r,np.angle(s21_ideal),label="fr=fq_0")
    plt.plot(f-f_r,np.angle(s21_ideal_2),label="fr=fq_1")
    plt.plot(0.05*f_win,np.angle(d1_pt),'o',label="fr=fq_0")
    plt.plot(0.05*f_win,np.angle(d2_pt),'o',label="fr=fq_1")
    plt.legend()
    plt.show()
    plt.plot(s21_ideal.real,s21_ideal.imag,label="fr=fq_0")
    plt.plot(s21_ideal_2.real,s21_ideal_2.imag,label="fr=fq_1")
    plt.plot(d1_pt.real,d1_pt.imag,'o',label="fr=fq_0")
    plt.plot(d2_pt.real,d2_pt.imag,'o',label="fr=fq_1")
    plt.legend()
    plt.show()
    # plt.plot(f-f_r,np.abs(s21_ideal),label="ki=0")
    # plt.plot(f-f_r,np.abs(s21_ki),label="Kc=ki")
    # plt.legend()
    # plt.show()
    # plt.plot(f-f_r,np.angle(s21_ideal),label="ki=0")
    # plt.plot(f-f_r,np.angle(s21_ki),label="Kc=ki")
    # plt.legend()
    # plt.show()
    # plt.plot(s21_ideal.real,s21_ideal.imag,label="ki=0")
    # plt.plot(s21_ki.real,s21_ki.imag,label="Kc=ki")
    # plt.legend()
    # plt.show()