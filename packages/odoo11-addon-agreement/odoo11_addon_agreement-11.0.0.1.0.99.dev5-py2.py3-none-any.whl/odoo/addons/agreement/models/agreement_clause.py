# Copyright (C) 2018 - TODAY, Pavlov Media
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AgreementClause(models.Model):
    _name = 'agreement.clause'
    _description = 'Agreement Clauses'
    _order = 'sequence'

    name = fields.Char(string="Name", required=True)
    title = fields.Char(string="Title",
                        help="The title is displayed on the PDF."
                             "The name is not.")
    sequence = fields.Integer(string="Sequence")
    agreement_id = fields.Many2one(
        'agreement',
        string="Agreement",
        ondelete="cascade"
    )
    section_id = fields.Many2one(
        'agreement.section',
        string="Section",
        ondelete="cascade"
    )
    content = fields.Html(string="Clause Content")
    dynamic_content = fields.Html(
        compute="_compute_dynamic_content",
        string="Dynamic Content",
        help='compute dynamic Content')
    active = fields.Boolean(
        string="Active",
        default=True,
        help="If unchecked, it will allow you to hide the agreement without "
             "removing it."
    )

    # compute the dynamic content for mako expression
    @api.multi
    def _compute_dynamic_content(self):
        MailTemplates = self.env['mail.template']
        for clause in self:
            lang = clause.agreement_id and \
                clause.agreement_id.partner_id.lang or 'en_US'
            content = MailTemplates.with_context(
                lang=lang).render_template(
                clause.content, 'agreement.clause', clause.id)
            clause.dynamic_content = content
