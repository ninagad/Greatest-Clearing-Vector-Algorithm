import scipy
import numpy as np

class Network:
    def __init__(self, L, e, alpha, beta):
        self.L: np.array() = L
        self.e: np.array() = e
        self.alpha: float = alpha
        self.beta: float = beta

        self.L_bar: np.array() = L.sum(axis=1)[:, np.newaxis]
        self.Pi: np.array() = np.divide(L, self.L_bar, out=np.zeros(L.shape), where=(self.L_bar > 0))

        self.insolvencyLevels: list[int] = [] #Contains the number of level-i insolvent banks at index i.
        self.insolvencySets: list[np.array()] = [np.array([])]  # The first insolvency set I_{-1} is empty

        self.greatestClearingVector: np.array() = np.zeros_like(e)


def GA(network):
    Pi = network.Pi
    insolvencySets = network.insolvencySets

    Lambda = np.copy(network.L_bar)
    n = network.L.shape[0]

    for mu in range(n+1):
        income = (Lambda.T @ Pi).sum(axis=0)[:, np.newaxis] + network.e
        v = income - network.L_bar

        insolvencySet = np.where(v < 0)[0] #Indices of insolvent banks
        insolvencySets.append(insolvencySet)

        #Compare previous insolvency set with current set and terminate if they are equal.
        #We compare the size of the insolvency sets since the truth value
        # is the same because the set of insolvent banks are monotonely increasing.
        if insolvencySets[mu].size == insolvencySets[mu+1].size:
            network.greatestClearingVector = Lambda
            return Lambda

        #Add the level-mu insolvent banks to insolvencylevel
        # Take the elements in insolvency set mu that are not in insolvency set mu-1 and count the number of elements.
        lvl_mu_insolvent = len(np.setdiff1d(insolvencySet, insolvencySets[-2]))
        network.insolvencyLevels.append(lvl_mu_insolvent)

        #Otherwise, compute new \Lambda
        Lambda = np.copy(network.L_bar)

        #The system of linear equations to solve for the insolvent banks.
        no_insolvent = insolvencySet.size
        #Construct the coefficient matrix a as a diagonal matrix with 1's and subtract
        #the rows and columns of the insolvent banks from Pi multiplied by beta
        beta_pi = network.beta * Pi[np.ix_(insolvencySet, insolvencySet)]
        a = np.diag(np.ones(no_insolvent)) - beta_pi.T

        e_insolvent = network.e[insolvencySet,:] #External assets for the insolvent banks
        #The nominal liabilities from solvent banks to insolvent banks
        #Keep the rows from solvent banks and the columns from insolvent banks
        L_solv_to_insolv = np.delete(network.L, insolvencySet, axis=0)[:, insolvencySet]
        income_insolv = L_solv_to_insolv.sum(axis=0)[:, np.newaxis]

        b = network.alpha*e_insolvent + network.beta*income_insolv

        x = scipy.linalg.solve(a,b)

        # Overwrite all the insolvent banks with the clearing payment
        np.put(Lambda, insolvencySet, x)

    raise Exception('The algorithm should converge in at most n iterations')


