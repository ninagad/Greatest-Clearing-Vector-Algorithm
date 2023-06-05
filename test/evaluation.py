import unittest
import numpy as np
from pyprobs import Probability as pr
import os

from src.GreatestClearingVectorAlgorithm import GA

#from GreatestClearingVectorAlgorithm import GA
#from ..GreatestClearingVectorAlgorithm import Network


def networkGenerator(no_of_banks, prob_of_liability, external_asset_coefficient, alpha, beta):
    L = np.zeros((no_of_banks, no_of_banks))
    e = np.empty((no_of_banks, 1))

    rng = np.random.default_rng()

    for i in range(no_of_banks):
        e[i] = external_asset_coefficient * rng.uniform()  # Uniform in the interval [0,1]

        for j in range(no_of_banks):
            haveLiability = pr.prob(prob_of_liability)
            if haveLiability & (i != j):
                L[i][j] = rng.uniform() #Uniformly distributed in [0,1]

    return Network(L, e, alpha, beta)



class Test_single_test_with_variable_p(unittest.TestCase):
    def setUp(self) -> None:
        n: int = 1000
        t: float = 20
        p_low: float = 0.01
        p_high: float = 0.1
        no_networks: int = 10
        alpha = 1 / 2
        beta = 1 / 2
        stepsize: float = (p_high - p_low) / (no_networks-1)

        self.networks: list[Network] = []
        self.ps: np.array = np.arange(p_low, p_high + stepsize, stepsize)

        for _p in self.ps:
            network = networkGenerator(n, _p, t, alpha, beta)
            self.networks.append(network)

            _ = GA(network)

    
    def test_p_insolvency_level(self):
        insolvency_levels: list[list[int]] = []
        for network in self.networks:
            il = network.insolvencyLevels
            insolvency_levels.append(il)

        xy = np.vstack((self.ps, np.array(insolvency_levels)))
        np.save(os.path.join('results', "insolvency-levels-test.npy"), xy)


# Same setup as above but averaging over a number of datapoints for each p.
class Test_multiple_tests_with_variable_p(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        n: int = 1000
        t: float = 20
        p_low: float = 0.01
        p_high: float = 0.1
        no_networks: int = 100
        alpha: float = 1 / 2
        beta: float = 1 / 2
        stepsize: float = (p_high - p_low) / (no_networks-1)
        cls.no_points_pr_p = 10

        cls.noInsolventBanks: list[list[int]] = []
        cls.greatestClearingVectors: list[list[np.array]] = []
        cls.ps: np.array = np.arange(p_low, p_high + stepsize, stepsize)

        for i in range(cls.no_points_pr_p):
            print(i)
            noInsolvent_i = []
            gcv_i = []

            for _p in cls.ps:
                network = networkGenerator(n, _p, t, alpha, beta)
                gcv = GA(network)
                gcv_i.append(gcv)
                no_insolvent = len(network.insolvencySets[-1])
                noInsolvent_i.append(no_insolvent)

            cls.noInsolventBanks.append(noInsolvent_i)
            cls.greatestClearingVectors.append(gcv_i)

    def test_p_no_insolvent(self):
        xy = np.vstack((self.ps, np.array(self.noInsolventBanks)))
        np.save(os.path.join('results', "p-no-of-insolvent-test.npy"), xy)

    def test_p_clearing_vectors(self):
        size_of_clearing_vectors: list[list[float]] = []

        for i in range(self.no_points_pr_p):
            scv: list[float] = []

            for gcv in self.greatestClearingVectors[i]:
                size = np.sum(gcv)
                scv.append(size)

            size_of_clearing_vectors.append(scv)

        xy = np.vstack((self.ps, np.array(size_of_clearing_vectors)))
        np.save(os.path.join('results', "p-size-of-gcv-test.npy"), xy)


class Test_multiple_tests_with_variable_t(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        n: int = 1000
        t_low: float = 1
        t_high: float = 100 
        p: float = 0.05 #In the middle of the interval for p [0.01,0.1]
        no_networks: int = 100
        alpha: float = 1 / 2
        beta: float = 1 / 2
        stepsize: float = (t_high - t_low) / (no_networks-1)
        cls.no_of_points_pr_t = 10

        cls.noInsolventBanks: list[list[int]] = []
        cls.greatestClearingVectors: list[list[np.array]] = []
        cls.ts: np.array = np.arange(t_low, t_high + stepsize, stepsize)

        for i in range(cls.no_of_points_pr_t):
            print(i)
            noInsolvent_i = []
            gcv_i = []

            for _t in cls.ts:
                network = networkGenerator(n, p, _t, alpha, beta)
                gcv = GA(network)
                gcv_i.append(gcv)
                no_insolvent = len(network.insolvencySets[-1])
                noInsolvent_i.append(no_insolvent)

            cls.noInsolventBanks.append(noInsolvent_i)
            cls.greatestClearingVectors.append(gcv_i)

    def test_t_no_insolvent(self):
        xy = np.vstack((self.ts, np.array(self.noInsolventBanks)))
        np.save(os.path.join('results', "t-no-of-insolvent-multiple-test.npy"), xy)
    

if __name__ == '__main__':
    # unittest.main()
    test = Test_single_test_with_variable_p()
    test.test_p_insolvency_level()



