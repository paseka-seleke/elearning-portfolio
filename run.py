"""
Convenience entry point so you can press Run in PyCharm.

In PyCharm Community:
  1. Right click run.py  ->  Run 'run'
  2. Open http://127.0.0.1:8000

Or from the terminal:
  uvicorn app.main:app --reload
"""
import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
