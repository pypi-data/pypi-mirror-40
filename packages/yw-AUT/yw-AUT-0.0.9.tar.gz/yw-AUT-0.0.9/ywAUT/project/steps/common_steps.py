#!/usr/bin/python
# -*- coding: gbk -*-
import os
from behave import *
from ywAUT.Driver import Driver
import ywAUT.Globalvar as gl
'''
    1. ��ʼ������driver
    2. �����豸
    3. ����driver������
    4. ���������ļ�
'''
driver = Driver(os.path.dirname(os.path.split(os.path.abspath(__file__))[0]))
d = driver.connect_device()
gl._init()
gl.set_value('device', d)


@step("��װapp")
def step_impl(context):
    driver.app_install()


@step("��app")
def step_impl(context):
    driver.app_start()


@step("�ر�app")
def step_impl(context):
    driver.app_stop()
    driver.close_remote()


@step('�������"{key_value}"���ı�')
def step_impl(context, key_value):
    d(text=key_value).click()


@step('�������"{key_value}"�İ�ť')
def step_impl(context, key_value):
    d(text=key_value).click()


@step('ҳ�����"{key_value}"')
def step_impl(context, key_value):
    assert d(text=key_value).wait(timeout=20)


@step('ҳ�治����"{key_value}"')
def step_impl(context, key_value):
    assert not d(text=key_value).wait(timeout=20)


@step('���ϻ�����"{key_value}"��')
def step_impl(context, key_value):
    d(scrollable=True).scroll.to(text=key_value)


@step('���󻬶���"{key_value}"��')
def step_impl(context, key_value):
    d(scrollable=True).scroll.horiz.forward(steps=100)


@step('��"{forward}"����(\d+)��')
def step_impl(context, forward, time):
    for i in range(int(time)):
        if forward == '��':
            d.swipe(370, 370, 70, 370, 0)
        elif forward == '��':
            d.swipe(70, 370, 370, 370, 0)
        elif forward == '��':
            d.swipe(370, 170, 370, 570, 0)
        elif forward == '��':
            d.swipe(370, 570, 370, 170, 0)

