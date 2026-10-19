#pragma once
#include <vector>
#include <queue>
#include <stack>
using namespace std;

//树节点结构（用于树的遍历算法）
template <typename T>
struct TreeNode
{
    T val;
    TreeNode<T>* left;
    TreeNode<T>* right;
    TreeNode(T value) : val(value), left(nullptr), right(nullptr) {}
};

template <typename ElemType>
class SearchAlgorithms
{
public:
    //顺序搜索：从前往后逐个比较，返回元素下标，未找到返回-1
    static int SequentialSearch(const vector<ElemType>& data, const ElemType& target)
    {
        for (int i = 0; i < (int)data.size(); i++)
        {
            if (data[i] == target)
                return i;
        }
        return -1;
    }

    //二分搜索：要求data已排序，返回元素下标，未找到返回-1
    static int BinarySearch(const vector<ElemType>& data, const ElemType& target)
    {
        int low = 0, high = (int)data.size() - 1;
        while (low <= high)
        {
            int mid = (low + high) / 2;
            if (data[mid] == target)
                return mid;
            else if (target < data[mid])
                high = mid - 1;
            else
                low = mid + 1;
        }
        return -1;
    }

    //分块搜索：将data分为blockSize大小的块，indexTable存储每块最大元素
    //先对索引表顺序搜索确定块，再在块内顺序搜索
    //indexTable[i]为第i块的最大元素下标
    static int BlockSearch(const vector<ElemType>& data, const vector<int>& indexTable, int blockSize, const ElemType& target)
    {
        //先在索引表中确定目标所在块
        int blockIndex = -1;
        for (int i = 0; i < (int)indexTable.size(); i++)
        {
            if (target <= data[indexTable[i]])
            {
                blockIndex = i;
                break;
            }
        }
        if (blockIndex == -1)
            return -1;

        //在确定的块内顺序搜索
        int start = blockIndex * blockSize;
        int end = start + blockSize;
        if (end > (int)data.size())
            end = data.size();
        for (int i = start; i < end; i++)
        {
            if (data[i] == target)
                return i;
        }
        return -1;
    }

    //广度优先搜索(BFS)：从startNode开始，逐层遍历图
    //adjList为邻接表表示的图，adjList[i]存储节点i的所有邻接点
    //返回遍历顺序的节点序列
    static vector<int> BFS(const vector<vector<int> >& adjList, int startNode)
    {
        vector<int> result;
        int n = (int)adjList.size();
        vector<bool> visited(n, false);
        queue<int> q;

        visited[startNode] = true;
        q.push(startNode);

        while (!q.empty())
        {
            int node = q.front();
            q.pop();
            result.push_back(node);

            //将所有未访问的邻接点加入队列
            for (int neighbor : adjList[node])
            {
                if (!visited[neighbor])
                {
                    visited[neighbor] = true;
                    q.push(neighbor);
                }
            }
        }
        return result;
    }

    //深度优先搜索(DFS)：从startNode开始，深度优先遍历图
    //adjList为邻接表表示的图，adjList[i]存储节点i的所有邻接点
    //返回遍历顺序的节点序列
    static vector<int> DFS(const vector<vector<int> >& adjList, int startNode)
    {
        vector<int> result;
        int n = (int)adjList.size();
        vector<bool> visited(n, false);
        DFSHelper(adjList, startNode, visited, result);
        return result;
    }

    //树的DFS-前序遍历：根 -> 左 -> 右
    static vector<ElemType> TreePreOrder(TreeNode<ElemType>* root)
    {
        vector<ElemType> result;
        TreePreOrderHelper(root, result);
        return result;
    }

    //树的DFS-中序遍历：左 -> 根 -> 右
    static vector<ElemType> TreeInOrder(TreeNode<ElemType>* root)
    {
        vector<ElemType> result;
        TreeInOrderHelper(root, result);
        return result;
    }

    //树的DFS-后序遍历：左 -> 右 -> 根
    static vector<ElemType> TreePostOrder(TreeNode<ElemType>* root)
    {
        vector<ElemType> result;
        TreePostOrderHelper(root, result);
        return result;
    }

    //树的BFS-层序遍历：按层从左到右遍历
    static vector<ElemType> TreeLevelOrder(TreeNode<ElemType>* root)
    {
        vector<ElemType> result;
        if (root == nullptr)
            return result;

        queue<TreeNode<ElemType>*> q;
        q.push(root);

        while (!q.empty())
        {
            TreeNode<ElemType>* node = q.front();
            q.pop();
            result.push_back(node->val);

            if (node->left != nullptr)
                q.push(node->left);
            if (node->right != nullptr)
                q.push(node->right);
        }
        return result;
    }

private:
    //DFS递归辅助函数
    static void DFSHelper(const vector<vector<int>>& adjList, int node, vector<bool>& visited, vector<int>& result)
    {
        visited[node] = true;
        result.push_back(node);

        for (int neighbor : adjList[node])
        {
            if (!visited[neighbor])
            {
                DFSHelper(adjList, neighbor, visited, result);
            }
        }
    }

    //树的前序遍历辅助函数
    static void TreePreOrderHelper(TreeNode<ElemType>* node, vector<ElemType>& result)
    {
        if (node == nullptr)
            return;
        result.push_back(node->val);//根
        TreePreOrderHelper(node->left, result);//左
        TreePreOrderHelper(node->right, result);//右
    }

    //树的中序遍历辅助函数
    static void TreeInOrderHelper(TreeNode<ElemType>* node, vector<ElemType>& result)
    {
        if (node == nullptr)
            return;
        TreeInOrderHelper(node->left, result);//左
        result.push_back(node->val);//根
        TreeInOrderHelper(node->right, result);//右
    }

    //树的后序遍历辅助函数
    static void TreePostOrderHelper(TreeNode<ElemType>* node, vector<ElemType>& result)
    {
        if (node == nullptr)
            return;
        TreePostOrderHelper(node->left, result);//左
        TreePostOrderHelper(node->right, result);//右
        result.push_back(node->val);//根
    }
};
