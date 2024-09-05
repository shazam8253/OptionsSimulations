import numpy as np


# Function to run Monte Carlo simulation and calculate option price and Greeks
def simulate_option_price_and_greeks(S0, K, T, r, sigma, num_simulations=10000, num_steps=100, epsilon=0.01):
    # Monte Carlo simulation setup
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
        payoffs = np.maximum(average_prices - K, 0)
        option_price = np.exp(-r * T) * np.mean(payoffs)
        return option_price

    # Base case: Calculate the option price
    price_paths = simulate_price_paths(S0, r, sigma, num_simulations, num_steps)
    option_price = calculate_option_price(price_paths, K, r, T)

    # Delta: Sensitivity to underlying asset price
    price_paths_up = simulate_price_paths(S0 + epsilon, r, sigma, num_simulations, num_steps)
    price_paths_down = simulate_price_paths(S0 - epsilon, r, sigma, num_simulations, num_steps)
    option_price_up = calculate_option_price(price_paths_up, K, r, T)
    option_price_down = calculate_option_price(price_paths_down, K, r, T)
    delta = (option_price_up - option_price_down) / (2 * epsilon)

    # Gamma: Sensitivity of Delta
    gamma = (option_price_up - 2 * option_price + option_price_down) / (epsilon ** 2)

    # Vega: Sensitivity to volatility
    price_paths_sigma_up = simulate_price_paths(S0, r, sigma + epsilon, num_simulations, num_steps)
    option_price_sigma_up = calculate_option_price(price_paths_sigma_up, K, r, T)
    vega = (option_price_sigma_up - option_price) / epsilon

    # Theta: Sensitivity to time
    T_epsilon = (T - epsilon/365)
    price_paths_theta = simulate_price_paths(S0, r, sigma, num_simulations, num_steps)
    option_price_theta = calculate_option_price(price_paths_theta, K, r, T_epsilon)
    theta = (option_price_theta - option_price) / epsilon

    # Rho: Sensitivity to interest rate
    price_paths_r_up = simulate_price_paths(S0, r + epsilon, sigma, num_simulations, num_steps)
    option_price_r_up = calculate_option_price(price_paths_r_up, K, r + epsilon, T)
    rho = (option_price_r_up - option_price) / epsilon

    # Return the calculated values
    return {
        "option_price": option_price,
        "delta": delta,
        "gamma": gamma,
        "vega": vega,
        "theta": theta,
        "rho": rho
    }

# Base parameters
S0 = 59720.0  # Current price of Bitcoin futures
K = 10000    # Strike price
T = 46 / 365  # Time to expiration in years
r = 0.01      # Risk-free rate (1%)
sigma = 0.7161  # Volatility

# Simulate the base case
results_base = simulate_option_price_and_greeks(S0, K, T, r, sigma)

# Sensitivity analysis: Higher Delta scenario
S0_higher_delta = S0 * 1.05  # 5% increase in underlying asset price
results_higher_delta = simulate_option_price_and_greeks(S0_higher_delta, K, T, r, sigma)

# Sensitivity analysis: Higher Vega scenario
sigma_higher_vega = sigma * 1.2  # 20% increase in volatility
results_higher_vega = simulate_option_price_and_greeks(S0, K, T, r, sigma_higher_vega)

# Print results
print("Base Case Results:")
print(f"Option Price: {results_base['option_price']:.2f} USD")
print(f"Delta: {results_base['delta']:.4f}")
print(f"Gamma: {results_base['gamma']:.4f}")
print(f"Vega: {results_base['vega']:.4f}")
print(f"Theta: {results_base['theta']:.4f}")
print(f"Rho: {results_base['rho']:.4f}\n")

print("Higher Delta Scenario Results:")
print(f"Option Price: {results_higher_delta['option_price']:.2f} USD")
print(f"Delta: {results_higher_delta['delta']:.4f}")
print(f"Gamma: {results_higher_delta['gamma']:.4f}")
print(f"Vega: {results_higher_delta['vega']:.4f}")
print(f"Theta: {results_higher_delta['theta']:.4f}")
print(f"Rho: {results_higher_delta['rho']:.4f}\n")

print("Higher Vega Scenario Results:")
print(f"Option Price: {results_higher_vega['option_price']:.2f} USD")
print(f"Delta: {results_higher_vega['delta']:.4f}")
print(f"Gamma: {results_higher_vega['gamma']:.4f}")
print(f"Vega: {results_higher_vega['vega']:.4f}")
print(f"Theta: {results_higher_vega['theta']:.4f}")
print(f"Rho: {results_higher_vega['rho']:.4f}")
