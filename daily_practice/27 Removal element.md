

## [27 移除元素][1]
**题目描述**
给你一个数组 nums 和一个值 val，你需要 原地 移除所有数值等于 val 的元素，并返回移除后数组的新长度。
不要使用额外的数组空间，你必须仅使用 O(1) 额外空间并 原地 修改输入数组。
元素的顺序可以改变。你不需要考虑数组中超出新长度后面的元素。

**解题思路**
```python
"""
解题思路：双指针
i, j 都初始化为0
想让nums[i]为槽
如果nums[j] == target: j移动到下一个元素，不占用当前槽
如果nums[j] != target: nums[i] = nums[j]，i移动到下一个槽，j 移动到下一个元素

3  2   2   3   val = 3
x  2   2   3
2  x   2   3
2  2   x   3
2  2   x   3

时间复杂度：O(n) 一次遍历
空间复杂度：O(1) 
"""
```

**代码**
```python
def remove_element(nums: List[int], val: int) -> int:
    i = 0
    for j in range(len(nums)):
        if nums[j] != val:
            nums[i] = nums[j]
            i += 1
    return i
```

**优化解法**
```python
"""
双指针优化，前后双指针
i, j 分别指向头部和尾部，目的是保证i指向的每一个元素都不等于target
nums[i] = nums[j - 1] j -= 1，直到nums[i] 不等于target，i 才递进一次。
边界条件：i < j

时间复杂度：O(n)
空间复杂度：O(1)
"""
def remove_element(nums: List[int], val: int) -> int:
    i, j = 0, len(nums)
    while i < j:
        if nums[i] == val:
            nums[i] = nums[j - 1]
            j -= 1
        else:
            i += 1
    return i
```
---- 
## [剑指 Offer 54. 二叉搜索树的第k大节点][2]
**描述**
给定一棵二叉搜索树，请找出其中第k大的节点。

```python

"""
解题思路
RNL遍历,弹出的第k个元素就是第k大节点
4 3 2 1
时间复杂度：O(n)
空间复杂度：O(n)
"""

def kth_largest(root: TreeNode, k: int) -> int:
    stack = []
    count = 0
    while stack or root:
        if root:
            stack.append(root)
            root = root.right
        else:
            peek = stack.pop()
            count += 1
            if count == k:
                return peek.val
            if peek.left:
                root = peek.left
```
---- 
##  **[二叉树最大宽度][3]**
```python

"""
662. 二叉树最大宽度
宽度很容易想到使用BFS算法
入队列的时候，同时添加节点的深度和位置
假设root节点的pos 为i
pos(root.left) = 2*i
pos(root.right)  2*i + 1
在同一深度上不断计算宽度，保存最大的宽度
时间复杂度：O(n)
空间复杂度：O(n)
"""

def width_of_binary_tree(root: TreeNode) -> int:
    if root is None: return 0
    queue = [(root, 0, 0)]
    max_width = 0
    last_depth = 0
    last_pos = 0
    while queue:
        root, depth, pos = queue.pop(0)
        if depth == last_depth:
            max_width = max(max_width, pos - last_pos)
        else:
            last_depth = depth
            last_pos = pos
        if root.left:
            queue.append((root.left, depth + 1, pos * 2))
        if root.right:
            queue.append((root.right, depth + 1, pos * 2 + 1)) 
    return max_width + 1
```
---- 
##  **[从中序与后序遍历序列构造二叉树][4]**

```python

"""
106. 从中序与后序遍历序列构造二叉树
中序遍历: [左子树  节点  右子树]
后序遍历: [左子树  右子树 节点] =>  [节点  右子树   左子树]
[9, 3, 15, 20, 7]
[3, 20, 7, 15, 9]
然后使用递归处理左子树，右子树
时间复杂度：O(n)
空间复杂度：O(n)
"""

def build_tree(inorder: List[int], postorder: List[int]) -> TreeNode:
    preorder = postorder[::-1]
    in_map = {}
    for i, item in enumerate(inorder):
        in_map[item] = i

    def dfs(pre_s: int, pre_e: int, in_s: int, in_e: int) -> TreeNode:
        if pre_s > pre_e or in_s > in_e:
            return None
        
        root = TreeNode(preorder[pre_s])
        root_index = in_map[root.val] # 1
        l_len = root_index - in_s    # 1
        r_len = in_e - root_index    # 3

        root.left = dfs(pre_s + r_len + 1, pre_e, in_s, root_index - 1)
        root.right = dfs(pre_s + 1, pre_s + r_len, root_index + 1, in_e)
        return root
    return dfs(0, len(preorder) - 1, 0, len(inorder) - 1)
```
---- 
## **[114. 二叉树展开为链表][5]**

