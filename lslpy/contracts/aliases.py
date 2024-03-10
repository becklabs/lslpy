from .derived import (_Any, _Boolean, _Constant, _Integer, _Natural, _Real,
                      _String)
from .primitives import _AllOf, _Function, _List, _OneOf, _Tuple

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

