# Robotics Mathematics Study Notes

## 1. Document Title

Recommended English title for a document about high-school mathematics needed for robotics:

> **High School Math for Robotics**

Other considered titles:
- High School Mathematics for Robotics
- Robotics Math: High School Foundations
- High School Math Foundations for Robotics
- Math Foundations for Robotics

---

# 2. Vectors, Coordinates, and Bases

## 2.1 Vector

A vector has both **magnitude and direction**.

Examples in robotics:
- Position
- Velocity
- Acceleration
- Force
- Rotation axis

An \(n\)-dimensional vector can be represented by \(n\) components:

\[
\mathbf a=
\begin{bmatrix}
a_1\\
a_2\\
\vdots\\
a_n
\end{bmatrix}
\]

Basic operations:

\[
\mathbf a+\mathbf b
\]

\[
c\mathbf a
\]

\[
|\mathbf a|
=
\sqrt{a_1^2+\cdots+a_n^2}
\]

## 2.2 Coordinates and Basis

A coordinate such as

\[
(x,y,z)
\]

describes a point relative to a chosen coordinate system.

A **basis** is a minimal set of independent directions used to represent vectors.

For 3D space, the standard basis is commonly written as:

\[
\mathbf e_x=(1,0,0),\quad
\mathbf e_y=(0,1,0),\quad
\mathbf e_z=(0,0,1)
\]

## 2.3 Vector Space, Subspace, Dimension

- **Vector space:** a set of vectors closed under vector addition and scalar multiplication.
- **Subspace:** a subset that is itself a vector space.
- **Basis:** a minimal set of linearly independent vectors that spans a space.
- **Dimension:** the number of vectors in a basis.

For example:

- A line through the origin → dimension 1
- A plane through the origin → dimension 2
- \(\mathbb R^3\) → dimension 3

---

# 3. Matrix Multiplication

## 3.1 Multiplication Condition

For

\[
A_{m\times n}B_{p\times q}
\]

to be defined:

\[
\boxed{n=p}
\]

In other words:

> The number of columns of the first matrix must equal the number of rows of the second matrix.

The result has size:

\[
\boxed{m\times q}
\]

### Example

\[
(2\times3)(3\times2)
\]

is possible and produces:

\[
2\times2
\]

But:

\[
(2\times3)(2\times2)
\]

is impossible because:

\[
3\neq2
\]

## 3.2 Example

\[
A=
\begin{bmatrix}
1&2\\
3&4
\end{bmatrix},
\qquad
B=
\begin{bmatrix}
5&6\\
7&8
\end{bmatrix}
\]

Then:

\[
AB=
\begin{bmatrix}
1(5)+2(7)&1(6)+2(8)\\
3(5)+4(7)&3(6)+4(8)
\end{bmatrix}
\]

\[
=
\begin{bmatrix}
19&22\\
43&50
\end{bmatrix}
\]

Core rule:

> **Matrix multiplication = row of the first matrix × column of the second matrix**

## 3.3 Example: \(4\times2\) and \(3\times5\)

\[
(4\times2)(3\times5)
\]

is impossible because:

\[
2\neq3
\]

Reversing the order also does not work:

\[
(3\times5)(4\times2)
\]

because:

\[
5\neq4
\]

Therefore, these two matrices cannot be multiplied in either order.

---

# 4. Matrix Dimension vs. Transpose

The size of a matrix is usually written as:

\[
\text{rows}\times\text{columns}
\]

For example, a \(2\times3\) matrix has:
- 2 rows
- 3 columns

## 4.1 Transpose

A transpose swaps rows and columns.

For:

\[
A=
\begin{bmatrix}
1&2&3\\
4&5&6
\end{bmatrix}
\]

the transpose is:

\[
A^T=
\begin{bmatrix}
1&4\\
2&5\\
3&6
\end{bmatrix}
\]

Thus:

\[
\boxed{2\times3\rightarrow3\times2}
\]

A \(2\times3\) matrix absolutely can have a transpose.

## 4.2 Transpose vs. Matrix Multiplication

These are different concepts.

- Transpose: possible for every matrix.
- Matrix multiplication: only possible when the inner dimensions match.

For a \(2\times3\) matrix \(A\):

\[
AA
\]

is not defined because:

\[
(2\times3)(2\times3)
\]

has \(3\neq2\).

But:

\[
AA^T
\]

is defined:

\[
(2\times3)(3\times2)\rightarrow2\times2
\]

and:

\[
A^TA
\]

is defined:

\[
(3\times2)(2\times3)\rightarrow3\times3
\]

---

# 5. Symmetric + Skew-Symmetric Decomposition

A matrix can always be decomposed into:

\[
\boxed{
A=
\frac{A+A^T}{2}
+
\frac{A-A^T}{2}
}
\]

The first part is symmetric:

