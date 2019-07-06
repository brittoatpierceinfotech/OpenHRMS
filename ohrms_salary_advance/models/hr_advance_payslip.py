# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import models


class SalaryRuleInput(models.Model):
    _inherit = 'hr.payslip'

    def get_inputs(self, contract_ids, date_from, date_to):
        """This Compute the other inputs to employee payslip.
                           """
        res = super(SalaryRuleInput, self).get_inputs(contract_ids, date_from, date_to)
        contract_obj = self.env['hr.contract']
        emp_id = contract_obj.browse(contract_ids[0].id).employee_id
        
        # Commented by Pierce Infotech - Start
        # adv_salary = self.env['salary.advance'].search([('employee_id', '=', emp_id.id)])
        # for adv_obj in adv_salary:
        #     current_date = datetime.strptime(date_from, '%Y-%m-%d').date().month
        #     date = adv_obj.date
        #     existing_date = datetime.strptime(date, '%Y-%m-%d').date().month
        #     if current_date == existing_date:
        #         state = adv_obj.state
        #         amount = adv_obj.advance
        #         for result in res:
        #             if state == 'approve' and amount != 0 and result.get('code') == 'SAR':
        #                 result['amount'] = amount
        # Commented by Pierce Infotech - End

        # Fix by Pierce Infotech - Start
        # This fix consider only the advance salaries got during the payroll period install of all. The previous logic of checking only the month would result in inclusion of the advance salary in every consecutive years on the specified month.
        adv_salary = self.env['salary.advance'].search([('employee_id', '=', emp_id.id), ('date', '>=', date_from), ('date', '<=', date_to)])
        for adv_obj in adv_salary:
            state = adv_obj.state
            amount = adv_obj.advance
            for result in res:
                if state == 'approve' and amount != 0 and result.get('code') == 'SAR':
                    result['amount'] = amount
        # Fix by Pierce Infotech - End
        
        return res
