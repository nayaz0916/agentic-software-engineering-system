"""
Brownfield Scenario Example
Demonstrates enhancing an existing system.
"""

import asyncio
from main import main


async def run_brownfield_example():
    """Run the brownfield scenario."""
    print("=" * 80)
    print("Brownfield Scenario: API Gateway Enhancement")
    print("=" * 80)
    print("\nRequirement: Add rate limiting and caching to the existing API gateway")
    print("to improve performance under load.")
    print("\nThis example demonstrates:")
    print("  - Analysis of existing codebase")
    print("  - Impact assessment on existing services")
    print("  - Safe modification strategies")
    print("  - Backward compatibility considerations")
    print("  - Migration planning")
    print("\n" + "=" * 80 + "\n")
    
    import sys
    sys.argv = ["main.py", "--scenario", "brownfield"]
    await main()


if __name__ == "__main__":
    asyncio.run(run_brownfield_example())
