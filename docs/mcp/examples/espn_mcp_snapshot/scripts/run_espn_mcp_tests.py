import asyncio
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from mcp.espn.tools import invoke_tool
from mcp.espn.espn_client import shutdown_client


async def run_tests() -> Dict[str, Any]:
    timestamp = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
    output_dir = Path('testing') / 'results' / f'espn_mcp_{timestamp}'
    output_dir.mkdir(parents=True, exist_ok=True)

    test_matrix = [
        ('team_meta', {'teamId': 22, 'season': 2024}),
        ('team_season_stats', {'teamId': 22, 'season': 2024}),
        ('team_recent_games', {'teamId': 22, 'season': 2024, 'gameLimit': 3}),
        ('team_recent_players', {'teamId': 22, 'season': 2024, 'gameLimit': 3}),
    ]

    results: Dict[str, Any] = {}

    for tool_name, params in test_matrix:
        payload = await invoke_tool(tool_name, params)
        results[tool_name] = payload
        output_path = output_dir / f'{tool_name}.json'
        output_path.write_text(json.dumps(payload, indent=2), encoding='utf-8')

    summary_path = output_dir / 'summary.json'
    summary_path.write_text(json.dumps({
        'timestamp': timestamp,
        'tests': [
            {
                'tool': name,
                'params': params,
                'output_path': f'{name}.json'
            }
            for (name, params) in test_matrix
        ]
    }, indent=2), encoding='utf-8')

    return {
        'timestamp': timestamp,
        'output_dir': output_dir.as_posix(),
        'results': results,
    }


def dump_headings(payload: Dict[str, Any]) -> Dict[str, Any]:
    data = payload.get('data')
    if isinstance(data, list):
        return {'count': len(data)}
    if isinstance(data, dict):
        keys = sorted(list(data.keys()))
        return {'keys': keys[:10], 'total_keys': len(keys)}
    return {'type': type(data).__name__}


async def main() -> None:
    run_info = await run_tests()
    notes = {}
    for tool_name, payload in run_info['results'].items():
        notes[tool_name] = dump_headings(payload)
    notes_path = Path(run_info['output_dir']) / 'quick_notes.json'
    notes_path.write_text(json.dumps(notes, indent=2), encoding='utf-8')

    print('ESPN MCP test run saved to', run_info['output_dir'])

    await shutdown_client()


if __name__ == '__main__':
    asyncio.run(main())
