import gin.tf
import numpy as np
import tensorflow as tf

from reaver.envs.base import Spec
from reaver.utils.tensorflow import SessionManager
from reaver.utils.typing import ModelBuilder, PolicyType
from reaver.agents.base import SyncRunningAgent, ActorCriticAgent, DEFAULTS


@gin.configurable('PPOAgent')
class ProximalPolicyOptimizationAgent(SyncRunningAgent, ActorCriticAgent):
    """
    PPO: clipped version of the Proximal Policy Optimization algorithm

    Here "clipped" refers to how trusted policy region is enforced.
    While orig. PPO relied on KL divergence, this clips the pi / pi_old ratio.

    See article for more details: https://arxiv.org/abs/1707.06347

    PPO specific parameters:

    :param n_updates: number of minibatch optimization steps
    :param minibatch_sz: size of the randomly sampled minibatch
    :param clip_ratio: max interval for pi / pi_old: [1-clip_ratio, 1+clip_ratio]
    """
    def __init__(
        self,
        obs_spec: Spec,
        act_spec: Spec,
        model_fn: ModelBuilder=None,
        policy_cls: PolicyType=None,
        sess_mgr: SessionManager=None,
        n_envs=4,
        n_updates=3,
        minibatch_sz=128,
        clip_ratio=0.2,
        learning_rate=DEFAULTS['learning_rate'],
        value_coef=DEFAULTS['value_coef'],
        entropy_coef=DEFAULTS['entropy_coef'],
        traj_len=DEFAULTS['traj_len'],
        batch_sz=DEFAULTS['batch_sz'],
        discount=DEFAULTS['discount'],
        gae_lambda=DEFAULTS['gae_lambda'],
        clip_rewards=DEFAULTS['clip_rewards'],
        clip_grads_norm=DEFAULTS['clip_grads_norm'],
        normalize_advantages=DEFAULTS['normalize_advantages'],
    ):
        self.n_updates = n_updates
        self.minibatch_sz = minibatch_sz
        self.clip_ratio = clip_ratio

        kwargs = {k: v for k, v in locals().items() if k in DEFAULTS and DEFAULTS[k] != v}

        SyncRunningAgent.__init__(self, n_envs)
        ActorCriticAgent.__init__(self, obs_spec, act_spec, sess_mgr=sess_mgr, **kwargs)

        self.start_step = self.start_step // self.n_updates

    def minimize(self, advantages, returns):
        inputs = [a.reshape(-1, *a.shape[2:]) for a in self.obs + self.acts]
        tf_inputs = self.model.inputs + self.policy.inputs
        logli_old = self.sess_mgr.run(self.policy.logli, tf_inputs, inputs)

        inputs += [advantages.flatten(), returns.flatten(), logli_old]
        tf_inputs += self.loss_inputs

        loss_terms = grads_norm = None
        # TODO: rewrite this with persistent tensors to load data only once into the graph
        for _ in range(self.n_updates):
            idx = np.random.permutation(self.batch_sz * self.traj_len)[:self.minibatch_sz]
            minibatch = [inpt[idx] for inpt in inputs]
            loss_terms, grads_norm, *_ = self.sess_mgr.run(self.minimize_ops, tf_inputs, minibatch)

        return loss_terms, grads_norm

    def loss_fn(self):
        adv = tf.placeholder(tf.float32, [None], name="advantages")
        returns = tf.placeholder(tf.float32, [None], name="returns")
        logli_old = tf.placeholder(tf.float32, [None], name="logli_old")

        ratio = tf.exp(self.policy.logli - logli_old)
        clipped_ratio = tf.clip_by_value(ratio, 1-self.clip_ratio, 1+self.clip_ratio)

        policy_loss = -tf.reduce_mean(tf.minimum(adv * ratio, adv * clipped_ratio))
        # TODO clip value loss
        value_loss = tf.reduce_mean((self.value - returns)**2) * self.value_coef
        entropy_loss = tf.reduce_mean(self.policy.entropy) * self.entropy_coef
        # we want to reduce policy and value errors, and maximize entropy
        # but since optimizer is minimizing the signs are opposite
        full_loss = policy_loss + value_loss - entropy_loss

        return full_loss, [policy_loss, value_loss, entropy_loss], [adv, returns, logli_old]
