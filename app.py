# app.py
from flask import Flask, request, abort, Response
from database import MapRepository
from renderer import WmsRenderer


app = Flask(__name__)

map_repository = MapRepository()
wms_renderer = WmsRenderer(map_repository)


@app.route("/<mapname>")
def wms_service(mapname):
    try:
        query_string = request.query_string.decode("utf-8")
        image_bytes, content_type = wms_renderer.render(mapname, query_string)

        return Response(image_bytes, content_type=content_type)

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        abort(500, description="Internal Server Error")


if __name__ == "__main__":
    app.run(port=3007, debug=True)
