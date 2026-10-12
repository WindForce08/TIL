Written for: the teammates who will SSH into the Pi and run the tests on the real hardware (one operator and one person supporting the camera).

# 라이브 테스트 가이드: 탐색 모드, 0.5 rad/s, 경계 정지

순서는 저속에서 정격 속도로, 탐색을 끈 상태에서 켠 상태로 진행합니다. 각 단계를 통과해야 다음 단계로 넘어갑니다. 명령은 모두 Pi에서 실행합니다.

## 0. 공통

**인원**
- 조작자 1명: 명령을 입력합니다.
- 지지자 1명: 카메라 옆에 있다가 reset, 토크 해제, FAULT 때 카메라를 받칩니다.

**모든 터미널에서 먼저 실행할 것**
```bash
source /opt/ros/lyrical/setup.bash
M=$HOME/git/Lv2_EYE4_Assignment/lv2_module5        # Pi의 실제 저장소 경로로 바꿀 것
source $M/ros2_ws/install/setup.bash
export ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST
CFG=$(ros2 pkg prefix realsense_tracker)/share/realsense_tracker/config
PORT=/dev/serial/by-id/usb-ROBOTIS_OpenCR_Virtual_ComPort_in_FS_Mode_FFFFFFFEFFFF-if00
```

**정지 명령은 터미널 하나에 미리 입력해 둡니다**
```bash
ros2 service call /control/enable std_srvs/srv/SetBool "{data: false}"   # 추적·탐색 정지 (ARM·토크 유지)
ros2 service call /opencr/disarm std_srvs/srv/Trigger                     # 구동 허가 해제
```
- 비상시에는 opencr_node 터미널에서 Ctrl+C를 누릅니다. bridge는 0.15 s, 보드는 300 ms 안에 두 축을 멈춥니다.

**바로 중단해야 하는 경우**
- 오차가 커지는 쪽으로 돈다
- 진동하거나 처진다
- 케이블이 당기거나 기구가 닿을 것 같다
- FAULT가 난다
- 경계에서 멈추지 않는다

## 1. 준비: 코드 옮기기, 빌드, 사전 시험 (모터 무관)

이번 변경은 아직 커밋되지 않았습니다. 브랜치에 커밋·push한 뒤 Pi에서 pull하는 방법을 권장합니다. bag 기록 도구가 기준 commit을 남기기 때문입니다.

```bash
cd $M/ros2_ws && colcon build --symlink-install --packages-select realsense_tracker_interfaces realsense_tracker
source install/setup.bash
cd $M && PYTHONPATH=ros2_ws/src/realsense_tracker python3 -m unittest discover -s ros2_ws/src/realsense_tracker/test
cd $M/firmware/opencr/tests
g++ -std=c++17 -Wall -Wextra -Werror -I native_stubs test_integrated_native.cpp -o /tmp/native-dry && /tmp/native-dry
g++ -std=c++17 -Wall -Wextra -Werror -DENABLE_MOTOR_OUTPUT=1 -I native_stubs test_integrated_native.cpp -o /tmp/native-live && /tmp/native-live
```

**통과 기준**
- 단위 시험: `Ran 50 tests ... OK`
- host 시험: `PASS native controller scenarios MODE=DRY`, `MODE=LIVE_STUB`
- PTY 시험(선택): [firmware/opencr/README.md](lv2_module5/firmware/opencr/README.md) 4절

## 2. 단계 1: DRY 펌웨어를 실제 보드에서 (모터 전원 OFF)

[펌웨어 README](lv2_module5/firmware/opencr/README.md) 2절을 그대로 따릅니다. DRY로 빌드·업로드한 뒤 `test_2axis_dry.py`를 실행합니다.

**통과 기준**: `ALL TWO-AXIS DRY CHECKS PASSED`

## 3. 단계 2: LIVE 펌웨어, ROS 없이

1. **기구 간섭 확인.** 토크가 꺼진 상태에서 Tilt를 손으로 받친 채 카메라를 돌려 봅니다.
   - 범위: 중앙 기준 Pan ±115°, Tilt ±55°
   - 케이블이 걸리거나 기구가 부딪히면 진행을 중단합니다. 펌웨어 경계 값을 줄여야 합니다.
