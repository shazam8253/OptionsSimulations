import numpy as np

# Parameters
S0 = 59907.5  # Current price of Bitcoin futures
K = 48000    # Strike price
T = 46 / 365  # Time to expiration in years
r = 0.01      # Risk-free rate (1%)
sigma = 0.71  # Volatility
num_simulations = 10000  # Number of Monte Carlo simulations
num_steps = 100  # Number of time steps in each simulation

# Monte Carlo simulation with optimizations
np.random.seed(42)
dt = T / num_steps
sqrt_dt = np.sqrt(dt)

def simulate_price_paths(S0, r, sigma, num_simulations, num_steps):
    z = np.random.standard_normal((num_simulations // 2, num_steps))
    z = np.concatenate((z, -z))  # Antithetic variates
    price_paths = np.zeros((num_simulations, num_steps + 1))
    price_paths[:, 0] = S0
    for t in range(1, num_steps + 1):
        price_paths[:, t] = price_paths[:, t-1] * np.exp((r - 0.5 * sigma ** 2) * dt + sigma * sqrt_dt * z[:, t-1])
    return price_paths

def calculate_option_price(price_paths, K, r, T, n_averaging_steps=30):
    average_prices = np.mean(price_paths[:, -n_averaging_steps:], axis=1)
    
    # For a put option, use the following payoff calculation
    payoffs = np.maximum(K - average_prices, 0)
    
    option_price = np.exp(-r * T) * np.mean(payoffs)
    return option_price

# Calculate the option price for a put option
price_paths = simulate_price_paths(S0, r, sigma, num_simulations, num_steps)
option_price = calculate_option_price(price_paths, K, r, T)

print(f"Estimated Asian Put Option Price: {option_price:.2f} USD")
