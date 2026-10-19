#pragma once

#include "define.h"
#include <iostream>

using namespace std;

template <typename ElemType>
class DouArray
{
public:
    DouArray();
    ~DouArray();
    DouArray(const DouArray& other);
    DouArray& operator=(const DouArray& other);

    Status CreateArray(ElemType m1,ElemType m2);
    Status DestroyArray();
    Status RetrieveArray();
    Status StoreArrayItem();
    Status OutputArray();

private:
    ElemType *data;
    int rows;
    int cols;
    int capacity;
    int length;
};

template <typename ElemType>
Status DouArray<ElemType>::CreateArray(ElemType m1,ElemType m2)
{
    if (m1<=0||m2<=0)
        return Status::Error;
    DestroyArray();
    rows=m1;
    cols=m2;
    capacity=cols*rows;
    data=new ElemType[capacity]();
    length=capacity;
    return Status::Ok;
}

template <typename ElemType>
Status DouArray<ElemType>::DestroyArray()
{
    delete[]data;
    data=nullptr;
    rows=0;
    cols=0;
    capacity=0;
    length=0;
    return Status::Ok;
}

template <typename ElemType>
Status DouArray<ElemType>::RetrieveArray()
{
    cout<<"Array:"<<endl;
    for (int i=0;i<rows;i++)
    {
        for (int j=0;j<cols;j++)
        {
            cout<<data[i*cols+j]<<" ";
        }
        cout<<endl;
    }
    return Status::Ok;
}
