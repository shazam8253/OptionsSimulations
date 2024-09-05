import numpy as np

# Parameters
S0 = 59720.0  # Current price of Bitcoin futures
K = 57211    # Strike price
T = 46 / 365  # Time to expiration in years
r = 0.01      # Risk-free rate (1%)
sigma = 0.7161  # Volatility
num_simulations = 10000  # Number of Monte Carlo simulations
num_steps = 100  # Number of time steps in each simulation (adjust for granularity)

# Monte Carlo simulation with optimizations
np.random.seed(42)
dt = T / num_steps  # time increment
sqrt_dt = np.sqrt(dt)

# Precompute the random normals for variance reduction
z = np.random.standard_normal((num_simulations // 2, num_steps))
z = np.concatenate((z, -z))  # Use antithetic variates for variance reduction

# Initialize price paths
price_paths = np.zeros((num_simulations, num_steps + 1))
price_paths[:, 0] = S0

# Simulate price paths
for t in range(1, num_steps + 1):
    price_paths[:, t] = price_paths[:, t-1] * np.exp((r - 0.5 * sigma ** 2) * dt + sigma * sqrt_dt * z[:, t-1])

# Focus on the last portion of the path, assuming averaging starts T-30m
# For simplicity, assume this corresponds to the last `n` steps
n_averaging_steps = 30  # Example: 30 time steps considered for averaging
average_prices = np.mean(price_paths[:, -n_averaging_steps:], axis=1)

# Calculate the payoff for a call option
payoffs = np.maximum(average_prices - K, 0)

# Discount the payoff back to present value
option_price = np.exp(-r * T) * np.mean(payoffs)

print(f"Estimated Asian Option Price: {option_price:.2f} USD")