from context_free_grammar import Context_Free_Grammar


def Grammar():
	
	grammar = Context_Free_Grammar()
	
	grammar.add_terminal('a', 'b', 'c', '~', ':', 'author', 'title')
	grammar.add_non_terminal('Text', 'Effect', 'Alpha')
	grammar.set_start_symbol('Text')
	
	grammar.add_production_rule('Text', ['~', 'Effect', ':', 'Text', '~'], ['Alpha'])
	grammar.add_production_rule('Effect', ['author'], ['title'])
	grammar.add_production_rule('Alpha', ['a'], ['b'])
	#grammar.add_production_rule('F', ['(', 'E', ')'], ['id'])
	
	return grammar

