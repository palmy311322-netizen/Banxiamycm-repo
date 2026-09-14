#include "define.h"
#include <iostream>
using namespace std;

typedef struct node
{
    ElemType element;
    struct node *link;
}node;

typedef struct singlelist
{
    node *first;
    int n;
}singlelist;

typedef int status;

status Init(singlelist *L)
{
    L->first=NULL;
    L->n=0;
    return OK;
}

status Find(singlelist L,int i,ElemType *x)
{
    if(i<0||i>=L.n)
        return ERROR;
    node *p=L.first;
    for(int j=0;j<i;j++)
        p=p->link;
    *x=p->element;
    return OK;
}

status Insert(singlelist *L,int i,ElemType x)
{
    if(i<-1||i>L->n)
        return ERROR;
    node *p,*q;
    p=L->first;
    for(int j=0;j<i;j++)
        p=p->link;
    q=new node;
    q->element=x;
    if(i>=0)
    {
        q->link=p->link;
        p->link=q;
    }
    else
    {
        q->link=L->first;
        L->first=q;
    }
    L->n++;
    return OK;
}

status Delete(singlelist *L,int i)
{
    if(i<0||i>L->n-1)
        return ERROR;
    node *p,*q;
    p=L->first;
    q=L->first;
    for(int j=0;j<i-1;j++)
        p=p->link;
    if(i==0)
        L->first=L->first->link;
    else
    {
        q=p->link;
        p->link=q->link;
    }
    delete q;
    L->n--;
    return OK;
}

status Output(singlelist *L)
{
    if(!L->n)
        return ERROR;
    node *p=L->first;
    while(p)
    {
        cout<<p->element<<endl;
        p=p->link;
    }
    return OK;
}

status Destroy(singlelist *L)
{
    node *p;
    while(L->first)
    {
        p=L->first->link;
        delete L->first;
        L->first=p;
    }
}

