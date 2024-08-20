from entidades import Mesh
import numpy as np


class BSPNode:
    def __init__(self, partition=None, front=None, back=None, objects=None):
        self.partition = partition  # Plano de partição
        self.front = front  # Subárvore de objetos à frente do plano
        self.back = back  # Subárvore de objetos atrás do plano
        self.objects = (
            objects if objects is not None else []
        )  # Objetos contidos neste nó


def is_in_front_triangle(triangle, partition_plane):
    # Verifica se todos os vértices do triângulo estão à frente do plano
    return all(
        np.dot(
            (vertex - partition_plane.vertices[triangle.vertices.index(vertex)]),
            partition_plane.triangle_normals[0],
        )
        > 0
        for vertex in triangle.vertices
    )


def is_behind_triangle(triangle, partition_plane):
    # Verifica se todos os vértices do triângulo estão atrás do plano
    return all(
        np.dot(
            (vertex - partition_plane.vertices[triangle.vertices.index(vertex)]),
            partition_plane.triangle_normals[0],
        )
        < 0
        for vertex in triangle.vertices
    )


def split_triangle(triangle, partition_plane):
    front_vertices = []
    back_vertices = []

    for i in range(3):
        start_vertex = triangle.vertices[i]
        end_vertex = triangle.vertices[(i + 1) % 3]

        start_dist = np.dot(
            (start_vertex - partition_plane.vertices[i]),
            partition_plane.triangle_normals[0],
        )
        end_dist = np.dot(
            (end_vertex - partition_plane.vertices[i]),
            partition_plane.triangle_normals[0],
        )

        if start_dist >= 0:
            front_vertices.append(start_vertex)
        else:
            back_vertices.append(start_vertex)

        if start_dist * end_dist < 0:  # A linha cruza o plano
            intersection_point = intersect_plane_line(
                partition_plane, i, start_vertex, end_vertex
            )
            front_vertices.append(intersection_point)
            back_vertices.append(intersection_point)

    # Criar novos triângulos a partir dos vértices divididos
    if len(front_vertices) >= 3:
        front_triangle = Mesh(
            triangle_quantity=1,
            vertices_quantity=3,
            vertices=front_vertices[:3],
            triangle_tuple_vertices=[(0, 1, 2)],
            triangle_normals=[triangle.triangle_normals[0]],
            vertex_normals=[],
            color=triangle.color,
        )
    else:
        front_triangle = None

    if len(back_vertices) >= 3:
        back_triangle = Mesh(
            triangle_quantity=1,
            vertices_quantity=3,
            vertices=back_vertices[:3],
            triangle_tuple_vertices=[(0, 1, 2)],
            triangle_normals=[triangle.triangle_normals[0]],
            vertex_normals=[],
            color=triangle.color,
        )
    else:
        back_triangle = None

    return front_triangle, back_triangle


def intersect_plane_line(plane, partition_plane_vertices_index, start, end):
    direction = end - start
    denominator = np.dot(plane.triangle_normals[0], direction)

    if abs(denominator) < 1e-6:  # Linha paralela ao plano
        return None

    t = (
        np.dot(
            (plane.vertices[partition_plane_vertices_index] - start),
            plane.triangle_normals[0],
        )
        / denominator
    )

    intersection_point = start + direction.__mul_escalar__(t)

    return intersection_point


def build_bsp(objects):
    if not objects:
        return None

    partition = objects[0]  # Select a polygon P from the list.
    front_list = []
    back_list = []

    for obj in objects[1:]:
        if is_in_front_triangle(
            obj, partition
        ):  # If that polygon is wholly in front of the plane containing P, move that polygon to the list of nodes in front of P.
            front_list.append(obj)
        elif is_behind_triangle(
            obj, partition
        ):  # If that polygon is wholly behind the plane containing P, move that polygon to the list of nodes behind P.
            back_list.append(obj)
        else:  # If that polygon is intersected by the plane containing P, split it into two polygons and move them to the respective lists of polygons behind and in front of P.
            front_split, back_split = split_triangle(obj, partition)
            if front_split:
                front_list.append(front_split)
            if back_split:
                back_list.append(back_split)

    front_node = build_bsp(
        front_list
    )  # Apply this algorithm to the list of polygons in front of P.
    back_node = build_bsp(
        back_list
    )  # Apply this algorithm to the list of polygons behind P.

    return BSPNode(
        partition=partition, front=front_node, back=back_node
    )  # Return a node containing P, the node returned from the first recursive call, and the node returned from the second recursive call.


def print_bsp_tree(node, depth=0):
    if node is None:
        return

    indent = "  " * depth
    print(f"{indent}Partition: color = {node.partition.color}")
    print(f"{indent}Objects: {len(node.objects)} objects")

    if node.front is not None:
        print(f"{indent}Front:")
        print_bsp_tree(node.front, depth + 1)
    else:
        print(f"{indent}Front: None")

    if node.back is not None:
        print(f"{indent}Back:")
        print_bsp_tree(node.back, depth + 1)
    else:
        print(f"{indent}Back: None")
