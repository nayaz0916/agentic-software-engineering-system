"""
Greenfield Scenario Example
Demonstrates building a new system from scratch.
"""

import asyncio
from main import main


async def run_greenfield_example():
    """Run the greenfield scenario."""
    print("=" * 80)
    print("Greenfield Scenario: Real-time Chat Application")
    print("=" * 80)
    print("\nRequirement: Build a real-time chat application with WebSocket support,")
    print("message persistence, and user authentication.")
    print("\nThis example demonstrates:")
    print("  - New system development from scratch")
    print("  - Architecture design for greenfield projects")
    print("  - Full stack generation (frontend, backend, database)")
    print("  - WebSocket implementation")
    print("  - Authentication system design")
    print("\n" + "=" * 80 + "\n")
    
    import sys
    sys.argv = ["main.py", "--scenario", "greenfield"]
    await main()


if __name__ == "__main__":
    asyncio.run(run_greenfield_example())
