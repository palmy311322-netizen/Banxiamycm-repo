#pragma once
#include <vector>
#include <algorithm>
using std::vector;

template <typename ElemType,typename Compare>
class Heap
{
private:
    vector<ElemType> data;
    Compare comp;
    int parent(int i){return (i-1)/2;};
    int lchild(int i){return 2*i+1;};
    int rchild(int i){return 2*i+2;};
    void UpAdjust();
    void DownAdjust();
public:
    Heap();
    Heap(const vector<ElemType>&arr);
    ~Heap();
    void push(ElemType elem);
    void pop();
    void clear();
    ElemType top();
    bool empty(){return data.empty();};
    int size(){return data.size();};
};

template <typename ElemType,typename Compare>//默认构造函数
Heap<ElemType,Compare>::Heap(){}

template <typename ElemType,typename Compare>//从数组建堆
Heap<ElemType,Compare>::Heap(const vector<ElemType>&arr)
{
    data=arr;
    for(int i=parent(data.size()-1);i>=0;i--)
        DownAdjust();
}

template <typename ElemType,typename Compare>
Heap<ElemType,Compare>::~Heap(){}//析构函数

template <typename ElemType,typename Compare>
void Heap<ElemType,Compare>::UpAdjust()//向上调整
{
    int i=data.size()-1;
    while(i>0&&comp(data[i],data[parent(i)]))
    {
        std::swap(data[i],data[parent(i)]);
        i=parent(i);
    }
}

template <typename ElemType,typename Compare>
void Heap<ElemType,Compare>::DownAdjust()//向下调整
{
    int i=0;
    while(lchild(i)<(int)data.size())
    {
        int child=lchild(i);
        if(child+1<(int)data.size()&&comp(data[child+1],data[child]))
            child++;
        if(comp(data[i],data[child])) 
            break;
        std::swap(data[i],data[child]);
        i=child;
    }
}

template <typename ElemType,typename Compare>
void Heap<ElemType,Compare>::push(ElemType elem)//加入新元素
{
    data.push_back(elem);
    UpAdjust();
}

template <typename ElemType,typename Compare>
void Heap<ElemType,Compare>::pop()//弹出堆顶元素
{
    data[0]=data.back();
    data.pop_back();
    if(!data.empty()) DownAdjust();
}

template <typename ElemType,typename Compare>
void Heap<ElemType,Compare>::clear()//清空堆
{
    data.clear();
}

template <typename ElemType,typename Compare>
ElemType Heap<ElemType,Compare>::top()//获取堆顶元素
{
    return data[0];
}