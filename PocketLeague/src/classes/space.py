import pymunk


class Space:

    __collision_func: None
    space: pymunk.Space = pymunk.Space()

    id = 1

    def init(function_on_collision):
        Space.__collision_func = function_on_collision

    def add_mapping(id, player):
        handler = Space.space.add_collision_handler(id, 0)  # 0 -> Ball.collision_type
        handler.post_solve = Space.__collision_func
        handler.data["player"] = player

    def get_and_incr_id():
        n = Space.id
        Space.id += 1
        return n
    
    def reset():
        Space.id = 1
        Space.space = pymunk.Space()
        Space.__collision_func = None
