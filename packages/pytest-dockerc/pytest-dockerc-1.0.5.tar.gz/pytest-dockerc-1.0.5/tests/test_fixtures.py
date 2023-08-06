import socket
import requests
import compose

from pytest_dockerc import Wait


def test_basic_workflow(dockerc, dockerc_logs):
    """ Basic test to check that the container is started and that
    the http server is ready to listen on the documented port.
    """
    assert dockerc is not None
    assert len(dockerc.containers()) == 1

    container = dockerc.containers()[0]
    assert container.is_running is True
    assert container.labels["com.docker.compose.service"] == "http"

    inspect = container.inspect()
    networks = inspect["NetworkSettings"]["Networks"]
    assert len(networks) == 1
    network = next(iter(inspect["NetworkSettings"]["Networks"]))
    ipv4 = networks[network]["IPAddress"]
    assert len(inspect["NetworkSettings"]["Ports"]) == 1
    port = next(iter(inspect["NetworkSettings"]["Ports"])).split("/")[0]

    res = Wait(ignored_exns=(requests.ConnectionError,))(
        lambda: requests.get("http://{0}:{1}".format(ipv4, port))
    )
    assert res.status_code == requests.codes.ok


def test_context(ctx):
    """ Test the provided Context by pytest_dockerc
    """
    http = ctx.containers["http"]
    assert isinstance(http, compose.container.Container)

    assert socket.inet_aton(ctx.container_addr("http"))
    assert ctx.container_port("http") == 80

    env = ctx.container_env("http")
    assert "PATH" in env
    assert "NGINX_VERSION" in env
