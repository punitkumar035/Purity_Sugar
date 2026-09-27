"""
server.py
Purity for Sugar — Server Entry Point
Listens on http://localhost:8765

Usage:
    python server.py
"""

import uvicorn

if __name__ == "__main__":
    print("Starting Purity for Sugar Calculation Server on http://localhost:8765 ...")
    uvicorn.run("server.app:app", host="0.0.0.0", port=8765, log_level="info")
