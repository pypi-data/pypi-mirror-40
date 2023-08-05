# ###############################################################
# plotter.py
# ==============
# Author: Leo Serena [leo.serena@epfl.ch]
# ###############################################################

import pickle
import numpy as np
from matplotlib import pyplot as plt


# for actual package
# ==================
from . alg_tools_1d import build_G_fourier
from . alg_tools_2d import plt_recon_fri_curve

# for html automodule
# ===================
# from fri_oo.alg_tools_1d import build_G_fourier
# from fri_oo.alg_tools_2d import plt_recon_fri_curve

def fetch_data(name):
    """
    retrieves dictionary of given simulation name

    The name of the simulation was given when using *save_results* on the object.
    To see the currently saved results, run retrieve_data()

    Parameters
    ----------
    name: str
        name of the wanted simulation
    
    Returns
    -------
    dic
        the corresponding dictionary
    """
    data_retrieved = False

    try:
        file = open("results", "rb")
        p = pickle.Unpickler(file)
        data = p.load()
        data_retrieved = True
        file.close()
    except FileNotFoundError:
        print("the data file wasn't found")
    except EOFError:
        print("no data was found in file")
        file.close()

    dic = dict()
    if data_retrieved:
        dic = data[name]
    else:
        print("a problem has occurred, the data couldn't be retrieved")
    
    return dic

def plot_irreg_samp(name, save_fig, fig_format):
    """
    plotter for the irrTimeSamp class

    This plotter plots plots the results of the named reconstruction.
    It also plots the original diracs and signal if default G matrix and a measurements were given.

    Parameters
    ----------
    name: str
        name of the reconstruction
    save_fig: bool
        saves the plots if True is given.
    fig_format: str
        specifies the fig format, using matplotlib.pyplot.savefig.
    """
    dic = fetch_data(name)

    original = dic['original']
    K = dic['K']
    tau = dic['tau']
    L = dic['L']
    P = dic['P']
    tk_recon = dic['tk_recon']
    ak_recon = dic['ak_recon']
    Tmax = dic['Tmax']
    B = dic['B']
    t_samp = dic['t_samp']
    yl = dic['yl']

    # delta has to be configured to have a good y border for good visualisation
    delta = 0.1

    plt.close()
    # plot of the first figure
    plt.figure(1)

    if original:
        # first subplot

        error = dic['t_error']
        tk = dic['tk']
        ak = dic['ak']

        plt.subplot(211)
        t_error_pow = np.int(np.floor(np.log10(error)))
        plt.title("initial data and reconstruction comparison\nK = {}   tau = {}   L = {}   SNR = {} dB\n".format(K, tau, L, P) 
                    + r"$error = {:.2f}*10^{}$".format(error/10**t_error_pow, {t_error_pow}))
        markerline, stemline, baseline = plt.stem(tk, ak , '-')
        plt.setp(baseline, color = 'black', linewidth = 2)
        plt.setp(stemline, color = 'blue', linewidth = 1)
        plt.setp(markerline, color = 'blue', marker = '^', markersize = 4)

        plt.axis([tk[0] - Tmax, tk[tk.size-1] + Tmax,
                np.amin(ak) - delta, np.amax(ak) + delta])
        plt.ylabel("original amplitudes", fontsize = 10, color = "blue")
    else:
        plt.title("Reconstructed diracs\nK = {}   tau = {}   L = {}   SNR = {} dB\n".format(K, tau, L, P))
        

    # second subplot
    plt.subplot(212)
    markerline, stemline, baseline = plt.stem(tk_recon, ak_recon, '-')
    plt.setp(baseline, color = 'black', linewidth = 2)
    plt.setp(stemline, color = 'red', linewidth = 1)
    plt.setp(markerline, color = 'red', marker = '^', markersize = 4)
    plt.axis([tk_recon[0] - Tmax, tk_recon[tk_recon.size-1] + Tmax,
            np.amin(ak_recon) - delta, np.amax(ak_recon) + delta])
    plt.ylabel("reconstructed amplitudes", fontsize = 10, color = 'red')
    plt.xlabel("time t", fontsize = 10, color = 'green')

    if(save_fig):
        plt.savefig(name + "_diracs" + "." + fig_format, format = fig_format)

    # plot of the second figure for case of irregular time samples
    plt.figure(2)
    t_plt = np.linspace(0, tau, num=np.max([10 * L, 1000]))
    m_plt_grid, t_plt_grid = np.meshgrid(np.arange(-np.floor(B * tau / 2.),
                                                1 + np.floor(B * tau / 2.)),
                                                t_plt)
    G_plt = 1. / B * np.exp(2j * np.pi / tau * m_plt_grid * t_plt_grid)
    if original:
        x_hat_noiseless = dic['x_hat_noiseless']
        
        y_plt = np.real(np.dot(G_plt, x_hat_noiseless))
        plt.plot(t_plt, y_plt, label = 'Ground Truth')
        
    plt.plot(t_samp, yl, 'o', label = 'Samples')
    plt.legend(loc = 'lower left')

    if save_fig:
        plt.savefig(name + "_cont" + "." + fig_format, format = fig_format)
        
    plt.show()

