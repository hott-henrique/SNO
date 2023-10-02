import datetime as dt

import flask

import pymongo.results

import connector


bp = flask.Blueprint("news", __name__, url_prefix="/news")

@bp.route("/", methods=[ "POST" ])
def create_news():
    if not flask.request.is_json:
        return flask.abort(415, "Expected a JSON object.")

    doc_in: dict = flask.request.get_json()

    db = connector.get_news_db()

    try:
        doc = dict(title=doc_in["title"],
                   content=doc_in["content"],
                   author=doc_in["author"],
                   timestamp=doc_in["timestamp"],
                   categories=doc_in["categories"],
                   link=doc_in["link"])

        r: pymongo.results.InsertOneResult = db.rawCollection.insert_one(doc)

        return flask.jsonify(id=str(r.inserted_id))
    except Exception as e:
        print(f"[{dt.datetime.now().strftime('%H:%M - %d/%m/%Y')}] {doc_in} {e.__class__} {e}", file=connector.get_log_file())
        return flask.abort(406)

@bp.route("/", methods=[ "GET" ])
def read_news():
    return flask.abort(501)