2. **LIVE 빌드·업로드.** 펌웨어 README 3절 명령을 씁니다(`-DENABLE_MOTOR_OUTPUT=1`, DRY와 다른 빌드 폴더). **이전 LIVE 펌웨어로는 시험할 수 없습니다.**
3. **원점 잡기.** 카메라를 기구 중앙(정면, 수평)에 두고 손으로 멈춰 둡니다. CHECK 때의 자세가 원점이 되고, 경계는 이 원점을 기준으로 정해집니다.
4. **miniterm 확인** (`python3 -m serial.tools.miniterm $PORT 115200`)
   - `STATUS`에 `MODE=LIVE`가 보여야 합니다.
   - `CHECK`, `HOLD`를 보낸 뒤 `STATUS`가 `DISARMED GOAL=0,0 VEL=0,0 TORQUE=1,1`이어야 합니다.
   - 처짐이 없으면 Ctrl+]로 나옵니다.
5. **단일 명령 시험.** `bench_2axis_once.py --port $PORT --execute-live --case zero`를 먼저 실행하고, 이어서 `pan-left`, `pan-right`, `tilt-up`, `tilt-down`, `both`를 하나씩 실행합니다.

> ⚠ **`tilt-up`과 `tilt-down`이라는 이름은 재조립 전 기준입니다.** `tilt-up`은 Tilt 원시 −0.024를 보냅니다. 2026-10-07 재조립 기록대로라면 지금은 `tilt-up`을 실행하면 카메라가 **아래로** 갑니다. 그래서 case 이름이 아니라 "원시 + 명령을 보내면 어느 쪽으로 가는가"로 기록합니다.

| 기록할 것 | control.yaml이 가정한 값 |
|---|---|
| Pan 원시 + | 좌측 (`pan_direction: -1`) |
| Tilt 원시 + | 위쪽 (`tilt_direction: -1`). 아래쪽이면 단계 3에서 +1로 바꿔 확인 |

마치면 bench가 timeout으로 DISARM합니다. 단계 3은 새로 BOOT한 상태에서 시작해야 하므로 **카메라를 받친 채 OpenCR를 reset**합니다.

## 4. 단계 3: ROS 폐루프 0.2 rad/s, 탐색 OFF (방향 확인)

**준비**: 카메라를 기구 중앙에 둡니다. `RUN=live_dir_01; mkdir -p ~/runs`

```bash
# T1: bridge (이 단계에서는 모터가 움직이지 않음)
ros2 run realsense_tracker opencr_node --ros-args --params-file $CFG/opencr_live.yaml \
  -p csv_path:=$HOME/runs/${RUN}_serial.csv
# T2: 카메라 + 인지
ros2 launch realsense_tracker tracker.launch.py
# T3: 제어 (저속, 탐색 끔)
ros2 run realsense_tracker control_node --ros-args --params-file $CFG/control.yaml \
  -p pan_speed_limit_rad_s:=0.2 -p tilt_speed_limit_rad_s:=0.2 -p search_enabled:=false
# T4: 관찰 (창마다 하나씩)
ros2 topic echo /tracking_status ; ros2 topic echo /opencr/bridge_status ; ros2 topic echo /opencr/limit ; ros2 topic echo /target
```

**순서**
1. `ros2 service call /opencr/prepare std_srvs/srv/Trigger`를 실행하고 bridge가 `READY`가 되는지 봅니다. 이후에는 카메라를 손으로 돌리지 않습니다.
2. 목표를 정면에 두고 `/tracking_status`가 `TRACKING`인지 확인합니다.
3. `ros2 service call /opencr/arm std_srvs/srv/Trigger`를 실행하고 `ARMED`가 되는지 봅니다. ARM은 아래 두 조건을 모두 만족할 때만 받아들여집니다.
   - 제어가 움직이라는 명령(TRACKING)을 내고 있다
   - 카메라가 원점 ±120 counts(약 ±10°) 안에 정지해 있다
4. 목표를 천천히 오른쪽, 왼쪽, 위, 아래로 옮깁니다. `/target`의 x, y가 0 쪽으로 줄어드는지 봅니다.
5. 목표를 가립니다. 바로 `LOST`가 되며 멈춰야 하고, 다시 보이면 3프레임 뒤 `TRACKING`으로 돌아와야 합니다.

