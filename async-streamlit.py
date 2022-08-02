from collections.abc import Awaitable
import streamlit.scriptrunner.script_runner as script_runner
import streamlit as st
import asyncio
import concurrent
import time


def async_write(value):
    dg = st.empty()

    pool = concurrent.futures.ThreadPoolExecutor()
    ctx = script_runner.get_script_run_ctx()

    def r():
        script_runner.add_script_run_ctx(None, ctx)
        return asyncio.run(_async_write(dg, value))

    return pool.submit(r)


async def _async_write(dg, value: Awaitable):
    print("awaiting value in _async_write")
    v = await value
    print("done waiting for value in _async_write")
    dg.write(v)
    print("called write on dg")


async def test_fn():
    await asyncio.sleep(5)
    return "async write"


start = time.time()
st.write("sync write")
async_write(test_fn())
mid = time.time()
st.write(mid - start)
time.sleep(6)
end = time.time()
st.write(end - mid)
