"""Focused regressions for the v16 ports. External AI/AWS calls are simulated."""
import importlib
import io
import queue
import unittest
from types import SimpleNamespace
from unittest.mock import patch

import frappe
from frappe.model.base_document import get_controller


def run(app):
    assert app in frappe.get_installed_apps()
    modules = frappe.get_all('Module Def', filters={'app_name': app}, pluck='name')
    doctypes = frappe.get_all('DocType', filters={'module': ['in', modules]}, pluck='name')
    for doctype in doctypes:
        frappe.get_meta(doctype)
        get_controller(doctype)
    globals()['check_' + app]()
    print({'app': app, 'controllers': len(doctypes), 'regressions': 'passed'})


def check_expenses():
    import expenses.libs
    from expenses.libs.logger import get_logger
    assert get_logger('info') is get_logger('info')
    doc = frappe.get_single('Expenses Settings')
    assert doc.doctype == 'Expenses Settings'
    for name in ['Expense', 'Expenses Request', 'Expenses Entry']:
        assert frappe.new_doc(name).doctype == name
