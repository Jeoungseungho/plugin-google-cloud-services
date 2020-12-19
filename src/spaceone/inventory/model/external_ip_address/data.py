from schematics import Model
from schematics.types import ModelType, ListType, StringType, IntType, DateTimeType, BooleanType, FloatType, DictType, UnionType, MultiType


class Labels(Model):
    key = StringType()
    value = StringType()


class ExternalIpAddress(Model):
    id = StringType(default='')
    name = StringType(default='')
    region = StringType(default='global')
    project = StringType()
    description = StringType(default='')
    address = StringType()
    subnet_name = StringType(serialize_when_none=False)
    address_type = StringType(choices=('INTERNAL', 'EXTERNAL'), deserialize_from='addressType')
    is_ephemeral = StringType(choices=('Static', 'Ephemeral'))
    purpose = StringType(choices=('GCE_ENDPOINT', 'DNS_RESOLVER', 'VPC_PEERING', 'IPSEC_INTERCONNECT'),
                         serialize_when_none=False)
    network_tier = StringType(choices=('PREMIUM', 'STANDARD'),  deserialize_from='networkTier', serialize_when_none=False)
    network_tier_display = StringType(default='')
    used_by = ListType(StringType(), default=[])
    self_link = StringType(deserialize_from='selfLink')
    ip_version = StringType(choices=('IPV4', 'IPV6'), deserialize_from='ipVersion', serialize_when_none=False)
    ip_version_display = StringType()
    status = StringType(choices=('RESERVED', 'RESERVING', 'IN_USE'))
    users = ListType(StringType(), default=[])
    labels = ListType(ModelType(Labels), default=[])
    tags = ListType(ModelType(Labels), default=[])
    creation_timestamp = DateTimeType(deserialize_from='creationTimestamp')

    def reference(self):
        return {
            "resource_id": self.self_link,
            "external_link": f"https://console.cloud.google.com/networking/addresses/list/project={self.project}"
        }