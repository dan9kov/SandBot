import socket
import time
import keyboard
import cv2
import cv2.aruco as aruco
import numpy as np

esp_start = True
cam = True

if esp_start:
    print("подключение esp")
    ESP32_IP = "192.168.0.101"  # Замените на реальный IP
    PORT = 1234
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ESP32_IP, PORT))

mot_left = 0
mot_right = 0
baraban = 0
speed_baraban = 175
sost = 21

max_otklon_serva = 21

flag = True
flag1 = True
flag2 = True

kp = 0.8
speed_forward_motors = 30
speed_turn_motors = 50
turn_check = 10

colors = (0, 255, 0)

aruci = {"robot": False, "left_up": False, "right_up": False, "left_down": False, "right_down": False}
aruci_coordinates_offset = {"robot": (0, 0), "left_up": (0, 0), "right_up": (0, 0), "left_down": (0, 0), "right_down": (0, 0)}
aruci_coordinates = {"robot": (0, 0), "left_up": (0, 0), "right_up": (0, 0), "left_down": (0, 0), "right_down": (0, 0)}
kub_coordinates = {"left_up": [0, 0], "right_up": [0, 0], "left_down": [0, 0], "right_down": [0, 0]}
offset_robot_up = (120, 70)
offset_robot_down = (150, 90)
robot_angle = 0

data_str = ""


def key_connect():
    global mot_left
    global mot_right
    global baraban
    global sost
    global flag
    global flag1
    global flag2
    global speed_baraban
    speed = 70
    if keyboard.is_pressed('w') and not (keyboard.is_pressed('a') or keyboard.is_pressed('d')): # прямо
        mot_left = speed
        mot_right = speed
    elif keyboard.is_pressed('a') and not keyboard.is_pressed('w'): # танк влево
        mot_left = -speed
        mot_right = speed
    elif keyboard.is_pressed('d') and not keyboard.is_pressed('w'): # танк вправо
        mot_left = speed
        mot_right = -speed
    elif keyboard.is_pressed('a') and keyboard.is_pressed('w'):  # одной влево
        mot_left = 0
        mot_right = speed
    elif keyboard.is_pressed('d') and keyboard.is_pressed('w'):  # одной вправо
        mot_left = speed
        mot_right = 0
    elif keyboard.is_pressed('s'):
        mot_left = -speed
        mot_right = -speed
    else:
        mot_left = 0
        mot_right = 0
    if keyboard.is_pressed('u'):
        sost = max_otklon_serva

    if keyboard.is_pressed('b') and flag:
        flag = False
    if not keyboard.is_pressed('b') and not flag:
        flag = True
        if baraban:
            baraban = 0
        else:
            baraban = speed_baraban

    if keyboard.is_pressed('y') and flag1:
        flag1 = False
    if not keyboard.is_pressed('y') and not flag1:
        flag1 = True
        sost += 1

    if keyboard.is_pressed('h') and flag2:
        flag2 = False
    if not keyboard.is_pressed('h') and not flag2:
        flag2 = True
        sost -= 1

    if sost > max_otklon_serva:
        sost = max_otklon_serva
    elif sost < -max_otklon_serva:
        sost = -max_otklon_serva

    if keyboard.is_pressed('1'):
        speed_baraban = 25 * 1
    if keyboard.is_pressed('2'):
        speed_baraban = 25 * 2
    if keyboard.is_pressed('3'):
        speed_baraban = 25 * 3
    if keyboard.is_pressed('4'):
        speed_baraban = 25 * 4
    if keyboard.is_pressed('5'):
        speed_baraban = 25 * 5
    if keyboard.is_pressed('6'):
        speed_baraban = 25 * 6
    if keyboard.is_pressed('7'):
        speed_baraban = 25 * 7
    if keyboard.is_pressed('8'):
        speed_baraban = 25 * 8
    if keyboard.is_pressed('9'):
        speed_baraban = 25 * 9
    if keyboard.is_pressed('0'):
        speed_baraban = 255
    print("клавиатура ")