\[
S=\frac{A+A^T}{2},
\qquad S=S^T
\]

The second part is skew-symmetric (antisymmetric):

\[
K=\frac{A-A^T}{2},
\qquad K^T=-K
\]

## 5.1 Important Correction

The explanation:

> "It is used to remove matrices damaged by calculation errors and extract the usable matrix."

is misleading.

Symmetric + skew-symmetric decomposition is **not primarily a method for detecting or removing corrupted matrices**.

It is a method for:

> **Separating one matrix into two components with different mathematical properties.**

## 5.2 Numerical Example

\[
A=
\begin{bmatrix}
2&5\\
1&3
\end{bmatrix}
\]

Then:

\[
A^T=
\begin{bmatrix}
2&1\\
5&3
\end{bmatrix}
\]

Symmetric part:

\[
S=
\frac{A+A^T}{2}
=
\begin{bmatrix}
2&3\\
3&3
\end{bmatrix}
\]

Skew-symmetric part:

\[
K=
\frac{A-A^T}{2}
=
\begin{bmatrix}
0&2\\
-2&0
\end{bmatrix}
\]

Therefore:

\[
A=S+K
\]

## 5.3 Robotics Connection

In robotics and physics, this decomposition can help separate different types of behavior in mathematical models.

In particular, skew-symmetric matrices have an important connection to:
- Cross products
- Angular velocity
- Rotation
- Torque
- Robot dynamics

---

# 6. Cross Product

## 6.1 Definition

The cross product is an operation between two 3D vectors:

\[
\boxed{\mathbf a\times\mathbf b=\mathbf c}
\]

The result is another vector.

The result is perpendicular to both input vectors:

\[
\mathbf c\perp\mathbf a
\]

\[
\mathbf c\perp\mathbf b
\]

Therefore:

> **The cross product produces a vector perpendicular to the plane formed by the two input vectors.**

## 6.2 Magnitude

The magnitude is:

\[
\boxed{
|\mathbf a\times\mathbf b|
=
|\mathbf a||\mathbf b|\sin\theta
}
\]

This is equal to the area of the parallelogram formed by \(\mathbf a\) and \(\mathbf b\).

So the cross product contains two kinds of information:

- Magnitude → parallelogram area
- Direction → perpendicular to the two vectors

## 6.3 Direction: Right-Hand Rule

The direction is determined by the right-hand rule.

For:

\[
\mathbf a\times\mathbf b
\]

the direction follows the right-hand convention.

Changing the order reverses the direction:

\[
\boxed{
\mathbf a\times\mathbf b
=
-(\mathbf b\times\mathbf a)
}
\]

Therefore:

\[
\mathbf i\times\mathbf j=\mathbf k
\]

but:

\[
\mathbf j\times\mathbf i=-\mathbf k
\]

## 6.4 Simple Example

\[
\mathbf a=
\begin{bmatrix}
1\\0\\0
\end{bmatrix},
\qquad
\mathbf b=
\begin{bmatrix}
0\\1\\0
\end{bmatrix}
\]

Then:

\[
\mathbf a\times\mathbf b
=
\begin{bmatrix}
0\\0\\1
\end{bmatrix}
\]

or:

\[
\boxed{\mathbf i\times\mathbf j=\mathbf k}
\]

---

# 7. Cross Product as a Skew-Symmetric Matrix

For:

\[
\mathbf a=
\begin{bmatrix}
a_1\\
a_2\\
a_3
\end{bmatrix}
\]

define:

\[
[\mathbf a]_\times
=
\begin{bmatrix}
0&-a_3&a_2\\
a_3&0&-a_1\\
-a_2&a_1&0
\end{bmatrix}
\]

Then:

\[
\boxed{
[\mathbf a]_\times\mathbf b
=
\mathbf a\times\mathbf b
}
\]

For:

\[
\mathbf b=
\begin{bmatrix}
b_1\\b_2\\b_3
\end{bmatrix}
\]

we get:

\[
[\mathbf a]_\times\mathbf b
=
\begin{bmatrix}
a_2b_3-a_3b_2\\
a_3b_1-a_1b_3\\
a_1b_2-a_2b_1
\end{bmatrix}
\]

which is exactly the standard cross-product formula.

This creates an important robotics connection:

\[
\boxed{
\text{cross product}
\leftrightarrow
\text{skew-symmetric matrix}
}
\]

---

# 8. Why Vectors, Matrices, and Linear Algebra Matter in Robotics

The overall connection is:

```text
Vectors
   ↓
Position / velocity / acceleration / force
   ↓
Matrices
   ↓
Rotation / coordinate transformation
   ↓
Linear algebra
   ↓
Kinematics / sensors / control / SLAM
   ↓
Robotics
```

## 8.1 Vector → Position

A robot's 2D position can be represented as:

