# Render MCP Server Setup for Qoder

This configuration allows you to use natural language commands to manage your Render services directly from Qoder IDE.

## Configuration Details

The configuration file (`render-mcp-config.json`) contains:

```json
{
  "servers": {
    "render": {
      "url": "https://mcp.render.com/mcp",
      "headers": {
        "Authorization": "Bearer rnd_x1Vs24RRntFU1i4HhWJAgMAXoWdN"
      },
      "name": "Render MCP Server"
    }
  }
}
```

## How to Use in Qoder

1. Locate your Qoder MCP configuration directory (typically in your user settings folder)
2. Add the Render server configuration from this file to your Qoder MCP settings
3. Restart Qoder if necessary

## Example Commands

Once configured, you can use natural language commands such as:

- "List all my Render services"
- "Show me the deployment logs for my Ramzas Chillas app"
- "Check the status of my database"
- "Deploy the latest version of my application"
- "Scale my web service to 2 instances"

## Security Note

Keep this configuration file secure as it contains your Render API key.