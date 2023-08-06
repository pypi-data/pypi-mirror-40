import os

from hokusai.lib.command import command
from hokusai.lib.config import config
from hokusai.lib.common import shout
from hokusai.lib.exceptions import HokusaiError

@command()
def build():
  docker_compose_yml = os.path.join(os.getcwd(), 'hokusai/build.yml')
  legacy_docker_compose_yml = os.path.join(os.getcwd(), 'hokusai/common.yml')
  if not os.path.isfile(docker_compose_yml) and not os.path.isfile(legacy_docker_compose_yml):
    raise HokusaiError("Yaml files %s / %s do not exist." % (docker_compose_yml, legacy_docker_compose_yml))

  if os.path.isfile(docker_compose_yml):
    shout("docker-compose -f %s -p hokusai build" % docker_compose_yml, print_output=True)
  if os.path.isfile(legacy_docker_compose_yml):
    shout("docker-compose -f %s -p hokusai build" % legacy_docker_compose_yml, print_output=True)