\[
\mathbf p=
\begin{bmatrix}
x\\y
\end{bmatrix}
\]

Moving by:

\[
\Delta\mathbf p=
\begin{bmatrix}
\Delta x\\
\Delta y
\end{bmatrix}
\]

gives:

\[
\mathbf p_{\text{new}}
=
\mathbf p+\Delta\mathbf p
\]

Thus vector addition represents accumulated movement.

## 8.2 Matrix → Rotation

A 2D rotation matrix is:

\[
R(\theta)=
\begin{bmatrix}
\cos\theta&-\sin\theta\\
\sin\theta&\cos\theta
\end{bmatrix}
\]

A vector can be rotated using:

\[
\mathbf p'=R\mathbf p
\]

This is the foundation for representing robot orientation.

## 8.3 Coordinate Frames

Robots typically use multiple coordinate frames:

- World frame
- Robot frame
- Camera frame
- LiDAR frame
- Arm/link frames
- End-effector frame

Matrices are used to transform quantities between these coordinate systems.

## 8.4 Dot Product

The dot product:

\[
\mathbf a\cdot\mathbf b
=
|\mathbf a||\mathbf b|\cos\theta
\]

produces a scalar and is useful for:
- Comparing directions
- Projection
- Measuring directional alignment
- Force components
- Control calculations

## 8.5 Cross Product and Torque

A key robotics equation is:

\[
\boxed{
\boldsymbol\tau
=
\mathbf r\times\mathbf F
}
\]

where:
- \(\mathbf r\) = position vector from the rotation axis to the force application point
- \(\mathbf F\) = force
- \(\boldsymbol\tau\) = torque

This connects cross products directly to robot joint rotation and dynamics.

---

# 9. Recommended Learning Flow for Robotics Mathematics

A useful progression is:

```text
High School Math
      ↓
Vectors
      ↓
Vector addition / scalar multiplication
      ↓
Dot product
      ↓
Cross product
      ↓
Matrices
      ↓
Matrix multiplication
      ↓
Transpose
      ↓
Symmetric / skew-symmetric matrices
      ↓
Linear transformations
      ↓
Basis / linear independence / dimension
      ↓
Rotation matrices
      ↓
Coordinate frames
      ↓
Homogeneous transformation matrices
      ↓
Forward Kinematics
      ↓
Inverse Kinematics
      ↓
Jacobian
      ↓
Robot Control
```

The key conceptual chain is:

\[
\boxed{
\text{Vector}
\rightarrow
\text{Matrix}
\rightarrow
\text{Linear Transformation}
\rightarrow
\text{Rotation / Coordinate Transformation}
\rightarrow
\text{Robotics}
}
\]

For cross products specifically:

\[
\boxed{
\text{Cross Product}
\rightarrow
\text{Perpendicular Direction}
\rightarrow
\text{Skew-Symmetric Matrix}
\rightarrow
\text{Angular Velocity / Torque}
\rightarrow
\text{Robotics}
}
\]

---

# 10. User Questions and Learning Progress

## Question 1
**"로봇공학을 위한 고등학교 수학 을 정리해서 마크다운 문서로 만들건데 영어로 제목을 만들어줘. 딱보면 무슨 문서인지 알수 있어야함. 짧아야함"**

Answer:
- Recommended: **High School Math for Robotics**

## Question 2
**"다음은 벡터의 행렬연산과 내적 외적"**

Answer:
- Recommended section title: **Vector & Matrix Operations**

## Question 3
**"비상 ppt 파일을 우분투에서 여는 방법을 알려줘"**

Answer:
- LibreOffice Impress is the most practical option for normal PPT/PPTX files.
- Microsoft PowerPoint desktop does not have an official Linux desktop version.
- If the file is a BIsang Education teaching material with DRM or a special format, the exact extension matters.

## Question 4
**"행렬을 다시 배우는 중인데 행렬의 곱 예제를 하나 만들어줘"**

Answer:
A basic \(2\times2\) multiplication example was used:

\[
\begin{bmatrix}
1&2\\
3&4
\end{bmatrix}
\begin{bmatrix}
5&6\\
7&8
\end{bmatrix}
=
\begin{bmatrix}
19&22\\
43&50
\end{bmatrix}
\]

Core rule:
> First matrix row × second matrix column.

## Question 5
**"앞 행렬의 행과 뒤 행렬의 열의 개수가 다르면?"**

Answer:
The number of rows of the first matrix and columns of the second matrix do not have to be equal.

The condition is:

\[
(m\times n)(n\times p)
\]

The inner dimensions must match:

\[
\boxed{n=n}
\]

The result is:

\[
m\times p
\]

## Question 6
**"예를 들어 4x2 행렬과 3x5 행렬은 ?"**

Answer:
\[
(4\times2)(3\times5)
\]

is impossible because:

\[
2\neq3
\]

