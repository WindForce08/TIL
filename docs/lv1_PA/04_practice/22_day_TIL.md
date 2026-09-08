> 2026-9-2 
>
> 학습내용 : 

# 4×4 동차변환 모듈 & 최소자승법

> Physical AI / Robotics Study Notes

## 0. 학습 목표

``` text
4×4 동차변환과 최소자승법을 처음 배우는 상황에서,
좌표계 → 회전 → 이동 → 동차변환 → 역변환 → 최소자승법의 흐름을 이해하고,
실제 로봇 개발에서 어떻게 사용되는지 연결한다.
```

``` mermaid
flowchart TD
    A[3D 좌표] --> B[회전 R]
    A --> C[이동 t]
    B --> D[4×4 동차변환 T]
    C --> D
    D --> E[Point / Direction]
    D --> F[좌표계 변환]
    F --> G[역변환 T⁻¹]
    H[센서 측정값] --> I[오차]
    I --> J[최소자승법]
    J --> K[가장 잘 맞는 값 추정]
```

------------------------------------------------------------------------

# 1. 좌표계(Frame)

로봇은 **어디에 있는지(Position)**와 **어느 방향을
보는지(Orientation)**를 알아야 한다.

  정보          의미             예시
  ------------- ---------------- ---------------------
  Position      어디에 있는가?   `(x,y,z)=(2,1,0.5)`
  Orientation   어느 방향인가?   Z축 기준 90°

로봇에는 여러 좌표계가 존재한다.

``` text
World Frame
    │
    └── Robot/Base Frame
            ├── Camera Frame
            └── LiDAR Frame
```

따라서 실제 로봇에서는

> Camera에서 측정한 점을 Robot 좌표계로 어떻게 바꿀 것인가?

가 중요한 문제가 된다.

------------------------------------------------------------------------

# 2. 회전(Rotation)

## 2.1 회전행렬

2차원 회전행렬:

$$
R =
\begin{bmatrix}
\cos\theta & -\sin\theta \\
\sin\theta & \cos\theta
\end{bmatrix}
$$

3차원에서는 `3×3` 회전행렬을 사용한다.

$$
R =
\begin{bmatrix}
r_{11}&r_{12}&r_{13}\\
r_{21}&r_{22}&r_{23}\\
r_{31}&r_{32}&r_{33}
\end{bmatrix}
$$

## 2.2 로봇에서의 사용

-   로봇 자세(Orientation)
-   카메라 방향
-   LiDAR → Robot 좌표 변환
-   IMU 자세 추정
-   로봇팔 End-Effector 방향
-   SLAM

------------------------------------------------------------------------

# 3. 이동(Translation)

3차원 이동벡터:

$$
t =
\begin{bmatrix}
t_x\\
t_y\\
t_z
\end{bmatrix}
$$

예:

$$
t =
\begin{bmatrix}
0.20\\
0.00\\
0.50
\end{bmatrix}
$$

→ 로봇 기준으로 카메라가 `20 cm` 앞쪽, `50 cm` 위쪽에 있다는 의미로
사용할 수 있다.

실제 로봇에서는 센서 장착 위치(Extrinsic Calibration)를 표현할 때
중요하다.

------------------------------------------------------------------------

# 4. 동차좌표(Homogeneous Coordinates)

일반적인 3D 점:

$$
p =
\begin{bmatrix}
x\\y\\z
\end{bmatrix}
$$

동차좌표:

$$
\tilde p =
\begin{bmatrix}
x\\y\\z\\1
\end{bmatrix}
$$

핵심은 **마지막에 1을 붙여 회전과 이동을 하나의 행렬곱으로 처리할 수
있게 만드는 것**이다.

일반적인 변환은:

$$
p'=Rp+t
$$

이다.

------------------------------------------------------------------------

# 5. 4×4 동차변환

3차원 동차변환:

$$
\boxed{
T=
\begin{bmatrix}
R&t\\
0&1
\end{bmatrix}}
$$

실제로는:

$$
T=
\begin{bmatrix}
r_{11}&r_{12}&r_{13}&t_x\\
r_{21}&r_{22}&r_{23}&t_y\\
r_{31}&r_{32}&r_{33}&t_z\\
0&0&0&1
\end{bmatrix}
$$

``` text
┌─────────────────┬──────────┐
│       R         │    t     │
│     3 × 3       │   3 × 1  │
│    Rotation     │Translation│
├─────────────────┼──────────┤
│   0   0   0     │    1     │
└─────────────────┴──────────┘
```

> **4×4 동차변환 = 회전 + 이동**

------------------------------------------------------------------------

# 6. Point와 Direction

## 6.1 Point

점은 위치를 가지므로:

$$
\boxed{
\tilde p=
\begin{bmatrix}
p\\1
\end{bmatrix}}
$$

