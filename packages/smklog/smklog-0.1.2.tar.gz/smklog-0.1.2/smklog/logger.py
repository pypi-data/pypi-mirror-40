import json
import logging
import sys

__all__ = ["SmkLog"]


class SmkLog(object):

    def __init__(self, platform: str, service: str):
        # e.g. youzan, or 'storefront_wechat' etc. for our own platform
        self.platform = platform

        # e.g. nomad_envoy_order or storefront_auth
        self.service = service

        self._logger = get_log("%s_%s" % (self.platform, self.service))

    def info(self,
             source: str,
             category: str,
             label: str,
             message: str,
             data: object,
             user: str,
             store_id: str = None,
             request_id: str = None,
             ) -> str:
        return self._log("info",
                         source, category, label, message, data,
                         user, store_id, request_id
                         )

    def debug(self,
              source: str,
              category: str,
              label: str,
              message: str,
              data: object,
              user: str,
              store_id: str = None,
              request_id: str = None,
              ) -> str:
        return self._log("debug",
                         source, category, label, message, data,
                         user, store_id, request_id
                         )

    def error(self,
              source: str,
              category: str,
              label: str,
              message: str,
              data: object,
              user: str,
              store_id: str = None,
              request_id: str = None,
              ) -> str:
        return self._log("error",
                         source, category, label, message, data,
                         user, store_id, request_id
                         )

    def warn(self,
             source: str,
             category: str,
             label: str,
             message: str,
             data: object,
             user: str,
             store_id: str = None,
             request_id: str = None,
             ) -> str:
        return self._log("warn",
                         source, category, label, message, data,
                         user, store_id, request_id
                         )

    def critical(self,
                 source: str,
                 category: str,
                 label: str,
                 message: str,
                 data: object,
                 user: str,
                 store_id: str = None,
                 request_id: str = None,
                 ) -> str:
        return self._log("critical",
                         source, category, label, message, data,
                         user, store_id, request_id
                         )

    def _log(self,
             log_level: str,
             source: str,
             category: str,
             label: str,
             message: str,
             data: object,
             user: str,
             store_id: str = None,
             request_id: str = None,
             ) -> str:

        msg = self._format_message(source, category, label, message, data,
                                   user, store_id, request_id)

        getattr(self._logger, log_level)(msg)
        return msg

    def _format_message(self,
                        source: str,
                        category: str,
                        label: str,
                        message: str,
                        data: object,
                        user: str,
                        store_id: str,
                        request_id: str,
                        ) -> str:
        if isinstance(data, (list, dict)):
            data = json_dumps_unicode(data)
        else:
            data = str(data)

        msg = {
            "platform": self.platform,
            "service": self.service,

            "source": source,
            "category": category,
            "label": label,
            "message": message,
            "data": data,
            "user": user,
        }
        if store_id:
            msg.update({"store_id": store_id})
        if request_id:
            msg.update({"request_id": request_id})
        return json_dumps_unicode(msg)


def json_dumps_unicode(obj):
    """
    Change Python default json.dumps acting like JavaScript, including allow
    Chinese characters and no space between any keys or values.
    """
    return json.dumps(obj,
                      ensure_ascii=False,
                      separators=(',', ':')
                      )


def get_log(name):
    log = logging.getLogger(name)
    log.setLevel(logging.INFO)

    # ref: https://stackoverflow.com/questions/19561058/duplicate-output-in-simple-python-logging-configuration  # noqa:E501
    log.propagate = False  # stop producing duplicated logs

    if not log.handlers:
        out_handler = logging.StreamHandler(sys.stdout)
        out_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        out_handler.setLevel(logging.INFO)
        log.addHandler(out_handler)

    return log
