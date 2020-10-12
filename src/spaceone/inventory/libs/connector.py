import google.oauth2.service_account
import googleapiclient
import googleapiclient.discovery

from spaceone.core.error import *
from spaceone.core.connector import BaseConnector

DEFAULT_SCHEMA = 'google_oauth_client_id'


class GoogleCloudConnector(BaseConnector):
    google_client_service = None
    version = 'v1'

    def __init__(self, **kwargs):
        """
        kwargs
            - schema
            - options
            - secret_data

        secret_data(dict)
            - type: ..
            - project_id: ...
            - token_uri: ...
            - ...
        """

        super().__init__(transaction=None, config=None)
        secret_data = kwargs.get('secret_data')
        self.project_id = secret_data.get('project_id')

        try:
            credentials = google.oauth2.service_account.Credentials.from_service_account_info(secret_data)
            self.client = googleapiclient.discovery.build(self.google_client_service, self.version,
                                                          credentials=credentials)

        except Exception as e:
            print()
            raise ERROR_UNKNOWN(message=e)

    def generate_query(self, **query):
        query.update({
            'project': self.project_id,
        })
        return query
