from mymath import is_prime,gcd,lcm,my_sqrt,fib,prime_list

def print_multiplication_table():
    for i in range(1,10):
        for j in range(1,i+1):
            print(f"{j}x{i}={i*j:<4}",end='')
        print()

def print_diamond(n):
    mid=n//2
    for i in range(n):
        if i<=mid:
            spaces=mid-i
            width=2*i+1
        else:
            spaces=i-mid
            width=2*(n-1-i)+1
        line=''
        for j in range(width):
            if j==0 or j==width-1:
                line+='*'
            else:
                line+=' '
        print(' '*spaces+line)

def main():
    while True:
        print('输入数字，')
        print('1. 打印九九乘法表')
        print('2. 打印空心菱形')
        print('3. 判断素数')
        print('4. 求最大公约数和最小公倍数')
        print('5. 求平方根')
        print('6. 斐波那契数列')
        print('7. 区间素数列表')
        print('q. 退出')
        choice=input('请选择：')
        if choice=='1':
            print_multiplication_table()
            print()
        elif choice=='2':
            try:
                n=int(input('请输入菱形行数（奇数）：'))
                if n%2==0:
                    print('请输入奇数\n')
                    continue
                print_diamond(n)
                print()
            except ValueError:
                print('请输入整数\n')
                continue
        elif choice=='3':
            try:
                n=int(input('请输入一个整数：'))
                if is_prime(n):
                    print(f'{n} 是素数\n')
                else:
                    print(f'{n} 不是素数\n')
            except ValueError:
                print('请输入整数\n')
                continue
        elif choice=='4':
            try:
                a=int(input('请输入第一个整数：'))
                b=int(input('请输入第二个整数：'))
                print(f'最大公约数：{gcd(a,b)}')
                print(f'最小公倍数：{lcm(a,b)}\n')
            except ValueError:
                print('请输入整数\n')
                continue
        elif choice=='5':
            try:
                x=float(input('请输入一个非负数：'))
                if x<0:
                    print('请输入非负数\n')
                    continue
                print(f'{x} 的平方根为：{my_sqrt(x)}\n')
            except ValueError:
                print('请输入数字\n')
                continue
        elif choice=='6':
            try:
                n=int(input('请输入项数n：'))
                method=input("请选择方式（loop/recursion，默认loop）：") or 'loop'
                print(f'fib({n}) = {fib(n,method)}\n')
            except ValueError:
                print('请输入整数\n')
                continue
        elif choice=='7':
            try:
                start=int(input('请输入起始值：'))
                end=int(input('请输入结束值：'))
                print(f'{start}到{end}之间的素数：{prime_list(start,end)}\n')
            except ValueError:
                print('请输入整数\n')
                continue
        elif choice=='q':
            print('再见！')
            break
        else:
            print('无效选项，请重新输入\n')
            continue

if __name__=='__main__':
    main()
