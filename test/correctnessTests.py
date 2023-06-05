import unittest
import numpy as np

import GreatestClearingVectorAlgorithm

class Test_GA_basic(unittest.TestCase):
    # Example 3.3 from Rogers and Veraart's article
    def setUp(self) -> None:
        L = np.array([[0, 2], [2.2, 0]])
        e = np.array([[1], [1]])
        alpha = 1 / 2
        beta = 1 / 2

        self.network = GreatestClearingVectorAlgorithm.Network(L, e, alpha, beta)

    def test_example3_3(self):
        res = GreatestClearingVectorAlgorithm.GA(self.network)
        expected = np.array([[2], [2.2]])
        self.assertSequenceEqual(expected.tolist(), res.tolist())


    #Example 3.3 where K_1 = 2.2 instead of K_1=2.
    def test_example3_3_v2(self):
        self.network.L[0][1] = 2.2
        self.network.L_bar[0] = 2.2

        res = GreatestClearingVectorAlgorithm.GA(self.network)
        expected = np.array([[2.2], [2.2]])
        self.assertSequenceEqual(expected.tolist(), res.tolist())


#Based on example in section 5.1 of Rogers and Veraart "Failure and Rescue in an Interbank Network"
class Test_GA_circular_network(unittest.TestCase):
    def setUp(self) -> None:
        self.gamma = 0.4
        self.epsilon = 1
        self.a = 2
        self.alpha = 1/2
        self.beta = 1/2
        self.n = 6

        L = np.zeros((self.n, self.n))
        L[0][1] = L[2][3] = L[4][5] = self.a
        L[1][2] = L[3][4] = L[5][0] = self.a + self.epsilon

        odd_e = self.gamma*(1-self.epsilon)
        even_e = self.gamma*(1+self.epsilon)
        e = np.array([odd_e, even_e, odd_e, even_e, odd_e, even_e])[:, np.newaxis]

        self.network = GreatestClearingVectorAlgorithm.Network(L, e, self.alpha, self.beta)


    def test_circular_network(self):
        res = GreatestClearingVectorAlgorithm.GA(self.network)

        #Since (13) from Rogers and Veraart does hold, the greatest clearing vector is \Lambda^(2) and all banks are insolvent
        odd_exp = ((self.alpha * self.gamma)/(1-self.beta**2))*((1-self.epsilon)+self.beta*(1+self.epsilon))
        even_exp = ((self.alpha*self.gamma)/(1-self.beta**2))*(self.beta*(1-self.epsilon)+(1+self.epsilon))
        expected = np.array([odd_exp, even_exp, odd_exp, even_exp, odd_exp, even_exp])[:, np.newaxis]

        self.assertEqual(expected.all(), res.all())
        self.assertEqual(self.n, len(self.network.insolvencySets[-1])) #All banks are insolvent

        # Insolvencylevel
        # The even banks are lvl-0 insolvent and the odd banks are lvl-1 insolvent.
        # Remember the indices is shifted by one because of 0-indexing.
        expected_insolv_lvls = [np.array([1,3,5]), np.array([0,2,4])]

        insolv_0 = np.setdiff1d(self.network.insolvencySets[1], self.network.insolvencySets[0])
        insolv_1 = np.setdiff1d(self.network.insolvencySets[2], self.network.insolvencySets[1])

        self.assertSequenceEqual(expected_insolv_lvls[0].tolist(), insolv_0.tolist())
        self.assertSequenceEqual(expected_insolv_lvls[1].tolist(), insolv_1.tolist())

class Test_randomized(unittest.TestCase):
    def test_random_network(self):
        L = np.array([[0, 0, 0.60141038],
                      [0, 0, 0],
                      [0, 0.61136804,0]])

        e = np.array([[0.47727664],
                      [0.63927659],
                      [0.32352602]])

        network = GreatestClearingVectorAlgorithm.Network(L, e, 1 / 2, 1 / 2)

        #Clearing vector
        res = GreatestClearingVectorAlgorithm.GA(network)

        expected_gcv = np.array([[0.47727664*(1/2)],
                                 [0],
                                 [0.47727664*(1/2) + 0.32352602*(1/2)]])

        self.assertEqual(expected_gcv.all(), res.all())

        #Insolvency level
        #We expect bank 0 to fail in the first round, and bank 2 to fail in the second round.
        expected_insolv_lvls = [np.array([0]), np.array([2])]

        insolv_0 = np.setdiff1d(network.insolvencySets[1], network.insolvencySets[0])
        insolv_1 = np.setdiff1d(network.insolvencySets[2], network.insolvencySets[1])

        self.assertSequenceEqual(expected_insolv_lvls[0].tolist(), insolv_0.tolist())
        self.assertSequenceEqual(expected_insolv_lvls[1].tolist(), insolv_1.tolist())





if __name__ == '__main__':
    unittest.main()



