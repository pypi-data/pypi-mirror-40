from decimal import Decimal, ROUND_DOWN, ROUND_UP
import logging
import os
import re
import shlex
import subprocess
from typing import Collection

import attr

from ai.backend.agent.accelerator import (
    AbstractAccelerator, AbstractAcceleratorInfo,
)
# from .nvidia import libcudart

log = logging.getLogger('ai.backend.accelerator.tpu')


@attr.s(auto_attribs=True)
class TPUAcceleratorInfo(AbstractAcceleratorInfo):

    # TODO: make this configurable
    unit_memory = (2 * (2 ** 30))  # 1 unit = 2 GiB
    unit_proc = 1                  # 1 unit = 1 TPU

    def max_share(self) -> Decimal:
        mem_shares = self.memory_size / self.unit_memory
        proc_shares = self.processing_units / self.unit_proc
        common_shares = min(mem_shares, proc_shares)
        quantum = Decimal('.01')
        return Decimal(common_shares).quantize(quantum, ROUND_DOWN)

    def share_to_spec(self, share: Decimal) -> (int, int):
        # TODO: consider the memory margin for heap size?
        return (
            int(self.unit_memory * share),
            int(self.unit_proc * share),
        )

    def spec_to_share(self, requested_memory: int,
                      requested_proc_units: int) -> Decimal:
        mem_share = requested_memory / self.unit_memory
        proc_share = requested_proc_units / self.unit_proc
        required_share = max(mem_share, proc_share)
        quantum = Decimal('.01')
        return Decimal(required_share).quantize(quantum, ROUND_UP)


class TPUAccelerator(AbstractAccelerator):

    slot_key = 'tpu'  # TODO: generalize

    ctpu_version = (0, 0)
    rx_ctpu_version = re.compile(r'^ctpu version: (\d+\.\d+)')

    num_devices = 0

    @classmethod
    def get_device_infos(cls):
        cmd = shlex.split('ctpu ls -no-header')
        ret = subprocess.run(cmd, stdout=subprocess.PIPE)
        dev_infos = ret.stdout.decode().strip().splitlines()
        return len(dev_infos), dev_infos

    @classmethod
    def list_devices(cls) -> Collection[TPUAcceleratorInfo]:
        all_devices = []
        num_devices, dev_infos = cls.get_device_infos()
        for dev_idx in range(num_devices):
            dev_name = dev_infos[dev_idx].split()[1]
            details = subprocess.run(['ctpu', 'status', '-details', '-name',
                                      dev_name], stdout=subprocess.PIPE)
            rx_hw_location = re.compile(r'\nCompute Engine Machine Type:(.+)\n')
            m = rx_hw_location.search(details.stdout.decode())
            if m is not None:
                hw_location = m.group(1).strip()
            else:
                hw_location = 'unknown'
            # TPU seems to use the memory of host compute instance.
            memory_size = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')
            dev_info = TPUAcceleratorInfo(
                device_id=dev_idx,
                hw_location=f'{hw_location}@{dev_name}',
                numa_node=None,
                memory_size=memory_size,
                processing_units=1,  # TPU sharing is not possible for now
            )
            all_devices.append(dev_info)
        return all_devices

    @classmethod
    async def generate_docker_args(cls, docker, numa_node, proc_shares):
        tpus = []
        tpu_names = []
        num_devices, dev_infos = cls.get_device_infos()
        for devidx in range(num_devices):
            if devidx not in proc_shares:
                tpus.append(devidx)
                tpu_names.append(f'TPU{dev_idx}_NAME={dev_infos[devidx].split()[1]}')
        # TODO: User code can access TPU with TPU_NAME environment variable. How to
        # make this eaiser if there are multiple TPU cores? Currently, we assume
        # there's only one TPU core.
        env = [
            f"TPU_VISIBLE_DEVICES={','.join(map(str, tpus))}",
            f'TPU_NAME={dev_infos[0].split()[1]}',
        ]
        env.extend(tpu_names)
        return {'Env': env}
