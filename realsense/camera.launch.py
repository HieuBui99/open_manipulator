import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():

    camera_usb = IncludeLaunchDescription(
        PythonLaunchDescriptionSource('usb_cam.launch.py'),
    )
    camera_realsense = IncludeLaunchDescription(
        PythonLaunchDescriptionSource('realsense_cam.launch.py'),
        # launch_arguments={
        #     'camera_name': 'realsense',
        #     'camera_namespace': 'realsense'
        # }.items()
    )

    return LaunchDescription([
        # camera_realsense
        camera_usb,
        TimerAction(period=10.0, actions=[camera_realsense]),
    ])