3D:

$$
[x,y,z,1]^T
$$

변환하면:

$$
T
\begin{bmatrix}
p\\1
\end{bmatrix}
=
\begin{bmatrix}
Rp+t\\1
\end{bmatrix}
$$

따라서 **회전 + 이동**이 적용된다.

## 6.2 Direction

방향은 특정 위치를 의미하지 않으므로:

$$
\boxed{
\tilde v=
\begin{bmatrix}
v\\0
\end{bmatrix}}
$$

변환하면:

$$
T
\begin{bmatrix}
v\\0
\end{bmatrix}
=
\begin{bmatrix}
Rv\\0
\end{bmatrix}
$$

따라서 **회전만 적용**된다.

  종류        동차 표현        회전   이동
  ----------- -------------- ------ ------
  Point       `[x,y,z,1]ᵀ`        O      O
  Direction   `[x,y,z,0]ᵀ`        O      X

------------------------------------------------------------------------

# A. 벡터의 정규화(Normalization)

벡터의 **방향은 유지하면서 크기를 1로 만드는 것**이다.

$$
\boxed{
\hat{v}=\frac{v}{\|v\|}
}
$$

* `v` : 원래 벡터
* `||v||` : 벡터의 크기
* `v̂` : 정규화된 벡터(Unit Vector)

## A.1 예제

$$
v=
\begin{bmatrix}
3\\
4
\end{bmatrix}
$$

벡터의 크기:

$$
\|v\|=\sqrt{3^2+4^2}=5
$$

정규화:

$$
\hat{v}
=
\frac{1}{5}
\begin{bmatrix}
3\\
4
\end{bmatrix}
=
\begin{bmatrix}
0.6\\
0.8
\end{bmatrix}
$$

따라서 **방향은 같고 크기는 1**이 된다.

## A.2 영벡터

영벡터는:

$$
v=
\begin{bmatrix}
0\\
0
\end{bmatrix}
$$

이므로:

$$
\|v\|=0
$$

정규화하면:

$$
\frac{v}{\|v\|}
=
\frac{v}{0}
$$

가 되어 **0으로 나누기가 발생한다.**

따라서:

$$
\boxed{\text{영벡터는 정규화할 수 없다.}}
$$

영벡터는 **방향 자체가 없기 때문**이다.

## 핵심 정리

> **벡터 정규화 = 벡터를 자신의 크기로 나누어 크기를 1로 만드는 것**

> **영벡터는 크기가 0이므로 정규화할 수 없다.**


------------------------------------------------------------------------

# 7. 실제 로봇: Camera → Robot

카메라가 물체를 발견했다고 하자.

카메라 좌표계에서:

$$
p_{camera}=
\begin{bmatrix}
1\\0.5\\2
\end{bmatrix}
$$

Camera → Robot 변환이 `T_robot_camera`라면:

$$
\boxed{
p_{robot}=T_{robot,camera}p_{camera}}
$$

``` mermaid
flowchart LR
    A[Camera] --> B[Object Detection]
    B --> C[Object Position<br/>Camera Frame]
    C --> D[T_robot_camera]
    D --> E[Object Position<br/>Robot Frame]
    E --> F[Motion Planner]
```

즉, 카메라가 얻은 좌표를 로봇이 이해할 수 있는 좌표로 바꾼다.

------------------------------------------------------------------------

# 8. 실제 로봇: LiDAR → Robot

UGV의 LiDAR가 측정한 Point Cloud는 LiDAR 좌표계에 있다.

``` text
LiDAR
  ↓
Point Cloud
  ↓
T_robot_lidar
  ↓
Robot Frame
  ↓
Obstacle Position
  ↓
Path Planning
```

$$
p_{robot}=T_{robot,lidar}p_{lidar}
$$

이런 좌표변환은 장애물 인식과 경로계획에 연결된다.

------------------------------------------------------------------------

# 9. 동차변환의 합성

여러 좌표계를 행렬곱으로 연결할 수 있다.

``` mermaid
flowchart LR
    W[World] -->|T_world_robot| R[Robot]
    R -->|T_robot_camera| C[Camera]
```

따라서:

$$
T_{world,camera}
=
T_{world,robot}T_{robot,camera}
$$

Camera의 점을 World로:

$$
p_{world}
=
T_{world,robot}
T_{robot,camera}
p_{camera}
$$

> **여러 좌표계의 관계를 행렬곱으로 연결한다.**

이 개념은 ROS TF/TF2 같은 좌표계 관리와 연결된다.

------------------------------------------------------------------------

# 10. 역변환(Inverse Transformation)

변환 방향을 반대로 바꾸고 싶을 때 사용한다.

Camera → Robot:

