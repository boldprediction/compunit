from models.request import Request


class Experiment:

    def __init__(self, inputs):
        req = Request(**inputs)
        for contrast in req.contrasts:
            print(contrast.name)

    def run(self):
        print("running")
