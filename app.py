import streamlit as st

# 绝对最小化配置
st.set_page_config(
    page_title="家务助手",
    page_icon="🧹",
    layout="centered"
)

# 仅使用基本数据类型，避免任何可能出错的库
if 'tasks' not in st.session_state:
    st.session_state.tasks = []

if 'members' not in st.session_state:
    st.session_state.members = ["爸爸", "妈妈"]

# 最简界面
st.title("🧹 家务助手")

# 1. 添加成员
new_member = st.text_input("添加成员")
if st.button("添加") and new_member:
    if new_member not in st.session_state.members:
        st.session_state.members.append(new_member)
        st.rerun()

# 2. 添加任务
new_task = st.text_input("添加任务")
if st.button("添加任务") and new_task:
    st.session_state.tasks.append({
        "name": new_task,
        "assigned": "未分配",
        "done": False
    })
    st.rerun()

# 3. 显示任务
st.divider()
if st.session_state.tasks:
    st.write("当前任务:")
    for i, task in enumerate(st.session_state.tasks):
        cols = st.columns([4, 2, 2])
        cols[0].write(f"• {task['name']}")
        cols[1].write(task['assigned'])
        if cols[2].button("完成", key=f"done_{i}"):
            st.session_state.tasks[i]['done'] = True
            st.rerun()
else:
    st.info("暂无任务")

# 4. 分配按钮
if st.button("随机分配") and st.session_state.members:
    for i in range(len(st.session_state.tasks)):
        if not st.session_state.tasks[i]['done']:
            st.session_state.tasks[i]['assigned'] = st.session_state.members[i % len(st.session_state.members)]
    st.rerun()

# 重置按钮
if st.button("重置"):
    st.session_state.tasks = []
    st.session_state.members = ["爸爸", "妈妈"]
    st.rerun()
