<script type="text/x-mathjax-config">
 MathJax.Hub.Config({tex2jax: {inlineMath:[['$','$']]}});
 </script>
 <script type="text/javascript" src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML"></script>

## 96. 不同的二叉搜索树
> 给定一个整数 n，求以 1 ... n 为节点组成的二叉搜索树有多少种？

```python
"""
G(n) 表示长度为n构成的二叉搜索树的总数
F(i, n) 以 i为根，长度为n 构成的二叉搜索树的个数

F(i, n)取决于[1, i - 1]  和 [i + 1, n] 构成的子树个数(笛卡尔积)
[1, i - 1] 构成的二叉搜索的个数可以用G(i-1) 表示
[i+1, n] 构成的二叉搜索树的个数可以用G(n-i) 表示

F(i, n) = G(i-1) * G(n - i)

G(n) = G(i-1) * G(n - i)   1 <= i <= n

eg: 
G(0) = 1
G(1) = 1
G(2) = F(1, 2) + F(2, 2) = 2
G(3) = G(0) * G(2) + G(1) * G(1) + G(2) * G(0) = 2 + 2 + 1 = 5
G(4) ...
可以计算G(n)
时间复杂度：O(n^2)
空间复杂度：O(n)
"""

def num_trees(n: int) -> int:
    if n <= 1: return 1
    dp = [0] * (n + 1)
    dp[0], dp[1] = 1, 1
    for i in range(2, n + 1):
        for j in range(1, i + 1):
            dp[i] += dp[j - 1] * dp[i - j]
    return dp[n]
```

## 95. 不同的二叉搜索树 II
> 给定一个整数 n，生成所有由 1 ... n 为节点所组成的 二叉搜索树

```python
"""
95. 不同的二叉搜索树 II
解题思路：利用二叉搜索数的特征
    左节点的值都小于root节点的值
    右节点的值都大于root节点的值

以1...n 为节点组成的二叉搜索数的数量假设为G
以i (1<=i<=n) 为节点的二叉树的数量为G(i)
那么G = G(1) + ... + G(n)

G(i) 取决于小于[1, i-1] 范围构成的左子树 和 [i+1, n] 范围内构成的右子树
以i为root，遍历组合左子树和右子树，就是以i为根节点构成的所有有效的二叉搜索树
时间复杂度：
空间复杂度：
卡塔兰数 
"""
from typing import List


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def generate_tree(n: int) -> List[TreeNode]:

    all_trees: List[TreeNode] = []
    def _generate_trees(start: int, end: int) -> List[TreeNode]:
        # 边界条件检查
        if start > end:
            return []
        for i in range(start, end + 1):
            left = _generate_trees(start, i - 1)
            right = _generate_trees(i + 1, end)
            
            for l_item in left:
                for r_item in right:
                    new_node = TreeNode(i)
                    new_node.left = l_item
                    new_node.right = r_item
                    all_trees.append(new_node)
            print(all_trees)
        return all_trees
    if n == 0:
        return []
    return _generate_trees(1, n)
```

## 22. 括号生成
### 题目描述
```python
数字 n 代表生成括号的对数，请你设计一个函数，用于能够生成所有可能的并且 有效的 括号组合。
输入：n = 3
输出：["((()))","(()())","(())()","()(())","()()()"]
```
### 解题思路
![][image-1]
重点：画图，画了图怎么解题，一目了然。
递归回溯下一个可以添加的括号，当数组的长度为2n时，检查括号对是否有效。
时间复杂度：O(n2^2n)从上图可以看出，层级的节点会按照指数级增长
$latex 1 \Rightarrow 2^2 \Rightarrow  2^3 \Rightarrow  2^4 \Rightarrow 2^5 \Rightarrow 2^6  \Rightarrow...\Rightarrow 2^{2n}$
$latex sum(nodes) = \begin{matrix} \sum\_{k=1}^{2n} 2^{k}\end{matrix}$

```python
"""
暴力解法
"""
def generate_parenthesis(n: int) -> List[str]:
    res = set()
    def helper(tmp, left, right):
        if len(tmp) == 2 * n:
            if valid(tmp):
                res.add("".join(tmp))
        else:
            tmp.append('(')
            helper(tmp, left + 1, right)
            tmp.pop()
            tmp.append(')')
            helper(tmp, left, right + 1)
            tmp.pop()
        return res
    helper([], 0, 0)
    return list(res)

```
从图中可以看到可以优化的点：
1. 同一方向的符号数量不能超过n，超过n就无效了
2. 先’(’后‘)’，保证‘)’的数量不大于’(‘的数量就能保证括号对的有效性。

```python
"""
优化后的代码
"""
def generate_parenthesis(n: int) -> List[str]:
    res = set()
    def helper(tmp, left, right):
        if len(tmp) == 2 * n:
            res.add("".join(tmp))
            return
        else:
            if left < n:
                tmp.append('(')
                helper(tmp, left + 1, right)
                tmp.pop()
            if right < left:
                tmp.append(')')
                helper(tmp, left, right + 1)
                tmp.pop()
        return res
    helper([], 0, 0)
    return list(res)     
```

```python
"""
验证括号对的有效性
"""
def valid(tmp):
    balance = 0
    if not tmp:
        return False
    for i in range(len(tmp)):
        if tmp[i] == '(':
            balance += 1
        else:
            balance -= 1
        if balance < 0:
            return False
    return balance == 0
```

## 卡塔兰数
英文名Catalan number，是组合数学中一个常出现在各种计数问题中的数列。
第n个卡塔兰数的公式如下：
 $latex h(n) = \frac{C_{2n}^n}{n+1} = C_{2n}^n - C\_{2n}^{n+1} $
其中关于组合的公式公式：
$latex \dbinom{2n}{n}=\binom{2n}{n}=\mathrm{C}\_{2n}^n=\frac{2n!}{{n!}{n!}}$
递归公式
$latex C_{n+1} = C\_0C\_n + C\_1C_{n-1} + ... + C\_nC\_0 = \begin{matrix} \sum_{k=0}^N C\_kC_{n-k} \end{matrix}$

￼## 引用
[1]()[mail.google.com/mail/u/0/#inbox][2]
[2][3][https://brooksj.com/2019/09/23/%E5%8D%A1%E7%89%B9%E5%85%B0%E6%95%B0-Catalan-Number/][4]

[2]:	mail.google.com/mail/u/0/#inbox
[3]:	https://brooksj.com/2019/09/23/%E5%8D%A1%E7%89%B9%E5%85%B0%E6%95%B0-Catalan-Number/
[4]:	https://brooksj.com/2019/09/23/%E5%8D%A1%E7%89%B9%E5%85%B0%E6%95%B0-Catalan-Number/

[image-1]:	https://tva1.sinaimg.cn/large/008eGmZEly1gpnzl2n0pcj30sy0ze0wh.jpg width=400 height=350