#!/usr/bin/python
# -*- coding: gbk -*-

from behave import *
import ywAUT.Globalvar as gl
d = gl.get_value('device')


@step("�˺������½")
def step_impl(context):
    d(resourceId="com.miui.home:id/icon_icon").click()
    d(description=u"2018��12��7��,ũ�����³�һ,������").click()
    d(description=u"2018��12��8��,ũ�����³���,������").click()



