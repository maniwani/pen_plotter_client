import asyncio

from pyaxidraw import axidraw
import socketio


def plot(svg: str):
    # connect to plotter
    ad = axidraw.AxiDraw()

    # plot the svg
    ad.plot_setup(svg)
    # TODO: enable this for the demo, probably easier to see on camera
    ad.options.auto_rotate = True
    ad.options.speed_pendown = 40
    # ad.options.speed_penup = 75
    ad.plot_run()

    # turn off the motors
    ad.plot_setup()
    ad.options.mode = "manual"
    ad.options.manual_cmd = "disable_xy"
    ad.plot_run()


sio = socketio.AsyncClient()


@sio.event
async def connect():
    print("Connected!")
    await sio.emit("join", {"room": "plotter"})


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
    uri = "<insert url here>"

    # connect to server
    await sio.connect(uri)

    # wait forever
    await sio.wait()


if __name__ == "__main__":
    asyncio.run(main())
