import csv
import platform
import random
import statistics
import time
from pathlib import Path

from algorithms import (
    iterative_binary_search,
    recursive_binary_search,
    sequential_search,
)

DATA_SIZES = [5_000, 50_000, 100_000, 150_000, 1_000_000]
NUMBER_OF_TRIALS = 10
RESULTS_FILE = Path(__file__).parent / "results.csv"


def generate_trial_data(size):

    values = sorted(random.randint(1, 1_000_000) for _ in range(size))
    if random.random() < 0.5:
        target = random.choice(values)
    else:
        target = 1_000_001
    return values, target


def time_search(search_function, *arguments):
    start = time.perf_counter()
    index = search_function(*arguments)
    elapsed_microseconds = (time.perf_counter() - start) * 1_000_000
    return index, elapsed_microseconds


def verify_result(values, target, index):
    if index != -1:
        assert values[index] == target
    else:
        assert target not in values


def run_trials_for_size(size):
    recursive_times = []
    iterative_times = []
    sequential_times = []

    for _ in range(NUMBER_OF_TRIALS):
        values, target = generate_trial_data(size)

        index, elapsed = time_search(
            recursive_binary_search, values, target, 0, len(values) - 1
        )
        recursive_times.append(elapsed)
        verify_result(values, target, index)

        index, elapsed = time_search(iterative_binary_search, values, target)
        iterative_times.append(elapsed)
        verify_result(values, target, index)

        index, elapsed = time_search(sequential_search, values, target)
        sequential_times.append(elapsed)
        verify_result(values, target, index)

    return recursive_times, iterative_times, sequential_times


def save_results(rows):
    with open(RESULTS_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(
            ["data_size", "recursive_binary_us", "iterative_binary_us",
             "sequential_us"]
        )
        writer.writerows(rows)


def main():
    print("Environment:", platform.platform())
    print("Python:", platform.python_version(), "|", platform.processor())
    print(f"Trials per size: {NUMBER_OF_TRIALS}\n")
    print(f"{'Size':>10} {'Recursive (us)':>16} {'Iterative (us)':>16} "
          f"{'Sequential (us)':>17}")

    rows = []
    for size in DATA_SIZES:
        recursive_times, iterative_times, sequential_times = (
            run_trials_for_size(size)
        )
        row = [
            size,
            round(statistics.median(recursive_times), 2),
            round(statistics.median(iterative_times), 2),
            round(statistics.median(sequential_times), 2),
        ]
        rows.append(row)
        print(f"{row[0]:>10,} {row[1]:>16.2f} {row[2]:>16.2f} {row[3]:>17.2f}")

    save_results(rows)
    print(f"\nAll {len(DATA_SIZES)} sizes x {NUMBER_OF_TRIALS} trials verified.")
    print(f"Results saved to {RESULTS_FILE.name}")


if __name__ == "__main__":
    main()