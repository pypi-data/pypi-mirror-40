# ###############################################################
# simulation.py
# ==============
# Author: Leo Serena [leo.serena@epfl.ch]
# ###############################################################


from abc import ABC, abstractmethod
import numpy as np
from scipy import linalg
import os
import pickle

class   Simulation(ABC):
    """
    abstract class defining a reconstruction simulation
    """
    def __init__(self, K, tau, L):
        """
        Parameters
        ----------
        K: int
            number of needed diracs to reconstruct
        tau: float
            period
        L: int
            number of samples
        """
        super().__init__()
        self.K = K
        self.tau = tau
        self.L = L

    @abstractmethod
    def setup(self):
        """
        abstract method for setup the reconstruction
        """
        pass

    @abstractmethod
    def add_noise(self, P, noiseless, complex = False):
        """
        Method for addition of noise to signal

        Parameters
        ----------
        P: float
            SNR ratio in db
        noiseless: ndarray
            signal without noise
        complex: bool
            True if needs a imaginary noise addition, for Fourier domain samples
        
        Returns
        -------
        withNoise: ndarray
            the signal with noise
        noise_level: float
            the noise_level
        """
        self.P = P
        if complex:
            noise = np.random.randn(self.L) + 1j*np.random.randn(self.L)
        else:
            noise = np.random.randn(self.L)
        noise = noise / linalg.norm(noise) * linalg.norm(noiseless) * 10 ** (-P / 20.)
        withNoise = noiseless + noise    

        noise_level = np.max([10e-14, linalg.norm(noise)])

        return withNoise, noise_level
    
    @abstractmethod
    def reconstruction(self):
        """
        abstract method for reconstruction
        """
        pass
    
    @abstractmethod
    def show_results(self):
        """
        shows the results fof the reconstructed data
        """
        pass
    
    @abstractmethod
    def save_results(self, simName):
        """
        save the results to the *results* file

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

    @abstractmethod
    def __str__(self):
        return r"""representation of the simulation:
            K = {},
            tau = {},
            number of samples L = {},""".format(self.K,
                                        self.tau,
                                        self.L)

    @abstractmethod
    def plot(self):
        """
        abstract plotting method
        """
        pass