```python

"""
解题思路：先序遍历方式
时间复杂度：O(n)
空间复杂度：O(n)
"""

def flatten(root: TreeNode) -> None:
    # 边界条件
    if not root: return
    res = []
    def dfs(root: TreeNode) -> None:
        if root is None: return
        res.append(root)
        left = dfs(root.left)
        right = dfs(root.right)
    # 执行递归，构造前序遍历
    dfs(root)
    # 对前序遍历结果进行连接
    res[0].left = None
    for i in range(1, len(res)):
        res[i - 1].right, res[i].left = res[i], None
    return res
        
"""
二叉树结构：
[1, 2, 5, 3, 4, null, 6]
迭代方式前序遍历过程中，stack 和 pre的变化过程：

stack = [1]   [5, 2]    [5, 3]   [5, 4]  [5]  [6]
pre   = None    1        2          3     4    6
在遍历的过程中，完成链表的构造：
    peek = stack.pop()
    pre.left = None
    pre.right = peek
时间复杂度：O(n)
空间复杂度：O(n)
"""
def flatten(root: TreeNode) -> None:
    # 边界条件处理
    if not root: return
    stack = [root]
    pre = None
    while stack:
        peek = stack.pop()
        if pre:
            pre.left = None
            pre.right = peek
        left, right = peek.left, peek.right
        if right:
            stack.append(right)
        if left:
            stack.append(left)
        pre = peek
```
---- 
## **[面试题 04.05. 合法二叉搜索树][6]**
```python
"""
解题思路：利用二叉搜索树的规则
左边的节点的值小于根节点的值
右边的节点的值大于根节点的值
时间复杂度：O(n)
空间复杂度：O(n)
"""


import sys
class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

def is_valid_bst(root: TreeNode) -> bool:
    if root is None: return True
    def dfs(root: TreeNode, low: int, high: int) -> bool:
        if root is None: return True
        if root.val <= low or root.val >= high: return False
        # 开始处理左右节点数据
        return dfs(root.left, low, root.val) and dfs(root.right, root.val, high)
    return dfs(root, -sys.maxsize, sys.maxsize)

# root = TreeNode(10)
# root.left = TreeNode(9)
# root.right = TreeNode(11)
# print(is_valid_bst(root))
```
---- 
## **[337. 打家劫舍 III][7]**
```python


def steal(root: TreeNode) -> int:
    in_map = {}
    def helper(root) -> int:
        if root is None: return 0
        # 检查是否已经处理过该节点
        if root in in_map:
            return in_map[root]
        
        left = helper(root.left)
        right = helper(root.right)
        l_left, l_right, r_left, r_right = 0, 0, 0, 0
        if root.left:
            l_left = helper(root.left.left)
            l_right = helper(root.left.right)
        if root.right:
            r_left= helper(root.right.left)
            r_right = helper(root.right.right)
        in_map[root] = max(left + right, l_left + l_right + r_left + r_right + root.val)
        
        return in_map[root]
    helper(root)
    return in_map[root]
```

[1]:	https://leetcode-cn.com/problems/remove-element/
[2]:	https://leetcode-cn.com/problems/er-cha-sou-suo-shu-de-di-kda-jie-dian-lcof/
[3]:	https://leetcode-cn.com/problems/maximum-width-of-binary-tree/
[4]:	https://leetcode-cn.com/problems/construct-binary-tree-from-inorder-and-postorder-traversal/
[5]:	https://leetcode-cn.com/problems/flatten-binary-tree-to-linked-list/
[6]:	https://leetcode-cn.com/problems/legal-binary-search-tree-lcci/
[7]:	https://leetcode-cn.com/problems/house-robber-iii/

#二叉树