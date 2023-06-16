import asyncio

from pyaxidraw import axidraw
import socketio


def plot(svg: str):
    # connect to plotter
    ad = axidraw.AxiDraw()

    # plot the svg
    ad.plot_setup(svg)
    ad.options.auto_rotate = False
    ad.options.speed_pendown = 40
    # ad.options.speed_penup = 75
    ad.plot_run()

    # turn off the motors
    ad.plot_setup()
    ad.options.mode = "manual"
    ad.options.manual_cmd = "disable_xy"
    ad.plot_run()


sio = socketio.AsyncClient()

num = 0


@sio.event
async def connect():
    global num
    print("Connected!")
    await sio.emit("join", {f"room": "plotter"})


@sio.event
async def connect_error(data):
    print("Connection failed!")


@sio.event
async def disconnect():
    print("Disconnected!")


@sio.on("plot")
async def on_plot(data):
    print("Received: ")
    print(data["svg"])
    plot(data["svg"])


async def main():
    global num
    uri = input("Please enter the URL (e.g. https://plotter.offkaiexpo.com): ")
    num = input("Please enter the number on this pen plotter: ")

    # connect to server
    await sio.connect(uri)

    # wait forever
    await sio.wait()


if __name__ == "__main__":
    asyncio.run(main())
