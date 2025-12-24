from mcp.server.fastmcp import FastMCP
import tools

mcp = FastMCP('gici-lib mcp')
mcp.add_tool(tools.list_directory, name='list_directory', description='List files and directories in the knowledge base root directory.')
mcp.add_tool(tools.list_directory_recursive, name='list_directory_recursive', description='Recursively list all files and directories in a specified path within the knowledge base root directory.')
mcp.add_tool(tools.read_file, name='read_file', description='Read the content of a specified file within the knowledge base root directory.')

def main():
    mcp.run('stdio')


if __name__ == "__main__":
    main()
