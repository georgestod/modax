# %% Imports
import jax
from jax import random, numpy as jnp
from flax import optim
from modax.models import Deepmod
from modax.training import create_update
from modax.losses import loss_fn_pinn

from modax.data.burgers import burgers
from time import time

# Making dataset
x = jnp.linspace(-3, 4, 100)
t = jnp.linspace(0.5, 5.0, 20)

t_grid, x_grid = jnp.meshgrid(t, x, indexing="ij")
u = burgers(x_grid, t_grid, 0.1, 1.0)

X_train = jnp.concatenate([t_grid.reshape(-1, 1), x_grid.reshape(-1, 1)], axis=1)
y_train = u.reshape(-1, 1)

# Instantiating model and optimizers
model = Deepmod(features=[50, 50, 1])
key = random.PRNGKey(42)
params = model.init(key, X_train)
optimizer = optim.Adam(learning_rate=2e-3, beta1=0.99, beta2=0.99)
optimizer = optimizer.create(params)

# Compiling train step
update = create_update(loss_fn_pinn, model=model, x=X_train, y=y_train)
_ = update(optimizer)  # triggering compilation

# Running to convergence
max_epochs = 10001
t_start = time()
for i in jnp.arange(max_epochs):
    optimizer, loss = update(optimizer)
    if i % 1000 == 0:
        print(f"Loss step {i}: {loss}")
t_end = time()
print(t_end - t_start)
theta, coeffs = model.apply(optimizer.target, X_train)[2:]
print(coeffs * jnp.linalg.norm(theta, axis=0, keepdims=True).T)
