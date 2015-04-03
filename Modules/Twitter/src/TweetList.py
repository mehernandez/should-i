class TweetList(list):

    def append(self, p_object):
        if not self.__contains__(p_object):
            super(self.__class__, self).append(p_object)
            return True
        else:
            False