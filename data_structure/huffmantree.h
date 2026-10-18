#pragma once

#include "heap.h"
#include <iostream>
#include <string>
#include <vector>
#include <map>
using namespace std;

template <typename ElemType>
class HuffmanTreeNode
{
private:
    ElemType data;
    int weight;
    HuffmanTreeNode<ElemType>* left;
    HuffmanTreeNode<ElemType>* right;
    HuffmanTreeNode<ElemType>* parent;
public:
    HuffmanTreeNode();
    HuffmanTreeNode(ElemType data, int weight);
    ElemType getData() const;
    void setData(ElemType data);
    int getWeight() const;
    void setWeight(int weight);
    HuffmanTreeNode<ElemType>* getLeft() const;
    void setLeft(HuffmanTreeNode<ElemType>* left);
    HuffmanTreeNode<ElemType>* getRight() const;
    void setRight(HuffmanTreeNode<ElemType>* right);
    HuffmanTreeNode<ElemType>* getParent() const;
    void setParent(HuffmanTreeNode<ElemType>* parent);
};

template <typename ElemType>
struct HuffmanNodeCompare
{
    bool operator()(const HuffmanTreeNode<ElemType>* a, const HuffmanTreeNode<ElemType>* b) const
    {
        return a->getWeight() < b->getWeight();
    }
};

template <typename ElemType>
class HuffmanTree
{
private:
    HuffmanTreeNode<ElemType>* root;
    void destroyTree(HuffmanTreeNode<ElemType>* node);
    void generateCodes(HuffmanTreeNode<ElemType>* node, string code, map<ElemType, string>& codes);
public:
    HuffmanTree();
    ~HuffmanTree();
    void build(const vector<ElemType>& data, const vector<int>& weights);
    HuffmanTreeNode<ElemType>* getRoot();
    map<ElemType, string> getCodes();
    void printCodes();
    vector<int> encode(const vector<ElemType>& text);
    vector<ElemType> decode(const vector<int>& bits);
};

//HuffmanTreeNode实现
template <typename ElemType>
HuffmanTreeNode<ElemType>::HuffmanTreeNode()//默认构造函数
{
    data = ElemType();
    weight = 0;
    left = nullptr;
    right = nullptr;
    parent = nullptr;
}

template <typename ElemType>
HuffmanTreeNode<ElemType>::HuffmanTreeNode(ElemType data, int weight)//带参构造函数
{
    this->data = data;
    this->weight = weight;
    this->left = nullptr;
    this->right = nullptr;
    this->parent = nullptr;
}

template <typename ElemType>
ElemType HuffmanTreeNode<ElemType>::getData() const
{
    return data;
}

template <typename ElemType>
void HuffmanTreeNode<ElemType>::setData(ElemType data)
{
    this->data = data;
}

template <typename ElemType>
int HuffmanTreeNode<ElemType>::getWeight() const
{
    return weight;
}

template <typename ElemType>
void HuffmanTreeNode<ElemType>::setWeight(int weight)
{
    this->weight = weight;
}

template <typename ElemType>
HuffmanTreeNode<ElemType>* HuffmanTreeNode<ElemType>::getLeft() const
{
    return left;
}

template <typename ElemType>
void HuffmanTreeNode<ElemType>::setLeft(HuffmanTreeNode<ElemType>* left)
{
    this->left = left;
}

template <typename ElemType>
HuffmanTreeNode<ElemType>* HuffmanTreeNode<ElemType>::getRight() const
{
    return right;
}

template <typename ElemType>
void HuffmanTreeNode<ElemType>::setRight(HuffmanTreeNode<ElemType>* right)
{
    this->right = right;
}

template <typename ElemType>
HuffmanTreeNode<ElemType>* HuffmanTreeNode<ElemType>::getParent() const
{
    return parent;
}

template <typename ElemType>
void HuffmanTreeNode<ElemType>::setParent(HuffmanTreeNode<ElemType>* parent)
{
    this->parent = parent;
}

