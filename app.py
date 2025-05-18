import streamlit as st
import random

def main():
    st.title("🧹 家务分配助手")
    st.write("公平分配家务，从今天开始！")

    # 初始化会话状态
    if 'members' not in st.session_state:
        st.session_state.members = []
    if 'assigned_chores' not in st.session_state:
        st.session_state.assigned_chores = {}

    # 家务类型和位置
    chores = {
        "扫地": ["客厅", "卧室", "厨房", "卫生间"],
        "拖地": ["客厅", "卧室", "厨房", "卫生间"],
        "洗碗": [],
        "擦桌子": ["餐桌", "茶几", "书桌"],
        "倒垃圾": []
    }

    # 添加家庭成员
    with st.expander("👨👩👧👦 添加家庭成员"):
        col1, col2 = st.columns([3, 1])
        new_member = col1.text_input("输入家庭成员名字")
        if col2.button("添加", key="add_member") and new_member:
            if new_member not in st.session_state.members:
                st.session_state.members.append(new_member)
                st.success(f"{new_member} 已加入！")
            else:
                st.warning(f"{new_member} 已在列表中！")
        
        if st.session_state.members:
            st.subheader("当前家庭成员")
            st.write(", ".join(st.session_state.members))
            if st.button("清空所有成员", key="clear_members"):
                st.session_state.members = []
                st.success("已清空所有成员！")

    # 分配家务
    if st.session_state.members:
        with st.expander("⚙️ 配置家务分配"):
            st.subheader("特殊家务设置")
            
            col1, col2 = st.columns(2)
            num_dishes = col1.number_input("今天要洗的碗碟数量", min_value=0, value=10)
            num_bags = col2.number_input("今天要倒的垃圾袋数量", min_value=0, value=1)
            
            if st.button("🚀 开始分配家务"):
                assigned_chores = {}
                for member in st.session_state.members:
                    assigned_chores[member] = []

                # 分配洗碗任务
                num_shifts = max(1, num_dishes // 10 + (1 if num_dishes % 10 != 0 else 0))
                for _ in range(num_shifts):
                    chosen_member = random.choice(st.session_state.members)
                    assigned_chores[chosen_member].append("洗碗")

                # 分配倒垃圾任务
                for _ in range(num_bags):
                    chosen_member = random.choice(st.session_state.members)
                    assigned_chores[chosen_member].append("倒垃圾")

                # 分配其他家务
                for chore, locations in chores.items():
                    if chore not in ["洗碗", "倒垃圾"]:
                        for location in locations:
                            chosen_member = random.choice(st.session_state.members)
                            assigned_chores[chosen_member].append(f"{chore} {location}")

                st.session_state.assigned_chores = assigned_chores
                st.success("家务分配完成！")

        # 显示分配结果
        if st.session_state.assigned_chores:
            st.subheader("📋 家务分配结果")
            
            for member, chores in st.session_state.assigned_chores.items():
                if chores:
                    with st.container():
                        st.markdown(f"**{member} 的任务**")
                        for chore in chores:
                            st.markdown(f"- {chore}")
                        st.divider()
                else:
                    st.info(f"{member} 今天很幸运，没有分配到家务~")
    else:
        st.warning("请先添加家庭成员！")

if __name__ == "__main__":
    main()
