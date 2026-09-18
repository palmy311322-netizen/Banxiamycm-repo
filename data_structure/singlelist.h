#pragma once

#include "define.h"
#include <iostream>
using namespace std;

template <typename ElemType>
class SingleList
{
public:
    SingleList();
    ~SingleList();

    SingleList(const SingleList&) = delete;
    SingleList& operator=(const SingleList&) = delete;

    int length() const;
    Status find(int index, ElemType& value) const;
    Status insert(int index, const ElemType& value);
    Status erase(int index);
    void output() const;
    void clear();

private:
    struct Node;

    Node* node_at(int index);

    Node* first;
    int size;
};

template <typename ElemType>
struct SingleList<ElemType>::Node //定义Node
{
    ElemType element{};
    Node* next = nullptr;
};

template <typename ElemType>
SingleList<ElemType>::SingleList() //构造函数
{
    first = nullptr;
    size = 0;
}

template <typename ElemType>
SingleList<ElemType>::~SingleList() //析构函数
{
    clear();
}

template <typename ElemType>
int SingleList<ElemType>::length() const //获取链表长度
{
    return size;
}

template <typename ElemType>
Status SingleList<ElemType>::find(int index, ElemType& value) const //查找元素
{
    if (index < 0 || index >= size)
        return Status::Error;

    const Node* current = first;
    for (int i = 0; i < index; ++i)
        current = current->next;
    value = current->element;
    return Status::Ok;
}

template <typename ElemType>
Status SingleList<ElemType>::insert(int index, const ElemType& value) //插入新元素
{
    if (index < 0 || index > size)
        return Status::Error;

    if (index == 0)
        first = new Node{value, first};
    else
    {
        Node* previous = node_at(index - 1);
        previous->next = new Node{value, previous->next};
    }
    ++size;
    return Status::Ok;
}

template <typename ElemType>
Status SingleList<ElemType>::erase(int index) //删除元素
{
    if (index < 0 || index >= size)
        return Status::Error;

    Node* removed;
    if (index == 0)
    {
        removed = first;
        first = first->next;
    }
    else
    {
        Node* previous = node_at(index - 1);
        removed = previous->next;
        previous->next = removed->next;
    }
    delete removed;
    --size;
    return Status::Ok;
}

template <typename ElemType>
void SingleList<ElemType>::output() const //输出链表
{
    for (const Node* current = first; current != nullptr; current = current->next)
        cout << current->element << '\n';
}

template <typename ElemType>
void SingleList<ElemType>::clear() //清空链表
{
    while (first != nullptr)
    {
        Node* next = first->next;
        delete first;
        first = next;
    }
    size = 0;
}

template <typename ElemType>
typename SingleList<ElemType>::Node* SingleList<ElemType>::node_at(int index) //按照索引返回对应的节点
{
    Node* current = first;
    for (int i = 0; i < index; ++i)
        current = current->next;
    return current;
}