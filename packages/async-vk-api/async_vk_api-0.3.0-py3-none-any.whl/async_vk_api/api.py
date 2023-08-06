from .errors import ApiError


class Api:

    def __init__(self, access_token, version, session, throttler):
        self._access_token = access_token
        self._version = version
        self._session = session
        self._throttler = throttler

    async def __call__(self, method_name, **params):
        async with self._throttler():
            response = await self._session.get(
                path=f'/{method_name}',
                params={**self._default_params, **params}
            )

        payload = response.json()

        try:
            return payload['response']
        except KeyError as exc:
            raise ApiError(payload['error']) from exc

    def __getattr__(self, item):
        return MethodGroup(name=item, api=self)

    @property
    def _default_params(self):
        return {
            'access_token': self._access_token,
            'v': self._version,
        }


class MethodGroup:

    def __init__(self, name, api):
        self.name = name
        self.api = api

    def __getattr__(self, item):
        return Method(name=item, group=self)


class Method:

    def __init__(self, name, group):
        self.name = name
        self.group = group

    @property
    def full_name(self):
        return f'{self.group.name}.{self.name}'

    async def __call__(self, **params):
        return await self.group.api(self.full_name, **params)
