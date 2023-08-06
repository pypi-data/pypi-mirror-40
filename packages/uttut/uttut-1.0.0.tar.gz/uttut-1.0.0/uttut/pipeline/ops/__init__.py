from .int_token import IntToken
from .float_token import FloatToken
from .int_token_with_space import IntTokenWithSpace
from .float_token_with_space import FloatTokenWithSpace
from .merge_whitespace_characters import MergeWhiteSpaceCharacters
from .strip_whitespace_characters import StripWhiteSpaceCharacters

from .char_tokenizer import CharTokenizer
from .eng_tokenizer import EngTokenizer
from .zh_char_tokenizer import ZhCharTokenizer

from .add_sos_eos import AddSosEos
from .pad import Pad
from .token_to_index import Token2Index

from .factory import OperatorFactory


op_factory = OperatorFactory()

# string -> string
op_factory.register(IntToken.__name__, IntToken)
op_factory.register(FloatToken.__name__, FloatToken)
op_factory.register(IntTokenWithSpace.__name__, IntTokenWithSpace)
op_factory.register(FloatTokenWithSpace.__name__, FloatTokenWithSpace)
op_factory.register(MergeWhiteSpaceCharacters.__name__, MergeWhiteSpaceCharacters)
op_factory.register(StripWhiteSpaceCharacters.__name__, StripWhiteSpaceCharacters)

# string -> tokens
op_factory.register(CharTokenizer.__name__, CharTokenizer)
op_factory.register(EngTokenizer.__name__, EngTokenizer)
op_factory.register(ZhCharTokenizer.__name__, ZhCharTokenizer)

# tokens -> tokens
op_factory.register(AddSosEos.__name__, AddSosEos)
op_factory.register(Pad.__name__, Pad)
op_factory.register(Token2Index.__name__, Token2Index)
