# -*- coding: utf-8 -*-

import copy
import random

from ..log import logger


class RocketBackend(object):
    """
    发送rocket
    """

    def __init__(self, sender_list):
        """
        初始化
        sender_list可以保证只要发送失败就尝试下一个
        """
        self.sender_list = sender_list

    def emit(self, title, content, receiver_list):
        """
        发送
        """

        sender_list = copy.deepcopy(self.sender_list)

        while sender_list:
            random.shuffle(sender_list)

            # 取出最后一个
            params = sender_list.pop()

            try:
                self._sendmail(receiver_list, title, content,
                               username=params['username'], password=params['password'],
                               domain=params['domain']
                               )
                return True
            except:
                logger.error('exc occur. params: %s', params, exc_info=True)
        else:
            # 就是循环完了，也没发送成功
            return False

    def _sendmail(self, receiver_list, subject, content, username, password, domain):
        """
        发送消息
        content_type: plain / html
        """
    	from rocketchat.api import RocketChatAPI
    	
    	api = RocketChatAPI(settings={'username': username, 'password': password, 'domain': domain})	
        full_content = '\n\n'.join([subject, content])
        for group_id in receiver_list:
        	api.send_message('@all', group_id)
        	api.send_message(full_content, group_id)
    	
	
