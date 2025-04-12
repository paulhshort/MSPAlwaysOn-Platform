"""
Keep.dev integration for MSPAlwaysOn.
"""

from .adapters.provider_factory_extension import extend_providers_factory

def initialize_keep_integration():
    """
    Initialize the Keep.dev integration.
    """
    # Extend the provider factory
    extend_providers_factory()
