from grammar import Grammar
from parser_toolkit import augment_grammar, follow
from context_free_grammar import Context_Free_Grammar
from copy import deepcopy



class slr():
	
	def __init__(self):
	
		self.augmented_grammar = augment_grammar(Grammar())
		self.parsing_table = {}
		self.grammars = [self.augmented_grammar]

	

	def generate_goto(self):
		
		self.goto_table = {}

		for symbol in list(self.augmented_grammar.terminal) + list(self.augmented_grammar.non_terminal):
			self.goto_table[symbol] = [None]
		
		for grammar in self.grammars:
			for symbol in list(grammar.non_terminal) + list(grammar.terminal):
				
				next_grammar = self.goto(grammar, symbol)
				if next_grammar.production != {}:
					
					if next_grammar not in self.grammars:
						self.grammars.append(next_grammar)
						for key in self.goto_table:
							self.goto_table[key].append(None)
					
					self.goto_table[symbol][self.grammars.index(grammar)] = self.grammars.index(next_grammar)
		
		for non_terminal in self.augmented_grammar.non_terminal:
			self.parsing_table[non_terminal] = self.goto_table[non_terminal]
	

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
	
	
	def generate_shift_reduce(self):
		
		for terminal in list(self.augmented_grammar.terminal) + ['$']:
			self.parsing_table[terminal] = [None] * len(self.grammars)

		for grammar in self.grammars:
			for LHS in grammar.production:
				for production in grammar.production[LHS]:
					index = production.index('.') + 1
					state = self.grammars.index(grammar)
					if index == len(production):
						for symbol in list(set(follow(self.augmented_grammar, LHS))):
							self.parsing_table[symbol][state] = ('R', LHS, self.augmented_grammar.production[LHS].index(['.'] + production[:-1]))
						if LHS == self.augmented_grammar.start_symbol:
							self.parsing_table[symbol][state] = 'Accept'
							
					elif production[index] in self.augmented_grammar.terminal:
						symbol = production[index]
						self.parsing_table[symbol][state] = ('S', self.goto_table[symbol][state])
	
	
	def show_table(self):
		print '\t',
		for key in self.parsing_table:
			print key,'\t',
		print
		print

		for i in range(len(self.grammars)):
			print i,'\t',
			for key in self.parsing_table:
				print self.parsing_table[key][i], '\t',
			print
		

a = slr()
a.generate_goto()
a.generate_shift_reduce()
a.show_table()
