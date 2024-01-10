import flask
from fast_sentence_transformers import FastSentenceTransformer as SentenceTransformer
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
    app.run('0.0.0.0', port=5001, debug=True)
