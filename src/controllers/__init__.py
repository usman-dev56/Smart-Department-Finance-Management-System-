# src/controllers/__init__.py
"""Controllers package - business logic layer"""

from .department_controller import (
    save_department,
    get_department,
    get_current_department,
    update_department,
    department_exists,
    get_receipt_prefix,
    get_next_receipt_number,
    get_department_summary
)

from .student_controller import (
    generate_roll_number,
    register_student,
    get_student_payments,
    search_students,
    delete_student,
    get_student_by_roll,
    get_all_students
)

from .campaign_controller import (
    create_campaign,
    get_eligible_students,
    get_paid_students,
    get_pending_students,
    get_campaign_summary,
    get_all_campaigns,
    deactivate_campaign,
    activate_campaign
)

from .payment_controller import (
    generate_receipt_number,
    collect_payment,
    get_payment_history,
    get_campaign_eligible_for_student,
    get_payment_by_receipt
)

from .academic_controller import (
    create_session,
    get_all_sessions,
    get_active_sessions,
    delete_session,
    toggle_session_status,
    create_program,
    get_all_programs,
    get_active_programs,
    delete_program,
    toggle_program_status,
    create_shift,
    get_all_shifts,
    get_active_shifts,
    delete_shift,
    toggle_shift_status,
    create_section,
    get_all_sections,
    get_active_sections,
    delete_section,
    toggle_section_status,
    get_academic_data,
    get_program_by_code
)

from .expense_controller import (
    add_expense,
    get_all_expenses,
    get_expense_by_id,
    update_expense,
    delete_expense,
    get_expenses_by_date_range,
    get_total_expenses_by_fund,
    get_expense_summary,
    get_monthly_expense_summary
)

from .fund_controller import (
    create_fund,
    get_all_funds,
    get_active_funds,
    get_fund_by_id,
    update_fund,
    delete_fund,
    toggle_fund_status,
    get_fund_summary,
    get_fund_dropdown_list
)

from .report_controller import (
    get_collection_report,
    get_campaign_report,
    get_pending_students_for_campaign,
    get_expense_report,
    get_fund_performance_report,
    get_student_payment_report,
    get_daily_summary,
    get_overall_summary
)