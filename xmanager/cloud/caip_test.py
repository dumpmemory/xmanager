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
"""Tests for xmanager.cloud.caip."""

import unittest

from xmanager import xm
from xmanager.xm_local import executables as local_executables
from xmanager.xm_local import executors as local_executors

from xmanager.cloud import caip  # pylint: disable=g-bad-import-order


class CaipTest(unittest.TestCase):

  def test_get_machine_spec_default(self):
    job = xm.Job(
        executable=local_executables.GoogleContainerRegistryImage(''),
        executor=local_executors.Caip(resources=xm.JobRequirements()),
        args={})
    machine_spec = caip.get_machine_spec(job)
    self.assertDictEqual(machine_spec, {'machineType': 'n1-standard-4'})

  def test_get_machine_spec_cpu(self):
    job = xm.Job(
        executable=local_executables.GoogleContainerRegistryImage(''),
        executor=local_executors.Caip(
            resources=xm.JobRequirements(cpu=20, ram=40)),
        args={})
    machine_spec = caip.get_machine_spec(job)
    self.assertDictEqual(machine_spec, {'machineType': 'n1-highcpu-64'})

  def test_get_machine_spec_gpu(self):
    job = xm.Job(
        executable=local_executables.GoogleContainerRegistryImage(''),
        executor=local_executors.Caip(resources=xm.JobRequirements(p100=2)),
        args={})
    machine_spec = caip.get_machine_spec(job)
    self.assertDictEqual(
        machine_spec, {
            'machineType': 'n1-standard-4',
            'acceleratorType': 'nvidia_tesla_p100',
            'acceleratorCount': '2',
        })

  def test_get_machine_spec_tpu(self):
    job = xm.Job(
        executable=local_executables.GoogleContainerRegistryImage(''),
        executor=local_executors.Caip(resources=xm.JobRequirements(v3=8)),
        args={})
    machine_spec = caip.get_machine_spec(job)
    self.assertDictEqual(
        machine_spec, {
            'machineType': 'n1-standard-4',
            'acceleratorType': 'tpu_v3',
            'acceleratorCount': '8',
        })

  def test_cpu_ram_to_machine_type_exact(self):
    self.assertEqual('n1-standard-16', caip.cpu_ram_to_machine_type(16, 60))

  def test_cpu_ram_to_machine_type_highmem(self):
    self.assertEqual('n1-highmem-64', caip.cpu_ram_to_machine_type(1, 415))

  def test_cpu_ram_to_machine_type_highcpu(self):
    self.assertEqual('n1-highcpu-64', caip.cpu_ram_to_machine_type(63, 1))

  def test_cpu_ram_to_machine_type_too_high(self):
    with self.assertRaises(ValueError):
      caip.cpu_ram_to_machine_type(1000, 1000)


if __name__ == '__main__':
  unittest.main()