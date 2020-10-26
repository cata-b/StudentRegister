class IDExistsError(Exception):
    """
    ID already exists in the list.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class InvalidParametersError(Exception):
    """
    Invalid (type or value) parameters.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class NoMoreStepsError(Exception):
    """
    No more undos/redos.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class NonExistentItemIDError(Exception):
    """
    Item ID does not exist in the list.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)