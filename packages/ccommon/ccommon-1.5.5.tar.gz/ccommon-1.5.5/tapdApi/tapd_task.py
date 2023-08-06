#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/15 9:54
# @Author  : chenjw
# @Site    : 
# @File    : tapd_task.py
# @Software: PyCharm Community Edition
# @Desc    :  do what

from urllib.parse import urlencode
from ccommon.httpSimple import HttpSimple
from tapdApi import tapd, tapd_param
import datetime


class TapdTasks(tapd.Tapd):
    def __init__(self, usr, pwd, delay=1000):
        tapd.Tapd.__init__(self, usr, pwd, delay)

    def listTasks(self, workspace_id, id=None, name=None, priority=None, status=None, iteration_id=None, owner=None,
                  cc=None, creator=None,
                  begin=None, due=None, created=None, modified=None, completed=None, effort=None, effort_completed=None,
                  remain=None, exceed=None, progress=None, story_id=None, description=None, limit=None, page=None,
                  order=None, fields=None):
        """
        :param workspace_id:        N       int         项目ID
        :param id:                  O       int         支持多ID查询、模糊匹配
        :param name:                O       str         标题	支持模糊匹配
        :param priority:            O       str         优先级	支持枚举查询
        :param status:              O       str         状态	支持枚举查询
        :param iteration_id:        O       int         迭代
        :param owner:               O       str         当前处理人	支持模糊匹配
        :param cc:                  O       str         抄送人
        :param creator:             O       str         创建人	支持模糊匹配
        :param begin:               O       date        预计开始	支持时间查询
        :param due:                 O       date        预计结束	支持时间查询
        :param created:             O       datetime    创建时间	支持时间查询
        :param modified:            O       datetime    最后修改时间
        :param completed:           O       datetime    完成时间	支持时间查询
        :param effort:              O       str         预估工时
        :param effort_completed:    O       str         完成工时
        :param remain:              O       float       剩余工时
        :param exceed:              O       float       超出工时
        :param progress:            O       int         进度
        :param story_id:            O       int         需求	支持多ID查询
        :param description:         O       str         详细描述
        :param limit:               O       int         设置返回数量限制，默认为30
        :param page:                O       int         返回当前数量限制下第N页的数据，默认为1（第一页）
        :param order:               O       str         排序规则，规则：字段名 ASC或者DESC，然后 urlencode	如按创建时间逆序：order=created%20desc
        :param fields:              O       str         置获取的字段，多个字段间以','逗号隔开
        :return:
        """
        url = 'https://api.tapd.cn/tasks?'
        param = tapd_param.TapdParam()
        param.setValue(workspace_id, int, 'workspace_id', True, {param.Int: {param.gt: 0}})
        param.setValue(id, int, 'id')
        param.setValue(name, str, 'name')
        param.setValue(priority, str, 'priority')
        param.setValue(status, str, 'status')
        param.setValue(iteration_id, int, 'iteration_id')
        param.setValue(owner, str, 'owner')
        param.setValue(cc, str, 'cc')
        param.setValue(creator, str, 'creator')
        param.setValue(begin, datetime.date, 'begin')
        param.setValue(due, datetime.date, 'due')
        param.setValue(effort, str, 'effort')
        param.setValue(effort_completed, str, 'effort_completed')
        param.setValue(remain, float, 'remain')
        param.setValue(exceed, float, 'exceed')
        param.setValue(progress, int, 'progress')
        param.setValue(story_id, int, 'story_id')
        param.setValue(description, str, 'description')
        param.setValue(limit, int, 'limit')
        param.setValue(page, int, 'page')
        param.setValue(order, str, 'order')
        param.setValue(fields, str, 'fields')

        self.wait()
        url = '%s%s' % (url, urlencode(param.data))
        url += self.dateTimeCombine('created', created)
        url += self.dateTimeCombine('modified', modified)
        url += self.dateTimeCombine('completed', completed)
        _json = HttpSimple(url).addMethod(HttpSimple.method_get).addAuth(self.retAuth()).run().retJson()
        self.checkApiStatus(_json)
        if _json.ExistP('data/Task/id'):
            return _json.JsonP('data/Task').Dict
        elif _json.ExistP('data/0/Task/id'):
            return [ain_json.Dict for ain_json in _json.AryJson('data')]
        else:
            return None


if __name__ == '__main__':
    pass
