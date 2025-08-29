"""
Defines the **MCPClient**, which is the dispatcher between nodes and servers.

Responsibilities:
- Receives ability execution requests from Node
- Routes them to the correct MCP server (Common 🏠 or Atlas 🌍)
- Returns server results back to the Node

How to extend:
- If you add new servers (besides Common/Atlas), update the `call()` method to handle them
"""

import logging
from typing import Dict, Any, Optional
import sys
import os

# Add the project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    # Import using absolute path from project root
    from servers.common import get_server as get_common_server
    from servers.atlas import get_server as get_atlas_server
except ImportError as e:
    logging.error(f"Failed to import server modules: {e}")
    # Fallback for testing
    get_common_server = None
    get_atlas_server = None

logger = logging.getLogger(__name__)

class MCPClient:
    """MCP Client - Dispatcher between nodes and MCP servers"""
    
    def __init__(self):
        """Initialize the MCP client with server connections"""
        self.servers = {}
        self._initialize_servers()
        logger.info("MCPClient initialized successfully")
    
    def _initialize_servers(self):
        """Initialize connections to available MCP servers"""
        try:
            # Initialize Common server (internal abilities)
            if get_common_server:
                self.servers['common'] = get_common_server()
                logger.info("Connected to Common server (internal abilities)")
            else:
                logger.warning("Common server not available")
            
            # Initialize Atlas server (external abilities)
            if get_atlas_server:
                self.servers['atlas'] = get_atlas_server()
                logger.info("Connected to Atlas server (external abilities)")
            else:
                logger.warning("Atlas server not available")
                
        except Exception as e:
            logger.error(f"Error initializing servers: {e}")
    
    def get_available_servers(self) -> Dict[str, Any]:
        """Get information about available servers"""
        server_info = {}
        for name, server in self.servers.items():
            try:
                server_info[name] = {
                    'name': server.name,
                    'description': server.description,
                    'abilities': server.get_abilities()
                }
            except Exception as e:
                logger.error(f"Error getting info for server {name}: {e}")
                server_info[name] = {'error': str(e)}
        
        return server_info
    
    def call(self, server_name: str, ability_name: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Route ability execution request to the appropriate MCP server
        
        Args:
            server_name: Name of the target server ('common' or 'atlas')
            ability_name: Name of the ability to execute
            context: Context data for the ability execution
            
        Returns:
            Dict containing the execution result
        """
        logger.info(f"Routing request: {server_name}.{ability_name}")
        
        # Validate server exists
        if server_name not in self.servers:
            error_msg = f"Server '{server_name}' not found. Available servers: {list(self.servers.keys())}"
            logger.error(error_msg)
            return {
                'success': False,
                'error': error_msg,
                'server': server_name,
                'ability': ability_name
            }
        
        # Get the target server
        server = self.servers[server_name]
        
        try:
            # Execute the ability on the target server
            result = server.execute_ability(ability_name, context)
            
            # Add metadata to the result
            if isinstance(result, dict):
                result['_metadata'] = {
                    'server': server_name,
                    'ability': ability_name,
                    'client': 'MCPClient'
                }
            
            logger.info(f"Successfully executed {server_name}.{ability_name}")
            return result
            
        except Exception as e:
            error_msg = f"Error executing {server_name}.{ability_name}: {str(e)}"
            logger.error(error_msg)
            return {
                'success': False,
                'error': error_msg,
                'server': server_name,
                'ability': ability_name,
                'exception_type': type(e).__name__
            }
    
    def call_common(self, ability_name: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Convenience method to call Common server abilities"""
        return self.call('common', ability_name, context)
    
    def call_atlas(self, ability_name: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Convenience method to call Atlas server abilities"""
        return self.call('atlas', ability_name, context)
    
    def get_server_abilities(self, server_name: str) -> Optional[list]:
        """Get list of abilities for a specific server"""
        if server_name in self.servers:
            try:
                return self.servers[server_name].get_abilities()
            except Exception as e:
                logger.error(f"Error getting abilities for {server_name}: {e}")
                return None
        else:
            logger.warning(f"Server '{server_name}' not found")
            return None
    
    def get_all_abilities(self) -> Dict[str, list]:
        """Get all abilities from all servers"""
        all_abilities = {}
        for server_name in self.servers:
            abilities = self.get_server_abilities(server_name)
            if abilities:
                all_abilities[server_name] = abilities
        return all_abilities
    
    def health_check(self) -> Dict[str, Any]:
        """Check health status of all connected servers"""
        health_status = {
            'client_status': 'healthy',
            'servers': {},
            'total_servers': len(self.servers),
            'healthy_servers': 0
        }
        
        for server_name, server in self.servers.items():
            try:
                # Try to get abilities as a health check
                abilities = server.get_abilities()
                health_status['servers'][server_name] = {
                    'status': 'healthy',
                    'abilities_count': len(abilities)
                }
                health_status['healthy_servers'] += 1
            except Exception as e:
                health_status['servers'][server_name] = {
                    'status': 'unhealthy',
                    'error': str(e)
                }
        
        return health_status
    
    def route_by_ability(self, ability_name: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Automatically route ability to the correct server based on ability name
        
        This method searches all servers for the requested ability and routes accordingly.
        Useful when you don't know which server contains a specific ability.
        """
        logger.info(f"Auto-routing ability: {ability_name}")
        
        # Search for the ability across all servers
        for server_name, server in self.servers.items():
            try:
                abilities = server.get_abilities()
                if ability_name in abilities:
                    logger.info(f"Found {ability_name} in {server_name} server")
                    return self.call(server_name, ability_name, context)
            except Exception as e:
                logger.error(f"Error checking abilities for {server_name}: {e}")
                continue
        
        # Ability not found in any server
        error_msg = f"Ability '{ability_name}' not found in any connected server"
        logger.error(error_msg)
        return {
            'success': False,
            'error': error_msg,
            'ability': ability_name,
            'searched_servers': list(self.servers.keys())
        }

# Global client instance
_mcp_client = None

def get_mcp_client() -> MCPClient:
    """Get the global MCP client instance (singleton pattern)"""
    global _mcp_client
    if _mcp_client is None:
        _mcp_client = MCPClient()
    return _mcp_client

def create_mcp_client() -> MCPClient:
    """Create a new MCP client instance"""
    return MCPClient()

if __name__ == "__main__":
    # Test the MCP client
    client = get_mcp_client()
    
    print("=== MCP Client Health Check ===")
    health = client.health_check()
    print(f"Health Status: {health}")
    
    print("\n=== Available Servers ===")
    servers = client.get_available_servers()
    for name, info in servers.items():
        print(f"{name}: {info}")
    
    print("\n=== All Abilities ===")
    abilities = client.get_all_abilities()
    for server, ability_list in abilities.items():
        print(f"{server}: {ability_list}")
    
    # Test ability routing
    print("\n=== Testing Ability Routing ===")
    test_context = {"test": "data"}
    
    # Test common server call
    if 'common' in client.servers:
        result = client.call_common('validate_input', test_context)
        print(f"Common server test: {result}")
    
    # Test atlas server call
    if 'atlas' in client.servers:
        result = client.call_atlas('extract_entities', test_context)
        print(f"Atlas server test: {result}")
    
    # Test auto-routing
    result = client.route_by_ability('validate_input', test_context)
    print(f"Auto-routing test: {result}")