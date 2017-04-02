

from mesh import Mesh
from vertex import Vertex
from commons import logger


class Placer:
    """High level interface for the Mesh class.

    End-user can be totally abstracted from the Mesh and Vertex concepts.

    """

    def __init__(self, width:int, height:int):
        self.mesh = Mesh(width, height)

    def add(self, obj:object, x:int, y:int):
        self.mesh.add()
