def is_prime(n):
    if n==2:
        return True
    if n<2:
        return False
    if n%2==0:
        return False
    i=3
    while i*i<=n:
        if n%i==0:
            return False
        i+=2
    return True

def gcd(a,b):
    while b!=0:
        a,b=b,a%b
    return a

def lcm(a,b):
    return a*b//gcd(a,b)

def my_sqrt(x,eps=1e-8):
    if x==0:
        return 0.0
    x_0=x
    while True:
        x_1=0.5*(x_0+x/x_0)
        if abs(x_1-x_0)<eps:
            return x_1
        x_0=x_1

def fib(n,method='loop'):
    if n<=2:
        return 1
    if method=='recursion':
        return fib(n-1,'recursion')+fib(n-2,'recursion')
    a=1
    b=1
    for i in range(3,n+1):
        temp=a+b
        a=b
        b=temp
    return b

def prime_list(start,end):
    result=[]
    for i in range(start,end+1):
        if is_prime(i):
            result.append(i)
    return result
