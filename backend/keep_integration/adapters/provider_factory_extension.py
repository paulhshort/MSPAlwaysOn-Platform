"""
Extension for Keep's provider factory to include MSP-specific providers.
"""

from keep.providers.providers_factory import ProvidersFactory
from keep_integration.providers import MSP_PROVIDERS

def extend_providers_factory():
    """
    Extend Keep's provider factory with MSP-specific providers.
    """
    # Add MSP providers to Keep's provider registry
    for provider_type, provider_class in MSP_PROVIDERS.items():
        ProvidersFactory.register_provider(provider_type, provider_class)
