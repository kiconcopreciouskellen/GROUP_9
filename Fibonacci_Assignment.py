import sys
import time
import math
from importlib import import_module

# Global counters and tables
counter_A = 0
counter_B = 0
fibtable = {}

# Check for matplotlib
try:
    plt = import_module("matplotlib.pyplot")
except ImportError:
    plt = None


# PRECIOUS: Core Algorithm Implementations and Basic Verification

def fib_A(n):
    """Algorithm A: Plain Recursion"""
    global counter_A
    counter_A += 1

    if n == 0 or n == 1:
        return n
    return fib_A(n - 1) + fib_A(n - 2)


def fib_B(n):
    """Algorithm B: Recursion with Memoization"""
    global counter_B
    counter_B += 1

    if n in fibtable:
        return fibtable[n]

    if n == 0 or n == 1:
        value = n
    else:
        value = fib_B(n - 1) + fib_B(n - 2)

    fibtable[n] = value
    return value


def verify_correctness():
    """Verifies that fib_A and fib_B return identical results for n = 0 to 20"""
    global counter_A, counter_B
    print(" PART 1: Verification (n = 0 to 20) ")
    all_matched = True

    for n in range(21):
        fibtable.clear()
        counter_A = 0
        counter_B = 0

        val_A = fib_A(n)
        val_B = fib_B(n)

        if val_A != val_B:
            all_matched = False

    if all_matched:
        print("SUCCESS: Both algorithms return identical results for n = 0 to 20.\n")
    else:
        print("FAILURE: Mismatch detected between implementations.\n")
    return all_matched


# MULOOSI AMON : Number2 ; Timing , Call Counting and Result Plotting


def run_experiments():
    global counter_A, counter_B
    print(" PART 2: Running Experiments ")

    # Experiment (a): Algorithm A
    results_A = []
    n_targets_A = [5, 10, 15, 20, 25, 30, 35]

    for n in n_targets_A:
        counter_A = 0
        start = time.perf_counter()
        fib_A(n)
        elapsed = time.perf_counter() - start
        results_A.append((n, counter_A, elapsed))
        print(f"Alg A | n={n:<2} | Calls: {counter_A:<10} | Time: {elapsed:.6f}s")
        if elapsed > 60.0:
            print(f"Stopping Algorithm A at n={n} (exceeded 60s limit)")
            break

    # Experiment (b): Algorithm B
    results_B = []
    n_targets_B = [10, 50, 100, 200, 500, 1000]

    for n in n_targets_B:
        counter_B = 0
        fibtable.clear()

        orig_limit = sys.getrecursionlimit()
        sys.setrecursionlimit(max(orig_limit, n + 500))

        start = time.perf_counter()
        fib_B(n)
        elapsed = time.perf_counter() - start
        results_B.append((n, counter_B, elapsed))
        print(f"Alg B | n={n:<4} | Calls: {counter_B:<10} | Time: {elapsed:.6f}s")

        sys.setrecursionlimit(orig_limit)

    plot_results(results_A, results_B)
    return results_A, results_B


def plot_results(results_A, results_B):
    if plt is None:
        print("Plot skipped: install matplotlib to generate the plot.\n")
        return

    nA, callsA, _ = zip(*results_A)
    nB, callsB, _ = zip(*results_B)

    plt.figure(figsize=(12, 5))

    # Log scale plot for Algorithm A
    plt.subplot(1, 2, 1)
    plt.plot(nA, callsA, "ro-", label="Algorithm A (Naive)")
    plt.yscale("log")
    plt.xlabel("n")
    plt.ylabel("Calls (Log Scale)")
    plt.title("Algorithm A: Calls vs n")
    plt.grid(True, which="both", ls="--")
    plt.legend()

    # Linear plot for Algorithm B
    plt.subplot(1, 2, 2)
    plt.plot(nB, callsB, "bo-", label="Algorithm B (Memoized)")
    plt.xlabel("n")
    plt.ylabel("Calls (Linear Scale)")
    plt.title("Algorithm B: Calls vs n")
    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.savefig("fibonacci_calls_plot.png")
    print("\nPlot successfully saved to 'fibonacci_calls_plot.png'.\n")
