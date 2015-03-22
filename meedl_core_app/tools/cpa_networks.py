__author__ = 'PerminovMA@live.ru'


class CPABase():
    LABEL = 'base'
    NAME = 'base'

    @staticmethod
    def add_sub_id(url_str, sub_id):
        """ add SUB_ID_LABEL to link for the introduction of the sub_id
        """
        pass

    @staticmethod
    def sub_id_is_added(url_str):
        """ check added a sub_id to link or not
        """
        pass


class CityAds(CPABase):
    LABEL = 'city_ads'
    NAME = 'city ads'

    @staticmethod
    def add_sub_id(url_str, sub_id):
        # CityAds example url http://cityadspix.com/click-BQDFB17V-ECAQBA4P?bt=25&tl=1&sa={{sub_id}} with sub_id
        return '%s&sa=%s' % (url_str, str(sub_id))

    @staticmethod
    def sub_id_is_added(url_str):
        if 'sa=' in url_str:
            return True
        else:
            return False


CPA_NETWORKS = [CityAds]  # to use the CPA networks you need to put they here