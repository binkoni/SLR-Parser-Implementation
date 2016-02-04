from context_free_grammar import Context_Free_Grammar


def Grammar():
	
	grammar = Context_Free_Grammar()
	
	grammar.add_terminal('+', '*', '(', ')', 'id')
	grammar.add_non_terminal('E', 'T', 'F')
	grammar.set_start_symbol('E')
	
	grammar.add_production_rule('E', ['E', '+', 'T'], ['T'])
	grammar.add_production_rule('T', ['T', '*', 'F'], ['F'])
	grammar.add_production_rule('F', ['(', 'E', ')'], ['id'])
	
	return grammar

