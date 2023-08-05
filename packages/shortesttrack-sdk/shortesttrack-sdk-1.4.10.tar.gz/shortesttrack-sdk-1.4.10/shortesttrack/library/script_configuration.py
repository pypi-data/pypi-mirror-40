import os
import json
from typing import Dict
from time import time

from shortesttrack import constants
from shortesttrack.utils import getLogger, APIClient
from shortesttrack.client import SECHelper, PerformanceHelper
from shortesttrack.models.matrix import Matrix
from shortesttrack_tools.functional import cached_property

import warnings

warnings.warn('This module is deprecated. Use models.script_configuration.py instead', DeprecationWarning, stacklevel=2)

logger = getLogger()


class ScriptConfiguration:
    def __init__(self, sec_id: str = APIClient.CONFIGURATION_ID,
                 path_for_trained_model_data: str = None,
                 manual_data_manage: bool = False):
        logger.info(f'ScriptConfiguration {sec_id}')
        if not sec_id:
            raise Exception(f'SEC invalid configuration: {sec_id}')

        self._sec_id = sec_id
        self.helper = SECHelper(self._sec_id)
        self.sec = self.helper.sec
        self.path_for_trained_model_data = path_for_trained_model_data or 'trained_model.sav'
        self._matrices_names = {}
        self._matrices = {}
        self._matrices_lists = {}

        if not manual_data_manage:
            self.__set_up_matrices()
            self.__set_up_trained_model()

    def __str__(self):
        return f'SEC({self._sec_id})'

    def __set_up_matrices(self) -> None:
        logger.info(f'setting up matrices...')
        for matrix in self.sec.get('matrices', []):
            self._matrices_names[matrix['id']] = matrix['matrixId']
            self._matrices[matrix['matrixId']] = Matrix(matrix)

        for matrix_list in self.sec.get('matricesLists', []):
            self._matrices_lists[matrix_list['id']] = dict()
            for matrix in matrix_list['matrices']:
                self._matrices_lists[matrix_list['id']][matrix['name']] = Matrix(matrix)

    def __set_up_trained_model(self) -> None:
        logger.info(f'setting up trained model...')

        if not self.helper.trained_model_required:
            logger.info(f'trained model not required, skip setup')
            return

        self.download_trained_model()

    @cached_property
    def matrices(self) -> dict:
        return self._matrices

    @property
    def matrices_lists(self) -> Dict[str, Dict[str, Matrix]]:
        return self._matrices_lists

    @cached_property
    def parameters(self) -> dict:
        return {
            p['id']: p.get('value') for p in self.sec.get('parameters', [])
        }

    def write_parameter(self, parameter_id, parameter_value, performance_id: str = APIClient.PERFORMANCE_ID,
                        parameter_type: str = 'default'):
        logger.info(f'writing output parameter to performance {performance_id}: {parameter_id}={parameter_value}')
        performance = PerformanceHelper(sec_id=self._sec_id, performance_id=performance_id)
        performance.write_parameter(parameter_id, parameter_value, parameter_type)

    def download_trained_model(self) -> None:
        tm_data = self.helper.pull_trained_model_data()
        if not tm_data:
            logger.info(f'no trained model data, skip writing to file')
            return

        logger.info(f'writing trained model to file {os.path.abspath(self.path_for_trained_model_data)}')
        with open(self.path_for_trained_model_data, 'wb') as f:
            f.write(tm_data)

    def upload_trained_model(self, file_path: str, name: str = None) -> None:
        name = name if name else f'trained_model_{int(time())}'
        uploaded_tm = self.helper.upload_trained_model(file_path, name)
        logger.info(f'uploaded trained model {uploaded_tm}')

        if APIClient.PERFORMANCE_ID:
            logger.info(f'notify Performance {APIClient.PERFORMANCE_ID}...')
            self.write_parameter(parameter_id='trained_model', parameter_value=json.dumps(uploaded_tm),
                                 parameter_type=constants.TYPE_TRAINED_MODEL)
