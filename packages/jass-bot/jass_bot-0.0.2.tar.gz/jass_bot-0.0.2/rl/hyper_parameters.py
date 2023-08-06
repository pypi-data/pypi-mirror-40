# ====================   Adjust this every time before conducting an experiment   ====================
experiment_name = "stich-higher-learning-rate"  # give a descriptive and memorable name here
# ====================================================================================================

rules_reward = False

if rules_reward:
    gamma = 0  # only care about immediate reward in the rule learning setting
else:
    gamma = 0.89  # care about rewards 9 steps into the future: 1 / (1 - gamma)

n_steps = 90  # = 10 games, determines the batch size
nminibatches = 10  # must be a divisor of n_steps!

learning_rate = 1e-3

total_timesteps = int(9e2)
