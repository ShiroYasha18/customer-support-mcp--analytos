#!/usr/bin/env python3
"""
Main entry point for the LangGraph Agent.
This module loads the graph configuration, initializes state with an input payload,
and executes all stages in sequence for customer support workflows.
"""

import json
import yaml
from pathlib import Path
from typing import Dict, Any
import logging
from datetime import datetime

from core.node import Node
from core.mcp_client import get_mcp_client

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class LangGraphAgent:
    """Main agent class that runs the customer support workflow."""
    
    def __init__(self, config_path: str = "graph_config.yaml"):
        """Initialize the agent with configuration."""
        self.config_path = config_path
        self.config = self._load_config()
        self.mcp_client = get_mcp_client()
        self.nodes = self._initialize_nodes()
        self.state = {}
        
        logger.info(f"🚀 LangGraph Agent initialized with {len(self.nodes)} stages")
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        try:
            with open(self.config_path, 'r') as f:
                config = yaml.safe_load(f)
                logger.info(f"📋 Configuration loaded from {self.config_path}")
                return config
        except FileNotFoundError:
            logger.error(f"❌ Configuration file {self.config_path} not found")
            raise
    
    def _initialize_nodes(self) -> Dict[str, Node]:
        """Initialize nodes based on configuration."""
        nodes = {}
        stages = self.config.get('stages', [])
        
        for stage_config in stages:
            stage_name = stage_config['name']
            # Import ExecutionMode and convert mode string to enum
            from core.node import ExecutionMode
            
            mode_str = stage_config.get('mode', 'deterministic')
            if mode_str == 'deterministic':
                execution_mode = ExecutionMode.DETERMINISTIC
            elif mode_str == 'non_deterministic':
                execution_mode = ExecutionMode.NON_DETERMINISTIC
            else:
                execution_mode = ExecutionMode.ADAPTIVE
                
            nodes[stage_name] = Node(
                name=stage_name,
                abilities=stage_config.get('abilities', []),
                mcp_client=self.mcp_client,
                execution_mode=execution_mode,
                server_type=stage_config.get('server', 'common'),
                timeout=stage_config.get('timeout', 30),
                quality_threshold=stage_config.get('quality_threshold', 0.8)
            )
            
        logger.info(f"🔧 Initialized {len(nodes)} workflow nodes")
        return nodes
    
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Run the customer support workflow through all 11 stages."""
        logger.info("🎯 Starting customer support workflow execution")
        
        # Initialize state with input data
        self.state = {
            'workflow_id': f"cs_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'start_time': datetime.now().isoformat(),
            'current_stage': 0,
            'total_stages': len(self.config.get('stages', [])),
            'stage_results': {},
            'workflow_status': 'running',
            **input_data
        }
        
        logger.info(f"📊 Initial state: {json.dumps({k: v for k, v in self.state.items() if k not in ['workflow_id', 'start_time']}, indent=2)}")
        
        # Execute stages in sequence
        stages = self.config.get('stages', [])
        for i, stage_config in enumerate(stages, 1):
            stage_name = stage_config['name']
            
            if stage_name in self.nodes:
                logger.info(f"\n🔄 [{i}/{len(stages)}] Executing stage: {stage_name.upper()}")
                logger.info(f"📝 Mode: {stage_config.get('mode', 'deterministic')}")
                logger.info(f"🎯 Abilities: {', '.join(stage_config.get('abilities', []))}")
                logger.info(f"🖥️  Server: {stage_config.get('server', 'common')}")
                
                # Update current stage in state
                self.state['current_stage'] = i
                self.state['current_stage_name'] = stage_name
                
                # Execute the node
                try:
                    stage_start_time = datetime.now()
                    self.state = self.nodes[stage_name].execute(self.state)
                    stage_end_time = datetime.now()
                    
                    # Record stage execution details
                    self.state['stage_results'][stage_name] = {
                        'status': 'completed',
                        'start_time': stage_start_time.isoformat(),
                        'end_time': stage_end_time.isoformat(),
                        'duration_ms': int((stage_end_time - stage_start_time).total_seconds() * 1000)
                    }
                    
                    logger.info(f"✅ Stage {stage_name} completed successfully")
                    
                except Exception as e:
                    logger.error(f"❌ Stage {stage_name} failed: {str(e)}")
                    self.state['error'] = f"Stage {stage_name} failed: {str(e)}"
                    self.state['workflow_status'] = 'failed'
                    self.state['failed_stage'] = stage_name
                    
                    # Record failed stage details
                    self.state['stage_results'][stage_name] = {
                        'status': 'failed',
                        'error': str(e),
                        'start_time': datetime.now().isoformat()
                    }
                    break
            else:
                logger.warning(f"⚠️  Stage '{stage_name}' not found in nodes")
                self.state['workflow_status'] = 'failed'
                self.state['error'] = f"Stage '{stage_name}' not found in nodes"
                break
        
        # Finalize state
        self.state['end_time'] = datetime.now().isoformat()
        if 'error' not in self.state:
            self.state['workflow_status'] = 'completed'
        
        # Calculate total workflow duration
        start_time = datetime.fromisoformat(self.state['start_time'])
        end_time = datetime.fromisoformat(self.state['end_time'])
        self.state['total_duration_ms'] = int((end_time - start_time).total_seconds() * 1000)
        
        logger.info(f"\n🏁 Workflow completed with status: {self.state['workflow_status'].upper()}")
        logger.info(f"⏱️  Total duration: {self.state['total_duration_ms']}ms")
        logger.info(f"📋 Final structured payload:")
        
        return self.state
    
    def get_workflow_summary(self) -> Dict[str, Any]:
        """Get a summary of the workflow execution."""
        if not self.state:
            return {'error': 'No workflow has been executed yet'}
        
        summary = {
            'workflow_id': self.state.get('workflow_id'),
            'status': self.state.get('workflow_status'),
            'total_stages': self.state.get('total_stages'),
            'completed_stages': len([r for r in self.state.get('stage_results', {}).values() if r.get('status') == 'completed']),
            'total_duration_ms': self.state.get('total_duration_ms'),
            'customer_info': {
                'name': self.state.get('customer', {}).get('name'),
                'email': self.state.get('customer', {}).get('email'),
                'tier': self.state.get('customer', {}).get('tier')
            },
            'case_info': {
                'case_id': self.state.get('case_id'),
                'priority': self.state.get('priority'),
                'category': self.state.get('category')
            }
        }
        
        if self.state.get('error'):
            summary['error'] = self.state['error']
            summary['failed_stage'] = self.state.get('failed_stage')
        
        return summary


def main():
    """Main function to run the customer support agent demo."""
    print("🏗️  LangGraph Agent - Customer Support Workflow Demo")
    print("=" * 55)
    
    try:
        # Load demo input
        with open('demo_input.json', 'r') as f:
            demo_input = json.load(f)
            
        logger.info(f"📥 Demo input loaded: {demo_input.get('customer', {}).get('name', 'Unknown')} - {demo_input.get('query', 'No query')}")
        
        # Initialize and run agent
        agent = LangGraphAgent()
        result = agent.run(demo_input)
        
        print("\n" + "=" * 55)
        print("📋 WORKFLOW SUMMARY:")
        print("=" * 55)
        summary = agent.get_workflow_summary()
        print(json.dumps(summary, indent=2, default=str))
        
        print("\n" + "=" * 55)
        print("📋 FINAL STRUCTURED PAYLOAD:")
        print("=" * 55)
        print(json.dumps(result, indent=2, default=str))
        
    except FileNotFoundError as e:
        logger.error(f"❌ Required file not found: {e}")
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        raise


if __name__ == "__main__":
    main()