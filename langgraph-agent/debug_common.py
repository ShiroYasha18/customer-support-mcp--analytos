#!/usr/bin/env python3

import sys
import os

# Add project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

print(f"Project root: {project_root}")
print(f"Python path: {sys.path[:3]}")

try:
    from servers.common import get_server, CommonServerAbilities
    print("✅ Successfully imported common server modules")
    
    # Test direct instantiation
    direct_server = CommonServerAbilities()
    print(f"✅ Direct server created: {type(direct_server)}")
    print(f"✅ Direct server has execute_ability: {hasattr(direct_server, 'execute_ability')}")
    
    # Test via get_server function
    server = get_server()
    print(f"✅ Server from get_server(): {type(server)}")
    print(f"✅ Server has execute_ability: {hasattr(server, 'execute_ability')}")
    
    # Test the execute_ability method
    if hasattr(server, 'execute_ability'):
        print("\n🔍 Testing execute_ability method:")
        test_data = {"test": "data"}
        
        # Test with a known method
        try:
            result = server.execute_ability('validate_input', test_data)
            print(f"✅ execute_ability('validate_input') worked: {result}")
        except Exception as e:
            print(f"❌ execute_ability('validate_input') failed: {e}")
    else:
        print("❌ execute_ability method not found")
        print(f"Available methods: {[method for method in dir(server) if not method.startswith('_')]}")
        
except ImportError as e:
    print(f"❌ Import failed: {e}")
except Exception as e:
    print(f"❌ Unexpected error: {e}")