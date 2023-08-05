def test_imports():
    import boundio as bio
    from boundio.asynchronous import raw_io, queues, tasks, utils
    from boundio.asynchronous.raw_io import files, sockets, stdin
    from boundio import asynchronous, examples, sockets, item_codes, stdin
    from boundio.examples import stdin_simple, websocket_simple
    from boundio.sockets import process, tasks, utils
    assert True is True
