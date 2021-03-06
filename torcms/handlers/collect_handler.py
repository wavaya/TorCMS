# -*- coding:utf-8 -*-

'''
For User collection
'''

import json
import tornado.web

from torcms.core.base_handler import BaseHandler
from torcms.core import tools
from torcms.model.collect_model import MCollect
from torcms.core.tools import logger
from config import CMS_CFG


class CollectHandler(BaseHandler):
    def initialize(self, **kwargs):
        super(CollectHandler, self).initialize()

    def get(self, *args):
        url_str = args[0]
        if len(url_str) > 0:
            url_arr = self.parse_url(url_str)
        else:
            return False

        if url_str == 'list':
            self.list(url_str)
        elif len(url_arr) == 2:
            self.list(url_arr[0], url_arr[1])
        elif len(url_arr) == 1 and (len(url_str) == 4 or len(url_str) == 5):
            if self.get_current_user():
                self.add_or_update(url_str)
            else:
                self.set_status(403)
                return False

    @tornado.web.authenticated
    def add_or_update(self, app_id):
        logger.info('Collect info: user-{0}, uid-{1}'.format(self.userinfo.uid, app_id))
        MCollect.add_or_update(self.userinfo.uid, app_id)
        out_dic = {'success': True}
        return json.dump(out_dic, self)

    @tornado.web.authenticated
    def list(self, list, cur_p=''):
        if cur_p == '':
            current_page_num = 1
        else:
            current_page_num = int(cur_p)

        current_page_num = 1 if current_page_num < 1 else current_page_num

        num_of_cat = MCollect.count_of_user(self.userinfo.uid)
        page_num = int(num_of_cat / CMS_CFG['list_num']) + 1

        kwd = {
            'current_page': current_page_num}

        self.render('misc/collect/list.html',
                    recs_collect=MCollect.query_pager_by_all(self.userinfo.uid,
                                                             current_page_num).naive(),
                    pager=tools.gen_pager_purecss('/collect/{0}'.format(list),
                                                  page_num,
                                                  current_page_num),
                    userinfo=self.userinfo,

                    cfg=CMS_CFG,
                    kwd=kwd)
