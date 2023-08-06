# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Defines the Mimic Explainer for computing explanations on black box models or pipeline functions.

The mimic explainer trains an explainable model to reproduce the output of the given black box model.
The explainable model is called a surrogate model and the black box model is called a teacher model.
Once trained to reproduce the output of the teacher model, the surrogate model's explanation can
be used to explain the teacher model.
"""

import numpy as np
from shap.common import DenseData

from azureml.explain.model._internal.common import _order_imp

from .blackbox_explainer import BlackBoxExplainer
from .explanation_utils import _convert_to_list
from .scoring_model import TreeScoringModel

from .model_distill import model_distill
from .explanation import create_local_explanation, create_global_explanation
from azureml.explain.model._internal.constants import Defaults, ExplainParams


class MimicExplainer(BlackBoxExplainer):
    """Defines the Mimic Explainer for explaining black box models or pipeline functions."""

    def __init__(self, model, initialization_examples, explainable_model, is_pipeline=False, **kwargs):
        """Initialize the MimicExplainer.

        :param model: The model or pipeline (if is_pipeline is True) to be explained.
        :type model: model that implements predict or predict_proba or pipeline function that accepts a 2d ndarray
        :param initialization_examples: A matrix of feature vector examples (# examples x # features) for
            initializing the explainer.
        :type initialization_examples: numpy.array or pandas.DataFrame or iml.datatypes.DenseData or
            scipy.sparse.csr_matrix
        :param is_pipeline: Default set to false, set to True if passing pipeline instead of model.
        :type is_pipeline: bool
        """
        super(MimicExplainer, self).__init__(model, initialization_examples, is_pipeline=is_pipeline,
                                             **kwargs)
        self._logger.debug('Initializing MimicExplainer')
        # Train the mimic model on the given model
        try:
            training_data = self.initialization_examples.dataset
            if isinstance(training_data, DenseData):
                training_data = training_data.data
            self.surrogate_model = model_distill(self.pipeline, explainable_model, training_data)
        except Exception as ex:
            self._logger.debug('Pipeline is invalid, failing with exception: {}'.format(ex))
            self.invalid_pipeline = True

    def _is_pipeline_valid(self, pipeline, **kwargs):
        return not self.invalid_pipeline

    def _explain_global(self, evaluation_examples, top_k=None,
                        explain_subset=None, allow_eval_sampling=False,
                        max_dim_clustering=Defaults.MAX_DIM, sampling_method=Defaults.HDBSCAN,
                        silent=True, nsamples=Defaults.AUTO, create_scoring_model=False, **kwargs):
        """Globally explains the blackbox model.

        :param evaluation_examples: A matrix of feature vector examples (# examples x # features) on which
            to explain the model's output.
        :type evaluation_examples: numpy.array or pandas.DataFrame or scipy.sparse.csr_matrix
        :param create_scoring_model: Creates a TreeExplainer that can be operationalized for
            local model explanations.
        :type create_scoring_model: bool
        :param explain_subset: List of feature indices. If specified, only selects a subset of the
            features in the evaluation dataset for explanation, which will speed up the explanation
            process when number of features is large and the user already knows the set of interested
            features. The subset can be the top-k features from the model summary.
        :type explain_subset: list[int]
        :return: Global explanation of given evaluation examples.
        :rtype: GlobalExplanation
        """
        overall_importance_values = self.surrogate_model.explain_global()
        order = _order_imp(overall_importance_values)
        if top_k is not None:
            order = order[0:top_k]
        overall_importance_values = overall_importance_values[order]
        classification = self.predict_proba_flag
        scoring_model = None
        self.create_scoring_model = create_scoring_model
        if self.create_scoring_model:
            scoring_model = TreeScoringModel(self.surrogate_model.model())
        return create_global_explanation(expected_values=None, classification=classification,
                                         scoring_model=scoring_model,
                                         overall_importance_values=overall_importance_values,
                                         order=order, **kwargs)

    def _explain_local(self, evaluation_examples, features=None, explain_subset=None, **kwargs):
        """Locally explains the blackbox model.

        :param evaluation_examples: A matrix of feature vector examples (# examples x # features) on which
            to explain the model's output.
        :type evaluation_examples: numpy.array or pandas.DataFrame or scipy.sparse.csr_matrix
        :param features: A list of feature names.
        :type features: list[str]
        :param explain_subset: List of feature indices. If specified, only selects a subset of the
            features in the evaluation dataset for explanation, which will speed up the explanation
            process when number of features is large and the user already knows the set of interested
            features. The subset can be the top-k features from the model summary.
        :type explain_subset: list[int]
        :return: Explanation of given evaluation examples.
        :rtype: LocalExplanation
        """
        feature_importance_values = self.surrogate_model.explain_local(evaluation_examples.dataset)
        expected_values = None
        classification = self.predict_proba_flag
        if classification and isinstance(feature_importance_values, np.ndarray):
            feature_importance_values = [feature_importance_values]
        scoring_model = None
        if self.create_scoring_model:
            scoring_model = TreeScoringModel(self.surrogate_model.model())
        kwargs[ExplainParams.FEATURES] = features
        # Reformat feature_importance_values result if explain_subset specified
        if explain_subset:
            self._logger.debug('Getting subset of feature_importance_values')
            if classification:
                for i in range(len(feature_importance_values)):
                    feature_importance_values[i] = feature_importance_values[i][:, explain_subset]
            else:
                feature_importance_values = feature_importance_values[:, explain_subset]
        feature_importance_values = _convert_to_list(feature_importance_values)
        return create_local_explanation(feature_importance_values=feature_importance_values,
                                        expected_values=expected_values,
                                        classification=classification,
                                        scoring_model=scoring_model, **kwargs)
