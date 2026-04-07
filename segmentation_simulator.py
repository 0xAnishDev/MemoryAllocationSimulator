import random

class Segment:
    def __init__(self, start, size, pid=None):
        self.start = start
        self.size = size
        self.pid = pid


def merge(memory):
    merged = []
    for seg in memory:
        if merged and seg.pid is None and merged[-1].pid is None:
            merged[-1].size += seg.size
        else:
            merged.append(seg)
    return merged


def simulate_segmentation(total_memory, num_processes, max_process_size, algorithm="First Fit"):

    memory = [Segment(0, total_memory)]
    failures = 0
    search_ops = 0
    active_pids = []
    last_allocated_index = 0

    for pid in range(1, num_processes + 1):

        process_size = random.randint(20, max_process_size)

        allocated = False
        target_index = -1

        if algorithm == "First Fit":
            for i, seg in enumerate(memory):
                search_ops += 1
                if seg.pid is None and seg.size >= process_size:
                    target_index = i
                    break
        elif algorithm == "Best Fit":
            best_diff = float('inf')
            for i, seg in enumerate(memory):
                search_ops += 1
                if seg.pid is None and seg.size >= process_size:
                    diff = seg.size - process_size
                    if diff < best_diff:
                        best_diff = diff
                        target_index = i
        elif algorithm == "Worst Fit":
            worst_diff = -1
            for i, seg in enumerate(memory):
                search_ops += 1
                if seg.pid is None and seg.size >= process_size:
                    diff = seg.size - process_size
                    if diff > worst_diff:
                        worst_diff = diff
                        target_index = i
        elif algorithm == "Next Fit":
            n = len(memory)
            if last_allocated_index >= n:
                last_allocated_index = 0
            
            for i in range(n):
                idx = (last_allocated_index + i) % n
                search_ops += 1
                seg = memory[idx]
                if seg.pid is None and seg.size >= process_size:
                    target_index = idx
                    break

        if target_index != -1:
            seg = memory[target_index]
            new_seg = Segment(seg.start, process_size, pid)

            seg.start += process_size
            seg.size -= process_size

            memory.insert(target_index, new_seg)

            if algorithm == "Next Fit":
                last_allocated_index = target_index

            if seg.size == 0:
                memory.pop(target_index + 1)

            active_pids.append(pid)
            allocated = True

        if not allocated:
            failures += 1

        # FORCE some processes to terminate
        if active_pids and random.random() < 0.5:
            victim = random.choice(active_pids)
            active_pids.remove(victim)

            for seg in memory:
                if seg.pid == victim:
                    seg.pid = None
                    break

        memory = merge(memory)

    # fragmentation calculation
    free_blocks = [seg.size for seg in memory if seg.pid is None]

    if len(free_blocks) <= 1:
        fragmentation = 0
    else:
        total_free = sum(free_blocks)
        largest = max(free_blocks)
        fragmentation = ((total_free - largest) / total_free) * 100

    return {
        "failures": failures,
        "search_ops": search_ops,
        "fragmentation": round(fragmentation, 2),
        "memory_layout": memory
    }