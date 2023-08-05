from abc import ABCMeta
from enum import Enum

from typing import List, Dict

from sidecar.messaging_service import MessagingConnectionProperties


class SidecarApplication:
    def __init__(self, name: str,
                 instances_count: int,
                 dependencies: List[str],
                 env: Dict[str, str],
                 healthcheck_timeout: int,
                 healthcheck_script: str,
                 default_health_check_ports_to_test: List[int],
                 has_public_access: bool):
        self.has_public_access = has_public_access
        self.name = name
        self.default_health_check_ports_to_test = default_health_check_ports_to_test
        self.healthcheck_timeout = healthcheck_timeout
        self.healthcheck_script = healthcheck_script
        self.env = env
        self.dependencies = dependencies
        self.instances_count = instances_count

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.name == other.name and \
                   self.instances_count == other.instances_count and \
                   self.dependencies == other.dependencies and \
                   self.env == other.env and \
                   self.healthcheck_timeout == other.healthcheck_timeout and \
                   self.default_health_check_ports_to_test == other.default_health_check_ports_to_test and \
                   self.healthcheck_script == other.healthcheck_script and \
                   self.has_public_access == other.has_public_access
        return False

    def __repr__(self):
        return "name={} " \
               "instances_count={} " \
               "dependencies={} " \
               "env={} " \
               "healthcheck_timeout={} " \
               "healthcheck_script={} " \
               "default_health_check_ports_to_test={} " \
               "has_public_access={} ".format(self.name,
                                              self.instances_count,
                                              self.dependencies,
                                              self.env,
                                              self.healthcheck_timeout,
                                              self.healthcheck_script,
                                              self.default_health_check_ports_to_test,
                                              self.has_public_access)


class EnvironmentType(Enum):
    Sandbox = "sandbox"
    ProductionBlue = "production-blue"
    ProductionGreen = "production-green"

    def __eq__(self, other):
        return self.value == other

    def __ne__(self, other):
        return self.value != other


class ISidecarConfiguration(metaclass=ABCMeta):
    def __init__(self,
                 environment: str,
                 provider: str,
                 sandbox_id: str,
                 production_id: str,
                 space_id: str,
                 cloud_external_key: str,
                 apps: List[SidecarApplication],
                 messaging: MessagingConnectionProperties,
                 env_type: str):
        self.messaging = messaging
        self.apps = apps
        self.space_id = space_id
        self.sandbox_id = sandbox_id
        self.production_id = production_id
        self.provider = provider
        self.environment = environment
        self.cloud_external_key = cloud_external_key
        self.env_type = EnvironmentType(env_type)


class AzureSidecarConfiguration(ISidecarConfiguration):
    def __init__(self,
                 management_resource_group: str,
                 subscription_id: str,
                 application_id: str,
                 application_secret: str,
                 tenant_id: str,
                 environment: str,
                 sandbox_id: str,
                 production_id: str,
                 space_id: str,
                 cloud_external_key: str,
                 apps: List[SidecarApplication],
                 messaging: MessagingConnectionProperties,
                 env_type: str):
        super().__init__(environment, "azure", sandbox_id, production_id, space_id, cloud_external_key, apps, messaging,
                         env_type)
        self.tenant_id = tenant_id
        self.application_secret = application_secret
        self.application_id = application_id
        self.subscription_id = subscription_id
        self.management_resource_group = management_resource_group

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.management_resource_group == other.management_resource_group and \
                   self.subscription_id == other.subscription_id and \
                   self.application_id == other.application_id and \
                   self.tenant_id == other.tenant_id and \
                   self.environment == other.environment and \
                   self.provider == other.provider and \
                   self.sandbox_id == other.sandbox_id and \
                   self.space_id == other.space_id and \
                   self.cloud_external_key == other.cloud_external_key and \
                   self.apps == other.apps and \
                   self.messaging == other.messaging
        return False

    def __repr__(self):
        return "management_resource_group={} " \
               "subscription_id={} " \
               "application_id={} " \
               "tenant_id={} " \
               "environment={} " \
               "provider={} " \
               "sandbox_id={} " \
               "production_id={} " \
               "space_id={} " \
               "cloud_external_key={} " \
               "apps={} " \
               "messaging={}".format(self.management_resource_group,
                                     self.subscription_id,
                                     self.application_id,
                                     self.tenant_id,
                                     self.environment,
                                     self.provider,
                                     self.sandbox_id,
                                     self.production_id,
                                     self.space_id,
                                     self.cloud_external_key,
                                     self.apps,
                                     self.messaging)


class AwsSidecarConfiguration(ISidecarConfiguration):
    def __init__(self,
                 region_name: str,
                 environment: str,
                 sandbox_id: str,
                 production_id: str,
                 space_id: str,
                 cloud_external_key: str,
                 apps: List[SidecarApplication],
                 messaging: MessagingConnectionProperties,
                 env_type: str):
        super().__init__(environment, "aws", sandbox_id, production_id, space_id, cloud_external_key, apps, messaging,
                         env_type)
        self.region_name = region_name

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.region_name == other.region_name and \
                   self.environment == other.environment and \
                   self.provider == other.provider and \
                   self.sandbox_id == other.sandbox_id and \
                   self.space_id == other.space_id and \
                   self.cloud_external_key == other.cloud_external_key and \
                   self.apps == other.apps and \
                   self.messaging == other.messaging
        return False

    def __repr__(self):
        return "region_name={} " \
               "environment={} " \
               "provider={} " \
               "sandbox_id={} " \
               "production_id={} " \
               "space_id={} " \
               "cloud_external_key={} " \
               "apps={} " \
               "messaging={}".format(self.region_name,
                                     self.environment,
                                     self.provider,
                                     self.sandbox_id,
                                     self.production_id,
                                     self.space_id,
                                     self.cloud_external_key,
                                     self.apps,
                                     self.messaging)


class KubernetesSidecarConfiguration(ISidecarConfiguration):
    def __init__(self, kub_api_address: str,
                 environment: str,
                 sandbox_id: str,
                 production_id: str,
                 space_id: str,
                 cloud_external_key: str,
                 apps: List[SidecarApplication],
                 messaging: MessagingConnectionProperties,
                 env_type: str):
        super().__init__(environment, "kubernetes", sandbox_id, production_id, space_id, cloud_external_key, apps,
                         messaging,
                         env_type)
        self.kub_api_address = kub_api_address

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.kub_api_address == other.kub_api_address and \
                   self.environment == other.environment and \
                   self.provider == other.provider and \
                   self.sandbox_id == other.sandbox_id and \
                   self.space_id == other.space_id and \
                   self.cloud_external_key == other.cloud_external_key and \
                   self.apps == other.apps and \
                   self.messaging == other.messaging
        return False

    def __repr__(self):
        return "kub_api_address={} " \
               "environment={} " \
               "provider={} " \
               "sandbox_id={} " \
               "production_id={} " \
               "space_id={} " \
               "cloud_external_key={} " \
               "apps={} " \
               "messaging={}".format(self.kub_api_address,
                                     self.environment,
                                     self.provider,
                                     self.sandbox_id,
                                     self.production_id,
                                     self.space_id,
                                     self.cloud_external_key,
                                     self.apps,
                                     self.messaging)
