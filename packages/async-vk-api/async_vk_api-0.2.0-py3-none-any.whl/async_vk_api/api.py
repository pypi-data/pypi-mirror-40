import attr

from .errors import ApiError
from .factories import make_session, make_throttler


@attr.s
class Api:

    _access_token = attr.ib()
    _version = attr.ib()

    _session = attr.ib(factory=make_session)
    _throttler = attr.ib(factory=make_throttler)

    async def __call__(self, method_name, **params):
        async with self._throttler():
            response = await self._session.get(
                path=f'/{method_name}',
                params={
                    'access_token': self._access_token,
                    'v': self._version,
                    **params
                }
            )

        payload = response.json()

        try:
            return payload['response']
        except KeyError as exc:
            raise ApiError(payload['error']) from exc

    def __getattr__(self, item):
        return MethodGroup(name=item, api=self)


@attr.s
class MethodGroup:

    name = attr.ib()
    api = attr.ib()

    def __getattr__(self, item):
        return Method(name=item, group=self)


@attr.s
class Method:

    name = attr.ib()
    group = attr.ib()

    @property
    def full_name(self):
        return f'{self.group.name}.{self.name}'

    async def __call__(self, **params):
        return await self.group.api(self.full_name, **params)