**오차가 커질 때**
1. enable false로 멈춥니다.
2. disarm합니다.
3. 카메라를 받친 채 reset하고 중앙에 둡니다.
4. control_node를 `-p tilt_direction:=1`(또는 해당 축 부호)로 다시 실행합니다.
5. prepare, arm을 다시 합니다.

**통과 기준**: 네 방향 모두 오차가 줄어들고 FAULT가 없습니다. 확정한 부호는 `control.yaml`과 `docs/hardware.md`에 기록합니다.

## 5. 단계 4: 경계 정지, 0.2 rad/s, 탐색 OFF

1. 목표를 천천히 한쪽으로 끌고 가서 카메라가 경계(Pan 약 ±115°, Tilt 약 ±55°)에서 멈추게 합니다. Pan +, Pan −, Tilt +, Tilt − 네 방향을 모두 합니다.
2. 경계에서 기대하는 동작:
   - `/opencr/limit`에 `pan:+1` 같은 메시지가 나온다
   - bridge는 **`ARMED`를 유지**한다(FAULT 아님)
   - `/tracking_status`는 `TRACKING`을 유지하고, 바깥쪽 명령만 막힌다
3. 목표를 안쪽으로 되돌리면 약 0.5 s 뒤 다시 따라와야 합니다.

**경계를 얼마나 넘었는지 확인** (`RUN`의 시리얼 CSV 사용):
```bash
python3 - $HOME/runs/${RUN}_serial.csv <<'EOF'
import csv, re, sys
rows = list(csv.reader(open(sys.argv[1])))[1:]
origin = None; peak = [0, 0]; after_check = False
for _, _, line in rows:
    if line.startswith('CHECK_OK'): after_check = True; continue
    m = re.search(r'POS=(-?\d+),(-?\d+)', line)
    if not (after_check and m): continue
    p = (int(m[1]), int(m[2]))
    if origin is None: origin = p; continue
    peak = [max(peak[i], abs(p[i] - origin[i])) for i in range(2)]
print('origin', origin, '| max |pos-origin| pan', peak[0], '(STOP 1305, FAULT 1365) tilt', peak[1], '(STOP 622, FAULT 682)')
print('limit events', sum('EVENT LIMIT STOPPED' in r[2] for r in rows), '| FAULT lines', sum('FAULT' in r[2] for r in rows))
EOF
```

**통과 기준**: 네 방향 모두 이벤트가 나오고, 최대값이 FAULT 경계보다 작습니다. 시뮬레이션에서는 STOP 경계를 최대 약 30 counts 넘었습니다.

## 6. 단계 5: 정격 0.5 rad/s, 탐색 OFF

1. T3를 `-p search_enabled:=false`만 붙여 다시 실행합니다(속도 상한은 기본 0.5). 실행 ID는 `RUN=live_fast_01`입니다.
   - control_node를 끄기 전에 **disarm을 먼저** 합니다. ARMED 상태에서 control_node가 꺼지면 bridge가 명령 끊김으로 FAULT가 됩니다.
2. 목표를 빠르게 움직이고 가렸다가 다시 보이게 합니다. 단계 4의 경계 시험도 반복합니다.

**통과 기준**
- `FAULT UNEXPECTED_SPEED`가 없다
- 가리면 바로 정지한다
- 경계를 넘은 거리가 FAULT 경계보다 작다

## 7. 단계 6: 탐색 ON (control.yaml 그대로)

**처음 한 번은 느리게 돌려 탐색 패턴의 모양만 봅니다.** 속도를 낮추면 한 방향 시간 상한도 함께 늘려야 경계까지 갑니다.
```bash
ros2 run realsense_tracker control_node --ros-args --params-file $CFG/control.yaml \
  -p search_speed_rad_s:=0.2 -p search_leg_timeout_sec:=40.0 -p search_timeout_sec:=300.0
```
그다음 `-p` 없이 기본값(0.4 rad/s, 120 s)으로 반복합니다. ARM은 반드시 **TRACKING일 때** 합니다. SEARCHING 중에 ARM하면 바로 탐색 동작이 시작됩니다.

