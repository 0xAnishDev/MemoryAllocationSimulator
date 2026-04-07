import streamlit as st
import random
import matplotlib.pyplot as plt
import time

from paging_simulator import PagingSystem
from segmentation_simulator import simulate_segmentation

st.set_page_config(page_title="Paging vs Segmentation Simulator", layout="wide")

st.title("Paging vs Segmentation Performance Visualizer")

# Sidebar Controls
st.sidebar.header("Simulation Controls")

total_memory = st.sidebar.number_input("Total Memory", min_value=256, max_value=4096, value=1024)
frame_size = st.sidebar.number_input("Frame Size (Paging)", min_value=16, max_value=256, value=64)
total_frames = st.sidebar.number_input("Number of Frames (Paging)", min_value=2, max_value=32, value=4)
num_processes = st.sidebar.number_input("Number of Processes", min_value=2, max_value=30, value=6)
max_process_size = st.sidebar.number_input("Max Process Size", min_value=50, max_value=500, value=300)

tab1, tab2 = st.tabs(["Paging", "Segmentation"])

# ---------------- PAGING TAB ----------------
with tab1:
    st.subheader("Paging Simulation")
    algorithm = st.selectbox("Select Page Replacement Algorithm", ["FIFO", "LRU", "Optimal"])

    if st.button("Run Paging Simulation"):

        start_time = time.perf_counter()

        paging = PagingSystem(total_frames=total_frames)

        pages = [random.randint(1, 10) for _ in range(50)]

        paging.simulate(pages, algorithm)

        end_time = time.perf_counter()
        execution_time = (end_time - start_time) * 1000  # milliseconds
        total_access = paging.hits + paging.page_faults
        fault_rate = (paging.page_faults / total_access) * 100

        st.write("### Results")
        st.write("Total Accesses:", total_access)
        st.write("Page Hits:", paging.hits)
        st.write("Page Faults:", paging.page_faults)
        st.write("Fault Rate: {:.2f}%".format(fault_rate))
        st.write("Execution Time: {:.4f} ms".format(execution_time))

        st.write("### Current Frames")
        cols = st.columns(len(paging.frames))
        for i, frame in enumerate(paging.frames):
            cols[i].metric(f"Frame {i}", frame)

        # Plot Access Sequence
        fig, ax = plt.subplots()
        ax.plot(pages)
        ax.set_title("Page Access Pattern")
        ax.set_xlabel("Access Index")
        ax.set_ylabel("Page Number")
        st.pyplot(fig)

# ---------------- SEGMENTATION TAB ----------------
# ---------------- SEGMENTATION TAB ----------------
with tab2:
    st.subheader("Segmentation Simulation (First Fit)")

    if st.button("Run Segmentation Simulation"):

        start_time = time.perf_counter()

        result = simulate_segmentation(total_memory, num_processes, max_process_size)

        end_time = time.perf_counter()
        execution_time = (end_time - start_time) * 1000

        st.write("### Results")
        st.write("Allocation Failures:", result["failures"])
        st.write("Search Operations:", result["search_ops"])
        st.write("External Fragmentation: {:.2f}%".format(result["fragmentation"]))
        st.write("Execution Time: {:.4f} ms".format(execution_time))

        st.write("### Memory Layout")

        layout = result["memory_layout"]

        memory_bar = []

        for seg in layout:
            if seg.pid is None:
                memory_bar.extend(["⬜"] * seg.size)
            else:
                memory_bar.extend(["🟩"] * seg.size)

        visual = "".join(memory_bar[:200])  # limit output
        st.text(visual)

        # Simple visualization bar
        st.write("### Memory Fragmentation Visualization")

        frag = result["fragmentation"]

        fig2, ax2 = plt.subplots()
        ax2.pie(
            [100-frag, frag],
            labels=["Usable Memory", "Fragmented Memory"],
            autopct="%1.1f%%"
        )

        ax2.set_title("External Fragmentation")
        st.pyplot(fig2)