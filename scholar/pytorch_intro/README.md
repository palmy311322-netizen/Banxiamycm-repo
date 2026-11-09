# PyTorch 基础教程（中文学习笔记）

本目录对照官方 [Learn the Basics](https://pytorch.org/tutorials/beginner/basics/) 教程整理，用中文重建一条从“张量”到“训练并保存模型”的完整知识链。

> 说明：
> - 这里是中文概括、知识补充、学习提示和官方链接，不是官方教程的逐字翻译或全文转载；代码示例沿用官方教程的思路并做了少量整理，完整解释以官方页面为准。
> - 内容核对时间：2026-11。代码默认面向 PyTorch 2.x 与 `torchvision.transforms.v2`；关键 API 已在本机 PyTorch 2.14.1 / torchvision 0.29.1 下验证。不同版本若 API 有差异，以官方文档为准。

## 这套笔记要解决什么

学完本目录，你应该能独立回答并动手完成：

1. 数据在 PyTorch 里如何表示和运算？
2. 如何把原始数据变成按批次送入模型的输入？
3. 如何用 `nn.Module` 搭建网络？
4. 梯度是如何自动算出来的？
5. 如何写一个正确的训练 / 评估循环？
6. 如何保存、恢复并再次使用训练好的模型？

## 知识地图

```text
01 入门介绍 ── 建立全局流程
      │
02 快速开始 ── 用 FashionMNIST 串起完整流程
      │
      ├─ 03 张量 ──────────────── 数据表示与运算
      │        │
      │        ├─ 04 数据集与 DataLoader ── 按批次读取数据
      │        │        │
      │        │        └─ 05 变换 ─────── 原始样本 → 模型输入
      │        │
      │        └─ 06 构建神经网络 ─────── 搭模型、管参数
      │                 │
      │                 └─ 07 自动微分 ── 计算梯度
      │                          │
      │                          └─ 08 优化模型参数 ── 训练循环
      │                                   │
      │                                   └─ 09 保存与加载模型
```

一句话心智模型：

```text
数据 → 前向传播 → 损失 → 反向传播 → 更新参数 → 评估 → 保存
```

## 章节导航

| 章节 | 核心问题 | 关键 API / 概念 |
| --- | --- | --- |
| [01 入门介绍](./01-入门介绍.md) | 训练一个模型要经历哪些步骤？ | 工作流、PyTorch 生态、运行方式 |
| [02 快速开始](./02-快速开始.md) | 最小可运行流程长什么样？ | `DataLoader`、`nn.Module`、`CrossEntropyLoss`、`SGD` |
| [03 张量](./03-张量.md) | 数据如何表示、变形和运算？ | `torch.tensor`、`shape/dtype/device`、`matmul`、`cat/stack` |
| [04 数据集与数据加载器](./04-数据集与数据加载器.md) | 数据如何按批次高效读取？ | `Dataset`、`DataLoader`、`random_split`、`num_workers` |
| [05 变换](./05-变换.md) | 原始样本如何变成模型输入？ | `transforms.v2.Compose`、`ToImage`、`ToDtype`、`Normalize` |
| [06 构建神经网络](./06-构建神经网络.md) | 网络如何用模块搭建？ | `nn.Module`、`nn.Linear`、`nn.Sequential`、`parameters()` |
| [07 自动微分](./07-自动微分.md) | 梯度如何自动计算？ | `requires_grad`、`backward()`、`no_grad()`、`detach()` |
| [08 优化模型参数](./08-优化模型参数.md) | 参数如何迭代更新？ | 损失函数、`optim.SGD/Adam`、`train()/eval()` |
| [09 保存与加载模型](./09-保存与加载模型.md) | 训练结果如何持久化？ | `state_dict`、`torch.save/load`、`map_location` |

## 建议学习路径

**零基础（推荐）**

1. 读 01、02，先看清完整流程，不必立刻抠细节；
2. 按 03 → 04 → 05 → 06 → 07 → 08 顺序学习；
3. 最后读 09，并回到 02 把快速开始代码完整跑一遍。

**有 NumPy / 其他深度学习框架经验**

1. 先看 02 了解 PyTorch 写法；
2. 重点看 06、07、08 中与其它框架不同的部分（动态图、`zero_grad`、`train/eval`）；
3. 按需查阅 03、04、05 的 API。

**只想先跑通训练**

直接进入 02，照着代码运行；遇到不理解的符号再回到对应章节。

## 环境准备

建议使用虚拟环境，并按官方安装选择器生成与你显卡 / 系统匹配的命令：

- 安装选择器：<https://pytorch.org/get-started/locally/>

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip

# 以下为 CPU 版示例；有 NVIDIA GPU 时请使用官网选择器给出的 CUDA 命令
pip install torch torchvision
```

验证安装：

```python
import torch
import torchvision

print("torch:", torch.__version__)
print("torchvision:", torchvision.__version__)
print("cuda available:", torch.cuda.is_available())
```

选择设备（新版本推荐写法，能自动适配 CUDA / MPS / XPU 等加速器）：

```python
device = (
    torch.accelerator.current_accelerator().type
    if torch.accelerator.is_available()
    else "cpu"
)
print(f"Using {device} device")
```

> 旧版本没有 `torch.accelerator` 时，可退回 `"cuda" if torch.cuda.is_available() else "cpu"`。

## 阅读约定

- 代码块中的 `device` 默认指上一节选出的训练设备。
- 输入张量形状统一用 `[N, C, H, W]` 表示：批大小、通道数、高、宽。
- 分类模型的输出默认是 **logits**（未归一化分数），通常直接交给 `nn.CrossEntropyLoss`。
- 训练集可以打乱并做随机增强；验证 / 测试集使用确定性预处理。
- 每个训练批次都要保证：清零梯度 → 前向 → 损失 → 反向 → 更新。

## 官方资源

- [Learn the Basics 教程总目录](https://pytorch.org/tutorials/beginner/basics/)
- [PyTorch 官方文档](https://docs.pytorch.org/docs/stable/)
- [PyTorch 安装选择器](https://pytorch.org/get-started/locally/)
- [torch API](https://pytorch.org/docs/stable/torch.html)
- [torch.nn API](https://pytorch.org/docs/stable/nn.html)
- [torch.utils.data API](https://pytorch.org/docs/stable/data.html)
- [torchvision.transforms.v2 API](https://pytorch.org/vision/stable/transforms.html)
- [PyTorch Tutorials GitHub](https://github.com/pytorch/tutorials)

## 章节入口

1. [入门介绍](./01-入门介绍.md)
2. [快速开始](./02-快速开始.md)
3. [张量](./03-张量.md)
4. [数据集与数据加载器](./04-数据集与数据加载器.md)
5. [变换](./05-变换.md)
6. [构建神经网络](./06-构建神经网络.md)
7. [自动微分](./07-自动微分.md)
8. [优化模型参数](./08-优化模型参数.md)
9. [保存与加载模型](./09-保存与加载模型.md)
