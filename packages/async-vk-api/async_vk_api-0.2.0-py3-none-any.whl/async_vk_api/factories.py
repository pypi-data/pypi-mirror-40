import asks

from .throttler import Throttler


def make_session(
    base_location='https://api.vk.com',
    endpoint='/method',
    connections=1,
    **kwargs
):
    return asks.Session(
        base_location=base_location,
        endpoint=endpoint,
        connections=connections,
        **kwargs
    )


def make_throttler(requests_per_second=3):
    return Throttler(rate=1/requests_per_second)
