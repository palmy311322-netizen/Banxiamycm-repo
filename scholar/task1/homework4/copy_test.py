import copy
from matrix import matmul, inverse

A=[[1, 2, 3],
     [4, 5, 6],
     [7, 8, 9]]

B=A
B[0][0] = 999
print("方式1: B=A")
print("B[0][0]=999后，A=",A,'\n')

A=[[1, 2, 3],
     [4, 5, 6],
     [7, 8, 9]]
B=A.copy()
B[0][0] = 999
print("方式2: B=A.copy()")
print("B[0][0]=999后， A =",A,'\n')

A=[[1, 2, 3],
     [4, 5, 6],
     [7, 8, 9]]
B=copy.deepcopy(A)
B[0][0] = 999
print("方式3: B=copy.deepcopy(A)")
print("B[0][0]=999后,A=",A,'\n')

def is_close_to_identity(M, tol=1e-9):
    n=len(M)
    for i in range(n):
        for j in range(n):
            expected = 1.0 if i==j else 0.0
            if abs(M[i][j]-expected) > tol:
                return False
    return True

A1=[[4, 7],
    [2, 6]]
result1=matmul(A1, inverse(A1))
print("A1=",A1)
print("matmul(A1, inverse(A1))=", result1)
print("接近单位矩阵:",is_close_to_identity(result1),"\n")

A2=[[2, 1, 1],
    [1, 3, 2],
    [1, 0, 0]]
result2=matmul(A2,inverse(A2))
print("A2=",A2)
print("matmul(A2,inverse(A2))=",result2)
print("接近单位矩阵:",is_close_to_identity(result2),"\n")

A3=[[1, 2, 0, 1],
    [0, 1, 1, 0],
    [1, 0, 2, 1],
    [2, 1, 0, 3]]
result3=matmul(A3, inverse(A3))
print("A3=",A3)
print("matmul(A3,inverse(A3))=",result3)
print("接近单位矩阵:",is_close_to_identity(result3),"\n")
