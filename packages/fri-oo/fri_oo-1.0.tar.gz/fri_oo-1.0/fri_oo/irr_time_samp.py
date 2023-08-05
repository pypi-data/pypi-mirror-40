# ###############################################################
# irr_time_samp.py
# ==============
# Author: Leo Serena [leo.serena@epfl.ch]
# ###############################################################

import numpy as np
import pandas as pd
from scipy import linalg
import pickle

# for package ref
# ===============
from . simulation import Simulation
from . alg_tools_1d import dirac_recon_time, periodicSinc, distance
from . import plotter

# for html automodule
# ===================
# from fri_oo.simulation import Simulation
# from fri_oo.alg_tools_1d import dirac_recon_time, periodicSinc, distance
# from fri_oo import plotter

class IrrTimeSamp(Simulation):
    """
    simuation of irregular time samples simulation reconstruction
    """
    def __init__(self, K, tau, B, L):
        """
        Parameters
        ----------
        K: int
            number of diracs
        tau: float
            period
        B: float
            bandwidth
        L: int
            number of samples
        """
        super().__init__(K, tau, L)
        self.type = 'ITS'
        self.B = B
        self.Tmax = tau/L
        self.M = np.floor(B * tau / 2)

        if(self.M < K):
            self.M = K
            self.L = 2 * K + 1
            self.B = (2. * self.M + 1) / tau

        
    def __str__(self):
        return super().__str__() + r"""
            B = {}""".format(self.B)
    
    
    def setup(self, G = None, a = None):
        """
        Setup the measurements a and the linear matrix G. If one of them isn't given, 
        function sets up random measurements a according to a Poisson distribution

        parameters
        ----------
        G: numpy.ndarray
            linear mapping between the sampled signal and the measurements, (*L* x *M*) matrix
        a: numpy.ndarray
            (*L* x *2*) matrix. First column are the time and second the amplitude of the measurements.
        """
        if G is None or a is None:
            self.t_samp = self.create_samples(self.L, self.tau, self.Tmax)
            self.ak = np.sign(np.random.randn(self.K)) * (1 + (np.random.rand(self.K) - 0.5) / 1.)
            self.tk = self.dir_loc(self.K, self.tau, self.L)
            self.G, self.yl, self.x_hat_noiseless = self.fourier_coeff(self.ak, self.tk, self.B, self.tau, self.t_samp)
            self.original = True
        else:
            self.G = G
            self.t_samp = a[:,0]
            self.yl = a[:,1]
            self.original = False
    
    def add_noise(self, P = float('inf')):
        self.yl, self.noise_lvl = super().add_noise(P, self.yl)
    
    def reconstruction(self, stop_cri = 'max_iter', max_ini = 100):
        """
        Main method of the clas. This reconstructs the signal according to the algorithm.

        Parameters
        ----------
        stop_cri: str
            the stopping criteria of the algorithm, can either be *mse* or *max_iter*
        max_ini: int
            maximum number of random initialisations
        """
        xhat_recon, min_error, c_opt, a  = dirac_recon_time(self.G,
                                                            self.yl,
                                                            self.K,
                                                            self.noise_lvl,
                                                            max_ini,
                                                            stop_cri)
        # reconstruction of Diracs locations tk
        z = np.roots(c_opt)
        z = z / np.abs(z)
        self.tk_recon = np.real(self.tau * 1j / (2 * np.pi) * np.log(z))
        self.tk_recon = np.sort(self.tk_recon - np.floor(self.tk_recon / self.tau) * self.tau)
        
        # reconstruction of Diracs amplitudes ak
        Phi_recon = periodicSinc(np.pi * self.B * (np.reshape(self.t_samp, (-1, 1), order='F') -
                                              np.reshape(self.tk_recon, (1, -1), order='F')),
                                 self.B * self.tau)
        self.ak_recon = np.real(linalg.lstsq(Phi_recon, self.yl)[0])
        
        if self.original:
            # location estimation error
            self.t_error = distance(self.tk_recon, self.tk)[0]
        
    def show_results(self):
        """
        Prints the some results after performing FRI reconstruction

        Returns
        -------
            pandas.DataFrame
        """

        if self.original:
            d = {'original tk' : self.tk, 'reconstructed tk' : self.tk_recon,
            'original ak' : self.ak, 'reconstructed ak' : self.ak_recon}
        else:
            d = {'reconstructed tk' : self.tk_recon, 'reconstructed ak' : self.ak_recon}
        return pd.DataFrame(data = d)

    def save_results(self, simName):
        super().save_results(simName)

    def plot(self, save_fig = False, fig_format = 'png'):
        """Plotting method of the results

        :parameters:
            :save_fig: boolean corresponding if the plot has to be saved or not
            :fig_format: the image format with which the file will be stored if save_fig is True"""
        plotter.plot_irreg_samp(self.name, save_fig, fig_format)

    # static methods

    @staticmethod
    def create_samples(L, tau, Tmax):
        """
        Creates the L time samples of x(t)
        """
        t_samp = np.arange(0, L, dtype=float) * Tmax
        t_samp += np.sign(np.random.randn(L)) * np.random.rand(L) * Tmax / 2
        t_samp -= np.floor(t_samp / tau) * tau
        return t_samp

    @staticmethod
    def dir_loc(K, tau, L):
        """
        Diracs locations generator
        """
        if K == 1:
            tk = np.random.rand()
        else:
            a = 4. / L
            uk = np.random.exponential(scale=1. / K, size=(K - 1, 1))
            tk = np.cumsum(a + (1. - K * a) * (1 - 0.1 * np.random.rand()) / uk.sum() * uk)
            tk = np.sort(np.hstack((np.random.rand() * tk[0] / 2., tk)) + (1 - tk[-1]) / 2.) * tau
        return tk

    @staticmethod
    def fourier_coeff(ak, tk, B, tau, t_samp):
        """
        Computation of noiseless Fourier series coefficients
        """
        tk_grid, m_grid_gt = np.meshgrid(tk, np.arange(-np.floor(B * tau / 2.), 1 + np.floor(B * tau / 2.)))
        x_hat_noiseless = 1. / tau * np.dot(np.exp(-2j * np.pi / tau * m_grid_gt * tk_grid), ak)

        m_grid, t_samp_grid = np.meshgrid(np.arange(-np.floor(B * tau / 2.), 1 + np.floor(B * tau / 2.)), t_samp)

        G = 1. / B * np.exp(2j * np.pi / tau * m_grid * t_samp_grid)
        y_ell_noiseless = np.real(np.dot(G, x_hat_noiseless))

        return G, y_ell_noiseless, x_hat_noiseless