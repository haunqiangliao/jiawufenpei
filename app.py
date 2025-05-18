import streamlit as st
import pandas as pd
from datetime import datetime

# 极简页面设置
st.set_page_config(
    page_title="家务分配助手",
    page_icon="🧹",
    layout="centered"
)

# 初始化数据（极简版只保留核心数据）
if 'tasks' not in st.session_state:
    st.session_state.tasks = pd.DataFrame(columns=["任务", "负责人", "完成状态"])

if 'members' not in st.session_state:
    st.session_state.members = ["爸爸", "妈妈"]  # 默认成员

# 主界面
st.title("🧹 极简家务助手")

# 1. 成员管理（简化版）
with st.expander("家庭成员管理"):
    new_member = st.text_input("添加成员", key="new_member")
    if st.button("添加"):
        if new_member and new_member not in st.session_state.members:
            st.session_state.members.append(new_member)
    st.write("当前成员:", ", ".join(st.session_state.members))

# 2. 任务管理（简化版）
task = st.text_input("添加任务", key="new_task")
if st.button("添加任务"):
    if task:
        new_task = pd.DataFrame([{
            "任务": task,
            "负责人": "未分配",
            "完成状态": "待完成"
        }])
        st.session_state.tasks = pd.concat([st.session_state.tasks, new_task])
        
# 3. 任务分配（简化版）
if st.button("随机分配"):
    if len(st.session_state.members) > 0 and not st.session_state.tasks.empty:
        st.session_state.tasks["负责人"] = [
            random.choice(st.session_state.members) 
            for _ in range(len(st.session_state.tasks))
        ]
        st.success("分配完成！")

# 4. 任务展示（简化版）
if not st.session_state.tasks.empty:
    st.divider()
    st.subheader("当前任务")
    for i, row in st.session_state.tasks.iterrows():
        cols = st.columns([3,2,2])
        cols[0].write(f"📌 {row['任务']}")
        cols[1].write(f"👤 {row['负责人']}")
        if cols[2].button("完成", key=f"complete_{i}"):
            st.session_state.tasks.at[i, "完成状态"] = "已完成"
            st.rerun()

# 重置按钮
if st.button("重置所有数据"):
    st.session_state.tasks = pd.DataFrame(columns=["任务", "负责人", "完成状态"])
    st.rerun()

# 页脚
st.divider()
st.caption("数据仅保存在当前会话中")
