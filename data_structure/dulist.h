#pragma once

#include "define.h"
#include <iostream>
using namespace std;

template <typename ElemType>
class DoubleList
{
public:
    DoubleList();
    ~DoubleList();
    //显式禁止对该类对象进行拷贝
    DoubleList(const DoubleList&) = delete;//删除拷贝构造函数
    DoubleList& operator=(const DoubleList&) = delete;//删除拷贝赋值运算符

    int length() const;
    Status find(int index, ElemType& value) const;
    Status insert(int index, const ElemType& value);
    Status erase(int index);
    void output() const;
    void clear();

private:
    struct Node;
    Node* node_at(int index) const;
    Node* first;
    Node* last;
    int size;
};

template <typename ElemType>
struct DoubleList<ElemType>::Node//定义Node
{
    ElemType element{};
    Node* previous = nullptr;
    Node* next = nullptr;
};

template <typename ElemType>
DoubleList<ElemType>::DoubleList()//构造函数
{
    first = nullptr;
    last = nullptr;
    size = 0;
}

template <typename ElemType>
DoubleList<ElemType>::~DoubleList()//析构函数
{
    clear();
}

template <typename ElemType>
int DoubleList<ElemType>::length() const//获取链表长度
{
    return size;
}

template <typename ElemType>
Status DoubleList<ElemType>::find(int index, ElemType& value) const//查找元素
{
    Node* current = node_at(index);
    if (current == nullptr)
        return Status::Error;
    value = current->element;
    return Status::Ok;
}

template <typename ElemType>
Status DoubleList<ElemType>::insert(int index, const ElemType& value)//插入新元素
{
    if (index < 0 || index > size)
        return Status::Error;

    Node* inserted = new Node{value};
    if (size == 0)
        first = last = inserted;
    else if (index == 0)
    {
        inserted->next = first;
        first->previous = inserted;
        first = inserted;
    }
    else if (index == size)
    {
        inserted->previous = last;
        last->next = inserted;
        last = inserted;
    }
    else
    {
        Node* next = node_at(index);
        inserted->previous = next->previous;
        inserted->next = next;
        next->previous->next = inserted;
        next->previous = inserted;
    }
    ++size;
    return Status::Ok;
}

template <typename ElemType>
Status DoubleList<ElemType>::erase(int index)//删除元素
{
    Node* removed = node_at(index);
    if (removed == nullptr)
        return Status::Error;

    if (removed->previous != nullptr)
        removed->previous->next = removed->next;
    else
        first = removed->next;
    if (removed->next != nullptr)
        removed->next->previous = removed->previous;
    else
        last = removed->previous;

    delete removed;
    --size;
    return Status::Ok;
}

template <typename ElemType>
void DoubleList<ElemType>::output() const//输出链表
{
    for (Node* current = first; current != nullptr; current = current->next)
        cout << current->element << endl;
}

template <typename ElemType>
void DoubleList<ElemType>::clear()//撤销链表
{
    while (first != nullptr)
    {
        Node* next = first->next;
        delete first;
        first = next;
    }
    last = nullptr;
    size = 0;
}

template <typename ElemType>
typename DoubleList<ElemType>::Node* DoubleList<ElemType>::node_at(int index) const//按照索引返回对应的节点
{
    if (index < 0 || index >= size)
        return nullptr;

    if (index < size / 2)
    {
        Node* current = first;
        for (int i = 0; i < index; ++i)
            current = current->next;
        return current;
    }

    Node* current = last;
    for (int i = size - 1; i > index; --i)
        current = current->previous;
    return current;
}