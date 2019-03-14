# -*- coding: utf-8 -*-
# Copyright 2014-2018 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from collections import defaultdict
import logging
import numbers

from odoo.report import report_sxw

from ..models.accounting_none import AccountingNone
from ..models.data_error import DataError

_logger = logging.getLogger(__name__)

try:
    from odoo.addons.report_xlsx.report.report_xlsx import ReportXlsx
except ImportError:
    _logger.debug("report_xlsx not installed, Excel export non functional")

    class ReportXlsx(object):
        def __init__(self, *args, **kwargs):
            pass


ROW_HEIGHT = 15  # xlsxwriter units
COL_WIDTH = 0.9  # xlsxwriter units
MIN_COL_WIDTH = 15  # characters
MAX_COL_WIDTH = 50  # characters


class MisBuilderXlsx(ReportXlsx):

    def generate_xlsx_report(self, workbook, data, objects):

        # get the computed result of the report
        matrix = objects._compute_matrix()
        style_obj = self.env['mis.report.style']

        # create worksheet
        report_name = u'{} - {}'.format(
            objects[0].name, u', '.join(
                [a.name for a in objects[0].query_company_ids]))
        sheet = workbook.add_worksheet(report_name[:31])
        row_pos = 0
        col_pos = 0
        # width of the labels column
        label_col_width = MIN_COL_WIDTH
        # {col_pos: max width in characters}
        col_width = defaultdict(lambda: MIN_COL_WIDTH)

        # document title
        bold = workbook.add_format({'bold': True})
        header_format = workbook.add_format({
            'bold': True, 'align': 'center', 'bg_color': '#F0EEEE'})
        sheet.write(row_pos, 0, report_name, bold)
        row_pos += 2

        # filters
        if not objects.hide_analytic_filters:
            for filter_description in \
                    objects.get_filter_descriptions_from_context():
                sheet.write(row_pos, 0, filter_description, bold)
                row_pos += 1
            row_pos += 2

        # column headers
        sheet.write(row_pos, 0, '', header_format)
        col_pos = 1
        for col in matrix.iter_cols():
            label = col.label
            if col.description:
                label += '\n' + col.description
                sheet.set_row(row_pos, ROW_HEIGHT * 2)
            if col.colspan > 1:
                sheet.merge_range(
                    row_pos, col_pos, row_pos,
                    col_pos + col.colspan-1,
                    label, header_format)
            else:
                sheet.write(row_pos, col_pos, label, header_format)
                col_width[col_pos] = max(col_width[col_pos],
                                         len(col.label or ''),
                                         len(col.description or ''))
            col_pos += col.colspan
        row_pos += 1

        # sub column headers
        sheet.write(row_pos, 0, '', header_format)
        col_pos = 1
        for subcol in matrix.iter_subcols():
            label = subcol.label
            if subcol.description:
                label += '\n' + subcol.description
                sheet.set_row(row_pos, ROW_HEIGHT * 2)
            sheet.write(row_pos, col_pos, label, header_format)
            col_width[col_pos] = max(col_width[col_pos],
                                     len(subcol.label or ''),
                                     len(subcol.description or ''))
            col_pos += 1
        row_pos += 1

        # rows
        for row in matrix.iter_rows():
            if (row.style_props.hide_empty and row.is_empty()) or \
                    row.style_props.hide_always:
                continue
            row_xlsx_style = style_obj.to_xlsx_style(row.style_props)
            row_format = workbook.add_format(row_xlsx_style)
            col_pos = 0
            label = row.label
            if row.description:
                label += '\n' + row.description
                sheet.set_row(row_pos, ROW_HEIGHT * 2)
            sheet.write(row_pos, col_pos, label, row_format)
            label_col_width = max(label_col_width,
                                  len(row.label or ''),
                                  len(row.description or ''))
            for cell in row.iter_cells():
                col_pos += 1
                if not cell or cell.val is AccountingNone:
                    # TODO col/subcol format
                    sheet.write(row_pos, col_pos, '', row_format)
                    continue
                cell_xlsx_style = style_obj.to_xlsx_style(
                    cell.style_props, no_indent=True)
                cell_xlsx_style['align'] = 'right'
                cell_format = workbook.add_format(cell_xlsx_style)
                if isinstance(cell.val, DataError):
                    val = cell.val.name
                    # TODO display cell.val.msg as Excel comment?
                elif cell.val is None or cell.val is AccountingNone:
                    val = ''
                else:
                    divider = float(cell.style_props.get('divider', 1))
                    if divider != 1 and isinstance(cell.val, numbers.Number):
                        val = cell.val / divider
                    else:
                        val = cell.val
                sheet.write(row_pos, col_pos, val, cell_format)
                col_width[col_pos] = max(col_width[col_pos],
                                         len(cell.val_rendered or ''))
            row_pos += 1

        # adjust col widths
        sheet.set_column(0, 0, min(label_col_width, MAX_COL_WIDTH) * COL_WIDTH)
        data_col_width = min(MAX_COL_WIDTH, max(col_width.values()))
        min_col_pos = min(col_width.keys())
        max_col_pos = max(col_width.keys())
        sheet.set_column(min_col_pos, max_col_pos, data_col_width * COL_WIDTH)


MisBuilderXlsx('report.mis.report.instance.xlsx',
               'mis.report.instance', parser=report_sxw.rml_parse)

