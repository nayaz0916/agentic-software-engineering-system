"""
URL Shortener Example - Mandatory Use Case
Demonstrates the system with: "Build a scalable URL shortener service with APIs, persistence, and analytics."
"""

import asyncio
from main import main


async def run_url_shortener_example():
    """Run the URL shortener use case."""
    print("=" * 80)
    print("URL Shortener Use Case")
    print("=" * 80)
    print("\nRequirement: Build a scalable URL shortener service with APIs, persistence, and analytics.")
    print("\nThis example demonstrates:")
    print("  - Requirement analysis and decomposition")
    print("  - Task orchestration with dependencies")
    print("  - Code generation for APIs, persistence, and analytics")
    print("  - Test generation")
    print("  - Documentation generation")
    print("  - Validation and risk assessment")
    print("\n" + "=" * 80 + "\n")
    
    # Import and run the main system
    import sys
    sys.argv = ["main.py", "--scenario", "url-shortener"]
    await main()


if __name__ == "__main__":
    asyncio.run(run_url_shortener_example())
