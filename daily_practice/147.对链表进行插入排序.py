"""
147. 对链表进行插入排序
因为按照升序排序，取dummy 为一个特别大的值, head = dummy
dummy->1->2->3->4->7-->6-->8-->2
要处理的节点是cur_node   6
处理6 之前需要记录下 6的上一个节点pre_node 和 下一个节点 next_node ; 边界pre_node = head

每次遍历都从dummy 开始，head 存储 dummy, 遍历到pre_order: head != pre_order and head.next.val < cur_order.val: head = head.next
上个循环语句的退出条件有两个，检查每个退出条件。
1. head == pre_order:  说明 cur_node 的位置合适，不需要调整
2. head.next.val < cur_order.val:  需要调整，先把cur_node 从原来的位置拿掉，然后放到当前head的后面
3. 处理下一个节点 next_node

时间复杂度：O(n^2)
空间复杂度：O(1)
"""


import sys


class ListNode:
    def __init__(self, val):
        self.val = val
        self.next = None


def insertion_sort_list(head: ListNode) -> ListNode:
    if not head or not head.next:
        return head
    # 定义哑巴节点
    dummy = ListNode(sys.maxsize - 1)
    dummy.next = head
    head = dummy

    pre_node = head
    cur_node = pre_node.next
    # 开始执行插入逻辑
    while cur_node:
        head = dummy
        next_node = cur_node.next
        while head != pre_node and head.next.val < cur_node.val:
            head = head.next
        # 如果当前节点不需要处理
        if head == pre_node:
            pre_node = cur_node
            cur_node = next_node
            continue

        # 需要执行交换, 在原来的位置拿掉该节点
        pre_node.next = next_node

        # 放到当前head的后面
        tmp = head.next
        head.next = cur_node
        head.next.next = tmp

        # 处理下一个节点
        cur_node = next_node
    return dummy.next
