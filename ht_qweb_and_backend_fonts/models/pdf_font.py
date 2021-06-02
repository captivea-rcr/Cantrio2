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
from odoo import fields, api, models


class ResConSetting(models.TransientModel):
    _inherit = 'res.config.settings'

    pdf_font = fields.Selection([('tazawal', 'Tazawal'),
                                 ('amiri', 'Amiri'),
                                 ('changa', 'Changa'),
                                 ('roboto', 'Roboto'),
                                 ('poppins', 'Poppins'),
                                 ('notosans', 'Notosans'),
                                 ('lato', 'Lato'),
                                 ('mukta', 'Mukta'),
                                 ('nunito', 'Nunito'),
                                 ('lora', 'Lora'),
                                 ('mulish', 'Mulish'),
                                 ('alegreya', 'Alegreya'),
                                 ('tinos', 'Tinos'),
                                 ('dutch', 'Dutch'),
                                 ('belgium', 'Belgium'),
                                 ('norway', 'Norway'),
                                 ('german', 'German'),
                                 ('madeleinasans', 'Madeleina-sans'),
                                 ('swansea', 'Swansea'),
                                 ('georgia', 'Georgia'),
                                 ('museo', 'Museo'),
                                 ('proxima_nova', 'Proxima Nova'),
                                 ('caslon', 'Caslon'),
                                 ('arabic', 'Arabic'),
                                 ('time_new_roman', 'Time New Roman'),
                                 ('sentinel', 'Sentinel-Light'),
                                 ('sentinelbook', 'Sentinel-Book'),
                                 ('sentinelbold', 'Sentinel-Bold'),
                                 ('foundersgroteskbold', 'FoundersGrotesk-Bold'),
                                 ('foundersgrotesklight', 'FoundersGrotesk-Light'),
                                 ('foundersgroteskMedium', 'FoundersGrotesk-Medium'),
                                 ('maisonNeue', 'MaisonNeue-Book')])

    backend_fonts = fields.Selection([('tazawal', 'Tazawal'),
                                      ('amiri', 'Amiri'),
                                      ('changa', 'Changa'),
                                      ('roboto', 'Roboto'),
                                      ('poppins', 'Poppins'),
                                      ('notosans', 'Notosans'),
                                      ('lato', 'Lato'),
                                      ('mukta', 'Mukta'),
                                      ('nunito', 'Nunito'),
                                      ('lora', 'Lora'),
                                      ('mulish', 'Mulish'),
                                      ('alegreya', 'Alegreya'),
                                      ('tinos', 'Tinos'),
                                      ('dutch', 'Dutch'),
                                      ('belgium', 'Belgium'),
                                      ('norway', 'Norway'),
                                      ('german', 'German'),
                                      ('madeleinasans', 'Madeleina-sans'),
                                      ('swansea', 'Swansea'),
                                      ('georgia', 'Georgia'),
                                      ('museo', 'Museo'),
                                      ('proxima_nova', 'Proxima Nova'),
                                      ('caslon', 'Caslon'),
                                      ('arabic', 'Arabic'),
                                      ('time_new_roman', 'Time New Roman'),
                                      ('sentinel', 'Sentinel-Light'),
                                      ('sentinelbook', 'Sentinel-Book'),
                                      ('sentinelbold', 'Sentinel-Bold'),
                                      ('foundersgroteskbold', 'FoundersGrotesk-Bold'),
                                      ('foundersgrotesklight', 'FoundersGrotesk-Light'),
                                      ('foundersgroteskMedium', 'FoundersGrotesk-Medium'),
                                      ('maisonNeue', 'MaisonNeue-Book')])

    @api.model
    def get_values(self):
        res = super(ResConSetting, self).get_values()
        config = self.env['ir.config_parameter'].sudo()
        res.update(
            pdf_font=config.get_param(
                'ht_qweb_and_backend_fonts.pdf_font'),
            backend_fonts=config.get_param(
                'ht_qweb_and_backend_fonts.backend_fonts'))
        return res

    def set_values(self):
        super(ResConSetting, self).set_values()
        param = self.env['ir.config_parameter'].sudo()
        param.set_param(
            'ht_qweb_and_backend_fonts.pdf_font', self.pdf_font)
        param.set_param(
            'ht_qweb_and_backend_fonts.backend_fonts', self.backend_fonts)
