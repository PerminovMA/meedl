__author__ = 'PerminovMA@live.ru'
from ua_parser import user_agent_parser


class UserAgentParser:
    # TODO add windows phone
    MOBILE_OS_TYPES = ['ios', 'android']  # mobile types must be lowercase

    def __init__(self, http_user_agent_srt):
        self.parsed_ua = user_agent_parser.Parse(http_user_agent_srt)
        self.os = UserAgentParser.get_os(self.parsed_ua)
        self.device = UserAgentParser.get_device(self.parsed_ua)
        self.browser = UserAgentParser.get_browser(self.parsed_ua)
        self.is_mobile = False

        if self.os and self.os.lower() in UserAgentParser.MOBILE_OS_TYPES:
            self.is_mobile = True


    @staticmethod
    def get_os(parsed_obj):
        try:
            if len(parsed_obj["os"]["family"]) > 0 and parsed_obj["os"]["family"] != "Other":
                return parsed_obj["os"]["family"]
        except KeyError:
            return None
        return None

    @staticmethod
    def get_device(parsed_obj):
        try:
            if len(parsed_obj["device"]["family"]) > 0 and parsed_obj["device"]["family"] != "Other":
                return parsed_obj["device"]["family"]
        except KeyError:
            return None
        return None

    @staticmethod
    def get_browser(parsed_obj):
        try:
            if len(parsed_obj["user_agent"]["family"]) > 0 and parsed_obj["user_agent"]["family"] != "Other":
                return parsed_obj["user_agent"]["family"]
        except KeyError:
            return None
        return None

    def get_data(self):
        return self.device, self.os, self.browser