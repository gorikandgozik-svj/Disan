# Open VIBE VISUAL FORGE on Android or Windows

## Browser-based app (current working delivery)

1. Visit https://vibe-visual-forge-cloud.vercel.app.
2. On Android Chrome/Samsung Internet choose **Install app** or **Add to Home screen** from the browser menu. On Windows Chrome/Edge use the install symbol in the address bar or the browser app menu. Installation UI varies.
3. Use UI Studio to export an interactive HTML file. Use 3D Workshop to export an actual GLB scene. Quality Lab tests color contrast.
4. Project settings are stored **only on that device**; they are not synchronized to other devices. Export files to transfer work. Offline PWA caching begins only after a successful load.

## ChatGPT plugin

The personal VIBE VISUAL FORGE plugin is linked to the hosted HTTPS MCP endpoint in `mcp.json`. Host-level installation/activation on mobile is not controlled by this source code. If the account plugin page still says **Unavailable**, use the web app while checking whether the ChatGPT client permits this plugin type. The public source repository does not automatically install the plugin.

## Desktop advanced mode (optional)

Install Python 3.11+ and the package requirements, and configure `mcp.local.json` inside a compatible desktop client for optional Blender recipes, local screenshots and file-based tools. This desktop add-on is not necessary for the cross-device PWA.

## 24/7 claim

The cloud frontend and MCP respond while the hosting service is available. They do not execute user projects continuously, and uptime is not guaranteed. A background autonomous build service requires a durable queue, database and worker service which is not implemented.
