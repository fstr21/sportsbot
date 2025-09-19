import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi import HTTPException
from mcp.espn.tools import invoke_tool
from mcp.espn.espn_client import shutdown_client


async def main() -> None:
    try:
        await invoke_tool('team_meta', {'teamId': -1, 'season': 2025})
    except HTTPException as exc:
        print('error_status:', exc.status_code)
        print('error_detail:', exc.detail)
    finally:
        await shutdown_client()


if __name__ == '__main__':
    asyncio.run(main())
