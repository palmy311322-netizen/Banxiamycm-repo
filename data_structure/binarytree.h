#pragma once
#include "queue.h"

template <typename ElemType>
class BinaryTreeNode
{
private:
    ElemType data;
    BinaryTreeNode<ElemType>* left;
    BinaryTreeNode<ElemType>* right;
public:
    BinaryTreeNode(ElemType data, BinaryTreeNode<ElemType>* left = nullptr, BinaryTreeNode<ElemType>* right = nullptr);
    ElemType getData() const;
    void setData(ElemType data);
    BinaryTreeNode<ElemType>* getLeft() const;
    void setLeft(BinaryTreeNode<ElemType>* left);
    BinaryTreeNode<ElemType>* getRight() const;
    void setRight(BinaryTreeNode<ElemType>* right);
};

template <typename ElemType>
class BinaryTree
{
private:
    BinaryTreeNode<ElemType>* root;
    void destroyTree(BinaryTreeNode<ElemType>* node);
    BinaryTreeNode<ElemType>* copyTree(BinaryTreeNode<ElemType>* node);
public:
    BinaryTree();
    ~BinaryTree();
    BinaryTree(const BinaryTree<ElemType>& other);
    BinaryTree<ElemType>& operator=(const BinaryTree<ElemType>& other);

    BinaryTreeNode<ElemType>* getRoot();
    BinaryTreeNode<ElemType>* NewNode(ElemType data, BinaryTreeNode<ElemType>* left, BinaryTreeNode<ElemType>* right);
    void MakeTree(BinaryTree<ElemType>* bt, ElemType data, BinaryTreeNode<ElemType>* left, BinaryTreeNode<ElemType>* right);
    void PreOrderPrint_recursive(BinaryTreeNode<ElemType>* node);
    void InOrderPrint_recursive(BinaryTreeNode<ElemType>* node);
    void PostOrderPrint_recursive(BinaryTreeNode<ElemType>* node);
    void LevelOrderPrint(BinaryTreeNode<ElemType>* node);
    int GetTreeHeight_recursive(BinaryTreeNode<ElemType>* node);
    int GetTreeNodeCount_recursive(BinaryTreeNode<ElemType>* node);
    int GetLeafNodeCount_recursive(BinaryTreeNode<ElemType>* node);
};

//BinaryTreeNode实现
template <typename ElemType>
BinaryTreeNode<ElemType>::BinaryTreeNode(ElemType data, BinaryTreeNode<ElemType>* left, BinaryTreeNode<ElemType>* right)
{
    this->data = data;
    this->left = left;
    this->right = right;
}

template <typename ElemType>
ElemType BinaryTreeNode<ElemType>::getData() const
{
    return data;
}

template <typename ElemType>
void BinaryTreeNode<ElemType>::setData(ElemType data)
{
    this->data = data;
}

template <typename ElemType>
BinaryTreeNode<ElemType>* BinaryTreeNode<ElemType>::getLeft() const
{
    return left;
}

template <typename ElemType>
void BinaryTreeNode<ElemType>::setLeft(BinaryTreeNode<ElemType>* left)
{
    this->left = left;
}

template <typename ElemType>
BinaryTreeNode<ElemType>* BinaryTreeNode<ElemType>::getRight() const
{
    return right;
}

template <typename ElemType>
void BinaryTreeNode<ElemType>::setRight(BinaryTreeNode<ElemType>* right)
{
    this->right = right;
}

//BinaryTree实现
template <typename ElemType>
BinaryTree<ElemType>::BinaryTree()//构造函数
{
    root = nullptr;
}

template <typename ElemType>
BinaryTree<ElemType>::~BinaryTree()//析构函数
{
    destroyTree(root);
}

template <typename ElemType>
void BinaryTree<ElemType>::destroyTree(BinaryTreeNode<ElemType>* node)//撤销树
{
    if (node != nullptr) 
    {
        destroyTree(node->getLeft());
        destroyTree(node->getRight());
        delete node;
    }
}

template <typename ElemType>
BinaryTreeNode<ElemType>* BinaryTree<ElemType>::copyTree(BinaryTreeNode<ElemType>* node)//复制树
{
    if (node == nullptr) 
    {
        return nullptr;
    }
    BinaryTreeNode<ElemType>* newNode = NewNode(node->getData(), copyTree(node->getLeft()), copyTree(node->getRight()));
    return newNode;
}

