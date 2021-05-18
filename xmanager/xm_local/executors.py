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
"""Local backend executors."""

from typing import Optional

import attr
from xmanager import xm


GOOGLE_KUBERNETES_ENGINE_CLOUD_PROVIDER = 'GOOGLE_KUBERNETES_ENGINE'


class LocalSpec(xm.ExecutorSpec):
  """Current machine executor's specification."""


class Local(xm.Executor):
  """Current machine executor."""

  @classmethod
  def Spec(cls):
    return LocalSpec()


@attr.s(auto_attribs=True)
class TpuCapability:
  """TPU capability configures the TPU software requested by an executor."""

  # Read about TPU versions:
  # https://cloud.google.com/tpu/docs/version-switching
  tpu_runtime_version: str


@attr.s(auto_attribs=True)
class CaipSpec(xm.ExecutorSpec):
  """Caip spec describes the Google Cloud Platform (GCP) location."""

  # An image registry name tag to push.
  # The image tag should be in the form 'myregistryhost/name:tag'
  push_image_tag: Optional[str] = None


@attr.s(auto_attribs=True)
class Caip(xm.Executor):
  """Caip Executor describes the runtime environment of GCP."""

  resources: xm.JobRequirements
  tpu_capability: Optional[TpuCapability] = None

  @classmethod
  def Spec(cls, *args, **kwargs):
    return CaipSpec(*args, **kwargs)


@attr.s(auto_attribs=True)
class KubernetesSpec(xm.ExecutorSpec):
  """K8s spec describes the K8s location."""

  # An image registry name tag to push.
  # The image tag should be in the form 'myregistryhost/name:tag'
  push_image_tag: Optional[str] = None


@attr.s(auto_attribs=True)
class Kubernetes(xm.Executor):
  """K8s Executor describes the runtime environment of Kubernetes."""

  resources: xm.JobRequirements
  cloud_provider: str = GOOGLE_KUBERNETES_ENGINE_CLOUD_PROVIDER
  tpu_capability: Optional[TpuCapability] = None

  @classmethod
  def Spec(cls, *args, **kwargs):
    return KubernetesSpec(*args, **kwargs)
