import sublime, sublime_plugin, re
from sublime import Region

# Match all the JavaScript function markers we know about.  Order doesn't
# matter, since they don't overlap when doing re.match.
__js_function_re__ = re.compile(r"""
	# Anonymous function
	(?:
		function \s*	# function
		\( [^\)]* \)	# (params)
	)
	|
	# Anonymous function as propery.
	(?:
		[_$a-zA-Z0-9]+ \s* : \s*	# propertyName :
		function \s*				# function
		\( [^\)]* \)				# (params)
	)
	|
	# Anonymous function as local variable.
	(?:
		var \s+ [_$a-zA-Z0-9]+ \s* = \s*	# var aName =
		function \s*						# function
		\( [^\)]* \)						# (params)
	)
	|
	# Normal named functions
	(?:
		function \s*		# function
		[_$a-zA-Z0-9]+ \s*	# aName
		\( [^\)]* \)		# (params)
	)
""", re.VERBOSE)

__open_brace_re__  = re.compile(r'\s*\{')

# When sel() regions are expanded, they are put on this stack. When we want to
# retract, we just pop them off and set a new selection. We clear this stack
# if we ever notice that the top regions are not covered by the current sel.
__old_regions_stack__ = []

def clear(seq):
	del seq[:]


class JavaScriptTextCommand(sublime_plugin.TextCommand):
	"""Base class for text commands that's only enabled for JavaScript source."""

	def is_enabled(self):
		for region in self.view.sel():
			if self.view.score_selector(region.a, 'source.js'):
				return True
		return False


class ContractSelection(JavaScriptTextCommand):
	""" After expanding selection to a function, contracts the selection back
	to the previous selection.

	Used to undo after selecting too much, or simply to visualize the active
	function scope.

	"""	
	
	def is_enabled(self):
		if not super(ContractSelection, self).is_enabled():
			return False;

		if not __old_regions_stack__:
			return False

		last_regions = __old_regions_stack__[-1]

		# Only works right after expanding. Expect that there are same number
		# the same number of selected regions.
		current_regions = self.view.sel()
		if len(current_regions) != len(last_regions):
			clear(__old_regions_stack__)
			return False

		# ...and that each current selection covers the equivalent old one.
		if not all(current.contains(last) for current, last in zip(current_regions, last_regions)):
			clear(__old_regions_stack__)
			return False

		return True

	def is_visible(self):
		return self.is_enabled()

	def run(self, edit):
		# assumes there are regions already checked by is_enabled
		sel = self.view.sel()
		sel.clear()
		last_regions = __old_regions_stack__.pop();
		for r in last_regions:
			sel.add(r) 


class ExpandSelectionToFunctionJavascript(JavaScriptTextCommand):
	"""Expands the current selection regions to select the current function.
	
	Consecutive calls continue to expand the selection to outer functions.
	Nothing happens if the outermost function is already selected.

	"""

	def find_previous(self, regex, from_point):
		"""Walks backwards from a point until it finds a region that matches
		the given regex.
		
		Attempts to find the longest match possible. So while "oobar:
		function()" may be a match, this will continue walking backwards until
		it can no longer match, since "foobar: function()" is preferred.
		
		"""
		a, b = from_point - 1, self.view.size()

		last_match = None

		while a > -1:
			text = self.view.substr(sublime.Region(a, b))
			match = regex.match(text)

			if match:
				# A match, but will still check if there is a longer one.
				last_match = match
			elif last_match:
				# No longer a match, so go back to the last match instead.
				a += 1
				break

			a -= 1

		if not last_match:
			return None
		else:
			return sublime.Region(a, a + len(last_match.group(0)))

	def find_balanced_braces(self, start_point):
		"""Returns a region that includes the next balanced set of parens after or from start_point."""

		# Next char is expected to be a {
		m = __open_brace_re__.match(self.view.substr(Region(start_point, self.view.size())))
		if not m:
			return None
		else:
			braces_start = start_point + len(m.group(0))

		# Inside the first bracket, we are at depth 1.
		# Increase and decrease the depth based on { and }. Once at depth 0, we're balanced
		depth = 1

		for i in xrange(braces_start + 1, self.view.size()):
			char = self.view.substr(i)

			# Short-circuit the scope check for "comment' since I assume it's
			# relatively slow compared to the strcmp.
			if char == '{' and not self.view.score_selector(i, 'comment'):
				depth += 1
			elif char == '}' and not self.view.score_selector(i, 'comment'):
				depth -= 1
				if depth == 0:
					return sublime.Region(braces_start, i + 1)
					
		# end of file. Fail
		return None			


	def expand_to_function(self, original_region):
		"""Returns a new, expanded region to cover the closest function that encloses the given region.
		
		If there is no enclosing region, the original region is returned.
		
		"""
		search_back_from_point = original_region.begin()

		while search_back_from_point > 0:
			function_start_region = self.find_previous(__js_function_re__, search_back_from_point)
			# The region is the beginning of the function, like: function spam(). Does not include function body.
			if not function_start_region:
				break
		
			brace_region = self.find_balanced_braces(function_start_region.end())
			if not brace_region:
				break

			if not self.view.substr(function_start_region).startswith('function'):
				# This is an assigned, anonymous function. Get the trailing , or ; if present
				after_brace = sublime.Region(brace_region.end(), self.view.size())
				m = re.match(r'\s*[,;]', self.view.substr(after_brace))
				if m:
					# If we matched a , or ; after the }, then add it (plus whitespace)
					# to our "brace" region
					old = brace_region
					brace_region = sublime.Region(old.begin(), old.end() + len(m.group()))

			total_region = function_start_region.cover(brace_region)

			if total_region.end() <= original_region.begin():
				# Oops, went too high. Must be no enclosing function here.
				# Move to before the current function and try again for a "more outer" function.
				search_back_from_point = function_start_region.begin()
				continue

			else:
				return total_region

		# Nothing. Give up and retain current selection.
		return original_region

	def run(self, edit):
		sel = self.view.sel()

		new_regions = [self.expand_to_function(region) for region in sel]

		# Don't add to the stack if the selection didn't change.
		if all(old == new for old, new in zip(sel, new_regions)): return

		# Make a modifiable copy of the the old regions
		old_regions = [r for r in sel]
		__old_regions_stack__.append(old_regions)
		sel.clear()
		for region in new_regions:
			sel.add(region)
			

