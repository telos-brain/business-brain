---
name: Update Finances
code: WF-UPDATE-FINANCES
description: >-
  Changes Xero data for the connected organisations. Reads current
  records, then uses Xero read and write tools to do what the request
  asks. The calling tool requires CFO approval before this run starts.
version: 3

# TOOL: invoked via tools/execution/finances/update-finances.yml as {{input.request}}.
type: TOOL

system-prompt-code: WF-SYSTEM-PROMPT

output-tokens: 4000, 8000, 12000
caching: automatic
max-turns: 50
thinking: adaptive
session-timeout: 30

# xero_get_connections is injected. Other Xero reads and writes stay in
# available-tools and are promoted with activate_tools.
tools:
  - find_available_tools
  - activate_tools
  - xero_get_connections

available-tools:
  - xero_au_approve_leave_application
  - xero_au_create_employee
  - xero_au_create_leave_application
  - xero_au_create_pay_item
  - xero_au_create_pay_run
  - xero_au_create_payroll_calendar
  - xero_au_create_superfund
  - xero_au_create_timesheet
  - xero_au_get_employee
  - xero_au_get_employees
  - xero_au_get_leave_application
  - xero_au_get_leave_applications
  - xero_au_get_leave_applications_v2
  - xero_au_get_pay_items
  - xero_au_get_pay_run
  - xero_au_get_pay_runs
  - xero_au_get_payroll_calendar
  - xero_au_get_payroll_calendars
  - xero_au_get_payslip
  - xero_au_get_settings
  - xero_au_get_superfund
  - xero_au_get_superfund_products
  - xero_au_get_superfunds
  - xero_au_get_timesheet
  - xero_au_get_timesheets
  - xero_au_reject_leave_application
  - xero_au_update_employee
  - xero_au_update_leave_application
  - xero_au_update_pay_run
  - xero_au_update_payslip
  - xero_au_update_superfund
  - xero_au_update_timesheet
  - xero_au_v2_approve_timesheet
  - xero_au_v2_create_timesheet
  - xero_au_v2_create_timesheet_line
  - xero_au_v2_delete_timesheet
  - xero_au_v2_delete_timesheet_line
  - xero_au_v2_get_timesheet
  - xero_au_v2_get_timesheets
  - xero_au_v2_revert_timesheet
  - xero_au_v2_update_timesheet_line
  - xero_create_account
  - xero_create_account_attachment_by_file_name
  - xero_create_bank_transaction_attachment_by_file_name
  - xero_create_bank_transaction_history_record
  - xero_create_bank_transactions
  - xero_create_bank_transfer
  - xero_create_bank_transfer_attachment_by_file_name
  - xero_create_bank_transfer_history_record
  - xero_create_batch_payment
  - xero_create_batch_payment_history_record
  - xero_create_branding_theme_payment_services
  - xero_create_contact_attachment_by_file_name
  - xero_create_contact_group
  - xero_create_contact_group_contacts
  - xero_create_contact_history
  - xero_create_contacts
  - xero_create_credit_note_allocation
  - xero_create_credit_note_attachment_by_file_name
  - xero_create_credit_note_history
  - xero_create_credit_notes
  - xero_create_currency
  - xero_create_expense_claim_history
  - xero_create_expense_claims
  - xero_create_invoice_attachment_by_file_name
  - xero_create_invoice_history
  - xero_create_invoices
  - xero_create_item_history
  - xero_create_items
  - xero_create_linked_transaction
  - xero_create_manual_journal_attachment_by_file_name
  - xero_create_manual_journal_history_record
  - xero_create_manual_journals
  - xero_create_overpayment_allocations
  - xero_create_overpayment_history
  - xero_create_payment
  - xero_create_payment_history
  - xero_create_payment_service
  - xero_create_payments
  - xero_create_prepayment_allocations
  - xero_create_prepayment_history
  - xero_create_purchase_order_attachment_by_file_name
  - xero_create_purchase_order_history
  - xero_create_purchase_orders
  - xero_create_quote_attachment_by_file_name
  - xero_create_quote_history
  - xero_create_quotes
  - xero_create_receipt
  - xero_create_receipt_attachment_by_file_name
  - xero_create_receipt_history
  - xero_create_repeating_invoice_attachment_by_file_name
  - xero_create_repeating_invoice_history
  - xero_create_repeating_invoices
  - xero_create_tax_rates
  - xero_create_tracking_category
  - xero_create_tracking_options
  - xero_delete_account
  - xero_delete_bank_transfer
  - xero_delete_bank_transfers
  - xero_delete_batch_payment
  - xero_delete_batch_payment_by_url_param
  - xero_delete_connection
  - xero_delete_contact_group_contact
  - xero_delete_contact_group_contacts
  - xero_delete_credit_note_allocations
  - xero_delete_item
  - xero_delete_linked_transaction
  - xero_delete_overpayment_allocations
  - xero_delete_payment
  - xero_delete_prepayment_allocations
  - xero_delete_tracking_category
  - xero_delete_tracking_options
  - xero_email_invoice
  - xero_get_account
  - xero_get_account_attachment_by_file_name
  - xero_get_account_attachment_by_id
  - xero_get_account_attachments
  - xero_get_accounts
  - xero_get_bank_transaction
  - xero_get_bank_transaction_attachment_by_file_name
  - xero_get_bank_transaction_attachment_by_id
  - xero_get_bank_transaction_attachments
  - xero_get_bank_transactions
  - xero_get_bank_transactions_history
  - xero_get_bank_transfer
  - xero_get_bank_transfer_attachment_by_file_name
  - xero_get_bank_transfer_attachment_by_id
  - xero_get_bank_transfer_attachments
  - xero_get_bank_transfer_history
  - xero_get_bank_transfers
  - xero_get_batch_payment
  - xero_get_batch_payment_history
  - xero_get_batch_payments
  - xero_get_branding_theme
  - xero_get_branding_theme_payment_services
  - xero_get_branding_themes
  - xero_get_budget
  - xero_get_budgets
  - xero_get_contact
  - xero_get_contact_attachment_by_file_name
  - xero_get_contact_attachment_by_id
  - xero_get_contact_attachments
  - xero_get_contact_by_contact_number
  - xero_get_contact_cissettings
  - xero_get_contact_group
  - xero_get_contact_groups
  - xero_get_contact_history
  - xero_get_contacts
  - xero_get_credit_note
  - xero_get_credit_note_as_pdf
  - xero_get_credit_note_attachment_by_file_name
  - xero_get_credit_note_attachment_by_id
  - xero_get_credit_note_attachments
  - xero_get_credit_note_history
  - xero_get_credit_notes
  - xero_get_currencies
  - xero_get_expense_claim
  - xero_get_expense_claim_history
  - xero_get_expense_claims
  - xero_get_invoice
  - xero_get_invoice_as_pdf
  - xero_get_invoice_attachment_by_file_name
  - xero_get_invoice_attachment_by_id
  - xero_get_invoice_attachments
  - xero_get_invoice_history
  - xero_get_invoice_reminders
  - xero_get_invoices
  - xero_get_item
  - xero_get_item_history
  - xero_get_items
  - xero_get_journal
  - xero_get_journal_by_number
  - xero_get_journals
  - xero_get_linked_transaction
  - xero_get_linked_transactions
  - xero_get_manual_journal
  - xero_get_manual_journal_attachment_by_file_name
  - xero_get_manual_journal_attachment_by_id
  - xero_get_manual_journal_attachments
  - xero_get_manual_journals
  - xero_get_manual_journals_history
  - xero_get_online_invoice
  - xero_get_organisation_actions
  - xero_get_organisation_cissettings
  - xero_get_organisations
  - xero_get_overpayment
  - xero_get_overpayment_history
  - xero_get_overpayments
  - xero_get_payment
  - xero_get_payment_history
  - xero_get_payment_services
  - xero_get_payments
  - xero_get_prepayment
  - xero_get_prepayment_history
  - xero_get_prepayments
  - xero_get_purchase_order
  - xero_get_purchase_order_as_pdf
  - xero_get_purchase_order_attachment_by_file_name
  - xero_get_purchase_order_attachment_by_id
  - xero_get_purchase_order_attachments
  - xero_get_purchase_order_by_number
  - xero_get_purchase_order_history
  - xero_get_purchase_orders
  - xero_get_quote
  - xero_get_quote_as_pdf
  - xero_get_quote_attachment_by_file_name
  - xero_get_quote_attachment_by_id
  - xero_get_quote_attachments
  - xero_get_quote_history
  - xero_get_quotes
  - xero_get_receipt
  - xero_get_receipt_attachment_by_file_name
  - xero_get_receipt_attachment_by_id
  - xero_get_receipt_attachments
  - xero_get_receipt_history
  - xero_get_receipts
  - xero_get_repeating_invoice
  - xero_get_repeating_invoice_attachment_by_file_name
  - xero_get_repeating_invoice_attachment_by_id
  - xero_get_repeating_invoice_attachments
  - xero_get_repeating_invoice_history
  - xero_get_repeating_invoices
  - xero_get_report_aged_payables_by_contact
  - xero_get_report_aged_receivables_by_contact
  - xero_get_report_balance_sheet
  - xero_get_report_bank_summary
  - xero_get_report_budget_summary
  - xero_get_report_executive_summary
  - xero_get_report_from_id
  - xero_get_report_profit_and_loss
  - xero_get_report_ten_ninety_nine
  - xero_get_report_trial_balance
  - xero_get_reports_list
  - xero_get_tax_rate_by_tax_type
  - xero_get_tax_rates
  - xero_get_tracking_categories
  - xero_get_tracking_category
  - xero_get_user
  - xero_get_users
  - xero_nz_approve_timesheet
  - xero_nz_create_deduction
  - xero_nz_create_earnings_rate
  - xero_nz_create_employee
  - xero_nz_create_employee_earnings_template
  - xero_nz_create_employee_leave
  - xero_nz_create_employee_leave_setup
  - xero_nz_create_employee_leave_type
  - xero_nz_create_employee_opening_balances
  - xero_nz_create_employee_payment_method
  - xero_nz_create_employee_salary_and_wage
  - xero_nz_create_employee_working_pattern
  - xero_nz_create_employment
  - xero_nz_create_leave_type
  - xero_nz_create_multiple_employee_earnings_template
  - xero_nz_create_pay_run
  - xero_nz_create_pay_run_calendar
  - xero_nz_create_reimbursement
  - xero_nz_create_superannuation
  - xero_nz_create_timesheet
  - xero_nz_create_timesheet_line
  - xero_nz_delete_employee_earnings_template
  - xero_nz_delete_employee_leave
  - xero_nz_delete_employee_salary_and_wage
  - xero_nz_delete_employee_working_pattern
  - xero_nz_delete_timesheet
  - xero_nz_delete_timesheet_line
  - xero_nz_get_deduction
  - xero_nz_get_deductions
  - xero_nz_get_earnings_rate
  - xero_nz_get_earnings_rates
  - xero_nz_get_employee
  - xero_nz_get_employee_leave_balances
  - xero_nz_get_employee_leave_periods
  - xero_nz_get_employee_leave_types
  - xero_nz_get_employee_leaves
  - xero_nz_get_employee_opening_balances
  - xero_nz_get_employee_pay_templates
  - xero_nz_get_employee_payment_method
  - xero_nz_get_employee_salary_and_wage
  - xero_nz_get_employee_salary_and_wages
  - xero_nz_get_employee_tax
  - xero_nz_get_employee_working_pattern
  - xero_nz_get_employee_working_patterns
  - xero_nz_get_employees
  - xero_nz_get_leave_type
  - xero_nz_get_leave_types
  - xero_nz_get_pay_run
  - xero_nz_get_pay_run_calendar
  - xero_nz_get_pay_run_calendars
  - xero_nz_get_pay_runs
  - xero_nz_get_pay_slip
  - xero_nz_get_pay_slips
  - xero_nz_get_reimbursement
  - xero_nz_get_reimbursements
  - xero_nz_get_settings
  - xero_nz_get_statutory_deduction
  - xero_nz_get_statutory_deductions
  - xero_nz_get_superannuation
  - xero_nz_get_superannuations
  - xero_nz_get_timesheet
  - xero_nz_get_timesheets
  - xero_nz_get_tracking_categories
  - xero_nz_revert_timesheet
  - xero_nz_update_employee
  - xero_nz_update_employee_earnings_template
  - xero_nz_update_employee_leave
  - xero_nz_update_employee_salary_and_wage
  - xero_nz_update_employee_tax
  - xero_nz_update_pay_slip_line_items
  - xero_nz_update_timesheet_line
  - xero_post_setup
  - xero_uk_approve_timesheet
  - xero_uk_create_benefit
  - xero_uk_create_deduction
  - xero_uk_create_earnings_rate
  - xero_uk_create_employee
  - xero_uk_create_employee_earnings_template
  - xero_uk_create_employee_leave
  - xero_uk_create_employee_leave_type
  - xero_uk_create_employee_opening_balances
  - xero_uk_create_employee_payment_method
  - xero_uk_create_employee_salary_and_wage
  - xero_uk_create_employee_statutory_sick_leave
  - xero_uk_create_employment
  - xero_uk_create_leave_type
  - xero_uk_create_multiple_employee_earnings_template
  - xero_uk_create_pay_run_calendar
  - xero_uk_create_reimbursement
  - xero_uk_create_timesheet
  - xero_uk_create_timesheet_line
  - xero_uk_delete_employee_earnings_template
  - xero_uk_delete_employee_leave
  - xero_uk_delete_employee_salary_and_wage
  - xero_uk_delete_timesheet
  - xero_uk_delete_timesheet_line
  - xero_uk_get_benefit
  - xero_uk_get_benefits
  - xero_uk_get_deduction
  - xero_uk_get_deductions
  - xero_uk_get_earnings_order
  - xero_uk_get_earnings_orders
  - xero_uk_get_earnings_rate
  - xero_uk_get_earnings_rates
  - xero_uk_get_employee
  - xero_uk_get_employee_leave
  - xero_uk_get_employee_leave_balances
  - xero_uk_get_employee_leave_periods
  - xero_uk_get_employee_leave_types
  - xero_uk_get_employee_leaves
  - xero_uk_get_employee_opening_balances
  - xero_uk_get_employee_pay_template
  - xero_uk_get_employee_payment_method
  - xero_uk_get_employee_salary_and_wage
  - xero_uk_get_employee_salary_and_wages
  - xero_uk_get_employee_statutory_leave_balances
  - xero_uk_get_employee_statutory_sick_leave
  - xero_uk_get_employee_tax
  - xero_uk_get_employees
  - xero_uk_get_leave_type
  - xero_uk_get_leave_types
  - xero_uk_get_pay_run
  - xero_uk_get_pay_run_calendar
  - xero_uk_get_pay_run_calendars
  - xero_uk_get_pay_runs
  - xero_uk_get_pay_slip
  - xero_uk_get_pay_slips
  - xero_uk_get_reimbursement
  - xero_uk_get_reimbursements
  - xero_uk_get_settings
  - xero_uk_get_statutory_leave_summary
  - xero_uk_get_timesheet
  - xero_uk_get_timesheets
  - xero_uk_get_tracking_categories
  - xero_uk_revert_timesheet
  - xero_uk_update_employee
  - xero_uk_update_employee_earnings_template
  - xero_uk_update_employee_leave
  - xero_uk_update_employee_opening_balances
  - xero_uk_update_employee_salary_and_wage
  - xero_uk_update_timesheet_line
  - xero_update_account
  - xero_update_account_attachment_by_file_name
  - xero_update_bank_transaction
  - xero_update_bank_transaction_attachment_by_file_name
  - xero_update_bank_transfer_attachment_by_file_name
  - xero_update_contact
  - xero_update_contact_attachment_by_file_name
  - xero_update_contact_group
  - xero_update_credit_note
  - xero_update_credit_note_attachment_by_file_name
  - xero_update_expense_claim
  - xero_update_invoice
  - xero_update_invoice_attachment_by_file_name
  - xero_update_item
  - xero_update_linked_transaction
  - xero_update_manual_journal
  - xero_update_manual_journal_attachment_by_file_name
  - xero_update_or_create_bank_transactions
  - xero_update_or_create_contacts
  - xero_update_or_create_credit_notes
  - xero_update_or_create_invoices
  - xero_update_or_create_items
  - xero_update_or_create_manual_journals
  - xero_update_or_create_purchase_orders
  - xero_update_or_create_quotes
  - xero_update_or_create_repeating_invoices
  - xero_update_purchase_order
  - xero_update_purchase_order_attachment_by_file_name
  - xero_update_quote
  - xero_update_quote_attachment_by_file_name
  - xero_update_receipt
  - xero_update_receipt_attachment_by_file_name
  - xero_update_repeating_invoice
  - xero_update_repeating_invoice_attachment_by_file_name
  - xero_update_tax_rate
  - xero_update_tracking_category
  - xero_update_tracking_options
