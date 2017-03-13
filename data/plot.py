import matplotlib.pyplot as plt
import numpy as np


# Messy python code for the different plots

hist = np.load("hist4.npy")
bins = np.load("bins4.npy")

rmax = bins[-1]
n_bins = len(hist)

plt.ylabel("g(r)", fontsize =  15)
plt.xlabel("$r$", fontsize =  15)
plt.tick_params(labelsize=15)

plt.bar(bins[:-1], hist, width = rmax/n_bins, edgecolor = "c", fill = True)
plt.axis([0.5,rmax,0,1.3])
plt.text(7.5,1.1,r"$\rho = 0.25$ $T = 1$",  fontsize =  15)
plt.show()


sp = np.fft.fft(hist)
freq = np.fft.fftfreq(hist.shape[-1])
plt.plot(freq,sp.real, freq, sp.imag)
plt.show()
# cp = np.zeros((20,20))
# cd = np.zeros((20,20))
#
# i  = 0
# j = 0
#
# rhos = np.linspace(.1,1.5,20)
# Ts = np.linspace(.4,3,20)
# for rhoi in rhos :
#     for Ti in Ts :
#         s1 = "data/Ds_rho=" + str(rhoi) + "_T=" + str(Ti) + ".npy"
#         s2 = "data/poss_rho=" + str(rhoi) + "_T=" + str(Ti) + ".npy"
#         s3 = "data/Ts_rho=" + str(rhoi) + "_T=" + str(Ti) + ".npy"
#         s4 = "data/Ps_rho=" + str(rhoi) + "_T=" + str(Ti) + ".npy"
#
#         # D = np.load(s1)
#         box_size = 5./(rhoi**(1/3.))
#
#         poss= np.load(s2)
#         T = np.load(s4)
#         P = np.load(s3)
#
#         pi = poss[0]
#         pp = np.average(P)
#         # if pp > 30 :
#         #     pp = 30
#         if pp < .01 :
#             pp = 0.1
#         cp[i][j] = np.log(pp)
#         cd[i][j] =  np.max(np.linalg.norm(np.average(np.abs(poss - pi), axis = 1 ), axis = 1))/box_size
#
#
#         print(rhoi,Ti, cp[i][j], cd[i][j], np.std(P), np.std(T), np.average(T))
#         j += 1
#     j= 0
#     i += 1
#
#
#
#
# x,y = np.meshgrid(rhos, Ts)
#
# plt.pcolormesh(x,y, cp)
# plt.ylabel(r"$T$", fontsize =  15)
# plt.xlabel(r"$\rho$", fontsize =  15)
# plt.tick_params(labelsize=15)
# bar = plt.colorbar()
# bar.set_label(r"$log(P)$",fontsize = 15)
# bar.ax.tick_params(labelsize=15)
#
# # plt.legend(fontsize = 15)
#
# plt.show()
#
# # rhos = np.round(rhos)
# # Ts = np.round(Ts)
#
# cd = np.flip(cd, axis = 1)
# cd = np.flip(cd, axis = 0)
#
# plt.pcolormesh(x,y, cd)
# bar = plt.colorbar()
#
# bar.set_label(r"$\hat{d}_{max}$", fontsize = 19)
# bar.ax.tick_params(labelsize=15)
#
# plt.ylabel(r"$T$", fontsize =  15)
# plt.xlabel(r"$\rho$", fontsize =  15)
# plt.tick_params(labelsize=15)
# plt.show()





# ps = np.load("data/pos1.npy")
# pl = np.load("data/pos2.npy")
# pg = np.load("data/pos3.npy")
#
#
# t = np.arange(0,8,0.004)
#
# si = ps[0]
# li = pl[0]
# gi = pg[0]
#
# ds = np.linalg.norm(np.average(np.abs(ps - si), axis = 1 ), axis = 1)
# dl = np.linalg.norm(np.average(np.abs(pl - li), axis = 1 ), axis = 1)
# dg = np.linalg.norm(np.average(np.abs(pg - gi), axis = 1 ), axis = 1)
#
# fs = 8/(1.2**(1/3.))
# fl = 8/(.8**(1/3.))
# fg = 8/(.3**(1/3.))
# print(fs,fl,fg)
#
# plt.plot(t,ds/fs,  'r', label = "solid")
# plt.plot(t,dl/fl, 'b',  label = "liquid")
# plt.plot(t,dg/fg, 'g',  label = "gas")
#
# plt.ylabel(r"$\hat{d}(t)$", fontsize =  15)
# plt.xlabel(r"$t$", fontsize =  15)
# plt.tick_params(labelsize=15)
# plt.legend(fontsize = 15)
#
# plt.show()
















# load arrays

# E_pot = np.load("data/U.npy")
# E_kin = np.load("data/KE.npy")
# pressure = np.load("data/P4.npy")
# D = np.load("data/D4.npy")

# print(E_kin)

# x = np.linspace(0,len(E_kin),len(E_kin))

# plt.figure()
# plt.subplot(211)
# plt.plot(x, E_kin, 'b', x, E_pot, 'r')

# plt.subplot(212)
# plt.plot(x, pressure, 'b')
# plt.show()

# D_flat = D.flatten()
#
# plt.hist(D_flat, bins=100)
# plt.show()
#
# D_hist, D_hist_edges = np.histogram(D_flat, bins = 100)
#
# sp = np.fft.fft(D_hist)
# freq = np.fft.fftfreq(D_hist.shape[-1])
# plt.plot(freq[2:50],sp.real[2:50])
# plt.show()
