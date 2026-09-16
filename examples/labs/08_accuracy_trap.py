"""Lab 08: never-fire wins accuracy and loses the exam."""

from inkfold.corpus import iter_problems
from inkfold.evaluate import accuracy_trap_demo


def main() -> None:
    trap = accuracy_trap_demo(iter_problems())
    for key, val in trap.items():
        print(f"{key:22s} {val}")
    print()
    print("If your first sentence is the accuracy number, start again.")


if __name__ == "__main__":
    main()
