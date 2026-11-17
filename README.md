# Cache Memory Mapping & Architecture Simulator
### Computer Organization and Architecture (ENCA302)
**K.R. Mangalam University — School of Engineering and Technology**  
- **Student Name:** Akash Sharma  
- **Roll Number:** 2401201108  
- **Program:** BCA (AI & DS) – Section B  
- **Course Coordinator:** Alina Banerjee  

---

## 📌 Project Overview
This project simulates and benchmarks the three canonical cache mapping architectures:
1. **Direct-Mapped Cache** (1-Way Associative)
2. **2-Way Set-Associative Cache** (2-Way Associative with LRU Replacement)
3. **Fully Associative Cache** (4-Way Associative with Global LRU Replacement)

Demonstrating explicit Tag and Set index address decomposition, cycle-by-cycle line state transitions, hit/miss detection, and conflict thrashing analysis for memory access sequence `[0, 4, 8, 0, 4, 12]`.

---

## 📁 Repository Directory Structure

```text
coa akash/
├── .vscode/
│   └── tasks.json                     # VS Code tasks for automated execution
├── docs/
│   ├── screenshots/
│   │   ├── architecture.png           # Hardware Tag/Index decoding architecture
│   │   ├── shot_build.png             # Simulator initialization & configuration
│   │   ├── shot_check1.png            # Address decomposition verification
│   │   ├── shot_direct.png            # Direct-Mapped execution trace
│   │   ├── shot_setassoc.png          # 2-Way Set-Associative execution trace
│   │   ├── shot_full.png              # Fully Associative execution trace
│   │   └── shot_summary.png           # Comparative performance matrix
│   └── terminal_output.log            # Execution log output
├── reports/                           # Academic report artifacts
│   └── .gitkeep
├── .gitignore                         # Python and environment ignores
├── cache_simulator.py                 # Object-oriented simulation engine
├── CACHE_SIMULATION_REPORT.md         # Detailed technical simulation report
└── README.md                          # Repository documentation
```

---

## 🚀 Execution Instructions

```bash
# Run default sequence [0, 4, 8, 0, 4, 12]:
python cache_simulator.py

# Run custom sequence:
python cache_simulator.py "0, 2, 4, 0, 2, 8"
```

---

## 📊 Summary of Benchmark Results

| Mapping Architecture | Hits | Misses | Hit Ratio | Miss Ratio | Cache Occupancy |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Direct-Mapped Cache** | 0 | 6 | 0.00% | 100.00% | 1 of 4 (25%) |
| **2-Way Set-Associative Cache** | 0 | 6 | 0.00% | 100.00% | 2 of 4 (50%) |
| **Fully Associative Cache** | **2** | **4** | **33.33%** | **66.67%** | **4 of 4 (100%)** |

> **Conclusion:** **Fully Associative Cache** provides the highest placement flexibility, eliminating conflict misses caused by stride-4 access patterns and achieving a 33.33% hit rate.
