from static import SHIBBOLETH_PASSWORD, SHIBBOLETH_USERNAME


def shibboleth_vars_validate():
    assert SHIBBOLETH_USERNAME is not None, "SHIBBOLETH_USERNAME is not given."
    assert SHIBBOLETH_USERNAME[0] == "b", "SHIBBOLETH_USERNAME is invalid. It should be start with 'b'."
    assert SHIBBOLETH_PASSWORD is not None, "SHIBBOLETH_PASSWORD is not given."
    assert len(SHIBBOLETH_PASSWORD) > 4, "SHIBBOLETH_PASSWORD is too short."
