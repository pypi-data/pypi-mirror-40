from .helpers import fetchJSON, stringifyQuery


class CharityBaseResult():

    def __init__(self, result):
        self.query = result.get('query', {})
        self.charities = result.get('charities', [])
        self.count = result.get('count', None)


class CharityBaseClient():

    def __init__(self, config):
        self.apiKey = config.get('apiKey')
        self.baseUrl = config.get('baseUrl')
        self.apiVersion = config.get('apiVersion')


class CharityClient(CharityBaseClient):

    def list(self, query):

        allowed_keys = [
            'apiKey',
            'fields',
            'ids.GB-CHC',
            'search',
            'incomeRange',
            'addressWithin',
            'areasOfOperation.id',
            'causes.id',
            'beneficiaries.id',
            'operations.id',
            'sort',
            'limit',
            'skip',
        ]

        query['apiKey'] = self.apiKey
        queryString = stringifyQuery(query, allowed_keys)
        url = "{}/{}/charities/?{}".format(
            self.baseUrl,
            self.apiVersion,
            queryString
        )
        return CharityBaseResult(fetchJSON(url, {}, query.get('accessToken')))

    def count(self, query):

        allowed_keys = [
            'apiKey',
            'ids.GB-CHC',
            'search',
            'incomeRange',
            'addressWithin',
            'areasOfOperation.id',
            'causes.id',
            'beneficiaries.id',
            'operations.id',
        ]

        query['apiKey'] = self.apiKey
        queryString = stringifyQuery(query, allowed_keys)
        url = "{}/{}/count-charities/?{}".format(
            self.baseUrl,
            self.apiVersion,
            queryString
        )
        return CharityBaseResult(fetchJSON(url, {}, query.get('accessToken')))


class ApiKeyClient(CharityBaseClient):

    allowed_keys = ['apiKey']

    def _base_query(self, method, query):
        query['apiKey'] = self.apiKey
        queryString = stringifyQuery(query, self.allowed_keys)
        url = "{}/{}/api-key/?{}".format(
            self.baseUrl,
            self.apiVersion,
            queryString
        )
        options = {"method": method}
        return fetchJSON(url, options, query.get('accessToken'))

    def get(self, query):
        return self._base_query('GET', query)

    def create(self, query):
        return self._base_query('POST', query)

    def remove(self, query):
        return self._base_query('DELETE', query)
