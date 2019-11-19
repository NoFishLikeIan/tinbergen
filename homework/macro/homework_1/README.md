# Heterogeneity in Risk Aversion - Simulation

This repository contains the code for the Heterogeneity in Risk Aversion problem. In general it implements a set of constraints and computes the consumption levels based on two models of risk adversion. 

## Init.py

To start working with it just install the required packages with the usual

```bash
pip install -r requirements.txt
```

and then you can run

```bash
python solve.py
```

to output the numerical results in the `out_data/` folder. Similarly `plot.py` and `arrow_securities.py` compute the standard plots and the Arrow securities.

## Loss
There is an initial implementation for an implementation of a loss function based optimization, that could be more robust to wrong initial guesses.