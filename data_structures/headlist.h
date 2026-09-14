#include "define.h"
#include <iostream>
using namespace std;

typedef struct headnode
{
	ElemType element;
	struct headnode *link;
}headnode;

typedef struct headlist
{
	headnode *head;
	int n;
}headlist;

typedef int status;

status Init(headlist *L)
{
	L->head = new headnode;
	L->head->link = NULL;
	L->n = 0;
	return OK;
}

status Find(headlist L, int i, ElemType *x)
{
	if(i < 0 || i >= L.n)
		return ERROR;
	headnode *p = L.head->link;
	for(int j = 0; j < i; j++)
		p = p->link;
	*x = p->element;
	return OK;
}

status Insert(headlist *L, int i, ElemType x)
{
	if(i < -1 || i >= L->n)
		return ERROR;
	headnode *p = L->head;
	if(i >= 0)
	{
		p = L->head->link;
		for(int j = 0; j < i; j++)
			p = p->link;
	}
	headnode *q = new headnode;
	q->element = x;
	q->link = p->link;
	p->link = q;
	L->n++;
	return OK;
}

status Delete(headlist *L, int i)
{
	if(i < 0 || i >= L->n)
		return ERROR;
	headnode *p = L->head;
	for(int j = 0; j < i; j++)
		p = p->link;
	headnode *q = p->link;
	p->link = q->link;
	delete q;
	L->n--;
	return OK;
}

status Output(headlist *L)
{
	if(L->n == 0)
		return ERROR;
	headnode *p = L->head->link;
	while(p)
	{
		cout << p->element << endl;
		p = p->link;
	}
	return OK;
}

status Destroy(headlist *L)
{
	headnode *p = L->head->link;
	while(p != NULL)
	{
		headnode *next = p->link;
		delete p;
		p = next;
	}
	delete L->head;
	L->head = NULL;
	L->n = 0;
	return OK;
}
