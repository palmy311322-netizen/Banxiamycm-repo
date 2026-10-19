#pragma once

template <typename ElemType>
class DynamicSet
{
public:
    virtual ~DynamicSet(){}

    virtual bool IsEmpty()=0;
    virtual int Size()const=0;
    virtual void Clear()=0;

    virtual void Insert(const ElemType&e)=0;
    virtual void Remove(const ElemType&e)=0;
    virtual bool Search(const ElemType&e)const=0;

    virtual bool Contain(const ElemType&e)const
    {
        return Search(e);
    }
};