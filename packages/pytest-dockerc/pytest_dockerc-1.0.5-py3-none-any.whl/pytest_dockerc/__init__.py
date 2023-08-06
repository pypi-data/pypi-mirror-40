import time


class Wait:
    """ Wait until helper to wait for a trigger state
    """

    def __init__(self, freq=0.2, timeout=10, ignored_exns=None):
        self.freq = freq
        self.timeout = timeout
        self.ignored_exns = tuple(ignored_exns) if ignored_exns else tuple()

    def __call__(self, trigger):
        end = time.time() + self.timeout

        while time.time() < end:
            try:
                res = trigger()
                return res
            except self.ignored_exns as exn:
                res = exn
            time.sleep(self.freq)
        raise StopIteration(str(res))


class Context:
    """ Context class with containers helpers
    """

    def __init__(self, dockerc):
        self.dockerc = dockerc

    @property
    def containers(self):
        """ store container in a dict with the service name as a key
        """
        project = "com.docker.compose.project"
        service = "com.docker.compose.service"
        return {
            c.labels[service]: c
            for c in self.dockerc.containers()
            if project in c.labels and c.labels[project] == self.dockerc.name
        }

    def container_addr(self, service_name):
        """ get the container IP of a service
        """
        project_name = self.dockerc.name
        network_name = next(iter(self.dockerc.networks.networks.keys()))
        name = "{}_{}".format(project_name, network_name)
        attrs = self.containers[service_name].inspect()
        return attrs["NetworkSettings"]["Networks"][name]["IPAddress"]

    def container_port(self, service_name):
        """ get the container exposed ports of a service

        Return a port of a list of ports
        """
        attrs = self.containers[service_name].inspect()
        ports = [int(p.split("/")[0]) for p in attrs["NetworkSettings"]["Ports"]]
        return ports[0] if len(ports) == 1 else ports

    def container_env(self, service_name):
        """ get the related environment of a service
        """
        container = self.containers[service_name]
        return {
            e.split("=")[0]: e.split("=")[1]
            for e in container.inspect()["Config"]["Env"]
        }

    def wait_for_running_state(self):
        NotImplemented
