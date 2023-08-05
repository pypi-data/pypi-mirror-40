import os
import subprocess
import uuid
import pytest
from compose.cli.main import TopLevelCommand
from compose.cli.main import project_from_options
from compose.cli.docopt_command import DocoptDispatcher


class DockercConfig:
    """ Format pytest options to docker-compose parameters
    """

    def __init__(self, config):
        opts = config.option
        self.run = not opts.dockerc_norun
        self.options = {}
        self.up_options = {}

        self.projectdir = opts.dockerc_projectdir or str(config.rootdir)
        self.options["--project-directory"] = self.projectdir
        if self.run:
            self.options["--project-name"] = self.generate_project_name()
        if opts.dockerc_filepath:
            self.options["--file"] = [opts.dockerc_filepath]

        if opts.dockerc_build is True:
            self.up_options["--build"] = True
        if opts.dockerc_services:
            self.up_options["SERVICE"] = opts.dockerc_services
        self.up_options["--detach"] = True

    def generate_project_name(self):
        """ Create a compose project

        The basename of the compose directory is used plus a random suffix, in order
        to run several tests suites in the same hosts.
        """
        return "{0}-{1}".format(
            os.path.basename(self.options["--project-directory"]),
            str(uuid.uuid4()).split("-")[0],
        )


@pytest.fixture(scope="session")
def dockerc_config(request):
    """ Return config parameter to init Compose project
    """
    return DockercConfig(request.config)


@pytest.fixture(scope="session")
def dockerc(dockerc_config):
    """ Run, manage and stop Docker Compose project from Docker API

    This fixture loads the `docker-compose.yml` file, then it runs
    command like `docker-compose up --build` at the beginning of the fixture,
    and `docker-compose down` at the end.

    Return a `compose.project.Project`_ object to deal with your containers.

    .. _compose.project.Project: https://github.com/docker/compose/blob/master/compose/project.py

    """  # noqa
    docopt = DocoptDispatcher(TopLevelCommand, {})
    project = project_from_options(
        dockerc_config.projectdir, options=dockerc_config.options
    )
    cmd = TopLevelCommand(project)

    if dockerc_config.run:
        opts = docopt.parse("up")[2]
        opts.update(dockerc_config.up_options)
        cmd.up(opts)

    yield project

    if dockerc_config.run:
        cmd.down(docopt.parse("down")[2])


@pytest.fixture(scope="session")
def dockerc_logs(dockerc_config):
    """ Display the logs of the Compose project
    """
    if dockerc_config.run:
        cmd = ["docker-compose"]
        for k, v in dockerc_config.options.items():
            cmd.append(k)
            cmd.append(v)
        cmd.extend(["logs", "-f"])

        proc = subprocess.Popen(cmd)
        yield proc
        proc.terminate()
    else:
        yield
