class KalaError(Exception):
    pass


class HttpError(KalaError):

    def __init__(self, response):
        """
        :param :class:`requests.Response` response: HTTP response
        """
        self.status_code = response.status_code
        self.error_message = response.text
        # content = response.json()
        # self.error_message = content["error"]
        super(HttpError, self).__init__(self.__str__())

    def __repr__(self):
        return 'HttpError: HTTP %s returned with message, "%s"' % \
               (self.status_code, self.error_message)

    def __str__(self):
        return self.__repr__()


class NotFoundError(HttpError):
    pass


class InternalServerError(HttpError):
    pass
