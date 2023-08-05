import os
from time import time
from typing import Dict

import requests
from urlobject import URLObject
from shortesttrack_tools.functional import cached_property
from shortesttrack_tools.logger.utils import get_prototype_logger

from shortesttrack import constants
from shortesttrack.utils import APIClient
from shortesttrack.client import PerformanceHelper
from shortesttrack.conf.lib_conf import ULibraryConfig
from shortesttrack.models.base.model import Model
from shortesttrack.models.matrix import Matrix

logger = get_prototype_logger('script-configuration')


class ScriptConfiguration(Model):
    def __init__(self, metadata: dict) -> None:
        super().__init__(metadata)
        self._datasets = {}
        self._matrices = {}
        self._matrices_lists = {}

        if not self._lib.config.manual_data_manage:
            self.__set_up_matrices()
            self.__set_up_trained_model()

        if self._lib.config.dataprovider:
            self.set_up_datasets()

    def __str__(self) -> str:
        return f'SEC({self.id})'

    @cached_property
    def datasets(self) -> dict:
        return self._datasets

    @cached_property
    def matrices(self) -> dict:
        return self._matrices

    @property
    def matrices_lists(self) -> Dict[str, Dict[str, Matrix]]:
        return self._matrices_lists

    @cached_property
    def parameters(self) -> dict:
        return {
            p['id']: p.get('value') for p in self.metadata.get('parameters', [])
        }

    def write_parameter(self, parameter_id: str, parameter_value: dict or str or list,
                        performance_id: str = APIClient.PERFORMANCE_ID,
                        parameter_type: str = constants.TYPE_DEFAULT) -> None:
        logger.info(f'writing output parameter to performance {performance_id}: {parameter_id}={parameter_value}')
        performance = PerformanceHelper(sec_id=self.id, performance_id=performance_id)
        performance.write_parameter(parameter_id, parameter_value, parameter_type)

    def download_trained_model(self) -> None:
        tm_data = self.pull_trained_model_data()
        if not tm_data:
            logger.info(f'no trained model data, skip writing to file')
            return

        logger.info(f'writing trained model to file {os.path.abspath(ULibraryConfig.trained_model_data_path)}')
        with open(ULibraryConfig.trained_model_data_path, 'wb') as f:
            f.write(tm_data)

    def upload_trained_model(self, file_path: str, name: str = None) -> None:
        if not name:
            name = f'trained_model_{int(time())}'

        uploaded_tm = self._do_upload_trained_model(file_path, name)
        logger.info(f'uploaded trained model {uploaded_tm}')

        if APIClient.PERFORMANCE_ID:
            logger.info(f'notify Performance {APIClient.PERFORMANCE_ID}...')
            self.write_parameter(parameter_id='trained_model', parameter_value=uploaded_tm,
                                 parameter_type=constants.TYPE_TRAINED_MODEL)

    def set_up_datasets(self) -> None:
        logger.info(f'setting up datasets...')

        if not self._metadata.get('datasets'):
            logger.info(f'skip datasets setup: no datasets in script configuration')
            return

        from shortesttrack.models.dataset import Dataset
        self._datasets['input'] = Dataset(metadata=constants.DEMO_INPUT_DATASET)
        self._datasets['output'] = Dataset(metadata=constants.DEMO_OUTPUT_DATASET)

    def __set_up_matrices(self) -> None:
        logger.info(f'setting up matrices...')

        human_readable_matrices = {}
        for matrix in self._metadata.get('matrices', []):
            human_readable_matrices[matrix['id']] = Matrix(matrix)

        self._matrices = human_readable_matrices

        for matrix_list in self.metadata.get('matricesLists', []):
            self._matrices_lists[matrix_list['id']] = dict()
            for matrix in matrix_list['matrices']:
                self._matrices_lists[matrix_list['id']][matrix['name']] = Matrix(matrix)

    def __set_up_trained_model(self) -> None:
        logger.info(f'setting up trained model...')

        if not self.trained_model_required:
            logger.info(f'trained model not required, skip setup')
            return

        self.download_trained_model()

    # Moved from SECHelper
    @property
    def trained_model_required(self) -> bool:
        return self.metadata.get('scriptOrSnapshot', {}).get('requiresTrainedModel', False)

    @cached_property
    def trained_model_id(self) -> str:
        return self.metadata.get("trainedModelId", None)

    @cached_property
    def trained_model_download_link(self) -> URLObject:
        raw_url = self._lib.data_endpoint.get_trained_model_download_link(self.trained_model_id)
        url = raw_url.decode("utf-8")
        return URLObject(url)

    def pull_trained_model_data(self) -> bytes or None:
        if not self.trained_model_id:
            return None

        logger.info(f'download trained model data: {self.trained_model_id}')
        link = self.trained_model_download_link

        response = requests.get(link)
        if response.status_code not in (200, 201):
            logger.error(f'{response.status_code, response.content}')
            raise Exception(f'Cannot download trained model data {self.trained_model_id}')

        logger.info(f'trained model downloaded {response.status_code}')
        return response.content

    def _do_upload_trained_model(self, file_path: str, name: str) -> dict:
        logger.info(f'uploading trained model {name} ({file_path})...')
        with open(file_path, 'rb') as f:
            return self._lib.data_endpoint.request(self._lib.data_endpoint.POST,
                                                   'trained-models/upload/',
                                                   files={name: (name, f, 'multipart/form-data')})
