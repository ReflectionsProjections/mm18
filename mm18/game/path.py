from collections import deque
import itertools

## @file path.py

class Path(object):
	def __init__(self, path):
		self.path = path
		self.waiting = deque()
		self.moving = deque([None for _ in path])

	## Queue a unit at the entrance.
	#  If not other units are waiting it will start moving
	#  the next time advance is called
	#  @param unit unit to enqueue
	def start(self, unit):
		self.waiting.append(unit)

	## Advance every unit a step, and starts first waiting unit.
	#  @return The unit that reached the base if any, or None
	def advance(self):
		if len(self.waiting) > 0:
			self.moving.append(self.waiting.popleft())
		else:
			self.moving.append(None)
		return self.moving.popleft()

	## An iterator over positions along the path, producing
	#  tuple of the unit or None and the position.
	#  Generate entries from the base outward
	def entries(self):
		return itertools.izip(self.moving, self.path)
