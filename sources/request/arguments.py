

# TODO: Redundant class. Remove it.
class VDOM_request_arguments:
    def __init__(self, args):
        self.__arguments = args

    def arguments(self, args=None):
        if args:
            self.__arguments = args

        return self.__arguments
