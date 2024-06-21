import subprocess
from collections.abc import Sequence


def main(argv: Sequence[str] | None = None) -> int:
    try:
        subprocess.run(["bump-my-version", "bump", "patch"], check=True)
        return 0
    except subprocess.CalledProcessError as e:
        print(f"Error during version bump or push: {e}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
