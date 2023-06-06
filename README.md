# Greatest-Clearing-Vector-Algorithm
Implementation and evaluation of the Greatest Clearing Vector Algorithm by Rogers, L. C. G., and L. A. M. Veraart in “Failure and Rescue in an Interbank Network."

This repository is a part of our bachelor's thesis in Computer Science at Aarhus University written by Nina Gad Lauridsen and Pi Gregersen Bohlbro.  


## Requirements installation

Installing requirements using the package manager [pip](https://pip.pypa.io/en/stable/).

```bash
pip install -r requirements.txt
```

## How to reproduce the results

To reproduce the results from the evaluation tests
- Clone the repository
- Install the dependencies (see above)
- Run `python -m unittest test.evaluation`
- Run `python plots.py` in test directory
- See resulting graphs in `test/results directory`


## General description

We have implemented the greatest clearing vector algorithm and have a few tests to test correctness of our implementation. 

Moreover, we have developed a simple probabilistic model of a financial network. In this model we have parameter $n$, which denotes the number of banks in the network. Parameter $p$ denotes the probability that bank $i$ owes bank $j$ money. If a liability exists the size of it is uniformly distributed in the interval [0,1]. The parameter $t$ is the external asset coefficient. For each bank $i$ the amount of external assets is uniformly distributed in [0,t]. As in Rogers and Veraart's model we use $\alpha$ to denote the default cost for the external assets and $\beta$ to denote the default cost for the internal assets. We use this model to create a network generator that can create random networks based on the five parameters $n$, $p$, $t$, $\alpha$ and $\beta$. This enables us to make tests based on a large amount of networks which reduces the effect of outliers. These tests investigate how the greatest clearing vector algorithm behave. 

**Test description**

In all tests, we have used $n=1000$ and $\alpha =\beta = \frac{1}{2}$. We have three tests with $p$ as a variable and one test where $t$ varies. 

In the first test suite, $p$ varies in the interval $[0.01, 0.1]$ with $t=20$. We consider 100 evenly distributed values of $p$ and for each value of $p$, we generate 10 networks with our network generator and run the greatest clearing vector algorithm for each. There are two tests related to this setup, namely a test that saves the number of insolvent banks to disk and a test that saves the sum of each greatest clearing vector (i.e. the systemic liquidity) to disk. These two tests are visualised with two plots. The first plot shows the number of defaults as a function of $p$. For each value of $p$ the value on the y-axis is the average of the number of defaults in the 10 networks. The second plot shows the systemic liquidity as a function of $p$. For each value of $p$ the value on the y-axis is the average of the sum of payments in the 10 networks. 

In the second test setup the external asset coefficient $t$ varies in the interval $[0, 100]$ with $p=0.05$. The setup of the networks is the same and the test saves the number of insolvent banks as a function of $t$.

In the last test we want to study the distribution of the insolvency levels as it is defined by Rogers and Veraart. In this setup $p$ varies in the interval $[0.01, 0.1]$ with $t=20$. We consider 10 evenly distributed values of $p$ and for each value we generate a network with our network generator and run the greatest clearing vector algorithm for each. We save how many \emph{level-}$\mu$ insolvent banks there are in each network for all levels $\mu$. The graph have a box plot for each network which show how the insolvent banks are distributed across the insolvency levels. 


## Our results
These are the results we produced and we invite you to try to reproduce these results. 

<p align="center">
  <img src="https://github.com/ninagad/Greatest-Clearing-Vector-Algorithm/blob/main/test/results/p-no-of-insolvent-plot.png" width ="700">
</p>

<p align="center">
  <img src="https://github.com/ninagad/Greatest-Clearing-Vector-Algorithm/blob/main/test/results/p-size-of-gcv-plot.png" width="700">
</p>
  
<p align="center">
  <img src="https://github.com/ninagad/Greatest-Clearing-Vector-Algorithm/blob/main/test/results/p-insolvency-levels-boxplot.png" width="700">
</p>
  
<p align="center">
  <img src="https://github.com/ninagad/Greatest-Clearing-Vector-Algorithm/blob/main/test/results/t-no-of-insolvent-plot.png" width="700">
</p>
  

### Disclaimer

**As the authors of this repository, we are not liable for any use of the code nor the correctness of the code in this repository.** 