def send():
    global data_str
    global mot_left
    global mot_right
    global baraban
    global sost
    data_str = str(mot_left) + ' ' + str(mot_right) + ' '
    if baraban:
        data_str += str(speed_baraban) + ' '
    else:
        data_str += str(baraban) + ' '
    data_str += str(sost) + ' \n'
    s.send(data_str.encode())
    #print("отправил " + data_str)

# def print_on_video(aru = False):
#     y = 10
#     x = 40
#     cv2.putText(frame, f"L motor: {mot_left}", (y, x), cv2.FONT_HERSHEY_SIMPLEX, 0.5, colors, 1)
#     cv2.putText(frame, f"R motor: {mot_right}", (y, 2 * x), cv2.FONT_HERSHEY_SIMPLEX, 0.5, colors, 1)
#     cv2.putText(frame, f"Baraban: {baraban} speed: {speed_baraban}", (y, 3 * x), cv2.FONT_HERSHEY_SIMPLEX, 0.5, colors, 1)
#     cv2.putText(frame, f"Height: {sost}", (y, 4 * x), cv2.FONT_HERSHEY_SIMPLEX, 0.5, colors, 1)
#     if aru:
#         cv2.putText(frame, f"robot: {aruci["robot"]} {aruci_coordinates_offset["robot"]}", (y, 5 * x), cv2.FONT_HERSHEY_SIMPLEX, 0.5, colors, 1)
#         cv2.putText(frame, f"left_up: {aruci["left_up"]} {aruci_coordinates_offset["left_up"]}", (y, 6 * x), cv2.FONT_HERSHEY_SIMPLEX, 0.5, colors, 1)
#         cv2.putText(frame, f"right_up: {aruci["right_up"]} {aruci_coordinates_offset["right_up"]}", (y, 7 * x), cv2.FONT_HERSHEY_SIMPLEX, 0.5, colors, 1)
#         cv2.putText(frame, f"left_down: {aruci["left_down"]} {aruci_coordinates_offset["left_down"]}", (y, 8 * x), cv2.FONT_HERSHEY_SIMPLEX, 0.5, colors, 1)
#         cv2.putText(frame, f"right_down: {aruci["right_down"]} {aruci_coordinates_offset["right_down"]}", (y, 9 * x), cv2.FONT_HERSHEY_SIMPLEX, 0.5, colors, 1)

def stop_motors():
    global mot_left
    global mot_right
    mot_left = 0
    mot_right = 0
    send()
    mot_left = 0
    mot_right = 0
    send()
    mot_left = 0
    mot_right = 0
    send()

def follow_line_forward(data_y, data_x, go_up):
    global mot_left
    global mot_right
    global kp
    err = 0
    u = 0
    while aruci_coordinates["robot"][1] > data_y and go_up:
        check_cam()
        err = data_x - aruci_coordinates["robot"][0]
        print(data_y, aruci_coordinates["robot"][1])
        u = err * kp
        mot_left = speed_forward_motors + u
        mot_right = speed_forward_motors - u
        send()
        #print_on_video(True)
        robot_is_destroy()
    while aruci_coordinates["robot"][1] < data_y and not go_up:
        check_cam()
        err = data_x - aruci_coordinates["robot"][0]
        print(data_y, aruci_coordinates["robot"][1])
        u = err * kp
        mot_left = speed_forward_motors - u
        mot_right = speed_forward_motors + u
        send()
        #print_on_video(True)
        robot_is_destroy()
    stop_motors()

def turn_right(angle):
    # global mot_left
    # global mot_right
    # while (((robot_angle < angle or robot_angle <= 180 and robot_angle >= 0) and angle < 0)
    #        or ((robot_angle < angle or robot_angle > -180 and robot_angle < 0) and angle >= 0)):
    #     print(robot_angle)
    #     check_cam()
    #     mot_left = speed_forward_motors
    #     mot_right = 0
    #     send()
    # stop_motors()
    global mot_left
    global mot_right
    global turn_check
    l = angle - turn_check
    if angle - turn_check < -180:
        l += 360
    r = angle + turn_check
    if angle + turn_check > 180:
        r -= 360
    while robot_angle < l or robot_angle > r:
        print(robot_angle)
        check_cam()
        mot_left = speed_forward_motors
        mot_right = -speed_forward_motors
        send()
    stop_motors()

