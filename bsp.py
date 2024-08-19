class BSPNode:
    def __init__(self, partition=None, front=None, back=None, objects=None):
        self.partition = partition  # Plano de partição
        self.front = front  # Subárvore de objetos à frente do plano
        self.back = back  # Subárvore de objetos atrás do plano
        self.objects = (
            objects if objects is not None else []
        )  # Objetos contidos neste nó


def is_in_front(obj, partition_plane):
    # Calcula o vetor do ponto do plano até o objeto
    vector = obj.position - partition_plane.point
    # Produto escalar entre o vetor e o normal do plano
    dot_product = vector.dot(partition_plane.normal)
    return dot_product > 0


def is_behind(obj, partition_plane):
    # Calcula o vetor do ponto do plano até o objeto
    vector = obj.position - partition_plane.point
    # Produto escalar entre o vetor e o normal do plano
    dot_product = vector.dot(partition_plane.normal)
    return dot_product < 0


def intersect_plane_line(plane, start, end):
    direction = end - start
    denominator = plane.normal.dot(direction)

    if abs(denominator) < 1e-6:  # Linha paralela ao plano
        return None

    t = (plane.point - start).dot(plane.normal) / denominator
    intersection_point = start + t * direction

    return intersection_point


def split_object(obj, partition_plane):
    front_part = None
    back_part = None

    # Para cada segmento de linha ou polígono no objeto
    for i in range(len(obj.vertices) - 1):
        start_vertex = obj.vertices[i]
        end_vertex = obj.vertices[i + 1]

        # Calcula as distâncias dos vértices ao plano
        start_dist = (start_vertex - partition_plane.point).dot(partition_plane.normal)
        end_dist = (end_vertex - partition_plane.point).dot(partition_plane.normal)

        if start_dist > 0 and end_dist > 0:
            # Ambos os vértices estão na frente
            if front_part is None:
                front_part = obj.copy()
            front_part.add_segment(start_vertex, end_vertex)

        elif start_dist < 0 and end_dist < 0:
            # Ambos os vértices estão atrás
            if back_part is None:
                back_part = obj.copy()
            back_part.add_segment(start_vertex, end_vertex)

        else:
            # A linha cruza o plano
            intersection_point = intersect_plane_line(
                partition_plane, start_vertex, end_vertex
            )

            if start_dist > 0:
                if front_part is None:
                    front_part = obj.copy()
                front_part.add_segment(start_vertex, intersection_point)

                if back_part is None:
                    back_part = obj.copy()
                back_part.add_segment(intersection_point, end_vertex)

            else:
                if back_part is None:
                    back_part = obj.copy()
                back_part.add_segment(start_vertex, intersection_point)

                if front_part is None:
                    front_part = obj.copy()
                front_part.add_segment(intersection_point, end_vertex)

    return front_part, back_part


def render_bsp(node, camera, targets):
    if node is None:
        return

    # Verifica se o nó atual está à frente ou atrás da câmera
    if is_in_front(camera.position, node.partition):
        # Primeiro renderiza o subárvore de trás
        render_bsp(node.back, camera, targets)
        # Renderiza o objeto atual
        render_node(node, camera, targets)
        # Depois renderiza o subárvore da frente
        render_bsp(node.front, camera, targets)
    else:
        # Primeiro renderiza o subárvore da frente
        render_bsp(node.front, camera, targets)
        # Renderiza o objeto atual
        render_node(node, camera, targets)
        # Depois renderiza o subárvore de trás
        render_bsp(node.back, camera, targets)


def render_node(node, camera, targets):
    # Renderiza os objetos deste nó
    for obj in node.objects:
        # Lógica para renderizar usando ray casting
        pass


def build_bsp(objects):
    if not objects:
        return None

    partition = objects[0]  # Select a polygon P from the list.
    front_list = []
    back_list = []

    for obj in objects[1:]:
        if is_in_front(
            obj, partition
        ):  # If that polygon is wholly in front of the plane containing P, move that polygon to the list of nodes in front of P.
            front_list.append(obj)
        elif is_behind(
            obj, partition
        ):  # If that polygon is wholly behind the plane containing P, move that polygon to the list of nodes behind P.
            back_list.append(obj)
        else:  # If that polygon is intersected by the plane containing P, split it into two polygons and move them to the respective lists of polygons behind and in front of P.
            front_split, back_split = split_object(obj, partition)
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
