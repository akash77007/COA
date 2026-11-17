# Cache Memory Mapping & Architecture Simulator
### Computer Organization and Architecture (ENCA302)
**K.R. Mangalam University — School of Engineering and Technology**  
- **Student Name:** Akash Sharma  
- **Roll Number:** 2401201108  
- **Program:** BCA (AI & DS) – Section B  
- **Course Coordinator:** Alina Banerjee  

---

## 📌 Project Overview
This project presents an empirical and architectural simulation comparing the three primary cache mapping paradigms:
1. **Direct-Mapped Cache** (1-Way Associative)
2. **2-Way Set-Associative Cache** (2-Way Associative with LRU Replacement)
3. **Fully Associative Cache** (4-Way Associative with Global LRU Replacement)

Evaluated under the primary benchmark access sequence `[0, 4, 8, 0, 4, 12]` as well as three independent stress tests:
- **Test 1:** `0, 1, 0, 1, 0, 1` (Repeated access to two non-conflicting blocks)
- **Test 2:** `2, 6, 10, 14, 2, 6` (Multiple blocks competing for the same set)
- **Test 3:** `0, 1, 2, 3, 4, 5, 0, 1` (Cache flushing and capacity limit analysis)

---

## 📁 Repository Directory Structure

```text
coa_akash/
├── .vscode/
│   └── tasks.json                     # VS Code tasks for automated execution
├── docs/
│   ├── screenshots/                   # Freshly generated terminal trace screenshots
│   │   ├── architecture.png           # Cache configuration & experimental setup
│   │   ├── shot_build.png             # Simulator initialization & configuration
│   │   ├── shot_check1.png            # Step-by-step analysis of Block 8 arrival
│   │   ├── shot_direct.png            # Direct-Mapped execution trace
│   │   ├── shot_setassoc.png          # 2-Way Set-Associative execution trace
│   │   ├── shot_full.png              # Fully Associative execution trace
│   │   └── shot_summary.png           # Comparative performance matrix
│   └── terminal_output.log            # Complete simulation log (main + 3 tests)
├── reports/                           # Academic report artifacts folder
│   └── .gitkeep
├── .gitignore                         # Python and environment ignores
├── cache_simulator.py                 # Simulation engine with `--all` benchmark support
├── CACHE_SIMULATION_REPORT.md         # Full report with Block 8 worked example & tests
└── README.md                          # Repository documentation
```

---

## 🚀 Execution Instructions

```bash
# Run default sequence [0, 4, 8, 0, 4, 12]:
python cache_simulator.py

# Run main benchmark + all three additional tests:
python cache_simulator.py --all

# Run custom sequence:
python cache_simulator.py "2, 6, 10, 14, 2, 6"
```

---

## 📊 Summary of Main Benchmark Results (`0, 4, 8, 0, 4, 12`)

| Mapping Architecture | Hits | Misses | Hit Ratio | Miss Ratio | Cache Occupancy |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Direct-Mapped Cache** | 0 | 6 | 0.00% | 100.00% | 1 of 4 (25%) |
| **2-Way Set-Associative Cache** | 0 | 6 | 0.00% | 100.00% | 2 of 4 (50%) |
| **Fully Associative Cache** | **2** | **4** | **33.33%** | **66.67%** | **4 of 4 (100%)** |

> **Conclusion:** **Fully Associative Cache** provides the highest placement flexibility, eliminating conflict misses caused by stride-4 access patterns and achieving a 33.33% hit rate.
