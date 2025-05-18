import streamlit as st
import random

# 基础设置
st.set_page_config(
    page_title="家务分配助手",
    page_icon="🧹",
    layout="centered"
)

# 初始化数据（带默认值）
if 'members' not in st.session_state:
    st.session_state.members = ["爸爸", "妈妈", "孩子"]  # 默认成员

if 'tasks' not in st.session_state:
    st.session_state.tasks = ["洗碗", "拖地", "倒垃圾"]  # 默认任务

if 'assignments' not in st.session_state:
    st.session_state.assignments = {}

# 主界面
st.title("🧹 家务分配助手")

# 1. 编辑家庭成员
st.subheader("家庭成员")
member_col1, member_col2 = st.columns([4, 1])
with member_col1:
    new_member = st.text_input("添加新成员", placeholder="输入称呼")
with member_col2:
    if st.button("添加", key="add_member") and new_member:
        if new_member not in st.session_state.members:
            st.session_state.members.append(new_member)

# 显示成员列表（带删除功能）
for i, member in enumerate(st.session_state.members[:]):  # 创建副本用于迭代
    col1, col2 = st.columns([4, 1])
    col1.write(f"👤 {member}")
    if col2.button("删除", key=f"del_member_{i}"):
        st.session_state.members.remove(member)
        st.rerun()

# 2. 编辑家务清单
st.subheader("家务清单")
task_col1, task_col2 = st.columns([4, 1])
with task_col1:
    new_task = st.text_input("添加新任务", placeholder="输入任务名称")
with task_col2:
    if st.button("添加", key="add_task") and new_task:
        if new_task not in st.session_state.tasks:
            st.session_state.tasks.append(new_task)

# 显示任务列表（带删除功能）
for i, task in enumerate(st.session_state.tasks[:]):
    col1, col2 = st.columns([4, 1])
    col1.write(f"📌 {task}")
    if col2.button("删除", key=f"del_task_{i}"):
        st.session_state.tasks.remove(task)
        st.rerun()

# 3. 分配功能
st.divider()
if st.button("🚀 一键分配家务", type="primary"):
    if not st.session_state.members:
        st.error("请先添加家庭成员")
    elif not st.session_state.tasks:
        st.error("请先添加家务任务")
    else:
        # 随机分配逻辑
        shuffled_tasks = random.sample(st.session_state.tasks, len(st.session_state.tasks))
        shuffled_members = random.sample(st.session_state.members, len(st.session_state.members))
        
        # 确保每个成员分配到大致相等的任务数量
        assignments = {}
        for i, task in enumerate(shuffled_tasks):
            member = shuffled_members[i % len(shuffled_members)]
            if member not in assignments:
                assignments[member] = []
            assignments[member].append(task)
        
        st.session_state.assignments = assignments
        st.success("分配完成！")

# 4. 显示分配结果
if st.session_state.assignments:
    st.subheader("分配结果")
    for member, tasks in st.session_state.assignments.items():
        with st.expander(f"👤 {member} 的任务"):
            for task in tasks:
                st.write(f"• {task}")

# 重置按钮
if st.button("🔄 重置分配结果"):
    st.session_state.assignments = {}
    st.rerun()

# 页脚
st.divider()
st.caption("数据仅在当前会话中保存")