class MisBuilder2Xlsx(ReportXlsx):

    def generate_xlsx_report(self, workbook, data, objects):

        # get the computed result of the report
        matrix = objects._compute_matrix()
        style_obj = self.env['mis.report.style']

        # create worksheet
        report_name = u'{} - {}'.format(
            objects[0].name, u', '.join(
                [a.name for a in objects[0].query_company_ids]))
        sheet = workbook.add_worksheet(report_name[:31])
        row_pos = 0
        col_pos = 0
        # width of the labels column
        label_col_width = MIN_COL_WIDTH
        # {col_pos: max width in characters}
        col_width = defaultdict(lambda: MIN_COL_WIDTH)

        # document title
        bold = workbook.add_format({'bold': True})
        header_format = workbook.add_format({
            'bold': True, 'align': 'center', 'bg_color': '#F0EEEE'})
        sheet.write(row_pos, 0, report_name, bold)
        row_pos += 2

        
        analytic_ids = [objects.analytic_account_id.id] + objects.env['account.analytic.account'].search([('parent_id', '=', objects.analytic_account_id.id)]).ids
    
        for aa in analytic_ids:
            _logger.info('IN LOOP: %s', aa)
            objects.write({'analytic_account_id': aa})
            context = dict(objects.env.context, mis_report_filters={})
            objects._add_analytic_filters_to_context(context)
            _logger.info('CONTEXT: %s', context)
            matrix = objects.with_context(context)._compute_matrix()
            
            # filters
            if not objects.hide_analytic_filters:
                for filter_description in \
                        objects.with_context(context).get_filter_descriptions_from_context():
                    sheet.write(row_pos, 0, filter_description.split(':')[1].strip(), bold)
                    row_pos += 1
                row_pos += 2
    
            # column headers
            sheet.write(row_pos, 0, '', header_format)
            col_pos = 1
            for col in matrix.iter_cols():
                label = col.label
                if col.description:
                    label += '\n' + col.description
                    sheet.set_row(row_pos, ROW_HEIGHT * 2)
                if col.colspan > 1:
                    sheet.merge_range(
                        row_pos, col_pos, row_pos,
                        col_pos + col.colspan-1,
                        label, header_format)
                else:
                    sheet.write(row_pos, col_pos, label, header_format)
                    col_width[col_pos] = max(col_width[col_pos],
                                             len(col.label or ''),
                                             len(col.description or ''))
                col_pos += col.colspan
            row_pos += 1
    
            # sub column headers
            sheet.write(row_pos, 0, '', header_format)
            col_pos = 1
            for subcol in matrix.iter_subcols():
                label = subcol.label
                if subcol.description:
                    label += '\n' + subcol.description
                    sheet.set_row(row_pos, ROW_HEIGHT * 2)
                sheet.write(row_pos, col_pos, label, header_format)
                col_width[col_pos] = max(col_width[col_pos],
                                         len(subcol.label or ''),
                                         len(subcol.description or ''))
                col_pos += 1
            row_pos += 1
    
            # rows
            for row in matrix.iter_rows():
                if (row.style_props.hide_empty and row.is_empty()) or \
                        row.style_props.hide_always:
                    continue
                row_xlsx_style = style_obj.to_xlsx_style(row.style_props)
                row_format = workbook.add_format(row_xlsx_style)
                col_pos = 0
                label = row.label
                if row.description:
                    label += '\n' + row.description
                    sheet.set_row(row_pos, ROW_HEIGHT * 2)
                sheet.write(row_pos, col_pos, label, row_format)
                label_col_width = max(label_col_width,
                                      len(row.label or ''),
                                      len(row.description or ''))
                for cell in row.iter_cells():
                    col_pos += 1
                    if not cell or cell.val is AccountingNone:
                        # TODO col/subcol format
                        sheet.write(row_pos, col_pos, '', row_format)
                        continue
                    cell_xlsx_style = style_obj.to_xlsx_style(
                        cell.style_props, no_indent=True)
                    cell_xlsx_style['align'] = 'right'
                    cell_format = workbook.add_format(cell_xlsx_style)
                    if isinstance(cell.val, DataError):
                        val = cell.val.name
                        # TODO display cell.val.msg as Excel comment?
                    elif cell.val is None or cell.val is AccountingNone:
                        val = ''
                    else:
                        divider = float(cell.style_props.get('divider', 1))
                        if divider != 1 and isinstance(cell.val, numbers.Number):
                            val = cell.val / divider
                        else:
                            val = cell.val
                    sheet.write(row_pos, col_pos, val, cell_format)
                    col_width[col_pos] = max(col_width[col_pos],
                                             len(cell.val_rendered or ''))
                row_pos += 1
            row_pos += 2
            
        # adjust col widths
        sheet.set_column(0, 0, min(label_col_width, MAX_COL_WIDTH) * COL_WIDTH)
        data_col_width = min(MAX_COL_WIDTH, max(col_width.values()))
        min_col_pos = min(col_width.keys())
        max_col_pos = max(col_width.keys())
        sheet.set_column(min_col_pos, max_col_pos, data_col_width * COL_WIDTH)
        
        objects.write({'analytic_account_id': False})


MisBuilder2Xlsx('report.mis.report.instance2.xlsx',
                'mis.report.instance', parser=report_sxw.rml_parse)
