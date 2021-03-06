import jax
from jax import numpy as jnp


def mse(y_pred, y):
    """Helper fuction to calculate MSE.
    """

    def squared_error(y, y_pred):
        return jnp.inner(y - y_pred, y - y_pred) / 2.0

    return jnp.mean(jax.vmap(squared_error)(y, y_pred), axis=0)


def loss_fn_mse(params, model, x, y):
    """ first argument should always be params!
    """
    prediction = model.apply(params, x)[0]
    loss = mse(prediction, y)

    return loss


def loss_fn_pinn(params, model, x, y):
    prediction, dt, theta, coeffs = model.apply(params, x)
    loss = mse(prediction, y) + mse(dt.squeeze(), (theta @ coeffs).squeeze())
    return loss
