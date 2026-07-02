#!/usr/bin/env python3
"""
Agentic Software Engineering System
Main entry point for the system.
"""

import asyncio
import argparse
from dotenv import load_dotenv
from src.orchestration.orchestrator import WorkflowOrchestrator
from src.models import ExecutionSummary
from rich.console import Console
from rich.panel import Panel

load_dotenv()
console = Console()


async def human_approval_callback(workflow):
    """Callback for human approval at critical steps."""
    console.print(Panel(f"\n[yellow]Human Approval Checkpoint[/yellow]\n"
                        f"Requirement: {workflow.requirement.original}\n"
                        f"Completed tasks: {sum(1 for t in workflow.tasks if t.status.value == 'completed')}/{len(workflow.tasks)}\n"
                        f"\nContinue? (y/n): ", title="Approval Required"))
    
    # In production, this would wait for actual user input
    # For demo, auto-approve
    return True


async def main():
    parser = argparse.ArgumentParser(description="Agentic Software Engineering System")
    parser.add_argument("--requirement", type=str, help="Software requirement to process")
    parser.add_argument("--codebase", type=str, help="Path to existing codebase (for brownfield)")
    parser.add_argument("--scenario", type=str, choices=["url-shortener", "greenfield", "brownfield", "ambiguous"],
                       help="Run predefined scenario")
    
    args = parser.parse_args()
    
    orchestrator = WorkflowOrchestrator()
    orchestrator.set_human_approval(human_approval_callback)
    
    # Determine requirement
    if args.scenario:
        requirement = get_scenario_requirement(args.scenario)
    elif args.requirement:
        requirement = args.requirement
    else:
        # Default to URL shortener
        requirement = "Build a scalable URL shortener service with APIs, persistence, and analytics."
        console.print("[yellow]No requirement specified, using default URL shortener scenario[/yellow]")
    
    # Execute workflow
    workflow = await orchestrator.execute(requirement, args.codebase)
    
    # Generate summary
    summary = generate_summary(workflow)
    display_summary(summary)
    
    # Save outputs
    save_outputs(workflow)


def get_scenario_requirement(scenario: str) -> str:
    """Get predefined scenario requirements."""
    scenarios = {
        "url-shortener": "Build a scalable URL shortener service with APIs, persistence, and analytics.",
        "greenfield": "Build a real-time chat application with WebSocket support, message persistence, and user authentication.",
        "brownfield": "Add rate limiting and caching to the existing API gateway to improve performance under load.",
        "ambiguous": "Make the system faster and better."
    }
    return scenarios.get(scenario, scenarios["url-shortener"])


def generate_summary(workflow) -> ExecutionSummary:
    """Generate final execution summary."""
    from src.validation.validator import Validator
    validator = Validator()
    
    risks = validator.assess_risks(workflow)
    
    return ExecutionSummary(
        implementation_plan=f"Implemented {len(workflow.tasks)} tasks to satisfy: {workflow.requirement.normalized}",
        rationale="Tasks were decomposed based on requirement analysis and executed with dependency management.",
        artifacts=workflow.artifacts,
        risks=risks,
        validation_approach="Generated outputs validated against requirements with confidence scoring.",
        assumptions=workflow.requirement.assumptions,
        limitations=["Simulated task execution", "Limited codebase analysis without actual file access"]
    )


def display_summary(summary: ExecutionSummary):
    """Display the execution summary."""
    console.print("\n[bold cyan]Execution Summary[/bold cyan]")
    console.print(Panel(summary.implementation_plan, title="Implementation Plan"))
    console.print(Panel(summary.rationale, title="Rationale"))
    
    console.print("\n[bold]Risks:[/bold]")
    for risk in summary.risks.risks:
        console.print(f"  - {risk}")
    
    console.print("\n[bold]Assumptions:[/bold]")
    for assumption in summary.assumptions:
        console.print(f"  - {assumption}")
    
    console.print("\n[bold]Limitations:[/bold]")
    for limitation in summary.limitations:
        console.print(f"  - {limitation}")


def save_outputs(workflow):
    """Save generated outputs to files."""
    import json
    from pathlib import Path
    
    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)
    
    # Save artifacts
    with open(output_dir / "artifacts.json", "w") as f:
        json.dump(workflow.artifacts, f, indent=2, default=str)
    
    # Save code outputs
    if "outputs" in workflow.artifacts:
        outputs = workflow.artifacts["outputs"]
        
        # Save code
        code_dir = output_dir / "code"
        code_dir.mkdir(exist_ok=True)
        for filename, content in outputs.code.items():
            (code_dir / filename).write_text(content)
        
        # Save tests
        test_dir = output_dir / "tests"
        test_dir.mkdir(exist_ok=True)
        for filename, content in outputs.tests.items():
            (test_dir / filename).write_text(content)
        
        # Save documentation
        docs_dir = output_dir / "docs"
        docs_dir.mkdir(exist_ok=True)
        for filename, content in outputs.documentation.items():
            (docs_dir / filename).write_text(content)
    
    console.print(f"[green]✓ Outputs saved to {output_dir}/[/green]")


if __name__ == "__main__":
    asyncio.run(main())
