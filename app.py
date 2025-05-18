import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random

# 页面设置
st.set_page_config(
    page_title="家务分配助手",
    page_icon="🧹",
    layout="centered"
)

# 初始化数据
if 'household_tasks' not in st.session_state:
    st.session_state.household_tasks = pd.DataFrame(columns=["任务", "频率", "上次完成", "负责人"])

if 'family_members' not in st.session_state:
    st.session_state.family_members = ["爸爸", "妈妈", "孩子"]

# 主界面
st.title("🧹 家务分配助手")
st.write("公平分配家务，让家庭生活更和谐")

# 侧边栏 - 家庭成员管理
with st.sidebar:
    st.subheader("家庭成员管理")
    new_member = st.text_input("添加新成员")
    if st.button("添加"):
        if new_member and new_member not in st.session_state.family_members:
            st.session_state.family_members.append(new_member)
            st.success(f"已添加 {new_member}")
    
    st.write("当前成员:")
    for member in st.session_state.family_members:
        st.write(f"- {member}")
    
    if st.button("清空成员"):
        st.session_state.family_members = []
        st.experimental_rerun()

# 家务任务管理
st.subheader("家务任务列表")

# 添加新任务
with st.expander("添加新任务"):
    col1, col2 = st.columns(2)
    with col1:
        new_task = st.text_input("任务名称", placeholder="例如: 洗碗")
    with col2:
        task_freq = st.selectbox("频率", ["每日", "每周", "每月"])
    
    if st.button("添加任务"):
        if new_task:
            new_row = {
                "任务": new_task,
                "频率": task_freq,
                "上次完成": "未完成",
                "负责人": "未分配"
            }
            st.session_state.household_tasks = st.session_state.household_tasks.append(new_row, ignore_index=True)
            st.success("任务已添加!")
        else:
            st.warning("请输入任务名称")

# 显示任务列表
if not st.session_state.household_tasks.empty:
    st.dataframe(st.session_state.household_tasks, use_container_width=True)
else:
    st.info("暂无家务任务，请添加")

# 任务分配功能
if st.button("智能分配家务"):
    if len(st.session_state.family_members) == 0:
        st.error("请先添加家庭成员")
    elif st.session_state.household_tasks.empty:
        st.error("请先添加家务任务")
    else:
        # 简单轮询分配算法
        tasks = st.session_state.household_tasks.copy()
        member_count = len(st.session_state.family_members)
        
        for i in range(len(tasks)):
            assigned_member = st.session_state.family_members[i % member_count]
            tasks.at[i, "负责人"] = assigned_member
            tasks.at[i, "上次完成"] = datetime.now().strftime("%Y-%m-%d")
        
        st.session_state.household_tasks = tasks
        st.success("家务已分配!")
        st.balloons()

# 完成任务功能
if not st.session_state.household_tasks.empty:
    st.subheader("完成任务")
    task_to_complete = st.selectbox(
        "选择已完成的任务",
        st.session_state.household_tasks["任务"].tolist()
    )
    
    if st.button("标记为已完成"):
        idx = st.session_state.household_tasks[st.session_state.household_tasks["任务"] == task_to_complete].index[0]
        st.session_state.household_tasks.at[idx, "上次完成"] = datetime.now().strftime("%Y-%m-%d")
        st.success(f"'{task_to_complete}' 已完成!")

# 重置功能
if st.button("重置所有数据"):
    st.session_state.household_tasks = pd.DataFrame(columns=["任务", "频率", "上次完成", "负责人"])
    st.experimental_rerun()

# 页脚
st.divider()
st.caption("让家务分配更公平，家庭生活更轻松")
