"""
================================================================================
COMPUTER ORGANIZATION AND ARCHITECTURE (ENCA302)
CACHE MEMORY MAPPING & PLACEMENT POLICY EXPERIMENT
Student Name : Akash Sharma
Roll Number  : 2401201108
Program      : BCA (Artificial Intelligence & Data Science) - Section B
Institution  : School of Engineering and Technology, K.R. Mangalam University
Coordinator  : Alina Banerjee
================================================================================
"""

import sys
from typing import List, Optional, Tuple


class CacheLine:
    """Models an individual hardware cache line."""
    def __init__(self, line_id: int):
        self.line_id: int = line_id
        self.valid: bool = False
        self.tag: Optional[int] = None
        self.block_id: Optional[int] = None
        self.last_access_cycle: int = 0

    def load(self, tag: int, block_id: int, cycle: int) -> None:
        self.valid = True
        self.tag = tag
        self.block_id = block_id
        self.last_access_cycle = cycle


class CacheSet:
    """Models an associative set of one or more lines."""
    def __init__(self, set_id: int, ways: int, base_line_id: int):
        self.set_id: int = set_id
        self.ways: int = ways
        self.lines: List[CacheLine] = [CacheLine(base_line_id + w) for w in range(ways)]

    def lookup(self, tag: int) -> Optional[CacheLine]:
        for line in self.lines:
            if line.valid and line.tag == tag:
                return line
        return None

    def insert(self, tag: int, block_id: int, cycle: int) -> Tuple[CacheLine, bool, Optional[int]]:
        # 1. Allocate first free / invalid slot if present
        for line in self.lines:
            if not line.valid:
                line.load(tag, block_id, cycle)
                return line, False, None

        # 2. Set full -> evict Least Recently Used (LRU) line
        lru_line = min(self.lines, key=lambda l: l.last_access_cycle)
        evicted_block = lru_line.block_id
        lru_line.load(tag, block_id, cycle)
        return lru_line, True, evicted_block


class CacheMemory:
    """Configurable cache engine supporting Direct, Set-Associative, and Fully-Associative modes."""
    def __init__(self, name: str, total_lines: int, ways_per_set: int):
        self.name: str = name
        self.total_lines: int = total_lines
        self.ways_per_set: int = ways_per_set
        self.num_sets: int = total_lines // ways_per_set

        self.sets: List[CacheSet] = [
            CacheSet(set_id=s, ways=ways_per_set, base_line_id=s * ways_per_set)
            for s in range(self.num_sets)
        ]

        self.hits: int = 0
        self.misses: int = 0
        self.cycle: int = 0
        self.trace: List[dict] = []

    def access(self, block: int) -> dict:
        self.cycle += 1
        set_idx = block % self.num_sets
        tag = block // self.num_sets
        cset = self.sets[set_idx]

        hit_line = cset.lookup(tag)
        if hit_line:
            self.hits += 1
            hit_line.last_access_cycle = self.cycle
            entry = {
                "cycle": self.cycle,
                "block": block,
                "tag": tag,
                "set": set_idx,
                "line": hit_line.line_id,
                "status": "HIT",
                "evicted": None
            }
        else:
            self.misses += 1
            alloc_line, is_evict, ev_block = cset.insert(tag, block, self.cycle)
            entry = {
                "cycle": self.cycle,
                "block": block,
                "tag": tag,
                "set": set_idx,
                "line": alloc_line.line_id,
                "status": "MISS",
                "evicted": ev_block
            }

        # Snapshot current cache contents
        flat = [None] * self.total_lines
        for s in self.sets:
            for l in s.lines:
                flat[l.line_id] = l.block_id if l.valid else None
        entry["state"] = flat
        self.trace.append(entry)
        return entry


def display_trace(cache: CacheMemory) -> None:
    print(f"\n--- {cache.name.upper()} (Sets: {cache.num_sets}, Ways/Set: {cache.ways_per_set}) ---")
    print(f"{'Step':^6} | {'Block':^6} | {'Tag':^4} | {'Set':^4} | {'Line':^5} | {'Result':^6} | {'Evicted':^8} | {'Cache Lines (L0, L1, L2, L3)':^28}")
    print("-" * 84)
    for t in cache.trace:
        ev_str = str(t['evicted']) if t['evicted'] is not None else "-"
        state_str = "[" + ", ".join(str(b) if b is not None else "-" for b in t['state']) + "]"
        print(f"{t['cycle']:^6} | {t['block']:^6} | {t['tag']:^4} | {t['set']:^4} | L{t['line']:<4} | {t['status']:^6} | {ev_str:^8} | {state_str:<28}")
    total = cache.hits + cache.misses
    hr = (cache.hits / total) * 100 if total else 0.0
    print(f"Summary: Hits = {cache.hits}, Misses = {cache.misses}, Hit Rate = {hr:.2f}%\n")


def execute_suite(title: str, sequence: List[int], num_lines: int = 4) -> List[CacheMemory]:
    print("=" * 84)
    print(f"EXPERIMENT: {title}")
    print(f"Access Sequence : {sequence} (Length: {len(sequence)})")
    print("=" * 84)

    dm = CacheMemory("Direct-Mapped Cache", num_lines, 1)
    sa = CacheMemory("2-Way Set-Associative Cache", num_lines, 2)
    fa = CacheMemory("Fully Associative Cache", num_lines, num_lines)
    caches = [dm, sa, fa]

    for b in sequence:
        for c in caches:
            c.access(b)

    for c in caches:
        display_trace(c)

    print("Performance Comparison:")
    print(f"{'Architecture':<28} | {'Hits':^6} | {'Misses':^8} | {'Hit Rate':^10} | {'Occupancy':^12}")
    print("-" * 74)
    for c in caches:
        total = len(sequence)
        hr = (c.hits / total) * 100
        occ = sum(1 for x in c.trace[-1]['state'] if x is not None)
        print(f"{c.name:<28} | {c.hits:^6} | {c.misses:^8} | {hr:>8.2f}%  | {f'{occ}/{c.total_lines} lines':^12}")
    print("=" * 84 + "\n")
    return caches


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--all":
        # Run main and all three additional verification experiments
        execute_suite("Main Question Benchmark", [0, 4, 8, 0, 4, 12])
        execute_suite("Additional Test 1: Repeated Access to Two Blocks", [0, 1, 0, 1, 0, 1])
        execute_suite("Additional Test 2: Competing Blocks for Same Set", [2, 6, 10, 14, 2, 6])
        execute_suite("Additional Test 3: Cache Flushing & Replacement", [0, 1, 2, 3, 4, 5, 0, 1])
    else:
        reqs = [int(x.strip()) for x in sys.argv[1].split(",")] if len(sys.argv) > 1 else [0, 4, 8, 0, 4, 12]
        execute_suite("Main Question Benchmark", reqs)
