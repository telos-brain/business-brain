---
name: Read Finances
code: WF-READ-FINANCES
description: >-
  Reads Xero for the connected organisations and answers a request with
  data from Xero read tools. Does not change the books.
version: 1

# TOOL: invoked via tools/execution/finances/read-finances.yml as {{input.request}}.
type: TOOL

system-prompt-code: WF-SYSTEM-PROMPT

output-tokens: 4096, 8192, 16384
caching: automatic
max-turns: 40
thinking: adaptive
session-timeout: 30

# Discovery only. Xero reads stay in available-tools and are promoted
# with activate_tools (BRA212 / BRA217 / BRA415).
tools:
  - find_available_tools
  - activate_tools

available-tools:
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
  - xero_get_connections
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
---

# Instructions

You read Xero. You do not create, update, delete, email, or otherwise
change anything. If the request asks for a change, say that
`update_finances` is the tool for that and stop.

## Request

<request>
{{input.request}}
</request>

## Connected organisations

A Xero connection can cover more than one organisation. Each connection
is an entity you can read.

1. `find_available_tools` for the connections tool (`xero_get_connections`).
   Then `activate_tools` with the names you will call. A search result is
   not callable. The tools are available on the **next** step.
2. Call `xero_get_connections`. Omit `xeroTenantId` on that call. Each
   result has `tenantId` and `tenantName`.
3. Use the organisation the request names. If there is one connection,
   use it. If there are several and the request does not say which, do
   not guess — report the `tenantName` / `tenantId` pairs and what you
   still need.
4. Later Accounting calls take `xeroTenantId` set to that `tenantId`.

## Getting the data

1. `find_available_tools` with a few tight queries for the records the
   request needs (for example `aged receivables`, `profit and loss`,
   `list invoices`). Then `activate_tools` with those names.
2. Read each tool's parameters before you call it. Prefer `where`,
   `page`, `searchTerm`, and date filters over fetching everything.
3. Call the tools. Do not invent contacts, invoices, balances, or
   identifiers. Quote Xero's error when a call fails.
4. If a call fails for tenant or authorisation, call
   `xero_get_connections` again and report the pairs.

## How to answer

Return what the request asked for: the organisation you used
(`tenantName` and `tenantId`), the figures and records, and anything you
could not retrieve. British English. No secrets.