---

# Instructions

You change Xero data. Read the current records before you write. Change
only what the request asks for.

CFO approval is required before this run starts. Once you are running,
the request has been approved. Still do not delete, void, disconnect, or
email a customer unless the request explicitly says to.

## Request

<request>
{{input.request}}
</request>

## Connected organisations

A Xero connection can cover more than one organisation. Each connection
is an entity you can read or change.

1. Call `xero_get_connections`. It is already available. Omit
   `xeroTenantId` on that call. Each result has `tenantId` and
   `tenantName`.
2. Use the organisation the request names. If there is one connection,
   use it. If there are several and the request does not say which, do
   not guess — report the `tenantName` / `tenantId` pairs and stop.
3. Later Accounting calls take `xeroTenantId` set to that `tenantId`.

## Doing the work

1. `find_available_tools` with tight queries for the read tools that show
   the current state, then the write tools the change needs. Payroll
   tools are regional: `xero_au_` (Australia), `xero_au_v2_` (Australia
   timesheets), `xero_nz_` (New Zealand), `xero_uk_` (United Kingdom).
   Call `activate_tools` with those names. They are callable on the next
   step.
2. Read first. Confirm contact ids, invoice ids, account codes, and
   amounts from tool results. Never guess them.
3. Call the write tool that matches the request. If Xero rejects the
   change, quote the error and stop. Do not try a different write to
   force it through.
4. Read the changed record back. Include its id, status, and amounts in
   your reply.

If the request is too vague to name the change, stop and say what is
missing. Do not call a write tool.

## How to answer

- Organisation (`tenantName` and `tenantId`)
- What you changed
- Key results (ids, amounts, statuses, dates)
- Anything you did not change, and why

Do not invent records. British English. No secrets.
