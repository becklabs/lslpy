from .derived import _Constant, _Boolean, _Natural, _Integer, _Real, _String, _Any
from .primitives import _Function, _List, _Tuple, _OneOf, _AllOf

Constant = _Constant(None)

Boolean = _Boolean()
Natural = _Natural()
Integer = _Integer()
Real = _Real()
String = _String()
Any = _Any()

Callable = _Function()
List = _List(Any)
Tuple = _Tuple()
OneOf = _OneOf()
AllOf = _AllOf()

