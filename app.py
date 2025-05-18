import random
import time

class ChoreAssignmentAssistant:
    def __init__(self):
        self.chores = {
            "扫地": ["客厅", "卧室", "厨房", "卫生间"],
            "拖地": ["客厅", "卧室", "厨房", "卫生间"],
            "洗碗": [],
            "擦桌子": ["餐桌", "茶几", "书桌"],
            "倒垃圾": []
        }
        self.members = []

    def display_welcome(self):
        print("=" * 40)
        print("       家务分配助手")
        print("=" * 40)
        print("欢迎使用家务分配助手！")
        print("让我们一起公平地分配家务吧~")

    def add_members(self):
        while True:
            member = input("请输入家庭成员名字（输入q退出）：").strip()
            if member.lower() == 'q':
                break
            elif member:
                self.members.append(member)
                print(f"{member} 已加入！")
            else:
                print("名字不能为空，请重新输入。")

    def assign_chores(self):
        if not self.members:
            print("请先添加家庭成员。")
            return
        assigned_chores = {}
        for member in self.members:
            assigned_chores[member] = []

        for chore, locations in self.chores.items():
            if chore == "洗碗":
                num_dishes = int(input("请输入今天要洗的碗碟数量："))
                num_shifts = num_dishes // 10 + (1 if num_dishes % 10 != 0 else 0)
                for _ in range(num_shifts):
                    chosen_member = random.choice(self.members)
                    assigned_chores[chosen_member].append(chore)
            elif chore == "倒垃圾":
                num_bags = int(input("请输入今天要倒的垃圾袋数量："))
                for _ in range(num_bags):
                    chosen_member = random.choice(self.members)
                    assigned_chores[chosen_member].append(chore)
            else:
                for location in locations:
                    chosen_member = random.choice(self.members)
                    assigned_chores[chosen_member].append(f"{chore} {location}")

        return assigned_chores

    def display_assignment(self, assigned_chores):
        print("\n以下是家务分配结果：")
        time.sleep(1)
        for member, chores in assigned_chores.items():
            if chores:
                print(f"{member} 的任务：")
                for chore in chores:
                    print(f"- {chore}")
            else:
                print(f"{member} 今天很幸运，没有分配到家务~")
            print()

    def run(self):
        self.display_welcome()
        self.add_members()
        assigned_chores = self.assign_chores()
        self.display_assignment(assigned_chores)


if __name__ == "__main__":
    assistant = ChoreAssignmentAssistant()
    assistant.run()
