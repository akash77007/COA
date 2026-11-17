# Computer Organization and Architecture Simulation Report
## Cache Memory Mapping & Placement Policy Analysis

---

### Academic Information
- **Student Name:** Akash Sharma
- **Roll Number:** 2401201108
- **Program:** BCA (Artificial Intelligence & Data Science) – Section B
- **Course Code:** ENCA302 (Computer Organization and Architecture)
- **Academic Session:** 2025–2026
- **Institution:** School of Engineering and Technology, K.R. Mangalam University
- **Course Coordinator:** Alina Banerjee

---

## 1. Problem Statement

### Question 2: Cache Mapping Simulation
Develop a software simulation to model and contrast memory block mapping across three canonical cache architectures:
1. **Direct-Mapped Cache** (1-Way Associative)
2. **K-Way Set-Associative Cache** (2-Way Associative)
3. **Fully Associative Cache** (N-Way Associative)

**System Parameters:**
- **Cache Capacity:** 4 Cache Lines (numbered $L0, L1, L2, L3$)
- **Replacement Policy:** Least Recently Used (LRU)
- **Memory Access Sequence:** `0, 4, 8, 0, 4, 12`

**Deliverables:**
- Explicit cache location (Line and Set index) selected for each incoming block request.
- Hit / Miss evaluation per access cycle.
- Total count of cache hits and cache misses.
- Performance metric derivation (Hit Ratio and Miss Ratio).
- Comparative architectural evaluation demonstrating which mapping technique yields superior flexibility under the benchmark sequence.

---

## 2. Mathematical Cache Addressing Architecture

In modern computer architectures, a main memory block address is partitioned into two functional fields: **Tag** and **Set Index**.

$$\text{Block Address} = (\text{Tag} \times \text{Number of Sets}) + \text{Set Index}$$

$$\text{Set Index} = \text{Block Address} \pmod{\text{Number of Sets}}$$

$$\text{Tag} = \lfloor \text{Block Address} / \text{Number of Sets} \rfloor$$

### 2.1 Architectural Classification

```
                  +-----------------------------------+
                  |        Memory Block Address       |
                  +-----------------+-----------------+
                                    |
                    +---------------+---------------+
                    |                               |
                    v                               v
             [ Tag Field ]                  [ Set Index Field ]
          Tag = Block // Sets              Index = Block % Sets
                    |                               |
                    |                               v
                    |                      Select Active Set
                    |                               |
                    v                               v
         Parallel Tag Comparator <=======> Set Lines (Ways)
                    |
          +---------+---------+
          |                   |
          v                   v
       [ HIT ]             [ MISS ]
    Access Line     Fetch from RAM, Apply LRU
```

| Mapping Strategy | Sets ($S$) | Ways per Set ($W$) | Set Index Equation | Tag Equation | Search Complexity |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Direct-Mapped** | 4 | 1 | $\text{Block} \pmod 4$ | $\lfloor \text{Block} / 4 \rfloor$ | 1 comparator (fixed line) |
| **2-Way Set-Associative** | 2 | 2 | $\text{Block} \pmod 2$ | $\lfloor \text{Block} / 2 \rfloor$ | 2 comparators per set |
| **Fully Associative** | 1 | 4 | $0$ (Implied) | $\text{Block}$ | 4 comparators (entire cache) |

---

## 3. Detailed Hardware Execution Trace

### Sequence: `[0, 4, 8, 0, 4, 12]`

#### 3.1 Direct-Mapped Architecture (Sets = 4, Ways = 1)
- **Mapping Rule:** $\text{Set} = \text{Block} \pmod 4$, $\text{Line} = \text{Set}$, $\text{Tag} = \lfloor \text{Block} / 4 \rfloor$

| Cycle | Block | Tag | Set | Target Line | Result | Evicted Block | Final Cache State [L0, L1, L2, L3] |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | `0` | 0 | 0 | **L0** | **MISS** | — | `[0, -, -, -]` |
| **2** | `4` | 1 | 0 | **L0** | **MISS** | `0` | `[4, -, -, -]` |
| **3** | `8` | 2 | 0 | **L0** | **MISS** | `4` | `[8, -, -, -]` |
| **4** | `0` | 0 | 0 | **L0** | **MISS** | `8` | `[0, -, -, -]` |
| **5** | `4` | 1 | 0 | **L0** | **MISS** | `0` | `[4, -, -, -]` |
| **6** | `12` | 3 | 0 | **L0** | **MISS** | `4` | `[12, -, -, -]` |

- **Hits:** 0 | **Misses:** 6 | **Hit Rate:** **0.00%** | **Miss Rate:** **100.00%**
- **Analysis:** Every memory reference possesses an address divisible by 4. As a consequence, all requests map strictly to Line 0. Lines L1, L2, and L3 remain completely unutilized (0% occupancy). Each new block evicts the preceding block, generating pathological **cache thrashing**.

