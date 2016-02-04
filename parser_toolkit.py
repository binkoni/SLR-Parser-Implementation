def recursion(LHS, RHS):
	return LHS in RHS

def first(grammar, symbol, result = []):
	
	if symbol in grammar.terminal:
		result.append(symbol)
		return result
	elif symbol in grammar.non_terminal:
		for production in grammar.production[symbol]:
			if not recursion(symbol, production):
				result += first(grammar, production[0], result)
	else:
		print "not found"
	
	return list(set(result))
	

def follow(grammar, symbol, result = []):
	
	if symbol is grammar.start_symbol:
		result.append('$')

	for LHS in grammar.production:
		for production in grammar.production[LHS]:
			if symbol in production:
				
				follow_index = production.index(symbol) + 1
				if follow_index < len(production):	
					follow_symbol = production[production.index(symbol) + 1]
					if follow_symbol in grammar.terminal:
						result.append(follow_symbol)
						return result
					elif follow_symbol in grammar.non_terminal:
						result += first(grammar, follow_symbol)
				else:
					follow(grammar, LHS)
	
	return list(set(result))


def augment_grammar(grammar):
	
	grammar.add_production_rule(grammar.start_symbol + '\'', [grammar.start_symbol])
	grammar.set_start_symbol(grammar.start_symbol + '\'')
	for LHS in grammar.production:
		for production in grammar.production[LHS]:
			production.insert(0,'.')
	print grammar
	return grammar
