#pragma once

#include <iostream>
using namespace std;

template <typename ElemType>
class Queue
{
public:
    explicit Queue(int capacity);
    ~Queue();

    Queue(const Queue&) = delete;
    Queue& operator=(const Queue&) = delete;

    bool empty() const;
    bool full() const;
    int size() const;
    int max_size() const;
    bool front(ElemType& value) const;
    bool enqueue(const ElemType& value);
    bool dequeue(ElemType& value);
    void clear();

private:
    ElemType* elements;
    int capacity;
    int front_index;
    int back_index;
    int count;
};

template <typename ElemType>
Queue<ElemType>::Queue(int capacity) //构造函数
{
    this->capacity = capacity;
    elements = capacity > 0 ? new ElemType[capacity] : nullptr;
    front_index = 0;
    back_index = 0;
    count = 0;
}

template <typename ElemType>
Queue<ElemType>::~Queue() //析构函数
{
    delete[] elements;
}

template <typename ElemType>
bool Queue<ElemType>::empty() const //判断队列是否为空
{
    return count == 0;
}

template <typename ElemType>
bool Queue<ElemType>::full() const //判断队列是否已满
{
    return count == capacity;
}

template <typename ElemType>
int Queue<ElemType>::size() const //获取队列当前长度
{
    return count;
}

template <typename ElemType>
int Queue<ElemType>::max_size() const //获取队列最大容量
{
    return capacity;
}

template <typename ElemType>
bool Queue<ElemType>::front(ElemType& value) const //获取队首元素
{
    if (empty())
        return false;
    value = elements[front_index];
    return true;
}

template <typename ElemType>
bool Queue<ElemType>::enqueue(const ElemType& value) //入队
{
    if (full())
        return false;
    elements[back_index] = value;
    back_index = (back_index + 1) % capacity;
    ++count;
    return true;
}

template <typename ElemType>
bool Queue<ElemType>::dequeue(ElemType& value) //出队
{
    if (!front(value))
        return false;
    front_index = (front_index + 1) % capacity;
    --count;
    return true;
}

template <typename ElemType>
void Queue<ElemType>::clear() //清空队列
{
    front_index = 0;
    back_index = 0;
    count = 0;
}
