import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from mcp.espn.tools import invoke_tool
from mcp.espn.espn_client import shutdown_client


async def main() -> None:
    payload = await invoke_tool('team_recent_games', {'teamId': 22, 'season': 2025, 'gameLimit': 12})
    print('params:', payload['params'])
    print('game_count:', len(payload['data']))
    await shutdown_client()


if __name__ == '__main__':
    asyncio.run(main())
