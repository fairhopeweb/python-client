from steamship.plugin.service import PluginResponse, PluginRequest
from steamship.plugin.embedder import Embedder, EmbedResponse, EmbedRequest
from steamship.app import App, post, create_lambda_handler
from typing import List

FEATURES = ["employee", "roses", "run", "bike", "ted", "grace", "violets", "sugar", "sweet", "cake",
            "flour", "chocolate", "vanilla", "flavors", "flavor", "can", "armadillo", "pizza",
            "ship", "run", "jerry", "ronaldo", "ted", "brenda", "susan", "sam", "jerry", "shoe",
            "cheese", "water", "drink", "glass", "egg", "sleep", "code", "jonathan", "dolphin", "apple",
            "orange", "number", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15",
            "16", "17", "bad", "terrible", "average", "good"]

DIMENSIONALITY = len(FEATURES)

def embed(s: str) -> List[float]:
    s = s.lower()
    return list(map(lambda word: 1.0 if word in s else 0.0, FEATURES))

class TestEmbedderPlugin(Embedder, App):
    def run(self, request: PluginRequest[EmbedRequest]) -> PluginResponse[EmbedResponse]:
        embeddings = list(map(lambda s: embed(s), request.data.docs))
        return PluginResponse(EmbedResponse(embeddings=embeddings))

    @post('do_import')
    def do_import(self, request: dict) -> dict:
        embedRequest = self.__class__.parse_request(request)
        embedResponse = self.run(embedRequest)
        return self.__class__.response_to_dict(embedResponse)

handler = create_lambda_handler(TestEmbedderPlugin)
