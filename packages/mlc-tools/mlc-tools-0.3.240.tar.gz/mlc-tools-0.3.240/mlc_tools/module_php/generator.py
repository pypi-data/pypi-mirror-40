from ..base.generator import GeneratorBase
from ..base.generator_visitor import GeneratorVisitor
from .generator_data_storage import GeneratorDataStorage
from .generator_factory import GeneratorFactory
from .generator_observer import GeneratorObserver


class Generator(GeneratorBase):

    def __init__(self):
        GeneratorBase.__init__(self)

    def generate(self, model, writer):
        GeneratorBase.generate(self, model, writer)
        GeneratorDataStorage().generate(model)
        GeneratorVisitor().generate(model, False)
        GeneratorFactory().generate(model, writer)
        GeneratorObserver().generate(writer)
