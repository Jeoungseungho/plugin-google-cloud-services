import time
import logging
import concurrent.futures
from spaceone.inventory.libs.manager import GoogleCloudManager
from spaceone.core.service import *


_LOGGER = logging.getLogger(__name__)
MAX_WORKER = 20
SUPPORTED_RESOURCE_TYPE = ['inventory.CloudService', 'inventory.CloudServiceType', 'inventory.Region']
SUPPORTED_FEATURES = ['garbage_collection']

FILTER_FORMAT = []


@authentication_handler
class CollectorService(BaseService):
    def __init__(self, metadata):
        super().__init__(metadata)
        # set google cloud service manager
        self.execute_managers = [
            # 'CloudSQLManager',
            # 'InstanceGroupManager',
            # 'InstanceTemplateManager',
            # 'MachineImageManager',
            # 'DiskManager',
            # 'SnapshotManager',
            # 'StorageManager',
            # 'VPCNetworkManager',
            # 'ExternalIPAddressManager',
            # 'FirewallManager',
            # 'RouteManager',
            'LoadBalancingManager'
        ]

    @check_required(['options'])
    def init(self, params):
        """ init plugin by options
        """
        capability = {
            'filter_format': FILTER_FORMAT,
            'supported_resource_type': SUPPORTED_RESOURCE_TYPE,
            'supported_features': SUPPORTED_FEATURES
        }
        return {'metadata': capability}

    @transaction
    @check_required(['options', 'secret_data'])
    def verify(self, params):
        """
        Args:
              params:
                - options
                - secret_data
        """
        options = params['options']
        secret_data = params.get('secret_data', {})
        if secret_data != {}:
            google_manager = GoogleCloudManager()
            active = google_manager.verify({}, secret_data)

        return {}

    @transaction
    @check_required(['options', 'secret_data', 'filter'])
    def list_resources(self, params):
        """
        Args:
            params:
                - options
                - schema
                - secret_data
                - filter
        """

        start_time = time.time()

        print("[ EXECUTOR START: Google Cloud Service ]")

        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKER) as executor:
            future_executors = []
            for execute_manager in self.execute_managers:
                print(f'@@@ {execute_manager} @@@')
                _manager = self.locator.get_manager(execute_manager)
                future_executors.append(executor.submit(_manager.collect_resources, params))

            for future in concurrent.futures.as_completed(future_executors):
                for result in future.result():
                    yield result.to_primitive()

        print(f'TOTAL TIME : {time.time() - start_time} Seconds')