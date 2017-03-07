from static import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET
from qkoubot.network import GetAuth
from qkoubot.my_exception import CouldNotAuthorize


def tweet_vars_validate():
    assert CONSUMER_KEY is not None, "CONSUMER_KEY is not given."
    assert CONSUMER_SECRET is not None, "CONSUMER_SECRET is not given."
    assert ACCESS_TOKEN is not None, "ACCESS_TOKEN is not given."
    assert ACCESS_SECRET is not None, "ACCESS_SECRET is not given."
    try:
        GetAuth()
    except Exception as e:
        raise CouldNotAuthorize(e.args)
