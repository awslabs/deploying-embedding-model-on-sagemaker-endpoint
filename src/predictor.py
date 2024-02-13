import flask
from sentence_transformers import SentenceTransformer
import json

# The flask app for serving predictions
app = flask.Flask(__name__)
EMBEDDING_MODEL_NAME = 'intfloat/multilingual-e5-large'


class EmbeddingService(object):
    model = None  # Where we keep the model when it's loaded

    @classmethod
    def get_model(cls):
        """Get the model object for this instance, loading it if it's not already loaded."""
        if cls.model == None:
            cls.model = SentenceTransformer(EMBEDDING_MODEL_NAME)
        return cls.model

    @classmethod
    def predict(cls, input):
        model = cls.get_model()
        return model.encode(input, normalize_embeddings=True)


@app.route("/ping", methods=["GET"])
def ping():
    response_body = "OK"
    status = 200

    return flask.Response(response=f"{response_body}\n", status=status, mimetype="application/json")


@app.route("/invocations", methods=["POST"])
def transformation():
    # The Message Body passed through POST /invocations can be received as follows:
    request_body = flask.request.data.decode("utf-8")
    print(">>>>>>>>>>>>", request_body)

    embedding_result = EmbeddingService.predict(request_body)

    json_response = {
        "status": 200,
        "vectors": embedding_result.tolist(),
    }
    print(">>>>>>>>>>>>", request_body, json_response)
    return flask.jsonify(json_response)


if __name__ == '__main__':
    # ⚠️ For the sake of testing convenience, this 'debug=True' settings have been configured.
    # It is recommended to include guidance suggesting disabling debug mode when deploying in a real production environment.
    app.run('127.0.0.1', port=5001, debug=True)
