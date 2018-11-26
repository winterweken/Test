def tolist(TypeCheck):
	if hasattr(TypeCheck,'__iter__'): return TypeCheck
	else : return [TypeCheck]
walls = UnwrapElement(tolist(IN[0]))

OUT = [getattr(w, 'CurtainGrid', None) is not None for w in walls]
