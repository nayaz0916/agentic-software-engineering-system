"""
Ambiguous Requirement Scenario Example
Demonstrates handling unclear requirements.
"""

import asyncio
from main import main


async def run_ambiguous_example():
    """Run the ambiguous requirement scenario."""
    print("=" * 80)
    print("Ambiguous Requirement Scenario")
    print("=" * 80)
    print("\nRequirement: Make the system faster and better.")
    print("\nThis example demonstrates:")
    print("  - Identifying ambiguities in requirements")
    print("  - Asking clarifying questions")
    print("  - Making reasonable assumptions")
    print("  - Proposing multiple solution approaches")
    print("  - Risk assessment for ambiguous requirements")
    print("\n" + "=" * 80 + "\n")
    
    import sys
    sys.argv = ["main.py", "--scenario", "ambiguous"]
    await main()


if __name__ == "__main__":
    asyncio.run(run_ambiguous_example())
