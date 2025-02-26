#!/usr/bin/env python3

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import math
from tf.transformations import quaternion_from_euler

def movebase_client(goal_x, goal_y):
    # 创建一个名为 "move_base" 的动作客户端，使用 MoveBaseAction 消息类型
    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)

    # 等待服务器启动
    client.wait_for_server()

    # 创建目标点
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"  # 使用 "map" 坐标系
    goal.target_pose.header.stamp = rospy.Time.now()

    # 设置目标位置
    goal.target_pose.pose.position.x = goal_x
    goal.target_pose.pose.position.y = goal_y

    # 计算偏航角（yaw）
    yaw = math.atan2(goal_y - 0, goal_x - 0)  # 假设机器人初始位置在 (0,0)
    quaternion = quaternion_from_euler(0, 0, yaw)

    # 设置目标的朝向
    goal.target_pose.pose.orientation.x = quaternion[0]
    goal.target_pose.pose.orientation.y = quaternion[1]
    goal.target_pose.pose.orientation.z = quaternion[2]
    goal.target_pose.pose.orientation.w = quaternion[3]

    # 发送目标到服务器
    client.send_goal(goal)

    # 等待结果
    wait = client.wait_for_result()
    if not wait:
        rospy.logerr("Action server not available!")
        rospy.signal_shutdown("Action server not available!")
        return False
    else:
        # 返回结果
        return client.get_result()

if __name__ == '__main__':
    try:
        # 初始化节点
        rospy.init_node('movebase_client_py')

        # 从命令行获取目标位置
        import sys
        if len(sys.argv) != 3:
            rospy.loginfo("Usage: movebase.py goal_x goal_y")
            sys.exit(1)

        goal_x = float(sys.argv[1])
        goal_y = float(sys.argv[2])

        result = movebase_client(goal_x, goal_y)
        if result:
            rospy.loginfo("Goal execution done!")
    except rospy.ROSInterruptException:
        rospy.loginfo("Navigation test finished.")