$$
T_{robot,camera}
$$

반대 방향:

$$
T_{camera,robot}
=
T_{robot,camera}^{-1}
$$

역변환 공식:

$$
\boxed{
T^{-1}=
\begin{bmatrix}
R^T&-R^Tt\\
0&1
\end{bmatrix}}
$$

회전행렬은:

$$
R^{-1}=R^T
$$

라는 성질을 가진다.

------------------------------------------------------------------------

# 11. 최소자승법(Least Squares)

동차변환과 최소자승법은 목적이 다르다.

  -----------------------------------------------------------------------
  개념                                핵심 질문
  ----------------------------------- -----------------------------------
  동차변환                            좌표를 어떻게 변환할까?

  최소자승법                          오차가 있는 데이터에서 가장
                                      그럴듯한 값을 어떻게 찾을까?
  -----------------------------------------------------------------------

실제 로봇 센서는 노이즈와 오차가 있기 때문에:

$$
Ax=b
$$

를 정확하게 만족하지 않을 수 있다.

그래서 가장 잘 맞는 `x`를 찾는다.

------------------------------------------------------------------------

# 12. 최소자승 문제

$$
\boxed{
\min_x\|Ax-b\|^2}
$$

  기호          의미
  ------------- ------------------
  `A`           데이터/모델 행렬
  `x`           찾고 싶은 미지수
  `b`           실제 측정값
  `Ax`          모델의 예측값
  `Ax-b`        오차
  `||Ax-b||²`   오차 제곱합

즉:

> **오차의 제곱합이 가장 작아지도록 `x`를 찾는다.**

------------------------------------------------------------------------

# 13. 직선 맞추기 예시

측정 데이터:

    x   측정 y
  --- --------
    1      2.1
    2      4.0
    3      6.2
    4      7.9

모델:

$$
y=ax+b
$$

데이터가 노이즈 때문에 완벽한 직선 위에 있지 않더라도, 전체 오차가 가장
작은 직선을 찾는다.

``` text
y
↑
│              ●
│          ●
│      ●
│  ●
│
└────────────────→ x
```

------------------------------------------------------------------------

# 14. 정규방정식(Normal Equation)

최소자승 문제:

$$
\min_x\|Ax-b\|^2
$$

를 풀면:

$$
\boxed{A^TAx=A^Tb}
$$

이것이 정규방정식이다.

역행렬이 존재하면:

$$
\boxed{x=(A^TA)^{-1}A^Tb}
$$

------------------------------------------------------------------------

# 15. 로봇에서 최소자승법 사용 사례

## 15.1 센서 데이터 보정

``` text
Sensor 1 ─┐
Sensor 2 ─┼──→ Estimation / Optimization ──→ Estimated State
Sensor 3 ─┘
```

사용 예:

-   위치 추정
-   속도 추정
-   센서 오프셋 추정
-   센서 캘리브레이션

## 15.2 Camera / LiDAR Calibration

``` mermaid
flowchart LR
    A[Camera Points] --> C[Correspondence]
    B[LiDAR Points] --> C
    C --> D[Optimization]
    D --> E[Estimated R, t]
    E --> F[T_camera_lidar]
```

센서 데이터로부터 가장 잘 맞는 `R`, `t`를 추정하고:

$$
T=
\begin{bmatrix}
R&t\\
0&1
\end{bmatrix}
$$

형태의 변환을 만들 수 있다.

## 15.3 위치 추정

``` text
GPS ──────┐
IMU ──────┼──→ State Estimation
Wheel ────┤
LiDAR ────┘
```

여러 센서의 오차가 있는 측정값을 이용해 로봇 상태를 추정한다.

------------------------------------------------------------------------

# 16. Python: 최소자승법

실제 개발에서는 수식을 직접 계산하기보다 NumPy 같은 라이브러리를
사용한다.

``` python
import numpy as np

# Ax = b
A = np.array([
    [1, 1],
    [2, 1],
    [3, 1],
    [4, 1]
])

b = np.array([
    2.1,
    4.0,
    6.2,
    7.9
])

# Least Squares
x, residuals, rank, s = np.linalg.lstsq(A, b, rcond=None)

print(x)
```

여기서 `x`는 `y=ax+b`의 `a`, `b`에 해당한다.

> 수치적으로는 직접 `(AᵀA)⁻¹Aᵀb`를 계산하기보다 `np.linalg.lstsq()` 같은
> 함수를 사용하는 편이 일반적으로 더 안정적이다.

------------------------------------------------------------------------

# 17. Python: 4×4 동차변환

``` python
import numpy as np

# Rotation matrix
R = np.array([
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 1]
])

# Translation vector
t = np.array([
    2,
    1,
    0.5
])

# 4x4 transformation matrix
T = np.eye(4)

T[:3, :3] = R
T[:3, 3] = t

print(T)
```