The reverse order:

\[
(3\times5)(4\times2)
\]

is also impossible because:

\[
5\neq4
\]

## Question 7
**"차원?"**

Answer:
In this context, the matrix's dimensions/size refer to rows × columns.

Example:

\[
2\times3
\]

means:
- 2 rows
- 3 columns

For matrix multiplication:

\[
(m\times n)(n\times p)=(m\times p)
\]

## Question 8
**User provided a visual page about vectors, coordinate systems, vector spaces, subspaces, basis, and dimension and asked for a visual explanation.**

Answer:
A visual educational infographic was generated covering:
- Vector basics
- Vector addition
- Scalar multiplication
- Vector magnitude
- 3D coordinate system
- Vector space
- Subspace
- Basis
- Dimension
- Key summary

## Question 9
**"백터와 행렬연산, 선형대수가 로보틱스에서 어떻게 응용되는지 알아야겠어"**

Answer:
The core robotics connection was explained:

- Vector → position, velocity, acceleration, force
- Matrix → rotation and coordinate transformation
- Dot product → directional relationship and projection
- Cross product → perpendicular direction, torque
- Linear algebra → kinematics, sensors, SLAM, control
- Homogeneous transformation → position + orientation
- Matrix chains → robot arm forward kinematics

Key chain:

\[
\text{Vectors}
\rightarrow
\text{Matrices}
\rightarrow
\text{Linear Algebra}
\rightarrow
\text{Coordinate Transformations}
\rightarrow
\text{Robotics}
\]

## Question 10
**"대칭 + 반대칭 분해를 아래 처럼 설명해주심. 계산중 오차가 발생하거나, 연사 오류로 인해서 망가진 행렬만을 빼내고 사용가능한 행렬을 가져오기 위해서 사용한다. 라고 하시는데 무슨 말인지 모르겟어"**

Answer:
That explanation was identified as misleading.

Symmetric + skew-symmetric decomposition is not primarily for removing corrupted matrices.

For any matrix:

\[
A=
\frac{A+A^T}{2}
+
\frac{A-A^T}{2}
\]

where:

\[
S=\frac{A+A^T}{2}
\]

is symmetric, and:

\[
K=\frac{A-A^T}{2}
\]

is skew-symmetric.

The purpose is to separate one matrix into two components with different mathematical properties.

In robotics, skew-symmetric matrices are strongly connected to:
- Cross products
- Angular velocity
- Rotation
- Torque
- Robot dynamics

## Question 11
**"2x3 행렬은 전치 행렬을 가질수 없는건가?"**

Answer:
Every matrix can have a transpose.

For:

\[
A=
\begin{bmatrix}
1&2&3\\
4&5&6
\end{bmatrix}
\]

\[
A^T=
\begin{bmatrix}
1&4\\
2&5\\
3&6
\end{bmatrix}
\]

Thus:

\[
2\times3\rightarrow3\times2
\]

Transpose and matrix multiplication are different concepts.

## Question 12
**User provided a slide about cross product and skew-symmetric matrices and asked for a definition and visual explanation.**

Answer:
The cross product was introduced as:

\[
\boxed{\mathbf a\times\mathbf b=\mathbf c}
\]

where \(\mathbf c\) is perpendicular to both \(\mathbf a\) and \(\mathbf b\).

Magnitude:

\[
|\mathbf a\times\mathbf b|
=
|\mathbf a||\mathbf b|\sin\theta
\]

This is the area of the parallelogram formed by the two vectors.

Direction:
- Perpendicular to both input vectors
- Determined by the right-hand rule

Important property:

\[
\mathbf a\times\mathbf b
=
-(\mathbf b\times\mathbf a)
\]

Simple basis example:

\[
\mathbf i\times\mathbf j=\mathbf k
\]

The robotics connection was then established:

\[
[\mathbf a]_\times
=
\begin{bmatrix}
0&-a_3&a_2\\
a_3&0&-a_1\\
-a_2&a_1&0
\end{bmatrix}
\]

and:

\[
[\mathbf a]_\times\mathbf b
=
\mathbf a\times\mathbf b
\]

For robotics:

\[
\boxed{
\boldsymbol\tau
=
\mathbf r\times\mathbf F
}
\]

This connects the cross product to torque and robot joint rotation.

---

# 11. Current Study Position

The current focus is understanding the mathematical foundations needed for robotics, especially:

1. Vectors
2. Matrix operations
3. Matrix multiplication
4. Transpose
5. Symmetric / skew-symmetric matrices
6. Dot product
7. Cross product
8. Linear algebra
9. Coordinate transformations
10. Robotics applications

The most important current conceptual connection is:

\[
\boxed{
\text{Cross Product}
\leftrightarrow
\text{Skew-Symmetric Matrix}
\leftrightarrow
\text{Torque / Rotation}
}
\]
