# -*- coding: utf_8 -*-
__author__ = 'PerminovMA@live.ru'

from datetime import datetime


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

    @staticmethod
    def get_data_for_conversion_model(request_obj):
        """
        :return: dict with data replicated Conversion model fields
        example:
            class Conversion(models.Model):
                a = Field1()
                b = Field2()
                c = Field3(null=True)

            this method return: {'a': '...', 'b': '...'}

            nice not about datetime formats https://docs.python.org/2/library/time.html#time.strptime
        """
        pass


class CityAds(CPABase):  # NOT TESTED
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

    @staticmethod
    def get_data_for_conversion_model(request_obj):
        d = {
            "adv_campaign": request_obj.GET.get('subaccount'),  # it's sub_id
            "payout": request_obj.GET.get('payout'),
            "payout_currency": request_obj.GET.get('payout_currency'),
            "conversion_time": request_obj.GET.get('conversion_time'),
            # datetime.strptime("21/11/06 16:30", "%d/%m/%y %H:%M")
            "user_ip": request_obj.GET.get('ip'),
            "user_country": request_obj.GET.get('country'),
            "user_city": request_obj.GET.get('city'),
            "user_browser": request_obj.GET.get('user_browser'),
            "user_os": request_obj.GET.get('user_os'),
            "user_device": request_obj.GET.get('user_device'),
            "status": request_obj.GET.get('status'),
        }

        return d


class AdInfo(CPABase):  # NOT TESTED
    LABEL = 'ad_info'
    NAME = 'ADINFO'

    @staticmethod
    def add_sub_id(url_str, sub_id):
        # AdInfo example url http://superdiski.info/xcopy/VIG?group_id=group01&sub_id=tiz1
        return '%s?sub_id=%s' % (url_str, str(sub_id))

    @staticmethod
    def sub_id_is_added(url_str):
        if 'sub_id=' in url_str:
            return True
        else:
            return False

    @staticmethod
    def get_data_for_conversion_model(request_obj):
        d = {
            "adv_campaign": request_obj.GET.get('sub_id'),  # it's sub_id
            "payout": request_obj.GET.get('commission'),
            "conversion_time": request_obj.GET.get('time'),  # datetime.strptime("21/11/06 16:30", "%d/%m/%y %H:%M")
            "user_ip": request_obj.GET.get('ip'),
            "status": request_obj.GET.get('status'),
        }

        return d


class AdSup(CPABase):
    LABEL = 'ad_sup'
    NAME = 'Ad Sup'

    @staticmethod
    def add_sub_id(url_str, sub_id):
        # AdSup example url http://tracking.adsup.me/aff_c?offer_id=1022&aff_id=9808&aff_sub=123
        return '%s&aff_sub=%s' % (url_str, str(sub_id))

    @staticmethod
    def sub_id_is_added(url_str):
        if 'aff_sub=' in url_str:
            return True
        else:
            return False

    @staticmethod
    def get_data_for_conversion_model(request_obj):
        d = {
            "adv_campaign": request_obj.GET.get('aff_sub'),  # it's sub_id
            "payout": request_obj.GET.get('payout'),
            "payout_currency": request_obj.GET.get('currency'),
            # conversion_time format:   YYYY-MM-DD HH:MM:SS for this cpa network
            "conversion_time": datetime.strptime(request_obj.GET.get('datetime'),
                                                 "%Y-%m-%d %H:%M:%S") if request_obj.GET.get('datetime') else None,
            "user_ip": request_obj.GET.get('ip'),
            "user_os": request_obj.GET.get('device_os'),
            "user_device": request_obj.GET.get('device_brand'),
            "offer_id": request_obj.GET.get('offer_id'),
            "offer_name": request_obj.GET.get('offer_name')
        }

        return d

        # postback example http://meedl.cloudapp.net/core/postback?cpa_network=ad_sup&aff_sub={aff_sub}&ip={ip}
        # &datetime={datetime}&currency={currency}&payout={payout}&device_brand={device_brand}&device_os={device_os}
        # &offer_id={offer_id}&offer_name={offer_name}


class MobiMops(CPABase):
    LABEL = 'mobimops'
    NAME = 'mobimops'

    @staticmethod
    def add_sub_id(url_str, sub_id):
        # MobiMops example url http://r.mobimops.com/X2q?sid1={sid1} with sub_id
        return '%s?sid1=%s' % (url_str, str(sub_id))

    @staticmethod
    def sub_id_is_added(url_str):
        if 'sid1=' in url_str:
            return True
        else:
            return False

    @staticmethod
    def get_data_for_conversion_model(request_obj):
        d = {
            "adv_campaign": request_obj.GET.get('sid1'),  # it's sub_id
            "payout": request_obj.GET.get('payout'),
            "conversion_time": datetime.fromtimestamp(
                float(request_obj.GET.get('time'))) if request_obj.GET.get('time') else None,  # unix timestamp
            "user_ip": request_obj.GET.get('ip'),
            "user_browser": request_obj.GET.get('user_agent'),
            # (1 - ожидает обработки, 2 - подтверждено, 3 - отклонено, 4 - холд, 5 - обработано)
            "status": request_obj.GET.get('status'),
        }

        return d

    # postback example http://meedl.cloudapp.net/core/postback?cpa_network=mobimops&payout={payout}&sid1={sid1}&time={time}&ip={ip}&user_agent={user_agent}&status={status}


CPA_NETWORKS = [CityAds, AdInfo, AdSup, MobiMops]  # to use the CPA networks you need to put they here


def get_cpa_network_out_of_label(cpa_network_label):
    """ :return CPA network class which corresponding cpa_network_label
    """
    if not cpa_network_label:
        return None

    for network in CPA_NETWORKS:
        if cpa_network_label == network.LABEL:
            return network
    return None