def turn_left(angle):
    global mot_left
    global mot_right
    global turn_check
    l = angle - turn_check
    if angle - turn_check < -180:
        l += 360
    r = angle + turn_check
    if angle + turn_check > 180:
        r -= 360
    while robot_angle < l or robot_angle > r:
        print(robot_angle)
        check_cam()
        mot_left = -speed_forward_motors
        mot_right = speed_forward_motors
        send()
    stop_motors()

def robot_is_destroy(destroy = False):
    global mot_left
    global mot_right
    global baraban
    global speed_baraban
    global sost
    if keyboard.is_pressed('q') or destroy:
        mot_left = 0
        mot_right = 0
        baraban = 0
        speed_baraban = 175
        sost = 21
        cap.release()
        cv2.destroyAllWindows()
        if esp_start:
            send()
            s.close()
        exit(0)

def check_cam():
    robot_is_destroy()

    global robot_angle
    ret, frame = cap.read()
    if not ret:
        print("Не удалось считать кадр")
        robot_is_destroy(True)

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Преобразование цветного изображения в черно-белое
    corners, ids, rejectedImgPoints = detector.detectMarkers(gray_frame)
    height, width = frame.shape[:2]
    center_x, center_y = width // 2, height // 2
    aruci = {"robot": False, "left_up": False, "right_up": False, "left_down": False, "right_down": False}

    if ids is not None:
        aruco.drawDetectedMarkers(frame, corners, ids)
        for i in range(len(ids)):
            # Получаем координаты углов маркера
            marker_corners = corners[i][0]  # Углы маркера в формате (x, y)
            marker_id = ids[i][0]  # ID маркера

            # Вычисляем центр маркера
            marker_center_x = int(np.mean(marker_corners[:, 0]))  # Среднее по x-координатам углов
            marker_center_y = int(np.mean(marker_corners[:, 1]))  # Среднее по y-координатам углов

            # Вычисляем смещение маркера относительно центра кадра
            offset_x = marker_center_x - center_x
            offset_y = marker_center_y - center_y

            # Вычисляем расстояние до маркера
            marker_width = np.linalg.norm(marker_corners[0] - marker_corners[1])  # Длина верхней стороны маркера
            distance = (marker_size * focal_length) / marker_width  # Расчет расстояния по формуле

            vector_x = marker_corners[1][0] - marker_corners[0][0]
            vector_y = marker_corners[1][1] - marker_corners[0][1]
            angle = np.degrees(np.arctan2(vector_y, vector_x))

            # Выводим ID, координаты центра и смещение
            # print(f"Marker ID: {marker_id}")
            # print(f"Marker Center: ({marker_center_x}, {marker_center_y})")
            # print(f"Offset from Center: (X: {offset_x}, Y: {offset_y})")
            #print(f"Rotation Angle: {angle} degrees")

            # Отображение информации на изображении
            cv2.putText(frame, f"ID: {marker_id}", (marker_center_x, marker_center_y - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, colors, 2)
            cv2.putText(frame, f"Offset: (X: {offset_x}, Y: {offset_y})", (marker_center_x, marker_center_y - 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, colors, 2)
            cv2.putText(frame, f"Angle: {angle:.2f} deg", (marker_center_x, marker_center_y - 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, colors, 2)

            # Рисуем центр маркера и центр кадра
            cv2.circle(frame, (marker_center_x, marker_center_y), 5, (0, 255, 0), -1)  # Центр маркера
            # cv2.circle(frame, (center_x, center_y), 5, (255, 0, 0), -1)  # Центр кадра

            if marker_id == 0:
                aruci["robot"] = True
                aruci_coordinates_offset["robot"] = (offset_x, offset_y)
                aruci_coordinates["robot"] = (marker_center_x, marker_center_y)
                robot_angle = angle
            if marker_id == 3:
                aruci["left_up"] = True
                aruci_coordinates_offset["left_up"] = (offset_x, offset_y)
                aruci_coordinates["left_up"] = (marker_center_x, marker_center_y)
            if marker_id == 1:
                aruci["right_up"] = True
                aruci_coordinates_offset["right_up"] = (offset_x, offset_y)
                aruci_coordinates["right_up"] = (marker_center_x, marker_center_y)
            if marker_id == 4:
                aruci["left_down"] = True
                aruci_coordinates_offset["left_down"] = (offset_x, offset_y)
                aruci_coordinates["left_down"] = (marker_center_x, marker_center_y)
            # if marker_id == 2:
            #     aruci["right_down"] = True
            #     aruci_coordinates_offset["right_down"] = (offset_x, offset_y)
            #     aruci_coordinates["right_down"] = (marker_center_x, marker_center_y)

            # mot_left = speed_loc - offset_x
            # mot_right = speed_loc + offset_x

    pts = np.array([[aruci_coordinates["right_up"][0] - offset_robot_up[0], aruci_coordinates["right_up"][1] + offset_robot_up[1]],
         [aruci_coordinates["left_up"][0] + offset_robot_up[0], aruci_coordinates["left_up"][1] + offset_robot_up[1]],
         [aruci_coordinates["left_down"][0] + offset_robot_down[0], aruci_coordinates["left_down"][1] - offset_robot_down[1]],
         [aruci_coordinates["right_up"][0] + (aruci_coordinates["left_up"][0] - aruci_coordinates["left_down"][0]) - offset_robot_down[0],
          aruci_coordinates["left_down"][1] - offset_robot_down[1]]], np.int32)
    kub_coordinates["right_up"] = [aruci_coordinates["right_up"][0] - offset_robot_up[0], aruci_coordinates["right_up"][1] + offset_robot_up[1]]
    kub_coordinates["left_up"] = [aruci_coordinates["left_up"][0] + offset_robot_up[0], aruci_coordinates["left_up"][1] + offset_robot_up[1]]
    kub_coordinates["left_down"] = [aruci_coordinates["left_down"][0] + offset_robot_down[0], aruci_coordinates["left_down"][1] - offset_robot_down[1]]
    kub_coordinates["right_down"] = [aruci_coordinates["right_up"][0] + (aruci_coordinates["left_up"][0] - aruci_coordinates["left_down"][0]) - offset_robot_down[0],
          aruci_coordinates["left_down"][1] - offset_robot_down[1]]

    pts = pts.reshape((-1, 1, 2))
    #print(kub_coordinates)
    #cv2.polylines(frame, [pts], True, colors, 3)

    cv2.line(frame, (kub_coordinates["left_up"][0], kub_coordinates["left_up"][1]), (kub_coordinates["left_up"][0], kub_coordinates["left_down"][1]), colors, 3)

    cv2.imshow('frame', frame)
    time.sleep(0.005)
    cv2.waitKey(1)

if cam:
    print("подключение камеры")
    marker_size = 0.066
    focal_length = 650

    dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_100)
    parameters = cv2.aruco.DetectorParameters()
    detector = cv2.aruco.ArucoDetector(dictionary, parameters)

    cap = cv2.VideoCapture(0)

print("запуск")
while True:
    if keyboard.is_pressed('w'):
        print("ручное управление\n")
        while not keyboard.is_pressed('z'):
            key_connect()
            send()
            check_cam()
    if keyboard.is_pressed('t'):
        print("автономное управление\n")
        follow_line_forward(kub_coordinates["left_up"][1], kub_coordinates["left_up"][0], True)
        turn_right(-10)
        follow_line_forward(kub_coordinates["left_down"][1], kub_coordinates["left_down"][0], False)
    if cam:
        check_cam()


robot_is_destroy(True)