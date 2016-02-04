from copy import deepcopy


class Context_Free_Grammar:
		
	def __init__(self):
		
		# Initating context-free-grammar G = (N, T, P, S)
		self.non_terminal = set()
		self.terminal = set()
		self.production = {}
		self.start_symbol = None
	
	
	def __str__(self):
		
		output = 'Context Free Grammar\n\n'

		output += "Non Terminals: " + str(self.non_terminal) + '\n'
		output += "Terminals: " + str(self.terminal) + '\n'
		output += "\nProduction Rules:" + '\n'

		for LHS in self.production:
			for RHS in self.production[LHS]:
				output += LHS + ' -> ' + ' '.join(RHS) + '\n'
		
		if self.start_symbol:
			output += "\nStart Symbol: " + self.start_symbol + '\n'
		
		return output
	
	def __eq__(self, grammar):
		
		non_terminal_match = self.non_terminal == grammar.non_terminal
		terminal_match = self.terminal == grammar.terminal
		production_match = self.production == grammar.production
		start_symbol_match = self.start_symbol == grammar.start_symbol

		if non_terminal_match and terminal_match and production_match and start_symbol_match:
			return True
		else:
			return False

	def add_non_terminal(self, *A):
		
		for non_terminal in A:
			self.non_terminal.add(non_terminal)


	def add_terminal(self, *a):
		
		for terminal in a:
			self.terminal.add(terminal)


	def add_production_rule(self, LHS, *productions):
		
		for rule in productions:
			
			# Add new production if necessary
			if LHS not in self.production.keys():
				self.production[LHS] = []
			
			for production in productions:
				if production not in self.production[LHS]:
					self.production[LHS].append(production)


	def set_start_symbol(self, S):
		
		self.start_symbol = S
	
	
	def left_recursion(self):
		
		for non_terminal in deepcopy(self.production):
			
			if non_terminal == self.production[non_terminal][0][0]:
				self.production[non_terminal + '\''] = [ self.production[non_terminal][0][1:] + [non_terminal + '\''] , [''] ]
				self.add_non_terminal(non_terminal + '\'')
				self.production[non_terminal].pop(0)
				for production in self.production[non_terminal]:
					production.append(non_terminal + '\'')


	def left_factoring(self):
		
		for non_terminal in deepcopy(self.production):
			
			# Add new production rule in case left factoring
			new_non_terminal = non_terminal + '"'
			self.production[new_non_terminal] = [[]]
			
			# Checking left factoring and updating productions accordingly
			for left_strings in zip(*self.production[non_terminal]):
				if len(left_strings) > 1 and len(set(left_strings)) == 1:
					self.production[new_non_terminal][0].append(left_strings[0])
					for rule in self.production[non_terminal]:
						rule.pop(0)
				else:
					break
			
			# Delete the new production rule if no left factoring
			if self.production[new_non_terminal] == [[]]:
				del self.production[new_non_terminal]

