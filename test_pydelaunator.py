

import pytest
from pydelaunator import Mesh, Edge, Face, Vertex


@pytest.fixture
def mesh():
    return Mesh(100, 100)


def test_object_corvering(mesh):
    face = mesh.object_covering(10, 10)
    assert isinstance(face, Face)

    edge = mesh.object_covering(50, 50)
    assert isinstance(edge, Edge)

    vrtx = mesh.object_covering(0, 0)
    assert isinstance(vrtx, Vertex)


def test_mesh(mesh):
    assert len(mesh.edges) == 12
    assert len(mesh.corners) == 4
    assert len(mesh.vertices) == 4
    assert mesh.vertices == mesh.corners
    added = mesh.add('object', 50, 50)
    assert mesh.vertices != mesh.corners
    assert len(mesh.vertices) == 5
    assert added in mesh.vertices
    assert added not in mesh.corners
    added = mesh.remove(added)
    assert len(mesh.edges) == 12
    assert len(mesh.corners) == 4
    assert len(mesh.vertices) == 4
    # from pprint import pprint
    # for edge in mesh.edges:
        # print(str(edge).ljust(10), '->', str(edge.next_left_edge))
    # assert False


def test_neighbors(mesh):
    for vertex in mesh.vertices:
        nb_nei = len(tuple(vertex.direct_neighbors))
        assert nb_nei == 3
        assert nb_nei == len(set(vertex.direct_neighbors))


def test_neighbors_more(mesh):
    added_vertex = mesh.add('object', 50, 50)
    assert len(tuple(added_vertex.direct_neighbors)) == 4
    for vertex in mesh.vertices:
        nb_nei = len(tuple(vertex.direct_neighbors))
        assert nb_nei in {3, 4}
        assert nb_nei == len(set(vertex.direct_neighbors))
