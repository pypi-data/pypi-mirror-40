from async_generator import yield_, async_generator
import pytest
import aioredis

import birdisle.aioredis


@pytest.fixture
@async_generator
async def server():
    server = birdisle.Server()
    await yield_(server)
    server.close()


@pytest.fixture
@async_generator
async def conn(server):
    conn = await birdisle.aioredis.create_connection(server)
    await yield_(conn)
    conn.close()
    await conn.wait_closed()


@pytest.fixture
@async_generator
async def pool(server):
    pool = await birdisle.aioredis.create_pool(server)
    await yield_(pool)
    pool.close()
    await pool.wait_closed()


@pytest.fixture
@async_generator
async def r(server):
    redis = await birdisle.aioredis.create_redis(server)
    await yield_(redis)
    redis.close()
    await redis.wait_closed()


@pytest.fixture
@async_generator
async def redis_pool(server):
    pool = await birdisle.aioredis.create_redis_pool(server)
    await yield_(pool)
    pool.close()
    await pool.wait_closed()


@pytest.mark.asyncio
async def test_create_connection(conn):
    await conn.execute('set', 'hello', 'create_redis')
    val = await conn.execute('get', 'hello')
    assert val == b'create_redis'


@pytest.mark.asyncio
async def test_create_pool(pool):
    await pool.execute('set', 'hello', 'create_pool')
    val = await pool.execute('get', 'hello')
    assert val == b'create_pool'


@pytest.mark.asyncio
async def test_create_redis(r):
    await r.set('hello', 'world')
    val = await r.get('hello')
    assert val == b'world'


@pytest.mark.asyncio
async def test_pubsub(redis_pool):
    res = await redis_pool.subscribe('chan')
    channel = res[0]
    await redis_pool.publish('chan', 'hello')
    msg = await channel.get()
    assert msg == b'hello'


@pytest.mark.asyncio
async def test_auth(server):
    r1 = await birdisle.aioredis.create_redis(server)
    await r1.config_set('requirepass', 'p@ssword')
    await r1.auth('p@ssword')
    await r1.set('foo', 'bar')
    r1.close()
    await r1.wait_closed()

    with pytest.raises(aioredis.AuthError):
        r2 = await birdisle.aioredis.create_redis(server)
        await r2.get('foo')

    r3 = await birdisle.aioredis.create_redis(server, password='p@ssword')
    assert await r3.get('foo') == b'bar'
