#!/bin/bash
# Add Q CLI MCP Server to Q CLI configuration

echo "Adding Q CLI MCP Server to Q CLI..."

# Get the current directory
CURRENT_DIR=$(pwd)

# Add the MCP server to Q CLI using the new package structure
q mcp add q-cli-proxy \
  --command "uvx" \
  --args "--from $CURRENT_DIR q-cli-mcp-server"

echo "MCP server added successfully!"
echo "Verify with: q mcp list"
echo "Check status with: q mcp status --name q-cli-proxy"
