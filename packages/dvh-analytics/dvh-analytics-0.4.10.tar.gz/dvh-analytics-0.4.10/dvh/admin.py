#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 13:43:28 2017
@author: nightowl
"""

from __future__ import print_function
import update_sys_path
from bokeh.models.widgets import Button, Tabs, Panel, TextInput,Div, PasswordInput
from bokeh.layouts import row, column
from bokeh.io import curdoc
from bokeh.models import Spacer
from tools import auth
from tools.io.preferences.import_settings import initialize_directories_settings
import time
from tools.io.preferences.options import load_options
from dvh_bokeh_models.admin.database_editor import DatabaseEditor
from dvh_bokeh_models.admin.roi_manager import RoiManager
from dvh_bokeh_models.admin.baseline_plans import Baseline
from dvh_bokeh_models.admin.backup import Backup


initialize_directories_settings()
options = load_options()


# This depends on a user defined function in dvh/auth.py.  By default, this returns True
# It is up to the user/installer to write their own function (e.g., using python-ldap)
# Proper execution of this requires placing Bokeh behind a reverse proxy with SSL setup (HTTPS)
# Please see Bokeh documentation for more information
ACCESS_GRANTED = not options.AUTH_USER_REQ


roi_manager = RoiManager()
database_editor = DatabaseEditor(roi_manager)
baseline = Baseline()
backup = Backup()


def auth_button_click():
    global ACCESS_GRANTED

    if not ACCESS_GRANTED:
        ACCESS_GRANTED = auth.check_credentials(auth_user.value, auth_pass.value, 'admin')
        if ACCESS_GRANTED:
            auth_button.label = 'Access Granted'
            auth_button.button_type = 'success'
            curdoc().clear()
            curdoc().add_root(tabs)
        else:
            auth_button.label = 'Failed'
            auth_button.button_type = 'danger'
            time.sleep(3)
            auth_button.label = 'Authenticate'
            auth_button.button_type = 'warning'


auth_user = TextInput(value='', title='User Name:', width=150)
auth_pass = PasswordInput(value='', title='Password:', width=150)
auth_button = Button(label="Authenticate", button_type="warning", width=100)
auth_button.on_click(auth_button_click)
auth_div = Div(text="<b>DVH Analytics Admin</b>", width=600)
layout_login = column(auth_div,
                      row(auth_user, Spacer(width=50), auth_pass, Spacer(width=50), auth_button))


roi_tab = Panel(child=roi_manager.layout, title='ROI Name Manager')
db_tab = Panel(child=database_editor.layout, title='Database Editor')
backup_tab = Panel(child=backup.layout, title='Backup & Restore')
baseline_tab = Panel(child=baseline.layout, title='Baseline Plans')

if options.DISABLE_BACKUP_TAB:
    tabs = Tabs(tabs=[db_tab, roi_tab, baseline_tab])
else:
    tabs = Tabs(tabs=[db_tab, roi_tab, baseline_tab, backup_tab])

if ACCESS_GRANTED:
    curdoc().add_root(tabs)
else:
    curdoc().add_root(layout_login)

curdoc().title = "DVH Analytics: Admin"
