import numpy as np
from scipy.stats import norm, qmc

# Parameters
S0 = 61097.5  # Current price of Bitcoin futures
K = 62000     # Strike price
T = 30 / 365  # Time to expiration in years
r = 0.01      # Risk-free rate (1%)
sigma = 0.71  # Volatility
num_simulations = 10000  # Number of Monte Carlo simulations
num_steps = 100  # Number of time steps in each simulation

# Initialize Sobol sequence generator
sobol = qmc.Sobol(d=num_steps)
samples = sobol.random(num_simulations)

# Transform Sobol samples to standard normal distribution
z = norm.ppf(samples)  # Inverse CDF (percent point function) to transform to standard normal

# Initialize price paths
price_paths = np.zeros((num_simulations, num_steps + 1))
price_paths[:, 0] = S0

# Simulate price paths using Sobol sequences
dt = T / num_steps  # time increment
sqrt_dt = np.sqrt(dt)

for t in range(1, num_steps + 1):
    price_paths[:, t] = price_paths[:, t-1] * np.exp((r - 0.5 * sigma ** 2) * dt + sigma * sqrt_dt * z[:, t-1])

# Calculate the average price for each path (Asian Option characteristic)
average_prices = np.mean(price_paths[:, -30:], axis=1)

# Calculate the payoff for a call option
payoffs = np.maximum(average_prices - K, 0)

# Discount the payoff back to present value
option_price = np.exp(-r * T) * np.mean(payoffs)

print(f"Estimated Asian Option Price using Sobol Sequences: {option_price:.2f} USD")
