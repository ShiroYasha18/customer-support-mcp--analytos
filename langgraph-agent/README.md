# LangGraph Agent - Customer Support Workflow

A sophisticated multi-stage customer support workflow system built with LangGraph, featuring deterministic and non-deterministic execution modes, comprehensive logging, and external system integration through MCP (Model Context Protocol) servers.

## 🏗️ Architecture Overview

This project implements an 11-stage customer support workflow that processes customer requests through a series of intelligent nodes, each with specialized abilities for handling different aspects of customer support operations.

### Core Components

- **Agent (`agent.py`)**: Main orchestrator that manages workflow execution
- **Nodes (`core/node.py`)**: Individual processing units with execution modes
- **MCP Client (`core/mcp_client.py`)**: Dispatcher for routing requests to appropriate servers
- **Common Server (`servers/common.py`)**: Internal customer support abilities
- **Atlas Server (`servers/atlas.py`)**: External-facing integration abilities
- **Configuration (`graph_config.yaml`)**: Workflow stage definitions and settings

## 🚀 Quick Start

### Prerequisites

```bash
python -m pip install pyyaml
```

### Running the Workflow

```bash
python agent.py
```

This will process the sample data in `demo_input.json` through all 11 workflow stages.

## 📋 Workflow Stages

1. **Accept Payload** - Initial request validation and normalization
2. **Validate Input** - Comprehensive data validation and enrichment
3. **Categorize Request** - Intelligent request classification
4. **Calculate SLA Risk** - SLA compliance assessment
5. **Assess Priority** - Dynamic priority calculation
6. **Draft Response** - Personalized response generation
7. **Suggest Actions** - Action plan recommendations
8. **Assign Agent** - Skill-based agent assignment
9. **Set Escalation Path** - Escalation route determination
10. **Finalize State** - State consolidation and metrics
11. **Send Notifications** - Multi-channel notification delivery

## 🎯 Cursor IDE Integration

### Project-Level Cursor Prompts

**Main Project Prompt:**