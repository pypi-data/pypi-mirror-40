from .clients import CharityClient, ApiKeyClient
from .helpers import InvalidAPIVersionError

DEFAULT_BASE_URL = "https://charitybase.uk/api"
DEFAULT_API_VERSION = 'v4.0.0'
SUPPORTED_API_RANGES = [
    "v4.0.x"
]

class CharityBase:

    def __init__(self, apiKey, baseUrl=None):
        self.config = {
            "apiKey": apiKey,
            "baseUrl": baseUrl if baseUrl else DEFAULT_BASE_URL,
            "apiVersion": DEFAULT_API_VERSION
        }
        self.charity = CharityClient(self.config)
        self.apiKey = ApiKeyClient(self.config)

    def getApiVersion(self):
        return self.config["apiVersion"]

    def setApiVersion(self, version):
        valid_version = self._validate_api_version(version)
        if not valid_version:
            raise InvalidAPIVersionError("{} not in supported API versions: {}".format(version, ", ".join(SUPPORTED_API_RANGES)))
        self.config["apiVersion"] = version

    def _validate_api_version(self, version):
        # @TODO python semver libraries don't currently support `.x` syntax
        # when it does this can replicate the proper check found in <https://github.com/charity-base/charity-base-client-js/blob/master/src/index.js#L8-L16>
        # - see <https://github.com/rbarrois/python-semanticversion/issues/66>
        return version.strip('v')
