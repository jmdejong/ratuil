

from ..bufferedscreen import BufferedScreen
from .ansiterm import DrawBackend as SimpleBackend


class DrawBackend(SimpleBackend):
	
	def create_screen(self, *args, **kwargs):
		return BufferedScreen(*args, **kwargs)
