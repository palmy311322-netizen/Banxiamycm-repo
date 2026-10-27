def zeros(rows,cols):
    matrix=[]
    for i in range(rows):
        row=[0]*cols
        matrix.append(row)
    return matrix

def eye(n):
    matrix=[]
    for i in range(n):
        row=[0]*n
        matrix.append(row)
    for i in range(n):
        matrix[i][i]=1.0
    return matrix

def add(A,B):
    if not A or not B:
        raise ValueError('矩阵不能为空')
    if not A[0] or not B[0]:
        raise ValueError('矩阵列不能为空')
    rows_A,cols_A=len(A),len(A[0])
    rows_B,cols_B=len(B),len(B[0])
    if rows_A!=rows_B or cols_A!=cols_B:
        raise ValueError('矩阵维度不同')
    matrix=[]
    for i in range(rows_A):
        row=[]
        for j in range(cols_A):
            row.append(A[i][j]+B[i][j])
        matrix.append(row)
    return matrix

def sub(A,B):
    if not A or not B:
        raise ValueError('矩阵不能为空')
    if not A[0] or not B[0]:
        raise ValueError('矩阵列不能为空')
    rows_A,cols_A=len(A),len(A[0])
    rows_B,cols_B=len(B),len(B[0])
    if rows_A!=rows_B or cols_A!=cols_B:
        raise ValueError('矩阵维度不同')
    matrix=[]
    for i in range(rows_A):
        row=[]
        for j in range(cols_A):
            row.append(A[i][j]-B[i][j])
        matrix.append(row)
    return matrix

def matmul(A,B):
    if not A or not B:
        raise ValueError('矩阵不能为空')
    if not A[0] or not B[0]:
        raise ValueError('矩阵列不能为空')
    rows_A,cols_A=len(A),len(A[0])
    rows_B,cols_B=len(B),len(B[0])
    if cols_A!=rows_B:
        raise ValueError('矩阵维度不匹配')
    matrix=[]
    for i in range(rows_A):
        row=[]
        for j in range(cols_B):
            s=0.0
            for k in range(cols_A):
                s+=A[i][k]*B[k][j]
            row.append(s)
        matrix.append(row)
    return matrix

def transpose_1(A):
    if not A:
        raise ValueError('矩阵不能为空')
    if not A[0]:
        raise ValueError('矩阵列不能为空')
    rows=len(A)
    cols=len(A[0])
    matrix=[]
    for i in range(cols):
        row=[]
        for j in range(rows):
            row.append(A[j][i])
        matrix.append(row)
    return matrix

def transpose_2(A):
    if not A:
        raise ValueError('矩阵不能为空')
    if not A[0]:
        raise ValueError('矩阵列不能为空')
    matrix=[]
    for row in zip*A:
        matrix.append(row)
    return matrix

def det(A):
    if not A:
        raise ValueError('矩阵不能为空')
    if not A[0]:
        raise ValueError('矩阵列不能为空')
    n=len(A)
    if n!=len(A[0]):
        raise ValueError('矩阵必须是方阵')
    if n==1:
        return A[0][0]
    result=0.0
    for j in range(n):
        minor=[]
        for i in range(1,n):
            minor_row=[]
            for k in range(n):
                if k!=j:
                    minor_row.append(A[i][k])
            minor.append(minor_row)
        sign=(-1)**j
        result+=sign*A[0][j]*det(minor)
    return result

def inverse(A):
    if not A:
        raise ValueError('矩阵不能为空')
    if not A[0]:
        raise ValueError('矩阵列不能为空')
    n=len(A)
    if n!=len(A[0]):
        raise ValueError('矩阵必须是方阵')
    if det(A)==0:
        raise ValueError('奇异矩阵，不可逆')
    I=eye(n)
    aug=[]
    for i in range(n):
        aug_row=[]
        for k in range(n):
            aug_row.append(A[i][k])
        for k in range(n):
            aug_row.append(I[i][k])
        aug.append(aug_row)
    for col in range(n):
        pivot=col
        for row in range(col+1,n):
            if abs(aug[row][col])>abs(aug[pivot][col]):
                pivot=row
        aug[col],aug[pivot]=aug[pivot],aug[col]
        div=aug[col][col]
        for j in range(2*n):
            aug[col][j]/=div
        for row in range(n):
            if row!=col:
                factor=aug[row][col]
                for j in range(2*n):
                    aug[row][j]-=factor*aug[col][j]
    result=[]
    for i in range(n):
        res_row=[]
        for j in range(n,2*n):
            res_row.append(aug[i][j])
        result.append(res_row)
    return result


