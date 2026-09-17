#include "define.h"
#include<iostream>

typedef struct queue
{
    int front;
    int rear;
    int maxSize;
    ElemType *element;
}queue;

void Create(queue *Q,int maxSize)
{
    Q->maxSize=maxSize;
    Q->element=new ElemType[maxSize];
    Q->front=Q->rear=0;
}

void Destroy(queue *Q)
{
    Q->maxSize=0;
    delete []Q->element;
    Q->front=Q->rear=-1;
}

bool Isempty(queue *Q)
{
    return Q->front==Q->rear;
}

bool Isfull(queue *Q)
{
    return (Q->rear+1)%Q->maxSize==Q->front;
}

bool Front(queue *Q,ElemType *x)
{
    if(Isempty(Q))
        return false;
    *x=Q->element[(Q->front+1)%Q->maxSize];
    return true;
}

bool Enqueue(queue *Q,ElemType x)
{
    if(Isfull(Q))
        return false;
    Q->rear=(Q->rear+1)%Q->maxSize;
    Q->element[Q->rear]=x;
    return true;
}

bool Dequeue(queue *Q)
{
    if(Isempty(Q))
        return false;
    Q->front=(Q->front+1)%Q->maxSize;
    return true;
}

void Clear(queue *Q)
{
    Q->front=Q->rear=0;
}