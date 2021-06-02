# -*- coding: utf-8 -*-
##############################################################################
#
#    Harhu IT Solutions
#    Copyright (C) 2020-TODAY Harhu IT Solutions(<https://www.harhu.com>).
#    Author: Harhu IT Solutions(<https://www.harhu.com>)
#    you can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    It is forbidden to publish, distribute, sublicense, or sell copies
#    of the Software or modified copies of the Software.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    GENERAL PUBLIC LICENSE (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'Qweb & Backend fonts',
    'summary': 'Set your own choice of font on backend views and qweb reports globally from given popular 25 fonts.',
    'version': '14.0.0.1.0',
    'category': 'report',
    'author': 'Harhu IT Solutions',
    'maintainer': 'Harhu IT Solutions',
    'contributors': ["Harhu IT Solutions"],
    'website': 'http://www.harhu.com',
    'live_test_url': 'https://www.harhu.com/contactus',
    'depends': ['web', 'sale_management'],
    'data': [
        'views/assets.xml',
        'views/res_config_setting.xml',
    ],
    'price': 35.00,
    'currency': "USD",
    'license': 'AGPL-3',
    'images': ['static/description/poster_image.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
