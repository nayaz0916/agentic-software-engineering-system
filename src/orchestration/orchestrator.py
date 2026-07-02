from typing import List, Optional, Callable
from src.models import Workflow, Task, TaskStatus, Requirement
from src.agents.requirement_agent import RequirementUnderstandingAgent
from src.agents.task_decomposition_agent import TaskDecompositionAgent
from src.agents.codebase_agent import CodebaseReasoningAgent
from src.generation.code_generator import CodeGenerator
from src.validation.validator import Validator
import asyncio
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()


class WorkflowOrchestrator:
    """Orchestrates multi-step workflow execution with dependency management."""
    
    def __init__(self):
        self.requirement_agent = RequirementUnderstandingAgent()
        self.task_agent = TaskDecompositionAgent()
        self.codebase_agent = CodebaseReasoningAgent()
        self.code_generator = CodeGenerator()
        self.validator = Validator()
        self.human_approval_callback: Optional[Callable] = None
    
    def set_human_approval(self, callback: Callable):
        """Set callback for human approval at critical steps."""
        self.human_approval_callback = callback
    
    async def execute(self, requirement_text: str, codebase_path: Optional[str] = None) -> Workflow:
        """Execute the full workflow from requirement to output."""
        
        console.print("\n[bold blue]Starting Agentic Software Engineering Workflow[/bold blue]\n")
        
        # Step 1: Understand requirement
        console.print("[yellow]Step 1: Understanding requirement...[/yellow]")
        requirement = self.requirement_agent.analyze(requirement_text)
        console.print(f"[green]✓ Requirement type: {requirement.type}[/green]")
        console.print(f"[green]✓ Normalized: {requirement.normalized}[/green]")
        
        # Step 2: Decompose tasks
        console.print("\n[yellow]Step 2: Decomposing tasks...[/yellow]")
        tasks = self.task_agent.decompose(requirement)
        console.print(f"[green]✓ Created {len(tasks)} tasks[/green]")
        
        # Step 3: Codebase analysis (if brownfield)
        if requirement.type == "brownfield" or codebase_path:
            console.print("\n[yellow]Step 3: Analyzing codebase...[/yellow]")
            codebase_analysis = self.codebase_agent.analyze(requirement, codebase_path)
            console.print(f"[green]✓ Identified {len(codebase_analysis.impacted_services)} impacted services[/green]")
        else:
            codebase_analysis = None
        
        # Create workflow
        workflow = Workflow(
            id="WF-" + str(hash(requirement_text))[:8],
            requirement=requirement,
            tasks=tasks,
            status=TaskStatus.IN_PROGRESS
        )
        
        # Step 4: Execute tasks with orchestration
        console.print("\n[yellow]Step 4: Executing tasks with orchestration...[/yellow]")
        await self._execute_tasks(workflow)
        
        # Step 5: Generate outputs
        console.print("\n[yellow]Step 5: Generating engineering outputs...[/yellow]")
        outputs = self.code_generator.generate(workflow, codebase_analysis)
        workflow.artifacts["outputs"] = outputs
        console.print("[green]✓ Generated code, tests, and documentation[/green]")
        
        # Step 6: Validate
        console.print("\n[yellow]Step 6: Validating outputs...[/yellow]")
        validation = self.validator.validate(workflow, outputs)
        workflow.artifacts["validation"] = validation
        console.print(f"[green]✓ Validation score: {validation.confidence_score:.2f}[/green]")
        
        workflow.status = TaskStatus.COMPLETED
        
        console.print("\n[bold green]✓ Workflow completed successfully[/bold green]\n")
        
        return workflow
    
    async def _execute_tasks(self, workflow: Workflow):
        """Execute tasks respecting dependencies with parallel execution where possible."""
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            
            completed_tasks = set()
            
            while len(completed_tasks) < len(workflow.tasks):
                # Find tasks ready to execute (dependencies satisfied)
                ready_tasks = [
                    task for task in workflow.tasks
                    if task.status == TaskStatus.PENDING
                    and all(dep in completed_tasks for dep in task.dependencies)
                ]
                
                if not ready_tasks:
                    # Check for circular dependencies or blocked tasks
                    pending_tasks = [t for t in workflow.tasks if t.status == TaskStatus.PENDING]
                    if pending_tasks:
                        console.print(f"[red]Blocked tasks: {[t.id for t in pending_tasks]}[/red]")
                        # Force execute remaining tasks
                        ready_tasks = pending_tasks
                
                # Execute ready tasks in parallel
                task_progress = [
                    progress.add_task(f"Executing {task.id}: {task.description}", total=None)
                    for task in ready_tasks
                ]
                
                await asyncio.gather(*[
                    self._execute_single_task(task, workflow)
                    for task in ready_tasks
                ])
                
                # Mark as completed
                for task in ready_tasks:
                    task.status = TaskStatus.COMPLETED
                    completed_tasks.add(task.id)
                    progress.remove_task(task_progress[ready_tasks.index(task)])
                    console.print(f"[green]✓ Completed {task.id}[/green]")
                
                # Human approval checkpoint
                if self.human_approval_callback:
                    should_continue = await self.human_approval_callback(workflow)
                    if not should_continue:
                        console.print("[yellow]Workflow paused by human approval[/yellow]")
                        break
    
    async def _execute_single_task(self, task: Task, workflow: Workflow):
        """Execute a single task (simulated)."""
        # In production, this would call actual tools/agents
        await asyncio.sleep(0.5)  # Simulate work
        
        # Store task output
        task.outputs.append(f"Output for {task.id}")
        workflow.artifacts[f"task_{task.id}"] = {
            "description": task.description,
            "status": "completed",
            "output": f"Simulated output for {task.id}"
        }
