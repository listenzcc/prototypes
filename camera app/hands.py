import cv2
import mediapipe as mp
import numpy as np

# 初始化MediaPipe手部模型
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# 打开摄像头
cap = cv2.VideoCapture(0)

# 初始化绘图相关变量
drawing = False  # 是否正在绘制
last_point = None  # 上一个绘制点
trail_points = []  # 存储所有轨迹点
trail_image = None  # 存储轨迹图像

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("无法获取摄像头画面")
        break

    # 转换颜色空间 BGR to RGB
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # 处理手部检测
    results = hands.process(image)

    # 转换回BGR用于显示
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # 如果有检测到手
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # 绘制手部关键点
            mp_drawing.draw_landmarks(
                image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # 获取关键点坐标
            landmarks = hand_landmarks.landmark
            hand_points = np.array([[lm.x * image.shape[1], lm.y * image.shape[0]]
                                    for lm in landmarks], dtype=np.int32)

            # 手指关键点索引 (MediaPipe的手部21个关键点)
            # 指尖: 4(拇指), 8(食指), 12(中指), 16(无名指), 20(小指)
            # 指节: 3, 7, 11, 15, 19
            fingertips = [4, 8, 12, 16, 20]
            finger_joints = [3, 7, 11, 15, 19]

            fingertips = [8, 12, 16, 20]
            finger_joints = [7, 11, 15, 19]

            # 检测每根手指是否伸直 (指尖y坐标 < 指节y坐标)
            finger_states = []
            for tip, joint in zip(fingertips, finger_joints):
                if tip == 4:  # 拇指特殊处理
                    # 使用x坐标判断，因为拇指运动方向不同
                    if hand_points[tip][0] < hand_points[joint][0]:
                        finger_states.append(True)  # 拇指伸直
                    else:
                        finger_states.append(False)  # 拇指弯曲
                else:
                    if hand_points[tip][1] < hand_points[joint][1]:
                        finger_states.append(True)  # 手指伸直
                    else:
                        finger_states.append(False)  # 手指弯曲

            # 手势识别逻辑
            # 1. 检测食指伸出，其他手指弯曲
            if (finger_states[0] == True and  # 食指伸直
                    all(f == False for i, f in enumerate(finger_states) if i != 0)):  # 其他手指弯曲
                gesture = "Pointing (Index Finger)"
                index_tip = hand_points[8]  # 食指尖坐标(第8个关键点)
                drawing = True

                # 添加到轨迹点
                if last_point is None:
                    last_point = index_tip
                trail_points.append(index_tip)

            # 2. 检测握拳 (所有手指弯曲)
            elif all(f == False for f in finger_states):
                gesture = "Fist"
                drawing = False
                last_point = None
                # 清除轨迹
                trail_points = []
                trail_image = np.zeros_like(frame)

            # 3. 检测张开手掌 (所有手指伸直)
            elif all(f == True for f in finger_states):
                gesture = "Open Hand"
                last_point = None

            # 4. 其他手势
            else:
                gesture = "Other Gesture"
                last_point = None

            # 显示识别结果
            cv2.putText(image, f"Gesture: {gesture}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # 绘制轨迹
    if len(trail_points) > 1:
        for i in range(1, len(trail_points)):
            cv2.line(trail_image, tuple(trail_points[i-1]), tuple(trail_points[i]),
                     (0, 0, 255), 5)  # 红色线条，粗细为5

    # 合并原始图像和轨迹图像
    if trail_image is None:
        combined_image = image
    else:
        combined_image = cv2.addWeighted(image, 0.8, trail_image, 0.8, 0)

    # 显示画面
    # cv2.imshow('Hand Gesture Recognition', image)
    cv2.imshow('Hand Gesture Recognition', combined_image)

    # 按'q'退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放资源
cap.release()
cv2.destroyAllWindows()
