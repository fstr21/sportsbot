Traceback (most recent call last):
  File "/app/.venv/bin/uvicorn", line 7, in <module>
    sys.exit(main())
             ~~~~^^
  File "/app/.venv/lib/python3.13/site-packages/click/core.py", line 1462, in __call__
    return self.main(*args, **kwargs)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/app/.venv/lib/python3.13/site-packages/click/core.py", line 1383, in main
    rv = self.invoke(ctx)
  File "/app/.venv/lib/python3.13/site-packages/click/core.py", line 1246, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/app/.venv/lib/python3.13/site-packages/click/core.py", line 814, in invoke
    return callback(*args, **kwargs)
  File "/app/.venv/lib/python3.13/site-packages/uvicorn/main.py", line 410, in main
    run(
    ~~~^
        app,
        ^^^^
    ...<45 lines>...
        h11_max_incomplete_event_size=h11_max_incomplete_event_size,
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/app/.venv/lib/python3.13/site-packages/uvicorn/main.py", line 577, in run
    server.run()
    ~~~~~~~~~~^^
  File "/app/.venv/lib/python3.13/site-packages/uvicorn/server.py", line 65, in run
    return asyncio.run(self.serve(sockets=sockets))
           ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/mise/installs/python/3.13.7/lib/python3.13/asyncio/runners.py", line 195, in run
    return runner.run(main)
           ~~~~~~~~~~^^^^^^
  File "/mise/installs/python/3.13.7/lib/python3.13/asyncio/runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
  File "uvloop/loop.pyx", line 1518, in uvloop.loop.Loop.run_until_complete
  File "/app/.venv/lib/python3.13/site-packages/uvicorn/server.py", line 69, in serve
    await self._serve(sockets)
  File "/app/.venv/lib/python3.13/site-packages/uvicorn/server.py", line 76, in _serve
    config.load()
    ~~~~~~~~~~~^^
  File "/app/.venv/lib/python3.13/site-packages/uvicorn/config.py", line 434, in load
    self.loaded_app = import_from_string(self.app)
                      ~~~~~~~~~~~~~~~~~~^^^^^^^^^^
  File "/app/.venv/lib/python3.13/site-packages/uvicorn/importer.py", line 22, in import_from_string
    raise exc from None
  File "/app/.venv/lib/python3.13/site-packages/uvicorn/importer.py", line 19, in import_from_string
    module = importlib.import_module(module_str)
  File "/mise/installs/python/3.13.7/lib/python3.13/importlib/__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1310, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1310, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1324, in _find_and_load_unlocked
ModuleNotFoundError: No module named 'mcp'
Traceback (most recent call last):
  File "/app/.venv/bin/uvicorn", line 7, in <module>
    sys.exit(main())
             ~~~~^^
  File "/app/.venv/lib/python3.13/site-packages/click/core.py", line 1462, in __call__
    return self.main(*args, **kwargs)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/app/.venv/lib/python3.13/site-packages/click/core.py", line 1383, in main
    rv = self.invoke(ctx)
  File "/app/.venv/lib/python3.13/site-packages/click/core.py", line 1246, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/app/.venv/lib/python3.13/site-packages/click/core.py", line 814, in invoke
    return callback(*args, **kwargs)
  File "/app/.venv/lib/python3.13/site-packages/uvicorn/main.py", line 410, in main
    run(
    ~~~^
        app,
        ^^^^
    ...<45 lines>...
        h11_max_incomplete_event_size=h11_max_incomplete_event_size,
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/app/.venv/lib/python3.13/site-packages/uvicorn/main.py", line 577, in run
    server.run()
    ~~~~~~~~~~^^
  File "/app/.venv/lib/python3.13/site-packages/uvicorn/server.py", line 65, in run
    return asyncio.run(self.serve(sockets=sockets))
           ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/mise/installs/python/3.13.7/lib/python3.13/asyncio/runners.py", line 195, in run
    return runner.run(main)
           ~~~~~~~~~~^^^^^^
  File "/mise/installs/python/3.13.7/lib/python3.13/asyncio/runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
  File "uvloop/loop.pyx", line 1518, in uvloop.loop.Loop.run_until_complete
  File "/app/.venv/lib/python3.13/site-packages/uvicorn/server.py", line 69, in serve
    await self._serve(sockets)
  File "/app/.venv/lib/python3.13/site-packages/uvicorn/server.py", line 76, in _serve
    config.load()
    ~~~~~~~~~~~^^
  File "/app/.venv/lib/python3.13/site-packages/uvicorn/config.py", line 434, in load
    self.loaded_app = import_from_string(self.app)
                      ~~~~~~~~~~~~~~~~~~^^^^^^^^^^
  File "/app/.venv/lib/python3.13/site-packages/uvicorn/importer.py", line 22, in import_from_string
    raise exc from None
  File "/app/.venv/lib/python3.13/site-packages/uvicorn/importer.py", line 19, in import_from_string
    module = importlib.import_module(module_str)
  File "/mise/installs/python/3.13.7/lib/python3.13/importlib/__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1310, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1310, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1324, in _find_and_load_unlocked
ModuleNotFoundError: No module named 'mcp'
Traceback (most recent call last):
  File "/app/.venv/bin/uvicorn", line 7, in <module>
    sys.exit(main())
             ~~~~^^
  File "/app/.venv/lib/python3.13/site-packages/click/core.py", line 1462, in __call__
    return self.main(*args, **kwargs)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^