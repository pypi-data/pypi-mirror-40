# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Defines constants for explain model."""


class ExplanationParams(object):
    """Constants for explanation parameters"""
    CLASSES = 'classes'
    EXPECTED_VALUES = 'expected_values'


class History(object):
    """Constants related to uploading assets to run history"""
    EXPLANATION = 'explanation'
    EXPLANATION_ASSET = 'explanation_asset'
    EXPLANATION_ASSET_TYPE = 'azureml.v1.model.explanation'
    FEATURE_NAMES = 'feature_names'
    OVERALL_FEATURE_ORDER = 'overall_feature_order'
    OVERALL_IMPORTANCE_ORDER = 'overall_importance_order'
    OVERALL_SUMMARY = 'overall_summary'
    PER_CLASS_FEATURE_ORDER = 'per_class_feature_order'
    PER_CLASS_IMPORTANCE_ORDER = 'per_class_importance_order'
    PER_CLASS_SUMMARY = 'per_class_summary'
    SHAP_VALUES = 'shap_values'
    PREFIX = 'prefix'
    NUM_CLASSES = 'num_classes'
    TYPE = 'type'
    VERSION_TYPE = 'version_type'


class ExplainType(object):
    """Constants for model and explainer type information, useful for visualization"""
    MODEL = 'model_type'
    EXPLAINER = 'explainer'
    CLASSIFICATION = 'classification'
    REGRESSION = 'regression'
    TABULAR = 'tabular'
    TEXT = 'text'


class IO(object):
    """File input and output related constants"""
    UTF8 = 'utf-8'


class ExplainParams(object):
    """Constants for explain model (explain_local and explain_global) parameters"""
    SCORING_MODEL = 'scoring_model'
    FEATURE_IMPORTANCE_VALUES = 'feature_importance_values'
    FEATURES = 'features'
    PER_CLASS_IMP = 'per_class_imp'
    PER_CLASS_RANK = 'per_class_rank'
    PER_CLASS_SUMMARY = 'per_class_summary'
    ORDER = 'order'
    OVERALL_IMPORTANCE_VALUES = 'overall_importance_values'
    LOCAL_EXPLANATION = 'local_explanation'


class Defaults(object):
    """Constants for default values to explain methods"""
    AUTO = 'auto'
    # hdbscan is an unsupervised learning library to find the optimal number of clusters in a dataset
    # See this github repo for more details: https://github.com/scikit-learn-contrib/hdbscan
    HDBSCAN = 'hdbscan'
    MAX_DIM = 50


class Attributes(object):
    """Constants for attributes"""
    EXPECTED_VALUE = 'expected_value'


class Dynamic(object):
    """Constants for dynamically generated classes"""
    LOCAL_EXPLANATION = 'DynamicLocalExplanation'
    GLOBAL_EXPLANATION = 'DynamicGlobalExplanation'


class Tensorflow(object):
    """Tensorflow and tensorboard related constants"""
    TFLOG = 'tflog'
    CPU0 = '/CPU:0'


class SKLearn(object):
    """Scikit-learn related constants"""
    PREDICTIONS = 'predictions'
    LABELS = 'labels'
    EXAMPLES = 'examples'
    BALL_TREE = 'ball_tree'


class Spacy(object):
    """Spacy related constants"""
    NER = 'ner'
    TAGGER = 'tagger'
    EN = 'en'
