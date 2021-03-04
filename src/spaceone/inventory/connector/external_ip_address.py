import logging

from spaceone.inventory.libs.connector import GoogleCloudConnector
from spaceone.inventory.error import *
from pprint import pprint

__all__ = ['ExternalIPAddressConnector']
_LOGGER = logging.getLogger(__name__)


class ExternalIPAddressConnector(GoogleCloudConnector):
    google_client_service = 'compute'
    version = 'v1'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def list_instance_for_networks(self, **query):
        instance_list = []
        query.update({'project': self.project_id, 'includeAllScopes': False, 'maxResults': 500})
        request = self.client.instances().aggregatedList(**query)
        try:
            while request is not None:
                response = request.execute()
                for name, instances_scoped_list in response['items'].items():
                    if 'instances' in instances_scoped_list:
                        instance_list.extend(instances_scoped_list.get('instances'))
                request = self.client.instances().aggregatedList_next(previous_request=request, previous_response=response)

        except Exception as e:
            print(f'Error occurred at ExternalIPAddressConnector: instances().aggregatedList(**query) : skipped \n {e}')
            pass
        return instance_list

    def list_forwarding_rule(self, **query):
        forwarding_rule_list = []
        query.update({'project': self.project_id, 'includeAllScopes': False, 'maxResults': 500})

        request = self.client.forwardingRules().aggregatedList(**query)
        try:
            while request is not None:
                response = request.execute()
                for name, forwarding_rules_scoped_list in response['items'].items():
                    if 'forwardingRules' in forwarding_rules_scoped_list:
                        forwarding_rule_list.extend(forwarding_rules_scoped_list.get('forwardingRules'))
                request = self.client.forwardingRules().aggregatedList_next(previous_request=request, previous_response=response)
        except Exception as e:
            print(f'Error occurred at ExternalIPAddressConnector: forwardingRules().aggregatedList(**query) : skipped \n {e}')
            pass
        return forwarding_rule_list

    def list_regional_addresses(self, **query):
        address_list = []
        query = self.generate_query(**query)

        request = self.client.addresses().aggregatedList(**query)
        try:
            while request is not None:
                response = request.execute()
                for name, _address_list in response['items'].items():
                    if 'addresses' in _address_list:
                        address_list.extend(_address_list.get('addresses'))
                request = self.client.addresses().aggregatedList_next(previous_request=request,
                                                                      previous_response=response)
        except Exception as e:
            print(f'Error occurred at ExternalIPAddressConnector: addresses().aggregatedList(**query) : skipped \n {e}')
            pass
        return address_list
