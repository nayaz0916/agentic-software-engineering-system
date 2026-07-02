from typing import List, Optional
from anthropic import Anthropic
from src.models import Requirement, Task, TaskStatus
import os
import uuid


class TaskDecompositionAgent:
    """Breaks high-level requirements into structured, actionable tasks."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.client = Anthropic(api_key=api_key or os.getenv("ANTHROPIC_API_KEY"))
    
    def decompose(self, requirement: Requirement) -> List[Task]:
        """Decompose a requirement into structured tasks with dependencies."""
        
        prompt = f"""Decompose the following software requirement into structured, actionable tasks.

Requirement: "{requirement.normalized or requirement.original}"
Type: {requirement.type}
Ambiguities: {requirement.ambiguities}
Assumptions: {requirement.assumptions}

Provide:
1. A list of 5-10 specific, actionable tasks
2. Dependencies between tasks (which tasks must complete before others)
3. Estimated effort for each task
4. Expected outputs for each task

Format each task as:
- Task ID: T1, T2, T3, etc.
- Description: Clear, specific action
- Dependencies: List of task IDs this depends on
- Effort: Low/Medium/High
- Outputs: What this task produces

Focus on engineering tasks: design, implementation, testing, documentation."""
        
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}]
        )
        
        content = response.content[0].text
        tasks = self._parse_tasks(content)
        
        return tasks
    
    def _parse_tasks(self, content: str) -> List[Task]:
        """Parse tasks from the agent response."""
        tasks = []
        lines = content.split('\n')
        
        current_task = None
        for line in lines:
            line = line.strip()
            
            # Detect task start
            if line.startswith('Task ID:') or line.startswith('- Task'):
                if current_task:
                    tasks.append(current_task)
                task_id = line.split(':')[1].strip() if ':' in line else str(uuid.uuid4())[:8]
                current_task = Task(id=task_id, description="")
            
            # Parse task components
            elif current_task:
                if line.startswith('Description:'):
                    current_task.description = line.split(':', 1)[1].strip()
                elif line.startswith('Dependencies:'):
                    deps = line.split(':', 1)[1].strip()
                    current_task.dependencies = [d.strip() for d in deps.split(',') if d.strip()]
                elif line.startswith('Effort:'):
                    current_task.metadata['effort'] = line.split(':', 1)[1].strip()
                elif line.startswith('Outputs:'):
                    outputs = line.split(':', 1)[1].strip()
                    current_task.outputs = [o.strip() for o in outputs.split(',') if o.strip()]
        
        if current_task:
            tasks.append(current_task)
        
        # If parsing failed, create default tasks
        if not tasks:
            tasks = self._create_default_tasks()
        
        return tasks
    
    def _create_default_tasks(self) -> List[Task]:
        """Create default task structure if parsing fails."""
        return [
            Task(
                id="T1",
                description="Analyze requirements and design architecture",
                dependencies=[],
                metadata={"effort": "High"},
                outputs=["Architecture document", "API specifications"]
            ),
            Task(
                id="T2",
                description="Set up project structure and dependencies",
                dependencies=["T1"],
                metadata={"effort": "Low"},
                outputs=["Project scaffold", "Configuration files"]
            ),
            Task(
                id="T3",
                description="Implement core functionality",
                dependencies=["T2"],
                metadata={"effort": "High"},
                outputs=["Source code", "Unit tests"]
            ),
            Task(
                id="T4",
                description="Implement API endpoints",
                dependencies=["T3"],
                metadata={"effort": "Medium"},
                outputs=["API handlers", "Integration tests"]
            ),
            Task(
                id="T5",
                description="Add persistence layer",
                dependencies=["T3"],
                metadata={"effort": "Medium"},
                outputs=["Database schema", "Data access layer"]
            ),
            Task(
                id="T6",
                description="Write comprehensive tests",
                dependencies=["T4", "T5"],
                metadata={"effort": "High"},
                outputs=["Test suite", "Test coverage report"]
            ),
            Task(
                id="T7",
                description="Create documentation",
                dependencies=["T4", "T5"],
                metadata={"effort": "Medium"},
                outputs=["API docs", "User guide", "README"]
            ),
            Task(
                id="T8",
                description="Validate and review implementation",
                dependencies=["T6", "T7"],
                metadata={"effort": "Medium"},
                outputs=["Validation report", "Review checklist"]
            )
        ]
