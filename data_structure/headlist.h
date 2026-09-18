#pragma once

#include "define.h"
#include <iostream>
using namespace std;

template <typename ElemType>
class HeadList
{
public:
    HeadList();
    ~HeadList();

    HeadList(const HeadList&) = delete;
    HeadList& operator=(const HeadList&) = delete;

    int length() const;
    Status find(int index, ElemType& value) const;
    Status insert(int index, const ElemType& value);
    Status erase(int index);
    void output() const;
    void clear();

private:
    struct Node;

    Node* head;
    int size;
};

template <typename ElemType>
struct HeadList<ElemType>::Node //定义Node
{
    ElemType element{};
    Node* next = nullptr;
};

template <typename ElemType>
HeadList<ElemType>::HeadList() //构造函数
{
    head = new Node{};
    size = 0;
}

template <typename ElemType>
HeadList<ElemType>::~HeadList() //析构函数
{
    clear();
    delete head;
}

template <typename ElemType>
int HeadList<ElemType>::length() const //获取链表长度
{
    return size;
}

template <typename ElemType>
Status HeadList<ElemType>::find(int index, ElemType& value) const //查找元素
{
    if (index < 0 || index >= size)
        return Status::Error;

    const Node* current = head->next;
    for (int i = 0; i < index; ++i)
        current = current->next;
    value = current->element;
    return Status::Ok;
}

template <typename ElemType>
Status HeadList<ElemType>::insert(int index, const ElemType& value) //插入新元素
{
    if (index < 0 || index > size)
        return Status::Error;

    Node* previous = head;
    for (int i = 0; i < index; ++i)
        previous = previous->next;

    Node* inserted = new Node{value, previous->next};
    previous->next = inserted;
    ++size;
    return Status::Ok;
}

template <typename ElemType>
Status HeadList<ElemType>::erase(int index) //删除元素
{
    if (index < 0 || index >= size)
        return Status::Error;

    Node* previous = head;
    for (int i = 0; i < index; ++i)
        previous = previous->next;

    Node* removed = previous->next;
    previous->next = removed->next;
    delete removed;
    --size;
    return Status::Ok;
}

template <typename ElemType>
void HeadList<ElemType>::output() const //输出链表
{
    const Node* current = head->next;
    while (current != nullptr)
    {
        cout << current->element << '\n';
        current = current->next;
    }
}

template <typename ElemType>
void HeadList<ElemType>::clear() //清空链表
{
    Node* current = head->next;
    while (current != nullptr)
    {
        Node* next = current->next;
        delete current;
        current = next;
    }
    head->next = nullptr;
    size = 0;
}