점에 적용:

``` python
p = np.array([
    1,
    2,
    3,
    1
])

p_new = T @ p

print(p_new)
```

수학적으로:

$$
p'=Rp+t
$$

를 계산한 것이다.

------------------------------------------------------------------------

# 18. 좌표변환 표기 읽는 법

  표현               의미
  ------------------ ----------------
  `T_world_robot`    Robot → World
  `T_robot_camera`   Camera → Robot
  `T_robot_lidar`    LiDAR → Robot
  `T_camera_robot`   Robot → Camera
  `T⁻¹`              변환 방향 반대

예:

$$
p_{world}=T_{world,robot}p_{robot}
$$

Camera → World:

$$
p_{world}
=
T_{world,robot}
T_{robot,camera}
p_{camera}
$$

------------------------------------------------------------------------

# 19. Physical AI 전체 연결

``` mermaid
flowchart TB
    S[Camera / LiDAR / IMU] --> P[Perception]
    P --> C[Sensor Coordinate]
    C --> T[4×4 Coordinate Transform]
    T --> R[Robot / World Coordinate]
    R --> E[State Estimation / Optimization]
    E --> L[Localization]
    E --> M[Motion Planning]
    M --> CTRL[Control]
    CTRL --> ACT[Motor / Actuator]
```

전체 흐름을 말로 정리하면:

``` text
센서가 데이터를 얻는다
        ↓
센서 좌표계에서 데이터가 나온다
        ↓
4×4 동차변환으로 좌표계를 변환한다
        ↓
센서 오차가 있으므로 상태를 추정한다
        ↓
최적화 / 최소자승 / 필터 등을 사용한다
        ↓
로봇과 주변 물체의 위치를 파악한다
        ↓
경로계획
        ↓
제어
        ↓
모터 구동
```

------------------------------------------------------------------------

# 20. 핵심 요약

## 동차변환

$$
\boxed{
T=
\begin{bmatrix}
R&t\\
0&1
\end{bmatrix}}
$$

``` text
R = 회전
t = 이동
T = 회전 + 이동
```

### Point

$$
[x,y,z,1]^T
$$

→ 회전 + 이동

### Direction

$$
[v_x,v_y,v_z,0]^T
$$

→ 회전만

### 역변환

$$
T^{-1}
=
\begin{bmatrix}
R^T&-R^Tt\\
0&1
\end{bmatrix}
$$

------------------------------------------------------------------------

## 최소자승법

$$
\boxed{
\min_x\|Ax-b\|^2}
$$

→ 오차가 가장 작은 `x`를 찾는다.

정규방정식:

$$
\boxed{
A^TAx=A^Tb}
$$

------------------------------------------------------------------------

# 21. 지금 외울 것 vs 나중에 이해할 것

## 지금 반드시 기억

  개념              기억
  ----------------- -------------------------
  `R`               회전
  `t`               이동
  `T`               회전 + 이동
  `T` 형태          `[[R,t],[0,1]]`
  Point             마지막 값 `1`
  Direction         마지막 값 `0`
  `T⁻¹`             반대 방향 변환
  Least Squares     오차가 가장 작도록 추정
  기본식            `min ||Ax-b||²`
  Normal Equation   `AᵀAx=Aᵀb`

## 아직 암기하지 않아도 되는 것

``` text
- 4×4 행렬의 모든 원소 암기
- 정규방정식의 유도 과정
- 회전행렬의 모든 증명
- 복잡한 센서 Calibration 수식
```

먼저 **각 수식이 왜 필요한지**를 이해하는 것이 우선이다.

------------------------------------------------------------------------

# 22. 다음 학습 순서

``` text
① 벡터와 행렬
      ↓
② 좌표계(Frame)
      ↓
③ 회전행렬 R
      ↓
④ 이동벡터 t
      ↓
⑤ 4×4 동차변환 T
      ↓
⑥ Point / Direction
      ↓
⑦ T의 곱셈과 좌표계 연결
      ↓
⑧ T⁻¹ 역변환
      ↓
⑨ 최소자승법
      ↓
⑩ Sensor Calibration / Localization
      ↓
⑪ ROS TF / TF2
      ↓
⑫ 실제 UGV / Robot 프로젝트
```

------------------------------------------------------------------------

# 최종 한 줄 정리

> **동차변환은 로봇의 좌표계를 서로 연결하는 도구이고, 최소자승법은
> 오차가 있는 데이터에서 가장 그럴듯한 값을 찾는 도구이다.**

Physical AI에서는 이 두 개념이

**Camera / LiDAR / IMU → 좌표변환 → 위치추정 → 경로계획 → 제어**

로 이어지는 기초가 된다.