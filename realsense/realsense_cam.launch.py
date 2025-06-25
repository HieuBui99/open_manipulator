"""Launch realsense2_camera node."""
import copy
import os
import sys

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import OpaqueFunction
from launch.substitutions import LaunchConfiguration

# Add realsense2_camera/launch to sys.path using ROS package discovery
realsense2_camera_launch_dir = os.path.join(get_package_share_directory('realsense2_camera'),
                                            'launch')
sys.path.append(realsense2_camera_launch_dir)
import rs_launch  # noqa: E402, I100


local_parameters = [{'name': 'camera_name', 'default': 'd435i',
                     'description': 'camera1 unique name'},
                    {'name': 'camera_namespace', 'default': '',
                     'description': 'camera1 namespace'},
                    {'name': 'depth_module.depth_profile1', 'default': '480,270,15',
                     'description': 'depth stream profile for camera1'},
                    {'name': 'depth_module.color_profile1', 'default': '424,240,15',
                     'description': 'Depth module color stream profile for d405 camera1'},
                    ]


def set_configurable_parameters(local_params):
    return {param['original_name']: LaunchConfiguration(param['name'])
            for param in local_params}


def duplicate_params(general_params, posix):
    local_params = copy.deepcopy(general_params)
    for param in local_params:
        param['original_name'] = param['name']
        param['name'] += posix
    return local_params


def generate_launch_description():
    params1 = duplicate_params(rs_launch.configurable_parameters, '1')
    return LaunchDescription(
        rs_launch.declare_configurable_parameters(local_parameters) +
        rs_launch.declare_configurable_parameters(params1) +
        [
            OpaqueFunction(
                function=rs_launch.launch_setup,
                kwargs={
                    'params': set_configurable_parameters(params1),
                    'param_name_suffix': '1'
                }
            ),
        ]
    )