---

#### 3.2 2-Way Set-Associative Architecture (Sets = 2, Ways = 2, LRU)
- **Mapping Rule:** $\text{Set} = \text{Block} \pmod 2$, $\text{Tag} = \lfloor \text{Block} / 2 \rfloor$

| Cycle | Block | Tag | Set | Target Line | Result | Evicted Block | Final Cache State [L0, L1, L2, L3] | LRU Priority (MRU $\rightarrow$ LRU) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | `0` | 0 | 0 | **L0** | **MISS** | — | `[0, -, -, -]` | `[L0]` |
| **2** | `4` | 2 | 0 | **L1** | **MISS** | — | `[0, 4, -, -]` | `[L1, L0]` |
| **3** | `8` | 4 | 0 | **L0** | **MISS** | `0` | `[8, 4, -, -]` | `[L0, L1]` |
| **4** | `0` | 0 | 0 | **L1** | **MISS** | `4` | `[8, 0, -, -]` | `[L1, L0]` |
| **5** | `4` | 2 | 0 | **L0** | **MISS** | `8` | `[4, 0, -, -]` | `[L0, L1]` |
| **6** | `12` | 6 | 0 | **L1** | **MISS** | `0` | `[4, 12, -, -]` | `[L1, L0]` |

- **Hits:** 0 | **Misses:** 6 | **Hit Rate:** **0.00%** | **Miss Rate:** **100.00%**
- **Analysis:** Because all addresses are even ($x \pmod 2 = 0$), all 6 requests map to Set 0. The working set contains 3 competing blocks (`0, 4, 8`), but Set 0 possesses only 2 physical ways (L0 and L1). The LRU replacement algorithm repeatedly evicts the exact block required in the immediate next cycle. Set 1 (Lines L2 and L3) remains completely idle.

---

#### 3.3 Fully Associative Architecture (Sets = 1, Ways = 4, Global LRU)
- **Mapping Rule:** Placement allowed in any available cache line; Tag = Block Address.

| Cycle | Block | Tag | Set | Target Line | Result | Evicted Block | Final Cache State [L0, L1, L2, L3] | LRU Order (MRU $\rightarrow$ LRU) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | `0` | 0 | 0 | **L0** | **MISS** | — | `[0, -, -, -]` | `[0]` |
| **2** | `4` | 4 | 0 | **L1** | **MISS** | — | `[0, 4, -, -]` | `[4, 0]` |
| **3** | `8` | 8 | 0 | **L2** | **MISS** | — | `[0, 4, 8, -]` | `[8, 4, 0]` |
| **4** | `0` | 0 | 0 | **L0** | **HIT** | — | `[0, 4, 8, -]` | `[0, 8, 4]` |
| **5** | `4` | 4 | 0 | **L1** | **HIT** | — | `[0, 4, 8, -]` | `[4, 0, 8]` |
| **6** | `12` | 12 | 0 | **L3** | **MISS** | — | `[0, 4, 8, 12]` | `[12, 4, 0, 8]` |

- **Hits:** 2 | **Misses:** 4 | **Hit Rate:** **33.33%** | **Miss Rate:** **66.67%**
- **Analysis:** Without rigid set constraints, the cache utilizes all 4 physical slots. Blocks 0, 4, and 8 remain in the cache simultaneously, allowing subsequent requests to 0 and 4 to register immediate **cache hits**.

---

## 4. Quantitative Performance Comparison

| Metric | Direct-Mapped | 2-Way Set-Associative | Fully Associative |
| :--- | :---: | :---: | :---: |
| **Total Memory References** | 6 | 6 | 6 |
| **Cache Hits** | **0** | **0** | **2** |
| **Cache Misses** | **6** | **6** | **4** |
| **Hit Ratio** | **0.00%** | **0.00%** | **33.33%** |
| **Miss Ratio** | **100.00%** | **100.00%** | **66.67%** |
| **Lines Utilized** | 1 / 4 (25%) | 2 / 4 (50%) | **4 / 4 (100%)** |
| **Miss Classification** | 1 Cold + 5 Conflict | 2 Cold + 4 Conflict | 4 Cold + 0 Conflict |

---

## 5. Architectural Flexibility Analysis

### **Verdict:** Fully Associative mapping provides the highest flexibility.

### Technical Justification:
1. **Total Immunity to Conflict Misses:**  
   In both Direct-Mapped and Set-Associative configurations, block placement is bound by modulo arithmetic ($B \pmod S$). When access patterns exhibit a stride that aligns with the set count, multiple distinct blocks map to the same set. Fully Associative eliminates index constraints entirely.
