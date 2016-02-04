from grammar import Grammar
from parser_toolkit import augment_grammar, recursion
from context_free_grammar import Context_Free_Grammar
from copy import deepcopy



class slr():
	
	def __init__(self):
	
		self.augmented_grammar = augment_grammar(Grammar())
		self.parsing_table = {}
		self.grammars = [self.augmented_grammar]

	

	def generate_goto(self):
		
		goto_table = {}

		for symbol in list(self.augmented_grammar.terminal) + list(self.augmented_grammar.non_terminal):
			goto_table[symbol] = [None]
		
		for grammar in self.grammars:
			for symbol in list(grammar.non_terminal) + list(grammar.terminal):
				
				next_grammar = self.goto(grammar, symbol)
				if next_grammar.production != {}:
					print self.grammars.index(grammar), symbol, next_grammar
					
					if next_grammar not in self.grammars:
						self.grammars.append(next_grammar)
						for key in goto_table:
							goto_table[key].append(None)
					print self.grammars.index(next_grammar)
					raw_input()
					
					goto_table[symbol][self.grammars.index(grammar)] = self.grammars.index(next_grammar)
		
		print goto_table
		print len(self.grammars)
	

	def goto(self, grammar, symbol):
	
		new_grammar = Context_Free_Grammar() 

		for LHS in grammar.production:
			for production in grammar.production[LHS]:
				
				index = production.index('.') + 1
				if index < len(production) and production[index] == symbol:
					
					index += 1
					if index < len(production) and production[index] in self.augmented_grammar.non_terminal:
						new_grammar = self.track(grammar, new_grammar, production[index])
	
					new_production = deepcopy(production)
					new_production.insert(new_production.index('.') + 1, new_production.pop(new_production.index('.')))
					new_grammar.add_production_rule(LHS, new_production)
					
					for a_symbol in list(set([LHS] + production)):
						new_grammar = self.set_symbol(new_grammar, a_symbol)

		return new_grammar
	

	def track(self, grammar, new_grammar, LHS):
	

		for production in self.augmented_grammar.production[LHS]:
			new_grammar.add_production_rule(LHS, deepcopy(production))
			
			for symbol in list(set([LHS] + production)):
				new_grammar = self.set_symbol(new_grammar, symbol)
	
			index = production.index('.') + 1
			if index < len(production) and production[index] in self.augmented_grammar.non_terminal and production[index] not in new_grammar.production.keys():##
				new_grammar = self.track(grammar, new_grammar, production[index])
		
		return new_grammar	
		

	def set_symbol(self, grammar, symbol):
		
		if symbol in self.augmented_grammar.terminal:
			grammar.add_terminal(symbol)
		elif symbol in self.augmented_grammar.non_terminal:
			grammar.add_non_terminal(symbol)

		return grammar

a = slr()
a.generate_goto()