def plot_four_samp(name, save_fig, fig_format):
    """
    plotter for the IrrFourSamp class

    This plotter plots plots the results of the named reconstruction.

    Parameters
    ----------
    name: str
        name of the reconstruction
    save_fig: bool
        saves the plots if True is given.
    fig_format: str
        specifies the fig format, using matplotlib.pyplot.savefig.
    """
    
    dec = fetch_data(name)
    original = dec['original']
    tau = dec['tau']
    L = dec['L']
    M = dec['M']
    K = dec['K']
    P = dec['P']
    Tmax = 0.1
    ak_recon = dec['ak_recon']
    tk_recon = dec['tk_ref']
    interp_kernel = dec['interp_kernel']
    Xomega_Uniform_ref = dec['Xomega_Uniform_ref']

    plt.close()

    plt.figure(1)

    delta = 0.1

    if original:
        # first subplot

        error = dec['t_error']
        tk = dec['tk']
        ak = dec['ak']

        plt.subplot(211)
        t_error_pow = np.int(np.floor(np.log10(error)))
        markerline, stemline, baseline = plt.stem(tk, ak , '-')
        plt.setp(baseline, color = 'black', linewidth = 2)
        plt.setp(stemline, color = 'blue', linewidth = 1)
        plt.setp(markerline, color = 'blue', marker = '^', markersize = 4)

        plt.axis([tk[0] - Tmax, tk[tk.size-1] + Tmax,
                np.amin(ak) - delta, np.amax(ak) + delta])
        plt.ylabel("original amplitudes", fontsize = 10, color = "blue")
        plt.title("initial data and reconstruction comparison\nK = {}   L = {}   SNR = {} dB".format(K, L, P) 
            + r"$error = {:.2f}*10^{}$".format(error/10**t_error_pow, {t_error_pow}))
    else:
        plt.title("Reconstructed diracs\nK = {}   L = {}   SNR = {} dB".format(K, L, P))

    #  if original:
    #     ak = dec['ak']
    #     tk = dec['tk']
    #     error = dec['t_error']
    #     t_error_pow = np.int(np.floor(np.log10(error)))
    #     # sub-figure 1
    #     #ax1 = plt.axes([subplt_left_corner, 0.71, subplt_width, subplt_height])
    #     markerline311_1, stemlines311_1, baseline311_1 = ax1.stem(tk, ak, label='Original Diracs')
    #     plt.setp(stemlines311_1, linewidth=1.5, color=[0, 0.447, 0.741])
    #     plt.setp(markerline311_1, marker='^', linewidth=1.5, markersize=8, 
    #             markerfacecolor=[0, 0.447, 0.741], mec=[0, 0.447, 0.741])
    #     plt.setp(baseline311_1, linewidth=0)
    #     #ax1.yaxis.set_tick_params(labelsize=8.5)
    #     #ax1.xaxis.set_label_coords(0.5, -0.21)
    #     plt.title("initial data and reconstruction comparison\nK = {}   L = {}   SNR = {} dB".format(K, L, P) 
    #         + r"$error = {:.2f}*10^{}$".format(error/10**t_error_pow, {t_error_pow}))
    # else:
    #     plt.title("Reconstructed diracs\nK = {}   L = {}   SNR = {} dB".format(K, L, P))


    # second subplot
    plt.subplot(212)
    markerline, stemline, baseline = plt.stem(tk_recon, ak_recon, '-')
    plt.setp(baseline, color = 'black', linewidth = 2)
    plt.setp(stemline, color = 'red', linewidth = 1)
    plt.setp(markerline, color = 'red', marker = '^', markersize = 4)
    plt.axis([tk_recon[0] - Tmax, tk_recon[tk_recon.size-1] + Tmax,
            np.amin(ak_recon) - delta, np.amax(ak_recon) + delta])
    plt.ylabel("reconstructed amplitudes", fontsize = 10, color = 'red')
    plt.xlabel("time t", fontsize = 10, color = 'green')

    if(save_fig):
        plt.savefig(name + "_diracs" + "." + fig_format, format = fig_format)

    # markerline311_2, stemlines311_2, baseline311_2 = \
    #     plt.stem(tk_recon, ak_recon, label='Estimated Diracs')
    # plt.setp(stemlines311_2, linewidth=1.5, color=[0.850, 0.325, 0.098])
    # plt.setp(markerline311_2, marker='*', linewidth=1.5, markersize=10,
    #         markerfacecolor=[0.850, 0.325, 0.098], mec=[0.850, 0.325, 0.098])
    # plt.setp(baseline311_2, linewidth=0)
    # # ax1.yaxis.major.locator.set_params(nbins=7)
    # plt.axhline(0, color='k')
    # plt.xlim([-tau / 2, tau / 2])
    # if original:
    #     plt.ylim([1.18 * np.min(np.concatenate((ak, ak_recon, np.array(0)[np.newaxis]))),
    #             1.18 * np.max(np.concatenate((ak, ak_recon, np.array(0)[np.newaxis])))])
    # plt.xlabel(r'$t$', fontsize=12)
    # plt.ylabel(r'amplitudes', fontsize=12)
    # plt.legend(numpoints=1, loc=0, fontsize=9, framealpha=0.3,
    #         columnspacing=1.7, labelspacing=0.1)

    if save_fig:
        plt.savefig(name + "_diracs" + "." + fig_format, format = fig_format)

    plt.figure(2)

    omega_ell = dec['omega_ell']
    Xomega_ell = dec['Xomega_ell']

    omega_continuous = np.linspace(-np.pi * M, np.pi * M, num=np.max([10 * L, 10000]))
    if original:
        tk_grid_conti, omega_grid_conti = np.meshgrid(tk, omega_continuous)
        Xomegas_conti = np.dot(np.exp(-1j * omega_grid_conti * tk_grid_conti), ak)

    #m_limit = np.floor(M * tau / 2.)
    #m_grid_conti, omega_grid_conti_recon = np.meshgrid(np.arange(-m_limit, m_limit + 1), omega_continuous)
    G_conti_recon = build_G_fourier(omega_continuous, M, tau, interp_kernel, tk_ref=tk_recon)
    Xomegas_conti_recon = np.dot(G_conti_recon, Xomega_Uniform_ref)

    plt.subplot(211)

    plt.plot(omega_ell, np.real(Xomega_ell),'o', label = 'measurements')
    if original:
        plt.plot(omega_continuous, np.real(Xomegas_conti), label='Ground Truth')
    plt.plot(omega_continuous, np.real(Xomegas_conti_recon), label='Reconstruction')

    plt.ylabel(r'$\Re\left\{X(\omega)\right\}$')
    plt.xlabel(r'$\omega$')

    # ax2 = plt.axes([subplt_left_corner, 0.358, subplt_width, subplt_height])
    # line312_1 = ax2.plot(omega_ell, np.real(Xomega_ell), label='Measurements')
    # plt.setp(line312_1, marker='.', linestyle='None', markersize=5, color=[0, 0.447, 0.741])

    # if original:
    #     line312_2 = plt.plot(omega_continuous, np.real(Xomegas_conti), label='Ground Truth')
    #     plt.setp(line312_2, linestyle='-', color=[0.850, 0.325, 0.098], linewidth=1)

    # line312_3 = plt.plot(omega_continuous, np.real(Xomegas_conti_recon), label='Reconstruction')
    # plt.setp(line312_3, linestyle='--', color=[0.466, 0.674, 0.188], linewidth=1.5)
    # if original:    
    #     plt.ylim([1.1 * np.min(np.concatenate((np.real(Xomegas_conti), np.real(Xomega_ell)))),
    #          1.1 * np.max(np.concatenate((np.real(Xomegas_conti), np.real(Xomega_ell))))])
    # ax2.yaxis.major.locator.set_params(nbins=7)
    # plt.ylabel(r'$\Re\left\{X(\omega)\right\}$', fontsize=13)
    plt.legend(numpoints=1, loc=4, bbox_to_anchor=(1.013, 0.975), fontsize=9,
               handletextpad=.2, columnspacing=1.7, labelspacing=0.1, ncol=3)

    plt.subplot(212)

    plt.plot(omega_ell, np.imag(Xomega_ell), 'o', label = 'measurements')
    if original:
        plt.plot(omega_continuous, np.imag(Xomegas_conti), label='Ground Truth')
    plt.plot(omega_continuous, np.imag(Xomegas_conti_recon), label='Reconstruction')

    plt.ylabel(r'$\Im\left\{X(\omega)\right\}$')
    plt.xlabel(r'$\omega$')

    # ax3 = plt.axes([subplt_left_corner, 0.10, subplt_width, subplt_height])
    # line313_1 = ax3.plot(omega_ell, np.imag(Xomega_ell), label='Measurements')
    # plt.setp(line313_1, marker='.', linestyle='None', markersize=5, color=[0, 0.447, 0.741])

    # if original:
    #     line313_2 = plt.plot(omega_continuous, np.imag(Xomegas_conti), label='Ground Truth')
    #     plt.setp(line313_2, linestyle='-', color=[0.850, 0.325, 0.098], linewidth=1)

    # line313_3 = plt.plot(omega_continuous, np.imag(Xomegas_conti_recon), label='Reconstruction')
    # plt.setp(line313_3, linestyle='--', color=[0.466, 0.674, 0.188], linewidth=1.5)
    # if original:
    #     plt.ylim([1.1 * np.min(np.concatenate((np.imag(Xomegas_conti), np.imag(Xomega_ell_noisy)))),
    #             1.1 * np.max(np.concatenate((np.imag(Xomegas_conti), np.imag(Xomega_ell_noisy))))])
    # ax3.yaxis.major.locator.set_params(nbins=7)
    # plt.ylabel(r'$\Im\left\{X(\omega)\right\}$', fontsize=12)
    # plt.xlabel(r'$\omega$', fontsize=12)
    # ax3.xaxis.set_label_coords(0.5, -0.21)

    if save_fig:
        plt.savefig(name + "_cont" + "." + fig_format, format = fig_format)   

    plt.show()

