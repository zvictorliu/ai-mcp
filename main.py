from mcp.server.fastmcp import FastMCP
import tools
import os
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()
MCP_PORT = os.getenv("MCP_PORT")

mcp = FastMCP('gici-lib mcp', host='0.0.0.0', port=MCP_PORT)
mcp.add_tool(tools.list_directory, name='list_directory', description='List files and directories in the knowledge base root directory.')
mcp.add_tool(tools.list_directory_recursive, name='list_directory_recursive', description='Recursively list all files and directories in a specified path within the knowledge base root directory.')
mcp.add_tool(tools.read_file, name='read_file', description='Read the content of a specified file within the knowledge base root directory.')

def main():
    transport = os.getenv("MCP_TRANSPORT", "stdio") # stdio/sse/streamable-http
    mcp.run(transport)
    # sse 协议传输时，url 路径要加上 /sse
    # http 协议传输时，url 路径要加上 /mcp

if __name__ == "__main__":
    main()
