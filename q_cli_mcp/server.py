#!/usr/bin/env python3
"""
Simple Q CLI MCP Server using FastMCP with synchronous functions
"""

import subprocess
import logging
import sys
import os

# Import MCP FastMCP
from mcp.server.fastmcp import FastMCP

# Configure logging to stderr
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger("q-cli-mcp-server")

# Create FastMCP server
mcp = FastMCP("Q CLI MCP Server")

def execute_q_command_sync(args: list[str]) -> dict:
    """Execute a Q CLI command synchronously and return the result"""
    try:
        # Build the command properly: q chat <prompt> --flags
        cmd = ["q"] + args
        
        # For chat commands, add non-interactive flags at the end
        if "chat" in args:
            if "--no-interactive" not in cmd:
                cmd.append("--no-interactive")
            if "--trust-all-tools" not in cmd:
                cmd.append("--trust-all-tools")
        
        logger.info(f"Executing command: {' '.join(cmd)}")
        logger.info("Starting subprocess...")
        
        # Execute with environment variables and stdin closed
        env = os.environ.copy()
        env["PYTHONUNBUFFERED"] = "1"
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=10,  # 10 second timeout
            env=env,
            stdin=subprocess.DEVNULL  # Close stdin to prevent blocking
        )
        
        logger.info(f"Subprocess completed with return code: {result.returncode}")
        logger.info(f"Stdout: {result.stdout}")
        logger.info(f"Stderr: {result.stderr}")
        
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
            "command": ' '.join(cmd)
        }
        
    except subprocess.TimeoutExpired:
        logger.error("Command timed out")
        return {
            "success": False,
            "stdout": "",
            "stderr": "Command timed out after 1 minute",
            "returncode": -1,
            "command": ' '.join(cmd)
        }
    except Exception as e:
        logger.error(f"Error executing command: {e}")
        return {
            "success": False,
            "stdout": "",
            "stderr": str(e),
            "returncode": -1,
            "command": ' '.join(cmd)
        }

@mcp.tool()
def q_chat(prompt: str) -> dict:  # Changed return type to dict
    """Execute Q CLI chat command to interact with AI assistant"""
    logger.info(f"q_chat called with prompt: {prompt}")
    
    logger.info("Calling execute_q_command_sync...")
    result = execute_q_command_sync(["chat", prompt])
    logger.info(f"execute_q_command_sync returned: {result}")
    
    response_text = f"Output:\n{result['stdout']}"
    if result['stderr']:
        response_text += f"\n\nErrors:\n{result['stderr']}"
    
    logger.info(f"Returning response: {response_text}")
    return {"content": [{"type": "text", "text": response_text}]}  # Return proper MCP response format

@mcp.tool()
def q_whoami() -> str:
    """Get current Q CLI user information"""
    logger.info("q_whoami called")
    
    result = execute_q_command_sync(["whoami"])
    
    return f"User information:\n{result['stdout']}"

@mcp.tool()
def q_diagnostic() -> str:
    """Run Q CLI diagnostic tests"""
    logger.info("q_diagnostic called")
    
    result = execute_q_command_sync(["diagnostic"])
    
    return f"Diagnostic results:\n{result['stdout']}"

def main():
    """Main function to run the MCP server"""
    logger.info("Starting Simple Q CLI MCP Server with FastMCP")
    
    # Run the server using stdio
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
