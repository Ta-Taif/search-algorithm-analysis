
import random

from algorithms import (
    iterative_binary_search,
    recursive_binary_search,
    sequential_search,
)

NUMBER_OF_ROUNDS = 10  # enough rounds to see both found and not-found searches


def generate_sorted_list(size=20):
    values = [random.randint(1, 100) for _ in range(size)]
    values.sort()  # binary search requires a sorted list
    return values


def choose_target(values):

    if random.random() < 0.5:
        return random.choice(values), True
    # Values are 1-100, so 101 can never be in the list.
    return 101, False


def result_is_acceptable(values, target, index, expected_present):

    if expected_present:
        return index != -1 and values[index] == target
    return index == -1


def run_one_round(round_number):
    values = generate_sorted_list()
    target, expected_present = choose_target(values)

    print(f"\n=== Round {round_number} ===")
    print(f"Sorted list: {values}")
    print(f"Target: {target}")
    print(f"Intended to be present: {expected_present}")

    results = {
        "Recursive binary search": recursive_binary_search(
            values, target, 0, len(values) - 1
        ),
        "Iterative binary search": iterative_binary_search(values, target),
        "Sequential search": sequential_search(values, target),
    }

    all_passed = True
    for algorithm_name, index in results.items():
        acceptable = result_is_acceptable(
            values, target, index, expected_present
        )
        message = "acceptable" if acceptable else "NOT ACCEPTABLE"
        print(f"  {algorithm_name:<24} index={index:<3} {message}")
        all_passed = all_passed and acceptable

    return all_passed, expected_present


def main():
    rounds_passed = 0
    present_rounds = 0
    absent_rounds = 0

    for round_number in range(1, NUMBER_OF_ROUNDS + 1):
        passed, expected_present = run_one_round(round_number)
        rounds_passed += passed
        if expected_present:
            present_rounds += 1
        else:
            absent_rounds += 1

    print("\n=== Summary ===")
    print(f"Rounds passed: {rounds_passed} of {NUMBER_OF_ROUNDS}")
    print(f"Present-target rounds: {present_rounds}")
    print(f"Absent-target rounds: {absent_rounds}")
    if present_rounds == 0 or absent_rounds == 0:
        print("Only one kind of search happened. Run again to see both.")
    elif rounds_passed == NUMBER_OF_ROUNDS:
        print("All Phase 2 tests passed. You can start Phase 3.")
    else:
        print("Some rounds failed. Fix them before starting Phase 3.")


if __name__ == "__main__":
    main()