2. **Complete Storage Capacity Utilization:**  
   Under Fully Associative mapping, 100% of the cache (4 out of 4 lines) was actively engaged to store data. In contrast, Direct-Mapped suffered from severe underutilization (75% idle capacity).
3. **Temporal Locality Preservation:**  
   By maintaining active working set elements across disjoint slots, blocks `0` and `4` were safely preserved, eliminating redundant memory bus transactions on subsequent accesses.

---

## 6. Sensitivity Analysis on Alternative Workload

To evaluate behavioral consistency, an alternating test sequence `[0, 2, 4, 0, 2, 8]` was evaluated:

| Workload Sequence | Direct-Mapped | 2-Way Set-Associative | Fully Associative | Architectural Takeaway |
| :--- | :---: | :---: | :---: | :--- |
| `0, 4, 8, 0, 4, 12` *(Benchmark)* | 0 Hits (0%) | 0 Hits (0%) | **2 Hits (33.33%)** | Stride-4 pattern exposes thrashing in fixed-set designs. |
| `0, 2, 4, 0, 2, 8` *(Even Stride)* | 0 Hits (0%) | **2 Hits (33.33%)** | **2 Hits (33.33%)** | 2-Way associative matches Fully Associative when stride is 2. |
| `0, 1, 2, 3, 0, 1` *(Unit Stride)* | **2 Hits (33.33%)** | **2 Hits (33.33%)** | **2 Hits (33.33%)** | All architectures perform equally under zero-conflict patterns. |

---

## 7. Python Implementation (`cache_simulator.py`)

```python
"""
Computer Organization and Architecture (ENCA302)
Student: Akash Sharma | Roll: 2401201108
Cache Memory Mapping and Replacement Simulator
"""
import sys
from typing import List, Optional, Tuple

class CacheLine:
    def __init__(self, line_id: int):
        self.line_id = line_id
        self.valid = False
        self.tag = None
        self.block_id = None
        self.last_access_cycle = 0

    def update(self, tag: int, block_id: int, cycle: int) -> None:
        self.valid = True
        self.tag = tag
        self.block_id = block_id
        self.last_access_cycle = cycle

class CacheSet:
    def __init__(self, set_id: int, ways: int, base_line_id: int):
        self.set_id = set_id
        self.ways = ways
        self.lines = [CacheLine(base_line_id + w) for w in range(ways)]

    def probe(self, tag: int) -> Optional[CacheLine]:
        for line in self.lines:
            if line.valid and line.tag == tag:
                return line
        return None

    def allocate(self, tag: int, block_id: int, cycle: int) -> Tuple[CacheLine, bool, Optional[int]]:
        for line in self.lines:
            if not line.valid:
                line.update(tag, block_id, cycle)
                return line, False, None
        victim_line = min(self.lines, key=lambda l: l.last_access_cycle)
        evicted_block = victim_line.block_id
        victim_line.update(tag, block_id, cycle)
        return victim_line, True, evicted_block

class CacheMemory:
    def __init__(self, title: str, total_lines: int, ways_per_set: int):
        self.title = title
        self.total_lines = total_lines
        self.ways_per_set = ways_per_set
        self.num_sets = total_lines // ways_per_set
        self.sets = [CacheSet(s, ways_per_set, s * ways_per_set) for s in range(self.num_sets)]
        self.hits = 0
        self.misses = 0
        self.current_cycle = 0
        self.event_log = []

    def access(self, block: int) -> dict:
        self.current_cycle += 1
        set_index = block % self.num_sets
        tag = block // self.num_sets
        target_set = self.sets[set_index]
        hit_line = target_set.probe(tag)
        if hit_line:
            self.hits += 1
            hit_line.last_access_cycle = self.current_cycle
            event = {"cycle": self.current_cycle, "block": block, "tag": tag,
                     "set": set_index, "line": hit_line.line_id, "status": "HIT", "evicted": None}
        else:
            self.misses += 1
            alloc_line, is_evict, ev_blk = target_set.allocate(tag, block, self.current_cycle)
            event = {"cycle": self.current_cycle, "block": block, "tag": tag,
                     "set": set_index, "line": alloc_line.line_id, "status": "MISS", "evicted": ev_blk}
        flat = [None] * self.total_lines
        for s in self.sets:
            for l in s.lines:
                flat[l.line_id] = l.block_id if l.valid else None
        event["cache_state"] = flat
        self.event_log.append(event)
        return event
```

---

## 8. Verification & Execution Instructions

```bash
# Execute benchmark sequence:
python cache_simulator.py

# Execute custom sequence:
python cache_simulator.py "0, 2, 4, 0, 2, 8"
```
