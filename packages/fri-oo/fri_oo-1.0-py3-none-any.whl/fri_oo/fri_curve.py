# ###############################################################
# fri_curve.py
# ==============
# Author: Leo Serena [leo.serena@epfl.ch]
# ###############################################################

import numpy as np
from scipy import linalg
import pickle
import os

# for actual package
from . alg_tools_2d import recon_fri_curve, std_normalised, snr_normalised, gen_samples_edge_img, build_G_fri_curve, lsq_fri_curve, cadzow_iter_fri_curve, slra_fri_curve
from . import plotter

# for html automodule
# from fri_oo.alg_tools_2d import recon_fri_curve, std_normalised, snr_normalised, gen_samples_edge_img, build_G_fri_curve, lsq_fri_curve, cadzow_iter_fri_curve, slra_fri_curve
# from fri_oo import plotter

class FriCurve:
    """
    FRI curve reconstruction
    """
    def __init__(self, tau_x, tau_y):
        """
        Parameters
        ----------
        tau_x: float
            period on x axis
        tau_y: float
            period on y axis
        """
        self.tau_x = tau_x
        self.tau_y = tau_y
        self.type = 'FriCurve'

    def setup(self, M0, N0, B_x, B_y, P):
        """
        Simulation setup

        Parameters
        ----------
        M0: int
            number of samples in x axis
        N0: int
            number of samples in y axis
        B_x: int
            bandwidth in x axis
        B_y: int
            bandwidth in y axis
        P: float
            SNR in decibel
        """
        samples_size = np.array([2 * N0 + 1, 2 * M0 + 1])

        self.B_x = B_x
        self.B_y = B_y

        self.P = P
        self.coef = np.asarray(
                    [[-0.95563489, 1.70606045, 0.33067637],
                     [ 1.15539034, 0.58920854, 1.15539034],
                     [ 0.33067637, 1.70606045, -0.95563489]])
        #path = os.path.dirname(os.path.abspath(__file__))
        #stored_param = np.load(path + '/data/coef.npz')
        #self.coef = stored_param['coef']

        self.K = self.coef.shape[1]
        self.L = self.coef.shape[0]

        self.T1 = self.tau_x / samples_size[1]
        self.T2 = self.tau_y / samples_size[0]

        assert (self.B_x * self.tau_x) % 2 == 1 and (self.B_y * self.tau_y) % 2 == 1
        assert self.B_x * self.T1 <= 1 and self.B_y * self.T2 <= 1
        assert (self.B_x * self.tau_x - self.K + 1) * (self.B_y * self.tau_y - self.L + 1) >= self.K * self.L

        self.x_samp = np.linspace(0, self.tau_x, num = samples_size[1], endpoint=False)
        self.y_samp = np.linspace(0, self.tau_y, num = samples_size[0], endpoint=False)

        self.G = build_G_fri_curve(self.x_samp, self.y_samp, self.B_x, self.B_y, self.tau_x, self.tau_y)

        self.samples_noiseless, self.fourier_lowpass = \
            gen_samples_edge_img(self.coef, samples_size, self.B_x, self.B_y, self.tau_x, self.tau_y)
        # check whether we are in the case with real-valued samples or not
        real_valued = np.max(np.abs(np.imag(self.samples_noiseless))) < 1e-12
        # add Gaussian white noise
        if real_valued:
            noise = np.random.randn(samples_size[0], samples_size[1])
            samples_noiseless = np.real(self.samples_noiseless)
        else:
            noise = np.random.randn(samples_size[0], samples_size[1]) + \
                    1j * np.random.randn(samples_size[0], samples_size[1])
        noise = noise / linalg.norm(noise, 'fro') * \
                linalg.norm(samples_noiseless, 'fro') * 10 ** (-P / 20.)
        self.samples_noisy = samples_noiseless + noise
        # noise energy, in the noiseless case 1e-10 is considered as 0
        self.noise_level = np.max([1e-10, linalg.norm(noise, 'fro')])

    def reconstruction(self, max_ini = 20, stop_cri = 'max_iter', verbose = False, lsq = False, cadz = False, SLRA = False):
        """
        Main method.
        Reconstrucs FRI curve according to requested algorithms.
        
        Parameters
        ----------
        max_ini: int
            maximum number of random initialisations
        stop_cri: str
            the stopping criteria of the algorithm, can either be *mse* or *max_iter*
        verbose: bool
            if True outputs curve coefficients and curve coefficients error
        lsq: bool
            if True also runs least squre approximation reconstruction
        cadz: bool
            if True also runs cadzdow method reconstruction
        SLRA: bool
            if True also runs SLRA method reconstruction
        """
        self.lsq = lsq
        self.cadz = cadz
        self.SLRA = SLRA
        if lsq:
            # least square reconstruction
            self.coef_recon_lsq = lsq_fri_curve(self.G, self.samples_noisy, self.K, self.L, self.B_x, self.B_y, self.tau_x, self.tau_y)
            self.std_lsq = std_normalised(self.coef_recon_lsq, self.coef)[0]
            self.snr_lsq = snr_normalised(self.coef_recon_lsq, self.coef)

        if cadz:
            # cadzow iterative denoising
            self.K_cad = np.int(np.floor((self.B_x * self.tau_x - 1) / 4) * 2 + 1)
            self.L_cad = np.int(np.floor((self.B_y * self.tau_y - 1) / 4) * 2 + 1)
            self.coef_recon_cadzow = cadzow_iter_fri_curve(self.G, self.samples_noisy, self.K, self.L, self.K_cad, self.L_cad,
                                                    self.B_x, self.B_y, self.tau_x, self.tau_y, max_iter=1000)
            self.std_cadzow = std_normalised(self.coef_recon_cadzow, self.coef)[0]
            self.snr_cadzow = snr_normalised(self.coef_recon_cadzow, self.coef)

        if SLRA:
            # structured low rank approximation (SLRA) by L. Condat
            self.K_alg = np.int(np.floor((self.B_x * self.tau_x - 1) / 4) * 2 + 1)
            self.L_alg = np.int(np.floor((self.B_y * self.tau_y - 1) / 4) * 2 + 1)
            # weight_choise: '1': the default one based on the repetition of entries in
            # the block Toeplitz matrix
            # weight_choise: '2': based on the repetition of entries in the block Toeplitz
            # matrix and the frequency re-scaling factor in hat_partial_I
            # weight_choise: '3': equal weights for all entries in the block Toeplitz matrix
            self.coef_recon_slra = slra_fri_curve(self.G, self.samples_noisy, self.K, self.L, self.K_alg, self.L_alg,
                                            self.B_x, self.B_y, self.tau_x, self.tau_y, max_iter=1000,
                                            weight_choice='1')
            self.std_slra = std_normalised(self.coef_recon_slra, self.coef)[0]
            self.snr_slra = snr_normalised(self.coef_recon_slra, self.coef)

        # the proposed approach
        xhat_recon, min_error, self.coef_recon, ini = \
            recon_fri_curve(self.G, self.samples_noisy, self.K, self.L,
                            self.B_x, self.B_y, self.tau_x, self.tau_y, self.noise_level, max_ini, stop_cri)

        self.std_coef_error = std_normalised(self.coef_recon, self.coef)[0]
        self.snr_error = snr_normalised(self.coef_recon, self.coef)

        if verbose:
            if lsq:
                print('Least Square Minimisation')
                print('Standard deviation of the reconstructed ' +
                    'curve coefficients error: {:.4f}'.format(self.std_lsq))
                print('SNR of the reconstructed ' +
                    'curve coefficients: {:.4f}[dB]\n'.format(self.snr_lsq))

            if cadz:
                print('Cadzow Iterative Method')
                print('Standard deviation of the reconstructed ' +
                    'curve coefficients error: {:.4f}'.format(self.std_cadzow))
                print('SNR of the reconstructed ' +
                    'curve coefficients: {:.4f}[dB]\n'.format(self.snr_cadzow))

            if SLRA:
                print('SLRA Method')
                print('Standard deviation of the reconstructed ' +
                    'curve coefficients error: {:.4f}'.format(self.std_slra))
                print('SNR of the reconstructed ' +
                    'curve coefficients: {:.4f}[dB]\n'.format(self.snr_slra))

            print('Proposed Approach')
            print('Standard deviation of the reconstructed ' +
                'curve coefficients error: {:.4f}'.format(self.std_coef_error))
            print('SNR of the reconstructed ' +
                'curve coefficients: {:.4f}[dB]\n'.format(self.snr_error))

    def save_results(self, simName):
        """
        save results to the *results* file

        Parameters
        ----------
        simName: str
            string naming the file
        """
        self.name = simName #name can't be changed afterwards
        try:
            file = open("results", "rb")
            p = pickle.Unpickler(file)
            data = p.load()
            file.close()
        except FileNotFoundError:
            print("creating new data file")
            data = dict()
        except EOFError:
            print("no data was found in file")
            data = dict()
            file.close()

        data[simName] = self.__dict__

        with open("results", "wb") as f:
            p = pickle.Pickler(f)
            p.dump(data)
    
    def plot(self, save_fig = False, fig_format = 'png'):
        """
        plotter for the FRI curve
        
        Parameters
        ----------
        save_fig: bool
            saves the file is is True
        fig_format: str
            format used if saved
        """
        plotter.plot_friCurve(self.name, save_fig, fig_format)