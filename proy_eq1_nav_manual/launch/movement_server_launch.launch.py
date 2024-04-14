from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='proy_eq1_nav_manual',
            executable='movement_server',
            output='screen'
        ),
    ])
