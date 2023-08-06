import numpy as np
import pymc3 as pm
from sklearn.metrics import accuracy_score
import theano
import theano.tensor as T

from pymc3_models.exc import PyMC3ModelsError
from pymc3_models.models import BayesianModel


class HierarchicalLogisticRegression(BayesianModel):
    """
    Custom Hierachical Logistic Regression built using PyMC3.
    """

    def __init__(self):
        super(HierarchicalLogisticRegression, self).__init__()
        self.num_cats = None

    def create_model(self):
        """
        Creates and returns the PyMC3 model.

        Note: The size of the shared variables must match the size of the training data.
        Otherwise, setting the shared variables later will raise an error.
        See http://docs.pymc.io/advanced_theano.html

        Returns
        -------
        the PyMC3 model
        """
        model_input = theano.shared(np.zeros([self.num_training_samples, self.num_pred]))

        model_output = theano.shared(np.zeros(self.num_training_samples, dtype='int'))

        model_cats = theano.shared(np.zeros(self.num_training_samples, dtype='int'))

        self.shared_vars = {
            'model_input': model_input,
            'model_output': model_output,
            'model_cats': model_cats
        }

        model = pm.Model()

        with model:
            mu_alpha = pm.Normal('mu_alpha', mu=0, sd=100)
            sigma_alpha = pm.HalfNormal('sigma_alpha', sd=100)

            mu_beta = pm.Normal('mu_beta', mu=0, sd=100)
            sigma_beta = pm.HalfNormal('sigma_beta', sd=100)

            alpha = pm.Normal('alpha', mu=mu_alpha, sd=sigma_alpha, shape=(self.num_cats,))
            betas = pm.Normal('beta', mu=mu_beta, sd=sigma_beta, shape=(self.num_cats, self.num_pred))

            c = model_cats

            temp = alpha[c] + T.sum(betas[c] * model_input, 1)

            p = pm.invlogit(temp)

            o = pm.Bernoulli('o', p, observed=model_output)

        return model

    def fit(
        self,
        X,
        y,
        cats,
        inference_type='advi',
        num_advi_sample_draws=10000,
        minibatch_size=None,
        inference_args=None
    ):
        """
        Train the Hierarchical Logistic Regression model

        Parameters
        ----------
        X : numpy array
            shape [num_training_samples, num_pred]

        y : numpy array
            shape [num_training_samples, ]

        cats : numpy array
            shape [num_training_samples, ]

        inference_type : str (defaults to 'advi')
            specifies which inference method to call
            Currently, only 'advi' and 'nuts' are supported.

        num_advi_sample_draws : int (defaults to 10000)
            Number of samples to draw from ADVI approximation after it has been fit;
            not used if inference_type != 'advi'

        minibatch_size : int (defaults to None)
            number of samples to include in each minibatch for ADVI
            If None, minibatch is not run.

        inference_args : dict (defaults to None)
            arguments to be passed to the inference methods
            Check the PyMC3 docs for permissable values.
            If None, default values will be set.
        """
        self.num_cats = len(np.unique(cats))
        self.num_training_samples, self.num_pred = X.shape

        self.inference_type = inference_type

        if y.ndim != 1:
            y = np.squeeze(y)

        if not inference_args:
            inference_args = self._set_default_inference_args()

        if self.cached_model is None:
            self.cached_model = self.create_model()

        if minibatch_size:
            with self.cached_model:
                minibatches = {
                    self.shared_vars['model_input']: pm.Minibatch(X, batch_size=minibatch_size),
                    self.shared_vars['model_output']: pm.Minibatch(y, batch_size=minibatch_size),
                    self.shared_vars['model_cats']: pm.Minibatch(cats, batch_size=minibatch_size)
                }

                inference_args['more_replacements'] = minibatches
        else:
            self._set_shared_vars({
                'model_input': X,
                'model_output': y,
                'model_cats': cats
            })

        self._inference(inference_type, inference_args, num_advi_sample_draws=num_advi_sample_draws)

        return self

    def predict_proba(self, X, cats, return_std=False, num_ppc_samples=2000):
        """
        Predicts probabilities of new data with a trained Hierarchical Logistic Regression

        Parameters
        ----------
        X : numpy array
            shape [num_training_samples, num_pred]

        cats : numpy array
            shape [num_training_samples, ]

        return_std : bool (defaults to False)
            Flag of whether to return standard deviations with mean probabilities

        num_ppc_samples : int (defaults to 2000)
            'samples' parameter passed to pm.sample_ppc
        """

        if self.trace is None:
            raise PyMC3ModelsError('Run fit on the model before predict.')

        num_samples = X.shape[0]

        if self.cached_model is None:
            self.cached_model = self.create_model()

        self._set_shared_vars({
            'model_input': X,
            'model_output': np.zeros(num_samples, dtype='int'),
            'model_cats': cats
        })

        ppc = pm.sample_ppc(self.trace, model=self.cached_model, samples=num_ppc_samples)

        if return_std:
            return ppc['o'].mean(axis=0), ppc['o'].std(axis=0)
        else:
            return ppc['o'].mean(axis=0)

    def predict(self, X, cats, num_ppc_samples=2000):
        """
        Predicts labels of new data with a trained model

        Parameters
        ----------
        X : numpy array
            shape [num_training_samples, num_pred]

        cats : numpy array
            shape [num_training_samples, ]

        num_ppc_samples : int (defaults to 2000)
            'samples' parameter passed to pm.sample_ppc
        """
        ppc_mean = self.predict_proba(X, cats, num_ppc_samples=2000)

        pred = ppc_mean > 0.5

        return pred

    def score(self, X, y, cats, num_ppc_samples=2000):
        """
        Scores new data with a trained model.

        Parameters
        ----------
        X : numpy array
            shape [num_training_samples, num_pred]

        y : numpy array
            shape [num_training_samples, ]

        cats : numpy array
            shape [num_training_samples, ]

        num_ppc_samples : int (defaults to 2000)
            'samples' parameter passed to pm.sample_ppc
        """

        return accuracy_score(y, self.predict(X, cats, num_ppc_samples=num_ppc_samples))

    def save(self, file_prefix):
        params = {
            'inference_type': self.inference_type,
            'num_cats': self.num_cats,
            'num_pred': self.num_pred,
            'num_training_samples': self.num_training_samples
        }

        super(HierarchicalLogisticRegression, self).save(file_prefix, params)

    def load(self, file_prefix):
        params = super(HierarchicalLogisticRegression, self).load(file_prefix, load_custom_params=True)

        self.inference_type = params['inference_type']
        self.num_cats = params['num_cats']
        self.num_pred = params['num_pred']
        self.num_training_samples = params['num_training_samples']