//HuffmanTree实现
template <typename ElemType>
HuffmanTree<ElemType>::HuffmanTree()//构造函数
{
    root = nullptr;
}

template <typename ElemType>
HuffmanTree<ElemType>::~HuffmanTree()//析构函数
{
    destroyTree(root);
}

template <typename ElemType>
void HuffmanTree<ElemType>::destroyTree(HuffmanTreeNode<ElemType>* node)//撤销树
{
    if (node != nullptr)
    {
        destroyTree(node->getLeft());
        destroyTree(node->getRight());
        delete node;
    }
}

template <typename ElemType>
void HuffmanTree<ElemType>::build(const vector<ElemType>& data, const vector<int>& weights)//构建哈夫曼树
{
    Heap<HuffmanTreeNode<ElemType>*, HuffmanNodeCompare<ElemType>> heap;
    for (int i = 0; i < (int)data.size(); i++)
    {
        HuffmanTreeNode<ElemType>* node = new HuffmanTreeNode<ElemType>(data[i], weights[i]);
        heap.push(node);
    }
    while (heap.size() > 1)
    {
        HuffmanTreeNode<ElemType>* left = heap.top();
        heap.pop();
        HuffmanTreeNode<ElemType>* right = heap.top();
        heap.pop();

        HuffmanTreeNode<ElemType>* parent = new HuffmanTreeNode<ElemType>();
        parent->setWeight(left->getWeight() + right->getWeight());
        parent->setLeft(left);
        parent->setRight(right);
        left->setParent(parent);
        right->setParent(parent);

        heap.push(parent);
    }
    root = heap.top();
    root->setParent(nullptr);
}

template <typename ElemType>
HuffmanTreeNode<ElemType>* HuffmanTree<ElemType>::getRoot()//获取根结点
{
    return root;
}

template <typename ElemType>
void HuffmanTree<ElemType>::generateCodes(HuffmanTreeNode<ElemType>* node, string code, map<ElemType, string>& codes)//递归生成哈夫曼编码
{
    if (node == nullptr) return;
    if (node->getLeft() == nullptr && node->getRight() == nullptr)//叶子结点
    {
        codes[node->getData()] = code;
        return;
    }
    generateCodes(node->getLeft(), code + "0", codes);
    generateCodes(node->getRight(), code + "1", codes);
}

template <typename ElemType>
map<ElemType, string> HuffmanTree<ElemType>::getCodes()//获取哈夫曼编码表
{
    map<ElemType, string> codes;
    generateCodes(root, "", codes);
    return codes;
}

template <typename ElemType>
void HuffmanTree<ElemType>::printCodes()//输出哈夫曼编码表
{
    map<ElemType, string> codes = getCodes();
    for (typename map<ElemType, string>::iterator it = codes.begin(); it != codes.end(); it++)
    {
        cout << it->first << ": " << it->second << endl;
    }
}

template <typename ElemType>
vector<int> HuffmanTree<ElemType>::encode(const vector<ElemType>& text)//哈夫曼编码
{
    map<ElemType, string> codes = getCodes();
    vector<int> bits;
    for (int i = 0; i < (int)text.size(); i++)
    {
        string code = codes[text[i]];
        for (int j = 0; j < (int)code.size(); j++)
        {
            bits.push_back(code[j] - '0');
        }
    }
    return bits;
}

template <typename ElemType>
vector<ElemType> HuffmanTree<ElemType>::decode(const vector<int>& bits)//哈夫曼解码
{
    vector<ElemType> result;
    HuffmanTreeNode<ElemType>* current = root;
    for (int i = 0; i < (int)bits.size(); i++)
    {
        if (bits[i] == 0)
            current = current->getLeft();
        else
            current = current->getRight();
        if (current->getLeft() == nullptr && current->getRight() == nullptr)//到达叶子结点
        {
            result.push_back(current->getData());
            current = root;
        }
    }
    return result;
}
