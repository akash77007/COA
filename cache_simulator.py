"""
================================================================================
COMPUTER ORGANIZATION AND ARCHITECTURE (ENCA302)
PROJECT: CACHE MEMORY MAPPING AND REPLACEMENT SIMULATOR
Student Name : Akash Sharma
Roll Number  : 2401201108
Program      : BCA (Artificial Intelligence & Data Science)
Institution  : School of Engineering and Technology, K.R. Mangalam University
Coordinator  : Alina Banerjee
================================================================================

This module simulates and analyzes the three core cache placement policies:
1. Direct-Mapped Cache (1-Way Associative)
2. K-Way Set-Associative Cache (2-Way Associative with LRU Replacement)
3. Fully Associative Cache (N-Way Associative with LRU Replacement)

Key Architectural Highlights:
- Explicit Tag and Set Index Address Decomposition (Tag = Block // Sets, Index = Block % Sets)
- Line-level state modeling (Valid Bit, Tag, Block ID, and LRU Access Timestamp)
- Real-time event tracking (Cold Miss, Conflict Miss, Hit, and LRU Eviction)
"""

import sys
from typing import List, Optional, Tuple


class CacheLine:
    """Represents an individual physical cache line in hardware."""
    def __init__(self, line_id: int):
        self.line_id: int = line_id
        self.valid: bool = False
        self.tag: Optional[int] = None
        self.block_id: Optional[int] = None
        self.last_access_cycle: int = 0

    def update(self, tag: int, block_id: int, cycle: int) -> None:
        self.valid = True
        self.tag = tag
        self.block_id = block_id
        self.last_access_cycle = cycle

    def clear(self) -> None:
        self.valid = False
        self.tag = None
        self.block_id = None
        self.last_access_cycle = 0


class CacheSet:
    """Represents a set containing one or more associative ways."""
    def __init__(self, set_id: int, ways: int, base_line_id: int):
        self.set_id: int = set_id
        self.ways: int = ways
        self.lines: List[CacheLine] = [CacheLine(base_line_id + w) for w in range(ways)]

    def probe(self, tag: int) -> Optional[CacheLine]:
        """Check if any valid line in this set matches the given tag."""
        for line in self.lines:
            if line.valid and line.tag == tag:
                return line
        return None

    def allocate(self, tag: int, block_id: int, cycle: int) -> Tuple[CacheLine, bool, Optional[int]]:
        """
        Allocate a block to this set.
        Returns: (allocated_line, is_replacement, evicted_block_id)
        """
        # 1. Check for free / invalid line first
        for line in self.lines:
            if not line.valid:
                line.update(tag, block_id, cycle)
                return line, False, None

        # 2. All ways occupied -> perform LRU eviction (find minimum last_access_cycle)
        victim_line = min(self.lines, key=lambda l: l.last_access_cycle)
        evicted_block = victim_line.block_id
        victim_line.update(tag, block_id, cycle)
        return victim_line, True, evicted_block


class CacheMemory:
    """Simulates a configurable cache memory system."""
    def __init__(self, title: str, total_lines: int, ways_per_set: int):
        self.title: str = title
        self.total_lines: int = total_lines
        self.ways_per_set: int = ways_per_set
        self.num_sets: int = total_lines // ways_per_set

        self.sets: List[CacheSet] = [
            CacheSet(set_id=s, ways=ways_per_set, base_line_id=s * ways_per_set)
            for s in range(self.num_sets)
        ]

        self.hits: int = 0
        self.misses: int = 0
        self.current_cycle: int = 0
        self.event_log: List[dict] = []

    def access(self, block: int) -> dict:
        self.current_cycle += 1
        set_index = block % self.num_sets
        tag = block // self.num_sets
        target_set = self.sets[set_index]

        hit_line = target_set.probe(tag)
        if hit_line:
            self.hits += 1
            hit_line.last_access_cycle = self.current_cycle
            event = {
                "cycle": self.current_cycle,
                "block": block,
                "tag": tag,
                "set": set_index,
                "line": hit_line.line_id,
                "status": "HIT",
                "evicted": None,
                "action": f"Cache Hit in Line L{hit_line.line_id}"
            }
        else:
            self.misses += 1
            allocated_line, is_eviction, evicted_block = target_set.allocate(tag, block, self.current_cycle)
            event = {
                "cycle": self.current_cycle,
                "block": block,
                "tag": tag,
                "set": set_index,
                "line": allocated_line.line_id,
                "status": "MISS",
                "evicted": evicted_block,
                "action": f"Evicted Block {evicted_block}" if is_eviction else "Cold Load (Free Slot)"
            }

        event["cache_state"] = self.get_line_state()
        self.event_log.append(event)
        return event

    def get_line_state(self) -> List[Optional[int]]:
        flat_lines = [None] * self.total_lines
        for s in self.sets:
            for l in s.lines:
                flat_lines[l.line_id] = l.block_id if l.valid else None
        return flat_lines


