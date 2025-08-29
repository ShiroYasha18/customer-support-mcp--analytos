"""
Node class for LangGraph agent.
Represents a single node in the workflow graph with deterministic/non-deterministic execution modes.

Cursor Prompt: This file defines the Node class that executes workflow stages. Each node can run in:
- Deterministic mode: Predictable, repeatable execution for critical stages
- Non-deterministic mode: Flexible execution allowing variability for creative tasks

Extend by adding new execution modes, validation rules, or performance optimizations.
"""

import time
import random
import logging
from typing import Dict, List, Any, Optional, Callable
from enum import Enum
from core.mcp_client import MCPClient

logger = logging.getLogger(__name__)


class ExecutionMode(Enum):
    """Execution modes for node processing."""
    DETERMINISTIC = "deterministic"
    NON_DETERMINISTIC = "non_deterministic"
    ADAPTIVE = "adaptive"


class NodeStatus(Enum):
    """Node execution status."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


class Node:
    """Represents a single node in the workflow graph."""
    
    def __init__(self, 
                 name: str, 
                 abilities: List[str], 
                 mcp_client: MCPClient,
                 execution_mode: ExecutionMode = ExecutionMode.DETERMINISTIC,
                 server_type: str = 'common',  # Add server_type parameter
                 timeout: Optional[int] = None,
                 retry_count: int = 3,
                 quality_threshold: float = 0.8,
                 validation_rules: Optional[List[Callable]] = None):
        """Initialize a workflow node."""
        self.name = name
        self.abilities = abilities
        self.mcp_client = mcp_client
        self.execution_mode = execution_mode
        self.server_type = server_type  # Store server type
        self.timeout = timeout or 30
        self.retry_count = retry_count
        self.quality_threshold = quality_threshold
        self.validation_rules = validation_rules or []
        
        # Initialize execution state
        self.status = NodeStatus.PENDING
        self.execution_history = []
        self.performance_metrics = {
            'total_executions': 0,
            'successful_executions': 0,
            'average_duration': 0.0,
            'quality_scores': []
        }
        
        logger.info(f"🔧 Node '{name}' initialized with {len(abilities)} abilities in {execution_mode.value} mode")
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the node's abilities with advanced error handling and monitoring."""
        start_time = time.time()
        self.status = NodeStatus.IN_PROGRESS
        
        execution_context = {
            "node_name": self.name,
            "execution_mode": self.execution_mode.value,
            "start_time": start_time,
            "attempt": 1
        }
        
        result = input_data.copy()
        
        try:
            # Execute based on mode
            if self.execution_mode == ExecutionMode.DETERMINISTIC:
                result = self._execute_deterministic(result, execution_context)
            elif self.execution_mode == ExecutionMode.NON_DETERMINISTIC:
                result = self._execute_non_deterministic(result, execution_context)
            else:  # ADAPTIVE
                result = self._execute_adaptive(result, execution_context)
            
            # Validate results
            if self._validate_results(result):
                self.status = NodeStatus.COMPLETED
                self.performance_metrics["successful_executions"] += 1
            else:
                self.status = NodeStatus.FAILED
                result["_validation_errors"] = "Results failed validation checks"
                
        except Exception as e:
            self.status = NodeStatus.FAILED
            result["_execution_error"] = str(e)
            print(f"Node '{self.name}' execution failed: {str(e)}")
        
        # Update performance metrics
        duration = time.time() - start_time
        self._update_performance_metrics(duration, result)
        
        # Add comprehensive metadata
        result["_node_metadata"] = {
            "node_name": self.name,
            "execution_mode": self.execution_mode.value,
            "status": self.status.value,
            "duration": duration,
            "executed_abilities": self.abilities,
            "quality_score": result.get("_quality_score", 0.0),
            "timestamp": time.time()
        }
        
        self.performance_metrics["total_executions"] += 1
        self.execution_history.append(execution_context)
        
        return result
    
    def _execute_deterministic(self, data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute abilities in deterministic mode with consistent ordering and behavior."""
        print(f"  [DETERMINISTIC] Executing node: {self.name}")
        
        # Sort abilities for consistent execution order
        sorted_abilities = sorted(self.abilities)
        
        for ability in sorted_abilities:
            data = self._execute_ability_with_retry(ability, data, context)
        
        # Add deterministic quality score
        data["_quality_score"] = self._calculate_deterministic_quality(data)
        return data
    
    def _execute_non_deterministic(self, data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute abilities in non-deterministic mode with randomization and creativity."""
        print(f"  [NON-DETERMINISTIC] Executing node: {self.name}")
        
        # Randomize ability execution order
        shuffled_abilities = self.abilities.copy()
        random.shuffle(shuffled_abilities)
        
        # Add some randomness to execution parameters
        context["creativity_factor"] = random.uniform(0.7, 1.3)
        context["exploration_mode"] = True
        
        for ability in shuffled_abilities:
            # Randomly skip some abilities based on context
            if random.random() > 0.9 and len(shuffled_abilities) > 1:
                print(f"    Skipping ability: {ability} (non-deterministic choice)")
                continue
                
            data = self._execute_ability_with_retry(ability, data, context)
        
        # Add non-deterministic quality score with variance
        base_quality = self._calculate_deterministic_quality(data)
        variance = random.uniform(-0.1, 0.1)
        data["_quality_score"] = max(0.0, min(1.0, base_quality + variance))
        
        return data
    
    def _execute_adaptive(self, data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute abilities in adaptive mode, switching between deterministic and non-deterministic based on context."""
        print(f"  [ADAPTIVE] Executing node: {self.name}")
        
        # Determine execution strategy based on data characteristics
        is_critical = data.get("priority", "medium") == "high"
        has_errors = any(key.endswith("_error") for key in data.keys())
        
        if is_critical or has_errors:
            print(f"    Switching to deterministic mode (critical: {is_critical}, errors: {has_errors})")
            return self._execute_deterministic(data, context)
        else:
            print(f"    Using non-deterministic mode for creative flexibility")
            return self._execute_non_deterministic(data, context)
    
    def _execute_ability_with_retry(self, ability: str, data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single ability with retry logic."""
        for attempt in range(self.retry_count):
            try:
                print(f"    Executing ability: {ability} (attempt {attempt + 1})")
                
                # Add execution context to the ability call
                enhanced_data = data.copy()
                enhanced_data["_execution_context"] = context
                
                # Use the correct MCPClient method: call(server_name, ability_name, context)
                ability_result = self.mcp_client.call(self.server_type, ability, enhanced_data)
                
                # Merge results intelligently
                if isinstance(ability_result, dict):
                    data.update(ability_result)
                else:
                    data[f"{ability}_result"] = ability_result
                
                return data
                
            except Exception as e:
                print(f"    Attempt {attempt + 1} failed for ability '{ability}': {str(e)}")
                if attempt == self.retry_count - 1:
                    data[f"{ability}_error"] = str(e)
                    data[f"{ability}_failed_attempts"] = self.retry_count
                else:
                    time.sleep(0.5 * (attempt + 1))  # Exponential backoff
        
        return data
    
    def _validate_results(self, data: Dict[str, Any]) -> bool:
        """Validate execution results using quality threshold and custom rules."""
        # Check quality threshold
        quality_score = data.get("_quality_score", 0.0)
        if quality_score < self.quality_threshold:
            return False
        
        # Apply custom validation rules
        for rule in self.validation_rules:
            try:
                if not rule(data):
                    return False
            except Exception as e:
                print(f"Validation rule failed: {str(e)}")
                return False
        
        return True
    
    def _calculate_deterministic_quality(self, data: Dict[str, Any]) -> float:
        """Calculate a deterministic quality score based on execution success."""
        total_abilities = len(self.abilities)
        if total_abilities == 0:
            return 1.0
        
        successful_abilities = sum(1 for ability in self.abilities 
                                 if f"{ability}_error" not in data)
        
        base_score = successful_abilities / total_abilities
        
        # Bonus for having required fields
        required_fields = ["customer_id", "ticket_id", "status"]
        field_bonus = sum(0.05 for field in required_fields if field in data)
        
        return min(1.0, base_score + field_bonus)
    
    def _update_performance_metrics(self, duration: float, result: Dict[str, Any]):
        """Update node performance metrics."""
        # Update average duration
        total_execs = self.performance_metrics["total_executions"]
        current_avg = self.performance_metrics["average_duration"]
        new_avg = (current_avg * total_execs + duration) / (total_execs + 1)
        self.performance_metrics["average_duration"] = new_avg
        
        # Track quality scores
        quality_score = result.get("_quality_score", 0.0)
        self.performance_metrics["quality_scores"].append(quality_score)
        
        # Keep only last 100 quality scores
        if len(self.performance_metrics["quality_scores"]) > 100:
            self.performance_metrics["quality_scores"] = self.performance_metrics["quality_scores"][-100:]
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get a summary of node performance metrics."""
        quality_scores = self.performance_metrics["quality_scores"]
        return {
            "node_name": self.name,
            "execution_mode": self.execution_mode.value,
            "total_executions": self.performance_metrics["total_executions"],
            "success_rate": (self.performance_metrics["successful_executions"] / 
                           max(1, self.performance_metrics["total_executions"])),
            "average_duration": self.performance_metrics["average_duration"],
            "average_quality": sum(quality_scores) / len(quality_scores) if quality_scores else 0.0,
            "current_status": self.status.value
        }
    
    def reset_performance_metrics(self):
        """Reset performance tracking metrics."""
        self.performance_metrics = {
            "total_executions": 0,
            "successful_executions": 0,
            "average_duration": 0.0,
            "quality_scores": []
        }
        self.execution_history = []
        self.status = NodeStatus.PENDING
    
    def __repr__(self) -> str:
        """String representation of the node."""
        return (f"Node(name='{self.name}', mode={self.execution_mode.value}, "
                f"abilities={self.abilities}, status={self.status.value})")