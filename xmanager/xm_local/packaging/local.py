# Copyright 2021 DeepMind Technologies Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Tools for local packaging."""

import os
from typing import Any

from xmanager import xm
from xmanager.bazel import client as bazel_client
from xmanager.cloud import build_image
from xmanager.docker import docker_adapter
from xmanager.xm import executables
from xmanager.xm import pattern_matching
from xmanager.xm_local import executables as local_executables


def _package_container(packageable: xm.Packageable,
                       container: executables.Container) -> xm.Executable:
  if not os.path.exists(container.image_path):
    raise ValueError(f'{container.image_path} does not exist on this machine')
  image_id = docker_adapter.instance().load_image(container.image_path)
  return local_executables.LoadedContainerImage(
      image_id=image_id, args=packageable.args, env_vars=packageable.env_vars)


def _package_binary(packageable: xm.Packageable, binary: executables.Binary):
  if not os.path.exists(binary.path):
    raise ValueError(f'{binary.path} does not exist on this machine')
  return local_executables.LocalBinary(
      path=binary.path, args=packageable.args, env_vars=packageable.env_vars)


def _package_python_container(packageable: xm.Packageable,
                              py_executable: executables.PythonContainer):
  image_id = build_image.build(py_executable, packageable.args,
                               packageable.env_vars)
  return local_executables.LoadedContainerImage(image_id=image_id)


def _package_bazel_container(
    packageable: xm.Packageable,
    container: executables.BazelContainer) -> xm.Executable:
  paths = bazel_client.build_single_target(container.label)
  assert len(paths) == 1
  image_id = docker_adapter.instance().load_image(paths[0])
  return local_executables.LoadedContainerImage(
      image_id=image_id, args=packageable.args, env_vars=packageable.env_vars)


def _package_bazel_binary(packageable: xm.Packageable,
                          binary: executables.BazelBinary) -> xm.Executable:
  paths = bazel_client.build_single_target(binary.label)
  assert len(paths) == 1
  return local_executables.LocalBinary(
      path=paths[0], args=packageable.args, env_vars=packageable.env_vars)


def _throw_on_unknown_executable(packageable: xm.Packageable, executable: Any):
  raise TypeError('Unsupported executable specification '
                  f'for local packaging: {executable!r}')


_LOCAL_PACKAGING_ROUTER = pattern_matching.match(
    _package_bazel_binary,
    _package_bazel_container,
    _package_binary,
    _package_container,
    _package_python_container,
    _throw_on_unknown_executable,
)


def package_for_local_executor(packageable: xm.Packageable,
                               executable_spec: xm.ExecutableSpec):
  return _LOCAL_PACKAGING_ROUTER(packageable, executable_spec)