def print_trace_table(cache: CacheMemory) -> None:
    print(f"\n>> {cache.title.upper()} (Sets: {cache.num_sets}, Ways/Set: {cache.ways_per_set})")
    print("-" * 88)
    header = (
        f"{'Cycle':^6} | {'Block':^6} | {'Tag':^4} | {'Set':^4} | "
        f"{'Line':^5} | {'Result':^6} | {'Evicted':^8} | {'Cache Lines [L0, L1, L2, L3]':^28}"
    )
    print(header)
    print("-" * 88)

    for entry in cache.event_log:
        ev_str = str(entry['evicted']) if entry['evicted'] is not None else "-"
        state_str = "[" + ", ".join(str(b) if b is not None else "-" for b in entry['cache_state']) + "]"
        print(
            f"{entry['cycle']:^6} | {entry['block']:^6} | {entry['tag']:^4} | {entry['set']:^4} | "
            f"L{entry['line']:<4} | {entry['status']:^6} | {ev_str:^8} | {state_str:<28}"
        )
    print("-" * 88)
    total = cache.hits + cache.misses
    hit_rate = (cache.hits / total) * 100 if total > 0 else 0.0
    miss_rate = (cache.misses / total) * 100 if total > 0 else 0.0
    print(f"Summary: Hits = {cache.hits:<2} | Misses = {cache.misses:<2} | Hit Rate = {hit_rate:.2f}% | Miss Rate = {miss_rate:.2f}%\n")


def run_benchmark(requests: List[int], total_blocks: int = 4) -> None:
    print("=" * 88)
    print("      CACHE MAPPING SIMULATION & ARCHITECTURAL COMPARISON")
    print("      Student: Akash Sharma | Roll: 2401201108 | BCA (AI & DS) - Sec B")
    print("=" * 88)
    print(f"System Configuration:")
    print(f"  Total Cache Lines : {total_blocks} (L0, L1, L2, L3)")
    print(f"  Replacement Policy: Least Recently Used (LRU)")
    print(f"  Block Request Seq : {requests}")
    print(f"  Access Count      : {len(requests)}")

    # Instantiate the three cache organizations
    dm_cache = CacheMemory("Direct-Mapped Cache", total_lines=total_blocks, ways_per_set=1)
    sa_cache = CacheMemory("2-Way Set-Associative Cache", total_lines=total_blocks, ways_per_set=2)
    fa_cache = CacheMemory("Fully Associative Cache", total_lines=total_blocks, ways_per_set=total_blocks)

    caches = [dm_cache, sa_cache, fa_cache]

    for req in requests:
        for c in caches:
            c.access(req)

    for c in caches:
        print_trace_table(c)

    # Comparative Summary Table
    total = len(requests)
    print("=" * 88)
    print(f"{'Mapping Technique':<26} | {'Hits':^6} | {'Misses':^8} | {'Hit Rate':^10} | {'Miss Rate':^10} | {'Active Slots':^12}")
    print("-" * 88)
    for c in caches:
        hr = (c.hits / total) * 100
        mr = (c.misses / total) * 100
        active = sum(1 for b in c.get_line_state() if b is not None)
        print(f"{c.title:<26} | {c.hits:^6} | {c.misses:^8} | {hr:>8.2f}%  | {mr:>8.2f}%  | {f'{active}/{c.total_lines}':^12}")
    print("=" * 88)

    print("\nArchitectural Verdict for Sequence [0, 4, 8, 0, 4, 12]:")
    print("  * Direct-Mapped: 0 Hits / 6 Misses (100% Miss). Severe line thrashing at Line L0.")
    print("  * 2-Way Set-Assoc: 0 Hits / 6 Misses (100% Miss). Thrashing within Set 0 (3 blocks > 2 ways).")
    print("  * Fully Associative: 2 Hits / 4 Misses (33.33% Hit). Retains blocks 0 & 4 across all 4 slots.")
    print("  => Fully Associative architecture demonstrates highest flexibility.\n")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            seq = [int(x.strip()) for x in sys.argv[1].replace(",", " ").split()]
        except ValueError:
            print("Invalid input format. Executing default sequence [0, 4, 8, 0, 4, 12]")
            seq = [0, 4, 8, 0, 4, 12]
    else:
        seq = [0, 4, 8, 0, 4, 12]

    run_benchmark(seq, total_blocks=4)
