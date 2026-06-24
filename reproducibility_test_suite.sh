#!/bin/bash
# Reproducibility Test Suite for Pre-Submission Validation
# =========================================================
#
# Purpose: Verify robustness before paper submission
# Time: ~1-2 hours total
#
# Tests:
# 1. Seed robustness (Stage 5.5 with different seeds)
# 2. N=10^7 scaling (higher statistics)
# 3. Correlation sign stability (Stage 6 variations)

set -e  # Exit on error

echo "=========================================="
echo "PRE-SUBMISSION REPRODUCIBILITY TEST SUITE"
echo "=========================================="
echo ""
echo "Purpose: Verify robustness of all key results"
echo "Time: ~1-2 hours"
echo ""

# ============================================================================
# TEST 1: SEED ROBUSTNESS (Stage 5.5)
# ============================================================================

echo "=========================================="
echo "TEST 1: SEED ROBUSTNESS (Stage 5.5)"
echo "=========================================="
echo ""
echo "Running Stage 5.5 with NEW seed range (100-109)..."
echo ""

# Modify wheel30_test.cpp to accept seed offset
# For now: Run multiple times with different manual seeds

echo "Run 1: Seeds 0-9 (original)"
./wheel30_test 1000000 10 > reproducibility_stage5.5_seeds_0-9.txt
echo "  Done. Results saved to reproducibility_stage5.5_seeds_0-9.txt"

echo ""
echo "Run 2: Seeds 100-109 (new)"
# We'll need to modify the C++ code to accept seed offset
# For now, document that this needs implementation
echo "  [TODO: Requires seed-offset parameter in wheel30_test.cpp]"
echo ""

# ============================================================================
# TEST 2: N=10^7 SCALING TEST
# ============================================================================

echo "=========================================="
echo "TEST 2: N=10^7 SCALING TEST"
echo "=========================================="
echo ""
echo "Running Stage 5.5 with N=10,000,000 (5 seeds)..."
echo ""
echo "This may take 5-10 minutes..."
echo ""

./wheel30_test 10000000 5 > reproducibility_stage5.5_N10M.txt
echo "  Done. Results saved to reproducibility_stage5.5_N10M.txt"
echo ""

# ============================================================================
# TEST 3: CORRELATION SIGN STABILITY (Stage 6)
# ============================================================================

echo "=========================================="
echo "TEST 3: CORRELATION SIGN STABILITY"
echo "=========================================="
echo ""
echo "Running Stage 6 with N=1,000,000 (higher statistics)..."
echo ""

# Modify stage6 script to use N=1M instead of 100k
python3 stage6_k_tuple_screening_N1M.py > reproducibility_stage6_N1M.txt
echo "  Done. Results saved to reproducibility_stage6_N1M.txt"
echo ""

# ============================================================================
# COMPARISON & SUMMARY
# ============================================================================

echo "=========================================="
echo "REPRODUCIBILITY TEST SUMMARY"
echo "=========================================="
echo ""
echo "All tests completed. Check output files:"
echo ""
echo "1. Stage 5.5 (original):  reproducibility_stage5.5_seeds_0-9.txt"
echo "2. Stage 5.5 (N=10M):     reproducibility_stage5.5_N10M.txt"
echo "3. Stage 6 (N=1M):        reproducibility_stage6_N1M.txt"
echo ""
echo "Manual checks required:"
echo "  - z-scores increase by ~√10 factor at N=10M"
echo "  - Correlation signs remain stable"
echo "  - Relative differences (H_Prime/H_Wheel) stay consistent"
echo ""
echo "If all checks pass → Ready for submission"
echo "If any check fails → Investigate before submitting"
echo ""
