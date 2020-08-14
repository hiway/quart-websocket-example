import asyncio
import pytest


@pytest.fixture
def app():
    from app import app

    return app


@pytest.mark.asyncio
async def test_websocket(app):
    test_client = app.test_client()
    async with test_client.websocket("/") as websocket:
        await websocket.send("hello")
        result = await websocket.receive()
        assert result == "hello"
