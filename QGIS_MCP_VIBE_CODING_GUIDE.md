# QGIS MCP & Vibe Coding Guide
## Agent-Driven Spatial Analytics for Garissa DRR

The `GARISSADRM` project utilizes a cutting-edge approach to geographic information systems known as "Vibe Coding," facilitated by the **Google Antigravity IDE** and the **Model Context Protocol (MCP)** via the `qgis_mcp` plugin.

### What is Vibe Coding?
Vibe coding allows the geospatial analyst to abstract away from repetitive syntax generation. Instead of manually clicking through the QGIS GUI or writing boilerplate PyQGIS scripts, the analyst provides high-level natural language directives. The AI agent, communicating with QGIS through the MCP, autonomously generates and executes the necessary Python code.

### The QGIS MCP Architecture
1. **Antigravity IDE**: The environment where you (and the AI agent) operate.
2. **MCP Server**: Translates the LLM's intentions into validated execution commands.
3. **QGIS Plugin (`qgis_mcp`)**: A localized socket server running inside QGIS that receives commands from the MCP Server and executes them against the active map canvas.

### How to use `3_qgis_workspace_builder.py`
Because this script interacts directly with the QGIS visual interface (`QgsProject.instance()`, `QgsLayerTreeGroup`), it **cannot** be run in a standard headless Python terminal unless QGIS libraries are specifically mocked or initialized. 

**Execution Methods:**
1. **Via MCP (Automated):** When chatting with the AI agent inside Antigravity, you can instruct it: *"Agent, please run the workspace builder script in QGIS to organize the layers."* The agent will dispatch the command through the protocol.
2. **Via QGIS Python Console (Manual):**
    - Open QGIS Desktop.
    - Press `Ctrl + Alt + P` to open the Python Console.
    - Click the 'Show Editor' button.
    - Open `3_qgis_workspace_builder.py` and hit Run.

### Benefits for the Garissa El Niño Project
- **Rapid Ingestion:** The AI can quickly write logic to ingest complex data sources (like the remote Boreholes Google Sheet).
- **Automated Structuring:** Adding dozens of risk layers manually is tedious. PyQGIS automation categorizes "At-Risk Infrastructure" under specific logical groups instantly.
- **Dynamic Modeling:** Changing buffer sizes for High/Medium/Low risk can be done via a natural language prompt, instantly updating the underlying Python logic and re-rendering the QGIS map.