template <typename ElemType>
BinaryTree<ElemType>::BinaryTree(const BinaryTree<ElemType>& other)//拷贝构造函数
{
    root = copyTree(other.root);
}

template <typename ElemType>
BinaryTree<ElemType>& BinaryTree<ElemType>::operator=(const BinaryTree<ElemType>& other)//赋值运算符重载
{
    if (this != &other) 
    {
        destroyTree(root);
        root = copyTree(other.root);
    }
    return *this;
}

template <typename ElemType>
BinaryTreeNode<ElemType>* BinaryTree<ElemType>::getRoot()//获得根结点
{
    return root;
}

template <typename ElemType>
BinaryTreeNode<ElemType>* BinaryTree<ElemType>::NewNode(ElemType data, BinaryTreeNode<ElemType>* left, BinaryTreeNode<ElemType>* right)//创建新结点
{
    return new BinaryTreeNode<ElemType>(data, left, right);
}

template <typename ElemType>
void BinaryTree<ElemType>::MakeTree(BinaryTree<ElemType>* bt, ElemType data, BinaryTreeNode<ElemType>* left, BinaryTreeNode<ElemType>* right)//建树
{
    root = NewNode(data, left, right);
}

template <typename ElemType>
void BinaryTree<ElemType>::PreOrderPrint_recursive(BinaryTreeNode<ElemType>* node)//递归先序遍历二叉树
{
    if (node != nullptr) 
    {
        std::cout << node->getData() << " ";
        PreOrderPrint_recursive(node->getLeft());
        PreOrderPrint_recursive(node->getRight());
    }
}

template <typename ElemType>
void BinaryTree<ElemType>::InOrderPrint_recursive(BinaryTreeNode<ElemType>* node)//递归中序遍历二叉树
{
    if (node != nullptr) 
    {
        InOrderPrint_recursive(node->getLeft());
        std::cout << node->getData() << " ";
        InOrderPrint_recursive(node->getRight());
    }
}

template <typename ElemType>
void BinaryTree<ElemType>::PostOrderPrint_recursive(BinaryTreeNode<ElemType>* node)//递归后序遍历二叉树
{
    if (node != nullptr) 
    {
        PostOrderPrint_recursive(node->getLeft());
        PostOrderPrint_recursive(node->getRight());
        std::cout << node->getData() << " ";
    }
}

template <typename ElemType>
void BinaryTree<ElemType>::LevelOrderPrint(BinaryTreeNode<ElemType>* node)//层次遍历二叉树
{
    if (node == nullptr) return;
    Queue<BinaryTreeNode<ElemType>*> queue;
    queue.enqueue(node);
    while (!queue.isEmpty()) 
    {
        BinaryTreeNode<ElemType>* current = queue.dequeue();
        std::cout << current->getData() << " ";
        if (current->getLeft() != nullptr) 
        {
            queue.enqueue(current->getLeft());
        }
        if (current->getRight() != nullptr) 
        {
            queue.enqueue(current->getRight());
        }
    }
}

template <typename ElemType>
int BinaryTree<ElemType>::GetTreeHeight_recursive(BinaryTreeNode<ElemType>* node)//求树高
{
    if (node == nullptr) return 0;
    int leftHeight = GetTreeHeight_recursive(node->getLeft());
    int rightHeight = GetTreeHeight_recursive(node->getRight());
    return (leftHeight > rightHeight ? leftHeight : rightHeight) + 1;
}

template <typename ElemType>
int BinaryTree<ElemType>::GetTreeNodeCount_recursive(BinaryTreeNode<ElemType>* node)//求总结点数
{
    if (node == nullptr) return 0;
    return 1 + GetTreeNodeCount_recursive(node->getLeft()) + GetTreeNodeCount_recursive(node->getRight());
}

template <typename ElemType>
int BinaryTree<ElemType>::GetLeafNodeCount_recursive(BinaryTreeNode<ElemType>* node)//求叶子结点数
{
    if (node == nullptr) return 0;
    if (node->getLeft() == nullptr && node->getRight() == nullptr) return 1;
    return GetLeafNodeCount_recursive(node->getLeft()) + GetLeafNodeCount_recursive(node->getRight());
}