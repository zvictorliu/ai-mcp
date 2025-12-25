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
mcp.add_tool(tools.get_file_info, name='get_file_info', description='Get file metadata including size, creation time, modification time, permissions, etc.')
mcp.add_tool(tools.read_file_head, name='read_file_head', description='Read the first N lines of a file (default 20 lines).')
mcp.add_tool(tools.read_file_tail, name='read_file_tail', description='Read the last N lines of a file (default 20 lines).')
mcp.add_tool(tools.search_in_file, name='search_in_file', description='Search for a pattern in a file using regular expressions. Returns matching lines with line numbers.')
mcp.add_tool(tools.count_lines, name='count_lines', description='Count lines, words, and characters in a file.')
mcp.add_tool(tools.read_file_range, name='read_file_range', description='Read a specific range of lines from a file (1-indexed line numbers).')
mcp.add_tool(tools.glob_files, name='glob_files', description='Find files using glob patterns (e.g., "*.py", "**/*.md", "src/**/*.py"). Search can be limited to a specific subdirectory.')

def main():
    transport = os.getenv("MCP_TRANSPORT", "stdio") # stdio/sse/streamable-http
    mcp.run(transport)
    # sse 协议传输时，url 路径要加上 /sse
    # http 协议传输时，url 路径要加上 /mcp

if __name__ == "__main__":
    main()
