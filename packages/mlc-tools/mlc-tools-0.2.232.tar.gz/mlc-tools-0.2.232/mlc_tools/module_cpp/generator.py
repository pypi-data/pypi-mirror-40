from ..base.generator import GeneratorBase
from .generator_data_storage import GeneratorDataStorage
from ..base.generator_visitor import GeneratorVisitor
from .generator_predefined_files import GeneratorPredefinedFiles
from .generator_operator_equals import GeneratorOperatorEquals
from .generator_observer import GeneratorObserver


class Generator(GeneratorBase):

    def __init__(self):
        GeneratorBase.__init__(self)

    def generate(self, model, writer):
        GeneratorBase.generate(self, model, writer)
        GeneratorDataStorage().generate(model)
        GeneratorVisitor().generate(model, True)
        GeneratorPredefinedFiles().generate(model, writer)
        GeneratorOperatorEquals().generate(model)
        GeneratorObserver().generate(writer)
