# -*- coding: utf-8 -*-
"""
模拟12306车票候补模块（基础版 + 增强功能）
==========================================
数据结构：队列（FIFO）—— 使用 collections.deque 实现
作者：karry628
"""

from collections import deque
import time
import re


class Order:
    """候补订单类：订单号、旅客姓名、身份证号、所需票数、下单时间"""

    def __init__(self, order_id, name, id_card, tickets=1):
        self.order_id = order_id          # 订单号
        self.name = name                 # 旅客姓名
        self.id_card = id_card           # 身份证号
        self.tickets = tickets           # 所需票数（默认1张）
        self.create_time = time.strftime("%Y-%m-%d %H:%M:%S")  # 下单时间

    def __repr__(self):
        return (f"[订单号:{self.order_id}] 旅客:{self.name} "
                f"身份证:{self.id_card[:6]}********{self.id_card[-4:]} "
                f"票数:{self.tickets} 下单时间:{self.create_time}")


class WaitListSystem:
    """12306候补排队系统"""

    def __init__(self):
        self.queue = deque()        # 候补队列（队首在左，队尾在右）
        self.order_counter = 1000   # 订单号自增计数器
        self.total_wait = 0         # 队列中等待的总票数

    # ---------- 工具方法 ----------
    def _next_order_id(self):
        """生成下一个订单号"""
        self.order_counter += 1
        return f"WX{self.order_counter}"

    def _validate_id_card(self, id_card):
        """简单校验身份证号（18位）"""
        return bool(re.match(r"^\d{17}[\dXx]$", id_card))

    # ---------- 核心操作1：新增候补订单（入队） ----------
    def add_order(self):
        print("\n" + "=" * 40)
        print("  新增候补订单")
        print("=" * 40)

        name = input("请输入旅客姓名：").strip()
        if not name:
            print("✗ 姓名不能为空！")
            return

        id_card = input("请输入身份证号（18位）：").strip()
        if not self._validate_id_card(id_card):
            print("✗ 身份证号格式不正确（应为18位）！")
            return

        try:
            tickets = int(input("请输入所需票数（默认1）：").strip() or "1")
            if tickets <= 0:
                print("✗ 票数必须大于0！")
                return
        except ValueError:
            print("✗ 票数输入无效！")
            return

        order_id = self._next_order_id()
        order = Order(order_id, name, id_card, tickets)
        self.queue.append(order)   # 加入队尾
        self.total_wait += tickets

        print(f"\n✓ 候补订单提交成功！")
        print(f"  {order}")
        print(f"  当前队列位置：第 {len(self.queue)} 位，等待票数：{self.total_wait}")

    # ---------- 核心操作2：余票发放（出队） ----------
    def distribute_tickets(self):
        print("\n" + "=" * 40)
        print("  余票发放")
        print("=" * 40)

        if not self.queue:
            print("✗ 候补队列为空，无需发放。")
            return

        try:
            k = int(input("请输入本次释放余票数量 k：").strip())
            if k <= 0:
                print("✗ 余票数量必须大于0！")
                return
        except ValueError:
            print("✗ 输入无效！")
            return

        remaining = k
        success_count = 0

        print(f"\n--- 开始发放 {k} 张余票 ---")
        while remaining > 0 and self.queue:
            head = self.queue[0]   # 看队首，但先不出队

            if head.tickets <= remaining:
                # 队首订单需求 <= 剩余余票，可以出票
                self.queue.popleft()
                remaining -= head.tickets
                self.total_wait -= head.tickets
                success_count += 1
                print(f"✓ 出票成功：{head}")
            else:
                # 队首订单需求 > 剩余余票，暂不出票，等待下次放票
                print(f"△ 余票不足，{head.name} 的 {head.tickets} 张票暂无法满足，等待下次放票")
                break

        print(f"\n--- 发放结束 ---")
        print(f"  成功出票 {success_count} 张订单，剩余余票 {remaining} 张")
        if self.queue:
            print(f"  仍有 {len(self.queue)} 个订单在等待，共需 {self.total_wait} 张票")
        else:
            print(f"  候补队列已全部清空！")

    # ---------- 核心操作3：查看队列状态 ----------
    def show_queue(self):
        print("\n" + "=" * 40)
        print("  候补队列状态")
        print("=" * 40)

        if not self.queue:
            print("  候补队列为空。")
            return

        print(f"  队列总人数：{len(self.queue)} 人，等待总票数：{self.total_wait} 张")
        print("-" * 40)
        for i, order in enumerate(self.queue, 1):
            print(f"  第{i}位: {order}")

    # ---------- 增强功能：取消候补 ----------
    def cancel_order(self):
        print("\n" + "=" * 40)
        print("  取消候补订单")
        print("=" * 40)

        if not self.queue:
            print("✗ 候补队列为空。")
            return

        order_id = input("请输入要取消的订单号：").strip()
        for i, order in enumerate(self.queue):
            if order.order_id == order_id:
                self.queue.remove(order)
                self.total_wait -= order.tickets
                print(f"✓ 已取消订单：{order}")
                return
        print(f"✗ 未找到订单号为 {order_id} 的订单。")

    # ---------- 主菜单 ----------
    def run(self):
        print("=" * 50)
        print("   欢迎使用 12306 车票候补系统（模拟版）")
        print("=" * 50)

        while True:
            print("\n" + "-" * 30)
            print("  1. 新增候补订单（入队）")
            print("  2. 余票发放（出队）")
            print("  3. 查看候补队列")
            print("  4. 取消候补订单")
            print("  5. 退出程序")
            print("-" * 30)

            choice = input("请输入操作编号(1-5)：").strip()

            if choice == "1":
                self.add_order()
            elif choice == "2":
                self.distribute_tickets()
            elif choice == "3":
                self.show_queue()
            elif choice == "4":
                self.cancel_order()
            elif choice == "5":
                print("\n感谢使用，再见！")
                break
            else:
                print("✗ 输入无效，请输入 1-5 之间的数字。")


if __name__ == "__main__":
    system = WaitListSystem()
    system.run()
