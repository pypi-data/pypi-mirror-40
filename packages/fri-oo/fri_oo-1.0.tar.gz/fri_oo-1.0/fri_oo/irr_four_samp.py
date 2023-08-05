# ###############################################################
# irr_four_samp.py
# ==============
# Author: Leo Serena [leo.serena@epfl.ch]
# ###############################################################

import numpy as np
import pandas as pd
import pickle

# for actual package
# ==================
from . import plotter
from . simulation import Simulation
from . alg_tools_1d import distance, dirac_recon_irreg_fourier, build_G_fourier

# for html automodule
# ===================
# from fri_oo.simulation import Simulation
# from fri_oo import plotter
# from fri_oo.alg_tools_1d import distance, dirac_recon_irreg_fourier, build_G_fourier


class IrrFourSamp(Simulation):
    """
    Represents a simuation of irregular Fourier samples simulation reconstruction
    """
    def __init__(self, K, M, tau, L = None, periodic_spectrum = True):
        """
        Parameters
        ----------
        K: int
            number of diracs
        M: int
            number of samples over the signal
        tau: float
            period
        L: int
            number of samples
        periodic_spectrum: bool
            boolean deciding whether using interpolation or not
        """
        super().__init__(K, tau, L)
        self.type = 'IFS'
        self.M = M
        self.periodic_spectrum = periodic_spectrum
        
    def setup(self, a = None):
        """
        Method that sets up the measurements. If none is given, they will automatically be generated
        
        Parameters
        ----------
            a: *(L x 2)* measurements with frequencies as first row and amplitudes as second row
        """
        if a is None:
            self.ak = np.sign(np.random.randn(self.K)) * (1 + (np.random.rand(self.K) - 0.5) / 1.)
            self.tk = self.dir_loc(self.periodic_spectrum, self.tau, self.K, self.M)
            # generate random frequencies to take samples
            self.omega_ell = np.pi * (np.random.rand(self.L) * (2 * self.M - 1) - self.M)
            # Fourier transform of the Diracs
            tk_grid, omega_grid = np.meshgrid(self.tk, self.omega_ell)
            self.Xomega_ell = np.dot(np.exp(-1j * omega_grid * tk_grid), self.ak)
            self.original = True
        else:
            self.Xomega_ell = a[:,1]
            self.omega_ell = a[:,0]
            self.original = False


    def add_noise(self, P = float('inf')):
        self.Xomega_ell, self.noise_lvl = super().add_noise(P, self.Xomega_ell, complex = True)

    def reconstruction(self, G = None, max_ini = 100, stop_cri = 'max_iter', interp_kernel = 'triangular'):
        """
        Main method of the class. It reconstructs the signal.

        Parameters
        ----------
        G: ndarray
            linear mapping
        max_ini: int
            maximum number of random initialisation
        stop_cri: str
            stopping criteria. Can either be *mse* or *max_iter*
        interp_kernel: str
            interpolation kernel mode. Can either be *dirichlet*, *triangular*, *cubic* or *keys*. If in periodic_spectrum, set to *dirichlet*
        """

        update_G = False
        # the update_G option has been removed
        self.interp_kernel = interp_kernel
        self.G = G


        if self.periodic_spectrum:
            print("spectrum periodic, correcting interpolation kernel")
            self.interp_kernel = 'dirichlet'
            #can be 1) dirichlet; 2) triangular; 3) cubic; 4) keys

        self.tk_ref, self.ak_recon, self.Xomega_Uniform_ref = \
            dirac_recon_irreg_fourier(self.Xomega_ell, self.K, self.tau, self.omega_ell, self.M,
                                      self.noise_lvl, self.G, update_G,
                                      max_ini, stop_cri, self.interp_kernel)
        if self.original:
            self.t_error = distance(self.tk_ref, self.tk)[0]    

    def show_results(self):
        """
        panda display of results

        Returns
        -------
            pandas.DataFrame
        """
        if self.original:
            d = {'original tk' : self.tk, 'reconstructed tk' : self.tk_ref,
            'original ak' : self.ak, 'reconstructed ak' : self.ak_recon}
        else:
            d = {'reconstructed tk' : self.tk_ref, 'reconstructed ak' : self.ak_recon}
        return pd.DataFrame(data = d)

    def save_results(self, simName):
        super().save_results(simName)

    def __str__(self):
        return super().__str__() + r"""
            M = {}
            periodic_spectrum: {}""".format(self.M, self.periodic_spectrum)

    def plot(self, save_fig = False, fig_format = 'png'):
        """
        Plotting method of the results

        Parameters
        ----------
        save_fig: bool
            boolean corresponding if the plot has to be saved or not
        fig_format: str
            the image format with which the file will be stored if save_fig is True
        """
        plotter.plot_four_samp(self.name, save_fig, fig_format)

    @staticmethod
    def dir_loc(periodic_spectrum, tau, K, M):
        """
        random dirac location generator
        """
        if periodic_spectrum:
            delta_t = 1. / M
            tk = np.sort(
                np.random.permutation(np.uint(np.floor(0.5 * tau / delta_t) * 2))[0:K] *
                delta_t) - np.floor(0.5 * tau / delta_t) * delta_t
        else:
            if K == 1:
                tk = np.random.rand()
            else:
                a = 4. / M
                uk = np.random.exponential(scale=1. / K, size=(K - 1, 1))
                tk = np.cumsum(a + (1. - K * a) * (1 - 0.1 * np.random.rand()) / uk.sum() * uk)
                tk = np.sort(np.hstack((np.random.rand() * tk[0] / 2., tk)) + (1 - tk[-1]) / 2.) * tau - 0.5 * tau
        return tk