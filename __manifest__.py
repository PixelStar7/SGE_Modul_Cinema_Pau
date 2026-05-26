# -*- coding: utf-8 -*-
{
    'name': 'Cinema',
    'version': '1.0',
    'category': 'Entertainment',
    'summary': 'Cinema Management',
    'description': """
          Module prepared by department 'Informàtica i comunicacions'
          of Institute Milà i Fontanals in Igualada (Barcelona-Spain)
          for learning in development and adaptation of modules of Odoo ERP.

          It is part of the learning materials for the module
          'Sistemes de gestió empresarial' in the course
          'CFS Desenvolupament d''aplicacions multiplataforma'.
    """,
    'author': 'Group DAM2 - Course 2025-2026',
    'website': 'http://www.infomila.info',
    'depends': ['base', 'board', 'mail'],
    'data': [
        'security/cinema_security.xml', # Primer la definció dels grups de seguretat 
        'security/ir.model.access.csv', # Després les regles d'accés als models
        'views/cinema_views.xml',
        'report/cinema_report_qweb.xml'
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}