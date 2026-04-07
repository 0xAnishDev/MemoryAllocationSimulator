import random
from collections import deque

class PagingSystem:
    def __init__(self, total_frames):
        self.total_frames = total_frames
        self.frames = []
        self.page_faults = 0
        self.hits = 0

    def simulate(self, pages, algorithm="FIFO"):
        self.frames = []
        self.page_faults = 0
        self.hits = 0
        
        if algorithm == "FIFO":
            self._simulate_fifo(pages)
        elif algorithm == "LRU":
            self._simulate_lru(pages)
        elif algorithm == "Optimal":
            self._simulate_optimal(pages)
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")

    def _simulate_fifo(self, pages):
        fifo_queue = deque()
        for page in pages:
            if page in self.frames:
                self.hits += 1
            else:
                self.page_faults += 1
                if len(self.frames) < self.total_frames:
                    self.frames.append(page)
                    fifo_queue.append(page)
                else:
                    oldest = fifo_queue.popleft()
                    self.frames.remove(oldest)
                    self.frames.append(page)
                    fifo_queue.append(page)

    def _simulate_lru(self, pages):
        lru_list = []
        for page in pages:
            if page in self.frames:
                self.hits += 1
                lru_list.remove(page)
                lru_list.append(page)
            else:
                self.page_faults += 1
                if len(self.frames) < self.total_frames:
                    self.frames.append(page)
                    lru_list.append(page)
                else:
                    lru = lru_list.pop(0)
                    self.frames.remove(lru)
                    self.frames.append(page)
                    lru_list.append(page)

    def _simulate_optimal(self, pages):
        for i, page in enumerate(pages):
            if page in self.frames:
                self.hits += 1
            else:
                self.page_faults += 1
                if len(self.frames) < self.total_frames:
                    self.frames.append(page)
                else:
                    farthest_index = -1
                    farthest_page = -1
                    for f_page in self.frames:
                        try:
                            next_use = pages[i+1:].index(f_page)
                            if next_use > farthest_index:
                                farthest_index = next_use
                                farthest_page = f_page
                        except ValueError:
                            farthest_page = f_page
                            break
                    
                    self.frames.remove(farthest_page)
                    self.frames.append(page)

    def report(self):
        total = self.hits + self.page_faults
        if total == 0:
            return
        fault_rate = (self.page_faults / total) * 100
        print(f"------ Paging Performance ------")
        print("Total Accesses:", total)
        print("Page Hits:", self.hits)
        print("Page Faults:", self.page_faults)
        print("Fault Rate: {:.2f}%".format(fault_rate))
        print("----------------------------------")


# -------------- TEST --------------

if __name__ == "__main__":
    paging = PagingSystem(total_frames=4)
    pages = [random.randint(1, 10) for _ in range(50)]
    
    paging.simulate(pages, "FIFO")
    paging.report()
    paging.simulate(pages, "LRU")
    paging.report()
    paging.simulate(pages, "Optimal")
    paging.report()