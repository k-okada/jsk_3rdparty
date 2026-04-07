# Eye Display Module

[![PlatformIO Build Workflow](https://github.com/sktometometo/eye-display/actions/workflows/main.yml/badge.svg)](https://github.com/sktometometo/eye-display/actions/workflows/main.yml)
[![Cakin Build and PlatformIO Build Workflow](https://github.com/sktometometo/eye-display/actions/workflows/full.yml/badge.svg)](https://github.com/sktometometo/eye-display/actions/workflows/full.yml)

https://github.com/user-attachments/assets/e2b44bc5-4f85-489f-b862-e851fd4cdf32

Eye Display Module

## Supported devices

1. Round Display Module with M5Stamp C3 (pio env name: `stampc3`) : https://www.switch-science.com/products/8098
2. Round Display Module with M5Stamp S3 (pio env name: `stamps3`) : https://www.switch-science.com/products/8971

## How to use

### Installation

First you have to install ROS and PlatformIO

```bash
pip install platformio
```

And then, you can build and upload the firmware to the device.

It is recommended to put this repo in a catkin workspace.

```bash
mkdir ~/catkin_ws/src
cd ~/catkin_ws
catkin init
cd ~/catkin_ws/src
git clone https://github.com/jsk-ros-pkg/jsk_3rdparty.git
cd eye_display
rosdep install --from-paths . --ignore-src -y -r
catkin build eye_display
source ~/catkin_ws/devel/setup.bash
```
If you do not want to download all jsk_3rdparty files, pleasea check `How to clone only this package` section.

### Simple demo


https://github.com/user-attachments/assets/e2b44bc5-4f85-489f-b862-e851fd4cdf32


You can check basic functionalities with a demo firmware.

```bash
roscd eye_display
pio run -e stampc3-ros
pio run -e stampc3-ros -t uploadfs --upload-port <port to device>
pio run -e stampc3-ros -t upload --upload-port <port to device>
```

Please replace `stampc3` with `stamps3` if you use type 2 device.

After building and uploading the firmware, you can control the device through ROS topic

```bash
roslaunch eye_display demo.launch port:=<port to device> mode_right:=<true or false>
```

Then you can control the device with the demo scripts.

```bash
rosrun eye_display pub_eye_status.py
```

```bash
rosrun eye_display demo_move_eye.py
```


You can also directly control pupil position by publish a message to "/eye_display/look_at" topic.

```bash
rostopic pub -1 /eye_display/look_at geometry_msgs/Point "{x: 40.0, y: -10.0, z: 0.0}"

```

You can control emotion expression with eye by publishing a message to "/eye_display/eye_status" topic.

```bash
rostopic pub -1 /eye_display/eye_status std_msgs/String "data: 'happy'"
```

To get the list of  emotional expression of the eyes, you can use following command.

```bash
$rosparam get eye_display/eye_asset/names
[normal, blink, surprised, sleepy, angry, sad, happy]
```

#### I2C version

If you want to control the device through I2C bus, please use following env.

- `stampc3-i2c`: Stamp C3 device
- `stamps3-i2c`: Stamp S3 device

```bash
roscd eye_display
pio run -e stampc3-i2c
pio run -e stampc3-i2c -t uploadfs --upload-port <port to device>
pio run -e stampc3-i2c -t upload --upload-port <port to device>
```

Then you can control the device with I2C.

```bash
roslaunch eye_display demo.launch use_i2c:=true i2c_device:=<device number> i2c_bus:=<bus number>
```

See `node_scripts/ros_to_i2c.py` for control protocol.

To monitor the serial output in the dual I2C mode. Use the following logger tool.

```bash
./node_scripts/dual_serial_logger.py /dev/ttyACM0 /dev/ttyACM1 115200
```
#### Dual eye mode

You can start two device with `demo_dual.launch`

```bash
roslaunch eye_display demo_dual.launch use_i2c:=false port_right:=/dev/ttyACM0 port_left:=/dev/ttyACM1 baud:=115200 debug:=true
```

You can control dual eye status with demo scripts
```bash
rosrun eye_display pub_eye_status.py --dual --rate 0.3 --names sleepy surprised happy
```

#### extra images

If you need more than the standard images (outline, iris, pupil, reflex, upperlid), use the extra　images.


```
  path_extra1: "/krmt_reflex_shine1.png"
  extra1_default_pos_x: 75
  extra1_default_pos_y: 75
  extra1_default_theta: 0
  extra1_position_x: [  0,  20, 40,  20,   0, -20, -40, -20]
  extra1_position_y: [ 40,  20,  0, -20, -40, -20,   0,  20]
  extra1_rotation_theta: [  0,  40,  80,  40,  0,  -40, -80, -40]
  extra1_zoom: [  1.0, 1.1, 1.2, 1.3, 1.4, 1.2, 1.0, 0.8, 0.7, 0.8, 0.9]
  path_extra2: "/krmt_reflex_heart.png"
  extra2_position_x: [  0,  20,   0, -20]
  extra2_position_y: [  0,  10,   0, -10]
  extra2_rotation_theta: [  0,  -40,  -80,  -40,  0,  40, 80, 40]
  extra2_zoom: [1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 1.5, 1.0, 0.5]
  extra2_default_pos_x: 75
  extra2_default_pos_y: 75
  extra2_default_theta: 0
```

#### Advanced control

You can control the eye status in more detail through the `eye_status` topics.
Use the following low-level commands.
`<emotion>` is defined in the names list in the configuration YAML file (e.g., `names: [normal, happy, blink]`).
`<type>` can be one of `iris`, `pupil`, `reflex`, `upperlid`, `extra1`, `extra2`.

```
eye_asset_image_path: <emotion>: <type>: <file name>
eye_asset_default_pos_x: <emotion>: <type>: <value>
eye_asset_default_pos_y: <emotion>: <type>: <value>
eye_asset_default_theta: <emotion>: <type>: <value in degree>
eye_asset_default_zoom: <emotion>: <type>: <value>
eye_asset_position_x: <emotion>: <type>: <comma separated values>
eye_asset_position_y: <emotion>: <type>: <comma separated values>
eye_asset_rotation_theta: <emotion>: <type>: <comma separated values>
eye_asset_zoom: <emotion>: <type>: <comma separated values>
```

### How to control with joystick
```
roslaunch eye_display control_eye_with_joystick.launch
```

### Description of direction

![eye_display_direction](./doc/eye_display_direction.svg)

### How to update image

![eye_layer_structure](./doc/eye_structure.svg)

## Robot Integration Development (로봇 탑재 개발)

### 현재 하드웨어 구성

| 항목 | 내용 |
|------|------|
| 눈 모듈 | M5Stamp S3 × 2 (240×240 GC9A01 원형 디스플레이) |
| 연결 방식 | USB → rosserial (USB CDC, baud 무관) |
| 포트 고정 | udev symlink (`/etc/udev/rules.d/99-eyemodule.rules`) |

```
/dev/ttyACM-lefteye   → 왼쪽 눈 (serial: F4:12:FA:9D:8E:94)
/dev/ttyACM-righteye  → 오른쪽 눈 (serial: 70:04:1D:D3:DD:7C)
```

좌우 전환 시 `/etc/udev/rules.d/99-eyemodule.rules`에서 symlink 이름만 교체 후:
```bash
sudo udevadm control --reload-rules && sudo udevadm trigger
```

### 펌웨어 빌드 & 플래시

```bash
cd ~/catkin_ws/src/jsk_3rdparty/eye_display

# 빌드
pio run -e stamps3-ros

# 펌웨어 업로드
pio run -e stamps3-ros -t upload --upload-port /dev/ttyACM-lefteye
pio run -e stamps3-ros -t upload --upload-port /dev/ttyACM-righteye

# 이미지(SPIFFS) 업로드 (펌웨어 최초 설치 시 또는 이미지 변경 시)
pio run -e stamps3-ros -t uploadfs --upload-port /dev/ttyACM-lefteye
pio run -e stamps3-ros -t uploadfs --upload-port /dev/ttyACM-righteye
```

### 듀얼 눈 실행

```bash
# 터미널 1: 눈 모듈 rosserial 연결
roslaunch eye_display demo_dual.launch \
  port_left:=/dev/ttyACM-lefteye \
  port_right:=/dev/ttyACM-righteye \
  direction_left:=4 \
  direction_right:=4

# 터미널 2: 조이스틱 제어
roslaunch eye_display control_eye_with_joystick.launch
```

### ROS 토픽 구조

```
/left/eye_display/look_at    (geometry_msgs/Point)  - 시선 좌표 (x, y: 픽셀 오프셋)
/right/eye_display/look_at   (geometry_msgs/Point)
/left/eye_display/eye_status (std_msgs/String)       - 감정 (normal/blink/happy/...)
/right/eye_display/eye_status(std_msgs/String)
```

### 앞으로의 개발 계획 (로봇 통합)

#### 1단계: 깊이 카메라 시선 추적 (SR300)
- `gaze_target_node.py`: 뎁스 카메라로 가장 가까운 사람 위치 감지 → `/gaze_target` 발행
- `gaze_controller.py`: 3D 좌표 → 양안 시선각 변환 → `look_at` 토픽 발행
- 관련 파라미터: `camera_y_offset`, `ipd`, `angle_scale`, `smoothing_factor`

#### 2단계: 로봇 동작과 연동
- 로봇 컴퓨터의 ROS 토픽(손/관절 좌표 등)을 구독하여 시선 자동 생성
- 예: `/right_hand_pose` (geometry_msgs/PoseStamped) → 손 방향으로 시선 이동
- 구현 방향: 별도 `robot_gaze_controller.py` 작성, `/gaze_target` 토픽에 발행

#### 3단계: 주변 사람 인식 반응
- 카메라(RGB 또는 뎁스) 기반 사람 감지
- 감지된 사람 방향으로 시선 이동 + 감정 표현 변화
- 구현 방향: OpenCV/MediaPipe 또는 YOLO 기반 face/body 감지 → `/gaze_target` 발행

#### 토픽 연동 설계 (예시)
```
[로봇 컴퓨터]                    [눈 모듈 컴퓨터]
/right_hand_pose ───────────────→ robot_gaze_controller.py
/person_detected ───────────────→        ↓
/camera/depth    ───────────────→ /gaze_target (geometry_msgs/Point)
                                         ↓
                                  gaze_controller.py
                                         ↓
                            /left/eye_display/look_at
                            /right/eye_display/look_at
```

## For Developers

### How to update msg

Message headers in [`lib/ros_lib`](./lib/ros_lib/) directory are automatically generated with `make_libraries.py` script in `rosserial_arduino` package.

And this repo provide easy way to update `ros_lib` as [update_ros_lib.sh](./scripts/update_ros_lib.sh).

So if you want to update message definition in [`msg`](./msg/) directory, please run the following command.

```bash
catkin build eye_display
source <path/to/catkin_ws>/devel/setup.bash
rosrun eye_display update_ros_lib.sh
```

### How to clone only this package

This feature requires git 2.27+, so if you use Ubuntu<=20.04, please install latest version of git https://git-scm.com/downloads/linux

```
git clone --filter=blob:none --sparse https://github.com/jsk-ros-pkg/jsk_3rdparty.git
cd jsk_3rdparty
git sparse-checkout set eye_display
git checkout eye_display
```
