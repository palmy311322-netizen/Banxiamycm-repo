#include "define.h"
#include<iostream>
typedef struct stack
{
    int top;
    int maxSize;
    ElemType *element;
}stack;

void Create(stack *S,int maxSize)
{
    S->maxSize=maxSize;
    S->element=new ElemType[maxSize];
    S->top=-1;
}

void Destroy(stack *S)
{
    S->maxSize=0;
    delete []S->element;
    S->top=-1;
}

bool Isempty(stack *S)
{
    return S->top==-1;
}

bool Isfull(stack *S)
{
    return S->top==S->maxSize-1;
}

bool Top(stack *S,ElemType *x)
{
    if(Isempty(S))
        return false;
    *x=S->element[S->top];
    return true;
}

bool Push(stack *S,ElemType x)
{
    if(Isfull(S))
        return false;
    S->top++;
    S->element[S->top]=x;
    return true;
}

bool Pop(stack *S)
{
    if(Isempty((S)))
        return false;
    S->top--;
    return true;
}

void Clear(stack *S)
{
    S->top=-1;
}