| # | 시험 | 기대 결과 |
|---|---|---|
| 6-1 | **발제 필수**: 2 s 가림 후 시야 안에서 재등장, 5회 | 매번 LOST 후 TRACKING으로 복귀. **SEARCHING이 나오면 안 됨.** `recovery_trials.csv`에 기록 |
| 6-2 | 3 s 넘게 가린 뒤 목표를 범위 안 다른 위치로 옮김 | 3 s 뒤 SEARCHING. 먼저 지금 높이에서 Pan을 훑고, 찾으면 3프레임 뒤 TRACKING |
| 6-3 | 목표를 아예 치움 | Pan을 양 끝까지 훑은 뒤 Tilt 끝으로 가서 줄 단위로 훑음. 120 s 안에 IDLE(search_done), 모터 정지, bridge는 ARMED 유지. 시뮬레이션 기준 약 82 s |
| 6-4 | 6-3 뒤 목표를 시야에 넣음 | TRACKING. IDLE에서 탐색을 반복하지 않음 |
| 6-5 | 추적 중 목표를 Pan 경계 바깥(카메라 옆·뒤)으로 | 경계 정지 → SEARCHING → 다시 찾음 → 또 경계 → **IDLE(out_of_range)**. 목표를 안쪽으로 되돌리면 TRACKING |
| 6-6 | SEARCHING 중 enable false | 바로 정지, IDLE(disabled). enable true 후 목표가 보이면 추적 |

- IDLE이 된 이유(`search_done`, `out_of_range`)는 `/tracking_status`에는 나오지 않습니다. **control_node 로그의 상태 전이 줄**에서 확인합니다.
- 탐색 중 `/opencr/limit` 이벤트가 나올 때마다 bridge는 ARMED를 유지해야 합니다. 시리얼 CSV에 FAULT가 0건이어야 합니다.

## 8. 단계 7: 탐색 중 연결 끊김

| 시험 (SEARCHING 중에) | 기대 결과 | 다음 할 일 |
|---|---|---|
| T2(카메라·인지) Ctrl+C | 0.5 s 뒤 LOST·정지. **이후 탐색을 시작하지 않음** | T2 재실행 |
| T3(control_node) Ctrl+C | bridge가 0.15 s 뒤 `ROS_COMMAND_TIMEOUT`으로 DISARM·FAULT | 재시작 절차 |
| `pkill -9 -f opencr_node` | 보드가 300 ms timeout으로 두 축 0, DISARM | 재시작 절차 |

- **재시작 절차**: 카메라를 받친 채 reset → 중앙에 두기 → opencr_node 재실행 → prepare → 목표를 TRACKING으로 → arm. 자동 재ARM은 없습니다.
- 결과는 `interruption_trials.csv`에 적습니다.

## 9. 종료
1. enable false
2. disarm
3. 카메라를 받친다
4. opencr_node를 종료한다
5. miniterm에서 `SUPPORTED_OFF`를 보내고 `TORQUE_OFF_CONFIRMED`를 확인한다

포트를 닫는 것만으로는 토크가 꺼지지 않습니다.

## 10. 남길 기록
- **실행 ID**: 단계마다 하나씩 정합니다(`live_dir_01`, `live_fast_01`, `search_01` 등). 시리얼 CSV와 `tools/tracking_logger.py --run-id $RUN`에 같은 이름을 씁니다. 대표 장면은 `tools/bag_record.sh $RUN --duration 20 --archive`로 남깁니다.
- **`docs/hardware.md`에 기록할 것**
  - 단계 2의 원시 부호와 방향
  - 확정한 `tilt_direction`
  - 기구 간섭 여부
  - 경계별 최대 |pos−origin|
  - 탐색 완료 시간
- **실패한 회차도 지우지 않습니다.**

---

이 가이드는 지금 출력만 했고 파일로는 저장하지 않았습니다. 원하면 `lv2_module5/docs/`에 md로 넣겠습니다. 작성하면서 확인했는데, README 10절의 "단위 시험 32개"는 지금 50개입니다. README 12·14절의 "중립 자세 Pan 3078" 조건도 현재 펌웨어(CHECK 때 멈춘 자세를 원점으로 씀)와 맞지 않습니다. 이 두 가지는 수정하지 않았습니다.