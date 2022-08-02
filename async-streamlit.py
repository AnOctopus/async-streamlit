from collections.abc import Awaitable
import streamlit
import streamlit as st
import asyncio
import concurrent
import time


def async_write(value):
    loop: asyncio.AbstractEventLoop = asyncio.new_event_loop()
    loop.set_debug(True)
    print("creating empty dg")
    dg = st.empty()
    print("created empty dg")
    # task = loop.create_task(_async_write(dg, value))
    pool = concurrent.futures.ThreadPoolExecutor()

    ctx = streamlit.scriptrunner.script_runner.get_script_run_ctx()

    def r():
        streamlit.scriptrunner.script_runner.add_script_run_ctx(None, ctx)
        return asyncio.run(_async_write(dg, value))

    return loop.run_in_executor(pool, r)


async def _async_write(dg, value: Awaitable):
    print("awaiting value in _async_write")
    v = await value
    print("done waiting for value in _async_write")
    dg.write(v)
    print("called write on dg")


async def test_fn():
    await asyncio.sleep(5)
    return "async write"


st.write("sync write")
async_write(test_fn())

time.sleep(6)
