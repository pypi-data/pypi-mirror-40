# with input in the DataFrame format
# update metadata of the dataset

import os, sys
import typing
import scipy.io
import numpy as np
from sklearn import preprocessing
#from common_primitives import utils
from d3m import container
from d3m.metadata import base as metadata_base
from d3m.metadata import hyperparams
from d3m.metadata import params
from d3m.primitive_interfaces.supervised_learning import SupervisedLearnerPrimitiveBase
from d3m.primitive_interfaces import base
from d3m.primitive_interfaces.base import CallResult
from rpi_d3m_primitives.structuredClassifier.structured_Classify_model import Model
from rpi_d3m_primitives.featSelect.RelationSet import RelationSet
import rpi_d3m_primitives


Inputs = container.DataFrame
Outputs = container.DataFrame

__all__ = ('NaiveBayes',)

class Params(params.Params):
    pass


class Hyperparams(hyperparams.Hyperparams):
    pass


class NaiveBayes(SupervisedLearnerPrimitiveBase[Inputs, Outputs, Params, Hyperparams]):

    metadata = metadata_base.PrimitiveMetadata({
        'id': '',
        'version': '2.1.5',
        'name': 'Naive Bayes Classifier',
        'keywords': ['Naive Bayes'],
        'source': {
            'name': 'RPI-ISL',
            'contact': 'mailto:cuiz3@rpi.edu',
            'uris': [
                'https://gitlab.datadrivendiscovery.org/zcui/rpi-primitives/blob/master/Feature_Selector_model.py',
                'https://gitlab.datadrivendiscovery.org/zcui/rpi-primitives.git'
                ]
        },
        'installation':[
            {
                'type': metadata_base.PrimitiveInstallationType.PIP,
                'package': 'rpi_d3m_primitives',
	            'version': '0.0.2'
            }
        ],
        'python_path': 'd3m.primitives.classification.naive_bayes.RPI',
        'algorithm_types': [
            metadata_base.PrimitiveAlgorithmType.NAIVE_BAYES_CLASSIFIER],
        'primitive_family': metadata_base.PrimitiveFamily.CLASSIFICATION
    })


    def __init__(self, *, hyperparams: Hyperparams, random_seed: int = 0, docker_containers: typing.Union[typing.Dict[str, base.DockerContainer]] = None) -> None:
        super().__init__(hyperparams=hyperparams, random_seed=random_seed, docker_containers=docker_containers)
        self._index = None
        self._training_inputs = None
        self._training_outputs = None
        self._fitted = False
        self._clf = Model('nb', bayesInf=1)

    def set_training_data(self, *, inputs: Inputs, outputs: Outputs) -> None:
        # set training labels
        [m,n] = inputs.shape
        self._training_outputs = np.zeros((m,))
        temp = list(outputs.iloc[:,0].values)
        for i in np.arange(len(temp)):
            self._training_outputs[i] = float(temp[i])
            
        # convert categorical values to numerical values in training data
        metadata = inputs.metadata
        [m,n] = inputs.shape
        self._training_inputs = np.zeros((m,n))
        for column_index in metadata.get_elements((metadata_base.ALL_ELEMENTS,)):
            if column_index is metadata_base.ALL_ELEMENTS: 
                continue
            column_metadata = metadata.query((metadata_base.ALL_ELEMENTS, column_index))
            semantic_types = column_metadata.get('semantic_types', [])
            if 'https://metadata.datadrivendiscovery.org/types/CategoricalData' in semantic_types:
                LE = preprocessing.LabelEncoder()
                LE = LE.fit(inputs.iloc[:,column_index])
                self._training_inputs[:,column_index] = LE.transform(inputs.iloc[:,column_index])  
            else:
                temp = list(inputs.iloc[:, column_index].values)
                for i in np.arange(len(temp)):
                    if bool(temp[i]):
                        self._training_inputs[i,column_index] = float(temp[i])
                    else:
                        self._training_inputs[i,column_index] = 'nan'
        self._fitted = False


    def fit(self, *, timeout: float = None, iterations: int = None) -> None:
        if self._fitted:
            return CallResult(None)

        if self._training_inputs.any() == None or self._training_outputs.any() == None: 
            raise ValueError('Missing training data, or missing values exist.')

        discTrainset = RelationSet(self._training_inputs, self._training_outputs.reshape(-1, 1))
        discTrainset.impute()
        discTrainset.discretize()
        discTrainset.remove()
        X_train = discTrainset.data - 1
        Y_train = discTrainset.labels - 1
        bins = discTrainset.NUM_STATES
        stateNo = np.append(bins, len(np.unique(Y_train)))
        self._clf.fit(X_train, Y_train, stateNo)

        self._fitted = True

        return CallResult(None)


    def produce(self, *, inputs: Inputs, timeout: float = None, iterations: int = None) -> base.CallResult[Outputs]:  # inputs: m x n numpy array
        if self._fitted:
            # get discrete bins from training data
            discTrainset = RelationSet(self._training_inputs, self._training_outputs.reshape(-1, 1))
            discTrainset.impute()
            discTrainset.discretize()
            discTrainset.remove()
            bins = discTrainset.NUM_STATES
            # convert categorical values to numerical values in testing data
            metadata = inputs.metadata
            [m, n] = inputs.shape
            X_test = np.zeros((m, n))
            for column_index in metadata.get_elements((metadata_base.ALL_ELEMENTS,)):
                if column_index is metadata_base.ALL_ELEMENTS:
                    continue
                column_metadata = metadata.query((metadata_base.ALL_ELEMENTS, column_index))
                semantic_types = column_metadata.get('semantic_types', [])
                if 'https://metadata.datadrivendiscovery.org/types/CategoricalData' in semantic_types:
                    LE = preprocessing.LabelEncoder()
                    LE = LE.fit(inputs.iloc[:, column_index])
                    X_test[:, column_index] = LE.transform(inputs.iloc[:, column_index])
                else:
                    temp = list(inputs.iloc[:, column_index].values)
                    for i in np.arange(len(temp)):
                        if bool(temp[i]):
                            X_test[i, column_index] = float(temp[i])
                        else:
                            X_test[i, column_index] = 'nan'
            discTestset = RelationSet(X_test, [])
            discTestset.impute()
            X_test = discTestset.data
            index_list = np.setdiff1d(np.arange(discTrainset.num_features),np.array(discTrainset.removeIdx))
            X_test = X_test[:, index_list]
            est = preprocessing.KBinsDiscretizer(n_bins=bins,encode='ordinal',strategy='uniform')
            est.fit(X_test)
            X_test = est.transform(X_test)
            output = self._clf.predict(X_test)
            output = container.DataFrame(output, generate_metadata=False, source=self)
            output.metadata = inputs.metadata.clear(source=self, for_value=output, generate_metadata=True)
            return CallResult(output)
        else:
            raise ValueError('Model should be fitted first.')


    def get_params(self) -> None:
        pass


    def set_params(self) -> None:
        pass

