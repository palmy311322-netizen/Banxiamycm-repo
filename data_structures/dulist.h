#include "define.h"
#include <iostream>
using namespace std;

typedef struct dunode
{
    ElemType element;
    struct dunode *llink;
    struct dunode *rlink;
}dunode;

typedef struct dulist
{
    dunode *first;
    dunode *last;
    int n;
}dulist;

typedef int status;

status Init(dulist *L)
{
    L->first = NULL;
    L->last = NULL;
    L->n = 0;
    return OK;
}

status Find(dulist L, int i, ElemType *x)
{
    if(i < 0 || i >= L.n)
        return ERROR;
    dunode *p = L.first;
    for(int j = 0; j < i; j++)
        p = p->rlink;
    *x = p->element;
    return OK;
}

status Insert(dulist *L, int i, ElemType x)
{
    if(i < 0 || i > L->n)
        return ERROR;
    dunode *q = new dunode;
    q->element = x;
    q->llink = NULL;
    q->rlink = NULL;
    if(L->n == 0)
    {
        L->first = q;
        L->last = q;
    }
    else if(i == 0)
    {
        q->rlink = L->first;
        L->first->llink = q;
        L->first = q;
    }
    else if(i == L->n)
    {
        q->llink = L->last;
        L->last->rlink = q;
        L->last = q;
    }
    else
    {
        dunode *p = L->first;
        for(int j = 0; j < i; j++)
            p = p->rlink;
        q->llink = p->llink;
        q->rlink = p;
        p->llink->rlink = q;
        p->llink = q;
    }
    L->n++;
    return OK;
}

status Delete(dulist *L, int i)
{
    if(i < 0 || i >= L->n)
        return ERROR;
    dunode *p = L->first;
    for(int j = 0; j < i; j++)
        p = p->rlink;
    if(p->llink != NULL)
        p->llink->rlink = p->rlink;
    else
        L->first = p->rlink;
    if(p->rlink != NULL)
        p->rlink->llink = p->llink;
    else
        L->last = p->llink;
    delete p;
    L->n--;
    return OK;
}

status Output(dulist *L)
{
    if(!L->n)
        return ERROR;
    dunode *p = L->first;
    while(p != NULL)
    {
        cout << p->element << endl;
        p = p->rlink;
    }
    return OK;
}

status Destroy(dulist *L)
{
    dunode *p = L->first;
    while(p != NULL)
    {
        dunode *next = p->rlink;
        delete p;
        p = next;
    }
    L->first = NULL;
    L->last = NULL;
    L->n = 0;
    return OK;
}
