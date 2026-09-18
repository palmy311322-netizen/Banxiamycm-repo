#pragma once

#include <iostream>
using namespace std;

template <typename ElemType>
class Stack
{
public:
    explicit Stack(int capacity);
    ~Stack();

    Stack(const Stack&) = delete;
    Stack& operator=(const Stack&) = delete;

    bool empty() const;
    bool full() const;
    int size() const;
    int max_size() const;
    bool top(ElemType& value) const;
    bool push(const ElemType& value);
    bool pop(ElemType& value);
    void clear();

private:
    ElemType* elements;
    int capacity;
    int count;
};

template <typename ElemType>
Stack<ElemType>::Stack(int capacity) //构造函数
{
    this->capacity = capacity;
    elements = capacity > 0 ? new ElemType[capacity] : nullptr;
    count = 0;
}

template <typename ElemType>
Stack<ElemType>::~Stack() //析构函数
{
    delete[] elements;
}

template <typename ElemType>
bool Stack<ElemType>::empty() const //判断栈是否为空
{
    return count == 0;
}

template <typename ElemType>
bool Stack<ElemType>::full() const //判断栈是否已满
{
    return count == capacity;
}

template <typename ElemType>
int Stack<ElemType>::size() const //获取栈当前长度
{
    return count;
}

template <typename ElemType>
int Stack<ElemType>::max_size() const //获取栈最大容量
{
    return capacity;
}

template <typename ElemType>
bool Stack<ElemType>::top(ElemType& value) const //获取栈顶元素
{
    if (empty())
        return false;
    value = elements[count - 1];
    return true;
}

template <typename ElemType>
bool Stack<ElemType>::push(const ElemType& value) //入栈
{
    if (full())
        return false;
    elements[count] = value;
    ++count;
    return true;
}

template <typename ElemType>
bool Stack<ElemType>::pop(ElemType& value) //出栈
{
    if (!top(value))
        return false;
    --count;
    return true;
}

template <typename ElemType>
void Stack<ElemType>::clear() //清空栈
{
    count = 0;
}
