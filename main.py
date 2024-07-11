print("Importing modules...", end="")
import generateMove as gm
import requests as req
import asyncio
import pathlib
print("Done")
events = 2

with open(str(pathlib.Path(__file__).parent.resolve())+"\\TOKEN.txt", "r") as f: TOKEN = f.read()

async def getStreamEvents(): global events; events = req.get("https://lichess.org/api/stream/event", headers={"Authorization": f"Bearer {TOKEN}"})

async def main():
    event = asyncio.Event()
    asyncio.create_task(getStreamEvents())
    print("Getting events...")
    while True:
        print(events)

asyncio.run(main())