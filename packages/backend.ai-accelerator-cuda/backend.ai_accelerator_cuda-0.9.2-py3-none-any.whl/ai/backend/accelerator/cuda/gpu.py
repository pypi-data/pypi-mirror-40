from decimal import Decimal, ROUND_DOWN, ROUND_UP
import logging
from pathlib import Path
import re
from typing import Collection, Sequence

import attr
import requests

from ai.backend.agent.accelerator import (
    AbstractAccelerator, AbstractAcceleratorInfo,
)
from .nvidia import libcudart

log = logging.getLogger('ai.backend.accelerator.cuda')


@attr.s(auto_attribs=True)
class CUDAAcceleratorInfo(AbstractAcceleratorInfo):

    # TODO: make this configurable
    unit_memory = (2 * (2 ** 30))  # 1 unit = 2 GiB
    unit_proc = 8                  # 1 unit = 8 SMPs

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


class CUDAAccelerator(AbstractAccelerator):

    slot_key = 'gpu'  # TODO: generalize

    nvdocker_version = (0, 0, 0)
    rx_nvdocker_version = re.compile(r'^NVIDIA Docker: (\d+\.\d+\.\d+)')

    @classmethod
    def list_devices(cls) -> Collection[CUDAAcceleratorInfo]:
        all_devices = []
        num_devices = libcudart.get_device_count()
        for dev_idx in range(num_devices):
            raw_info = libcudart.get_device_props(dev_idx)
            sysfs_node_path = "/sys/bus/pci/devices/" \
                              f"{raw_info['pciBusID_str'].lower()}/numa_node"
            try:
                node = int(Path(sysfs_node_path).read_text().strip())
            except OSError:
                node = None
            dev_info = CUDAAcceleratorInfo(
                device_id=dev_idx,
                hw_location=raw_info['pciBusID_str'],
                numa_node=node,
                memory_size=raw_info['totalGlobalMem'],
                processing_units=raw_info['multiProcessorCount'],
            )
            all_devices.append(dev_info)
        return all_devices

    @classmethod
    def get_hooks(cls, distro: str, arch: str) -> Sequence[Path]:
        # TODO: implement
        return []

    @classmethod
    async def generate_docker_args(cls, docker, numa_node, proc_shares):
        if cls.nvdocker_version[0] == 1:
            try:
                r = requests.get('http://localhost:3476/docker/cli/json')
                nvidia_params = r.json()
                r = requests.get('http://localhost:3476/gpu/info/json')
                gpu_info = r.json()
            except requests.exceptions.ConnectionError:
                raise RuntimeError('NVIDIA Docker plugin is not available.')

            volumes = await docker.volumes.list()
            existing_volumes = set(vol['Name'] for vol in volumes['Volumes'])
            required_volumes = set(vol.split(':')[0]
                                   for vol in nvidia_params['Volumes'])
            missing_volumes = required_volumes - existing_volumes
            binds = []
            for vol_name in missing_volumes:
                for vol_param in nvidia_params['Volumes']:
                    if vol_param.startswith(vol_name + ':'):
                        _, _, permission = vol_param.split(':')
                        driver = nvidia_params['VolumeDriver']
                        await docker.volumes.create({
                            'Name': vol_name,
                            'Driver': driver,
                        })
            for vol_name in required_volumes:
                for vol_param in nvidia_params['Volumes']:
                    if vol_param.startswith(vol_name + ':'):
                        _, mount_pt, permission = vol_param.split(':')
                        binds.append('{}:{}:{}'.format(
                            vol_name, mount_pt, permission))
            devices = []
            for dev in nvidia_params['Devices']:
                m = re.search(r'^/dev/nvidia(\d+)$', dev)
                # Add nvidiactl, nvidia-uvm, ... etc.
                if m is None:
                    devices.append(dev)
                    continue
                dev_idx = int(m.group(1))
                # Only expose GPUs in the same NUMA node.
                if dev_idx not in proc_shares:
                    continue
                for gpu in gpu_info['Devices']:
                    if gpu['Path'] == dev:
                        try:
                            pci_id = gpu['PCI']['BusID'].lower()
                            pci_path = f"/sys/bus/pci/devices/{pci_id}/numa_node"
                            gpu_node = int(Path(pci_path).read_text().strip())
                        except FileNotFoundError:
                            gpu_node = None
                        # Even when numa_node file exists, gpu_node may become -1
                        # (e.g., Amazon p2 instances)
                        if gpu_node == -1:
                            gpu_node = None
                        if gpu_node is None or gpu_node == numa_node:
                            devices.append(dev)
            devices = [{
                'PathOnHost': dev,
                'PathInContainer': dev,
                'CgroupPermissions': 'mrw',
            } for dev in devices]
            return {
                'HostConfig': {
                    'Binds': binds,
                    'Devices': devices,
                },
            }
        elif cls.nvdocker_version[0] == 2:
            gpus = []
            num_devices = libcudart.get_device_count()
            for dev_idx in range(num_devices):
                if dev_idx in proc_shares:
                    # TODO: check numa node
                    gpus.append(dev_idx)
            return {
                'HostConfig': {
                    'Runtime': 'nvidia',
                },
                'Env': [
                    f"NVIDIA_VISIBLE_DEVICES={','.join(map(str, gpus))}",
                ],
            }
        else:
            raise RuntimeError('BUG: should not be reached here!')
