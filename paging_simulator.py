import random
from collections import deque

class PagingSystem:
    def __init__(self, total_frames):
        self.total_frames = total_frames
        self.frames = []
        self.fifo_queue = deque()
        self.page_faults = 0
        self.hits = 0

    def access_page(self, page):
        if page in self.frames:
            self.hits += 1
            return

        # Page fault
        self.page_faults += 1

        if len(self.frames) < self.total_frames:
            self.frames.append(page)
            self.fifo_queue.append(page)
        else:
            # FIFO replacement
            oldest = self.fifo_queue.popleft()
            self.frames.remove(oldest)
            self.frames.append(page)
            self.fifo_queue.append(page)

    def report(self):
        total = self.hits + self.page_faults
        fault_rate = (self.page_faults / total) * 100
        print("------ Paging Performance ------")
        print("Total Accesses:", total)
        print("Page Hits:", self.hits)
        print("Page Faults:", self.page_faults)
        print("Fault Rate: {:.2f}%".format(fault_rate))
        print("----------------------------------")


# -------------- TEST --------------

if __name__ == "__main__":
    paging = PagingSystem(total_frames=4)

    # Random access sequence
    pages = [random.randint(1, 10) for _ in range(50)]

    for p in pages:
        paging.access_page(p)

    paging.report()