def plot_friCurve(name, save_fig, fig_format):
    """
    plotter for the IrrFourSamp class

    This plotter plots plots the results of the named reconstruction.

    Parameters
    ----------
    name: str
        name of the reconstruction
    save_fig: bool
        saves the plots if True is given.
    fig_format: str
        specifies the fig format, using matplotlib.pyplot.savefig.
    """
        
    dic = fetch_data(name)

    samples_noisy = dic['samples_noisy']
    tau_x = dic['tau_x']
    tau_y = dic['tau_y']
    coef = dic['coef']

    plt_size = np.array([1e3, 1e3])
    plt.imshow(np.abs(samples_noisy), origin='upper', cmap='gray')
    plt.axis('off')

    if save_fig:
        plt.savefig(name + "_FRIC" + "." + fig_format, format = fig_format)
    #if save_fig:
    #   file_name = (r'./result/TSP_eg3_K_{0}_L_{1}_' +
    #                r'noise_{2}dB_samples.' + fig_format).format(repr(K), repr(L), repr(P))
    #    plt.savefig(file_name, format=fig_format, dpi=300, transparent=True)

    if dic['cadz']:
        coef_recon_cadzow = dic['coef_recon_cadzow']

        # Cadzow denoising result
        file_name = name + "_Cadzow" + "." + fig_format
        curve_recon_cad = \
            plt_recon_fri_curve(coef_recon_cadzow, coef, tau_x, tau_y,
                                plt_size, save_fig, file_name, nargout=1,
                                file_format = fig_format)[0]

    if dic['SLRA']:
        coef_recon_slra = dic['coef_recon_slra']

        # SLRA result
        file_name = name + "_SLRA" + "." + fig_format
        curve_recon_slra = \
            plt_recon_fri_curve(coef_recon_slra, coef, tau_x, tau_y,
                                plt_size, save_fig, file_name, nargout=1,
                                file_format = fig_format)[0]

    coef_recon = dic['coef_recon']

    # proposed approach result
    file_name = name + "_propApproach" + "." + fig_format
    curve_recon_proposed, idx_x, idx_y, subset_idx = \
        plt_recon_fri_curve(coef_recon, coef, tau_x, tau_y,
                            plt_size, save_fig, file_name, nargout=4,
                            file_format = fig_format)
    
    plt.show()

