from copy import deepcopy, copy


class Transaction:
    """
    """
    state = None

    def commit(self, obj, deep=True):
        """

        :param obj:
        :param deep:
        :return:
        """
        self.state = copy(obj)
        if deep:
            self.state = deepcopy(obj)

    def rollback(self):
        """

        :return:
        """
        return self.state
