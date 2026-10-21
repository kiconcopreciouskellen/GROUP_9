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