def retrieve_data():
    """
    this method is used to display the data stored in the *results* file

    Returns
    -------
    data_names: list
        list of the names of all the saved results
    """
    try:
        file = open("results", "rb")
        p = pickle.Unpickler(file)
        data = p.load()
        file.close()
    except FileNotFoundError:
        print("the data file wasn't found")
    except EOFError:
        print("no data was found in file")
        file.close()

    data_names = list()
    for key in data.keys():
        data_names.append(key)

    return data_names

def delete_data(name):
    """
    This function is used to delete the stored data in the *results* file

    To know what are the currently stored simulations, run retrieve_data().

    Parameters
    ----------
    name: str
        name of the simulation that needs to be deleted.
    """
    try:
        file = open("results", "rb")
        p = pickle.Unpickler(file)
        data = p.load()
        file.close()
    except FileNotFoundError:
        print("the data file wasn't found")
    except EOFError:
        print("no data was found in file")
        file.close()

    try:
        del data[name]
        with open("results", "wb") as f:
            p = pickle.Pickler(f)
            p.dump(data)
    except KeyError:
        print("name not found in data")

def plot_data(name, save_fig = False, fig_format = 'png'):
    """
    Method used to plot data directly from the *results* file
    
    Parameters
    ----------
    name: str
        name of the reconstruction
    save_fig: bool
        saves the plots if True is given.
    fig_format: str
        specifies the fig format, using matplotlib.pyplot.savefig.
    """
    dic = fetch_data(name)
    if dic['type'] == 'ITS':
        plot_irreg_samp(name, save_fig, fig_format)
    elif dic['type'] == 'IFS':
        plot_four_samp(name, save_fig, fig_format)
    elif dic['type'] == 'Fricurve':
        plot_friCurve(name, save_fig, fig_format)