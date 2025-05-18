import streamlit as st
import random

# 基础配置（确保最低资源消耗）
st.set_page_config(
    page_title="家务分配助手",
    page_icon="🧹",
    layout="centered"
)

# 初始化数据（仅用基础数据类型）
if 'tasks' not in st.session_state:
    st.session_state.tasks = []
if 'members' not in st.session_state:
    st.session_state.members = ["👨 爸爸", "👩 妈妈"]

# 主界面
st.title("🧹 家务分配助手")

# 1. 成员管理（纯输入框+按钮）
with st.expander("👥 管理家庭成员", expanded=True):
    new_member = st.text_input("输入成员昵称", key="member_input")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("添加成员", key="add_member"):
            if new_member and new_member not in st.session_state.members:
                st.session_state.members.append(new_member)
    with col2:
        if st.button("清空成员", key="clear_members"):
            st.session_state.members = ["👨 爸爸", "👩 妈妈"]
    
    st.write("**当前成员:**", ", ".join(st.session_state.members))

# 2. 任务管理（无复杂操作）
with st.expander("📝 管理家务任务", expanded=True):
    new_task = st.text_input("输入任务名称", key="task_input")
    if st.button("添加任务", key="add_task") and new_task:
        st.session_state.tasks.append({
            "name": new_task,
            "assigned": None,
            "done": False
        })

# 3. 任务分配与展示（纯按钮交互）
if st.session_state.tasks:
    st.divider()
    st.subheader("🗒️ 当前家务清单")
    
    # 分配按钮
    if st.button("✨ 一键智能分配", type="primary"):
        if st.session_state.members:
            for task in st.session_state.tasks:
                if not task["done"]:
                    task["assigned"] = random.choice(st.session_state.members)
    
    # 任务列表
    for i, task in enumerate(st.session_state.tasks):
        status = "✅" if task["done"] else "⏳"
        assigned = task["assigned"] or "未分配"
        
        cols = st.columns([1, 3, 2, 2])
        cols[0].write(status)
        cols[1].write(task["name"])
        cols[2].write(assigned)
        
        if cols[3].button("完成", key=f"complete_{i}"):
            task["done"] = True
            st.rerun()
else:
    st.info("暂无家务任务，请先添加")

# 重置功能
if st.button("🔄 重置所有数据", type="secondary"):
    st.session_state.tasks = []
    st.session_state.members = ["👨 爸爸", "👩 妈妈"]
    st.rerun()

# 页脚说明
st.divider()
st.caption("💡 数据仅在当前会话中保存，刷新页面会重置")
