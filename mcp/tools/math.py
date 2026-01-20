from typing import Any
from server import mcp

@mcp.tool()
def base_conversion(number: int, base: int) -> str:
    '''
    Convert a number to a different base
    '''
    return bin(number)[2:]