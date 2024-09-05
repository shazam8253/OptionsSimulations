### README: Options Pricing and Simulation Framework

This project provides a comprehensive framework for simulating and pricing options, leveraging Monte Carlo simulations, Brownian motion, Sobol sequences for variance reduction, and calculating option Greeks. The framework also includes a bullish calendar strategy using the generated simulation data.

---

### **Project Overview**

The options pricing and simulation framework allows you to:

- Simulate future asset price paths using **Geometric Brownian Motion** (GBM) based on the Black-Scholes model.
- Use **Sobol sequences** to reduce variance in Monte Carlo simulations and improve accuracy.
- Calculate the **Greeks** (Delta, Gamma, Theta, Vega, and Rho) for options to assess risk.
- Implement a **Bullish Calendar Spread Strategy**, where you can simultaneously buy a longer-term option and sell a shorter-term option.

### **Table of Contents**
1. [Key Components](#key-components)
2. [Installation](#installation)
3. [Simulation Process](#simulation-process)
4. [Option Pricing](#option-pricing)
5. [Greeks Calculation](#greeks-calculation)
6. [Running a Bullish Calendar Strategy](#bullish-calendar-strategy)
7. [Usage Example](#usage-example)

---

### **1. Key Components**

- **Geometric Brownian Motion (GBM)**: This is used to simulate the price of an asset over time. GBM follows the formula:

  \[
  S_{t + \Delta t} = S_t \times \exp \left( \left( r - \frac{1}{2} \sigma^2 \right) \Delta t + \sigma \sqrt{\Delta t} Z \right)
  \]
  
  Where:
  - \(S_t\) is the asset price at time \(t\),
  - \(r\) is the risk-free interest rate,
  - \(\sigma\) is the asset’s volatility,
  - \(\Delta t\) is the time step, and
  - \(Z\) is a random variable drawn from a standard normal distribution (Sobol sequences can be used to enhance accuracy).

- **Sobol Sequences**: These are low-discrepancy sequences used to improve the Monte Carlo simulation's efficiency by generating quasi-random numbers instead of purely random ones, leading to better convergence.

- **Greeks**: Metrics that quantify an option's sensitivity to various factors, including the underlying asset’s price (Delta), volatility (Vega), time decay (Theta), and more.

- **Bullish Calendar Spread**: This strategy involves buying a longer-term option and selling a shorter-term option on the same underlying asset at the same strike price, aiming to profit from time decay and an anticipated rise in volatility.

---

### **2. Installation**

1. Clone this repository:
   ```bash
   git clone https://github.com/yourrepo/options-pricing-simulation.git
   cd options-pricing-simulation
   ```

2. Install the required dependencies:
   ```bash
   pip install numpy scipy matplotlib sobol_seq
   ```

---

### **3. Simulation Process**

The Monte Carlo simulation runs a large number of simulated paths for the underlying asset using **Geometric Brownian Motion (GBM)** to predict future price movements. The steps include:

1. **Set Parameters**:
   - Initial asset price \(S_0\),
   - Risk-free rate \(r\),
   - Volatility \(\sigma\),
   - Time to expiration \(T\),
   - Number of paths \(N\).

2. **Simulate Paths**:
   - Use a discretized form of the Black-Scholes **stochastic differential equation (SDE)** to simulate future price movements:
   
     \[
     S_{t + \Delta t} = S_t \times \exp \left( \left( r - \frac{1}{2} \sigma^2 \right) \Delta t + \sigma \sqrt{\Delta t} Z \right)
     \]
     
     Here, \(Z\) is a random number from a standard normal distribution, and \(\Delta t\) is the time step.

3. **Calculate Payoffs**:
   - For **call options**, the payoff at expiration is:
     \[
     \text{Payoff} = \max(S_T - K, 0)
     \]
   - For **put options**, the payoff is:
     \[
     \text{Payoff} = \max(K - S_T, 0)
     \]
     where \(S_T\) is the asset price at expiration and \(K\) is the strike price.

4. **Discount to Present Value**:
   - The payoff is discounted using the risk-free rate:
     \[
     \text{Present Value of Payoff} = e^{-rT} \times \text{Payoff}
     \]

---

### **4. Option Pricing**

To price options using Monte Carlo simulations:

1. **Generate Price Paths**:
   - Use **Geometric Brownian Motion (GBM)** to simulate future prices of the underlying asset.

2. **Calculate Option Payoffs**:
   - For each simulated path, calculate the payoff for call and put options.

3. **Average the Payoffs**:
   - The option price (premium) is the discounted average of the payoffs across all simulated paths:
     \[
     \text{Option Price} = \frac{1}{N} \sum_{i=1}^{N} e^{-rT} \times \text{Payoff}(S_T^{(i)})
     \]
     where \(S_T^{(i)}\) is the simulated asset price for the \(i^{\text{th}}\) path.

4. **Sobol Sequence for Variance Reduction**:
   - Implement Sobol sequences to generate low-discrepancy random numbers, reducing variance and improving the accuracy of the option price estimates.

---

### **5. Greeks Calculation**

The Greeks can be calculated using **finite difference approximations** to quantify the sensitivity of the option price to various factors:

- **Delta (\(\Delta\))**: Measures the sensitivity of the option price to changes in the underlying asset's price:
  \[
  \Delta = \frac{C(S_0 + \epsilon) - C(S_0)}{\epsilon}
  \]
  
- **Gamma (\(\Gamma\))**: Measures the sensitivity of Delta to changes in the underlying price:
  \[
  \Gamma = \frac{\Delta(S_0 + \epsilon) - \Delta(S_0)}{\epsilon}
  \]

- **Theta (\(\Theta\))**: Measures the sensitivity of the option price to the passage of time:
  \[
  \Theta = \frac{C(T - \epsilon) - C(T)}{\epsilon}
  \]

- **Vega (\(\nu\))**: Measures the sensitivity of the option price to changes in volatility:
  \[
  \nu = \frac{C(\sigma + \epsilon) - C(\sigma)}{\epsilon}
  \]

- **Rho (\(\rho\))**: Measures the sensitivity of the option price to changes in the risk-free interest rate:
  \[
  \rho = \frac{C(r + \epsilon) - C(r)}{\epsilon}
  \]

---

### **6. Running a Bullish Calendar Spread Strategy**

In a **Bullish Calendar Spread Strategy**, you:

1. **Buy a Long-Dated Call Option** (longer time to expiration).
   - Strike price \(K\), time to maturity \(T_2\), and implied volatility \(\sigma\).

2. **Sell a Short-Dated Call Option** (same strike price but shorter time to expiration).
   - Same strike price \(K\), shorter time to maturity \(T_1\).

3. **Profit Expectation**:
   - The strategy profits from the time decay of the short-dated option, which decays faster, and an anticipated increase in the price of the underlying asset or implied volatility over time.

---

### **7. Usage Example**

Here's a basic example of running the Monte Carlo simulation, pricing options, and calculating the Greeks for a bullish calendar spread:

```python
from options_simulation import MonteCarloSimulator, GreeksCalculator, CalendarSpread

# Simulation parameters
S0 = 100      # Initial stock price
K = 105       # Strike price
r = 0.05      # Risk-free rate
sigma = 0.2   # Volatility
T1 = 0.25     # Time to expiration for short option (3 months)
T2 = 1.0      # Time to expiration for long option (1 year)
N = 10000     # Number of simulations

# Simulate prices and calculate option premiums
simulator = MonteCarloSimulator(S0, K, r, sigma, N)
short_call_price = simulator.simulate(T1)
long_call_price = simulator.simulate(T2)

# Run a bullish calendar spread strategy
calendar_spread = CalendarSpread(short_call_price, long_call_price)
profit = calendar_spread.calculate_profit()

# Calculate Greeks for long option
greeks_calculator = GreeksCalculator(S0, K, r, sigma, T2)
delta = greeks_calculator.delta()
gamma = greeks_calculator.gamma()
theta = greeks_calculator.theta()

print(f"Profit from Bullish Calendar Spread: {profit}")
print(f"Delta: {delta}, Gamma: {gamma}, Theta: {theta}")
```

---

### **Conclusion**

This framework provides a flexible and efficient way to simulate options pricing using Monte Carlo simulations, Sobol sequences, and risk management via option Greeks. The **Bullish Calendar Spread Strategy** adds a practical example of how these techniques can be applied in real-world trading

 strategies.

Feel free to explore and customize this framework for your specific use cases!
