# Papers notes

## How Amsterdam got fiat money - Quinn, Roberds

### Early public banks

__Trade coins__ (real > nominal value) lead to:
- liquid and stable
- transaction costs (protection and assay)

$\xRightarrow{}$ Merchant use __banks__ as intermediaries, bank failures $\xRightarrow{}$ municipal intermediaries $\xRightarrow{}$ bank of Amsterdam

### Before 1683

High withdrawal fee $\xRightarrow{}$ intermediaries would buy and sell balances

**Regulatory asymmetry**: state legal recognition of foreign coins and requirement for the Bank to accept them at the assigned value. _Fees_ to cover for minting and other expenses (1.5%)

### 1683 change

Bank customers received a negotiable receipt $\xRightarrow{}$ _quasi-fiat money_.

Effective negative capital.


## Maintaining Central-Bank Financial Stability under New-Style Central Banking

### Financial stability of a central bank

Traditional financial instability:

- Debt of the central bank is liquid $\xRightarrow{}$ no liquidation
- Central bank do not operate for profit $\xRightarrow{}$ no market value
- Most assets are liabilities of the shareholders (government)

What is _financial instability_ then? Insolvency if private agents refuse to hold its liabilities:

- Theory: _hyperinflation_, $p = \infin$
- Practice: arises or instituted a new Central Bank

### Dividends and independency

- A Central Bank is independent if it does not ask for (explosive)  dividends


__Mark-to-market__ dividends follow,

$$
d_{s^\prime}  = \left[ \underbrace{\theta \cdot c_s + (1 - \theta) \cdot e_{s^\prime}}_{\textit{coupon payment}} + \underbrace{(1-\delta) \cdot q_{s^\prime} - q_s}_{\textit{capital gain}} \right] \cdot B_s + \underbrace{n_{s, s^\prime}}_{seigniorage} - \underbrace{r_s \cdot V}_{\textit{interest}}
$$

__Nominal__ net-worth (more common in practice)

$$
d_{s^\prime}  = \left[ \underbrace{\theta \cdot c_s + (1 - \theta) \cdot e_{s^\prime}}_{\textit{coupon payment}} + \underbrace{(1-\delta) \cdot q_{s^\prime} - \frac{q_s}{1 + \pi_s}}_{\textit{capital gain with inflation}} \right] \cdot B_s - \underbrace{\frac{i_s \cdot V}{1+\pi_s}}_{\textit{interest}}
$$

### How can dividends be negative?

Paying interest on reserves and holding investment with interest-rate, default, and exchange risk.

Deriving dividends from exogenous and initial conditions yields,

$$
d_{s^\prime}  = n_{s, s^\prime} + r_s \cdot (q_0 B_0 - V_0) + \left[\theta \cdot c_s + (1 - \theta) \cdot e_{s^\prime} - \delta \cdot q_{s^\prime} - r_s \cdot q_s \right] \cdot B_s + (q_{s^\prime} - q_s) \cdot B_s
$$

hence negative interest rates can arise from,

- No bond repayment $\delta$ is impaired
- Real exchange rate appreciates $e_s^{\prime}$
- Capital losses $q_{s^\prime}$

Note that a closed bank, with only safe assets, and a one-period policy (i.e. $\delta = \theta = c_s = 1$) would have only $d_{s^{\prime}} = n_{s, s^{\prime}} \geq 0$.

### Deferred assets

Let $D$ be the deferred assets (net income realizations that the Treasury did not cover), yields $d^\prime = \max\left(y^\prime - D, 0\right)$. Note that a high $D \equiv$ recapitalization.

### ECB case

Looking at the balance sheet $\delta \approx 0.233$, $\theta \approx 0.461$, $c_S \approx 0.858$

### Conclusion

Financial strength $D$.

## Currency wars at the ZLB

### Model idea

At the ZLB and under assets scarcity:

- One country is in a liquidity trap, drags the other in the liquidity trap
- One monetary authority can influence the exchange rate within a bound to create a Current Account Surplus, hence exporting recension
- Negative feedback loop between the global recession and inflation

### Models effect
Government expansion...
- increase output increases demand for home goods and reduces demand for assets via taxation
- deteriorates foreign position
- equivalence of monetary and fiscal authority

