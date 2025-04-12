"""
MSP-specific providers for Keep.dev.
"""

from .connectwise_provider import ConnectWiseManageProvider
from .sentinelone_provider import SentinelOneProvider
from .veeam_provider import VeeamProvider
from .itglue_provider import ITGlueProvider

# Register providers
MSP_PROVIDERS = {
    "connectwise-manage": ConnectWiseManageProvider,
    "sentinelone": SentinelOneProvider,
    "veeam": VeeamProvider,
    "itglue": ITGlueProvider
}
