import frappe
from frappe import _
from frappe.model.docstatus import DocStatus
from frappe.utils import * 
import json


def execute(filters=None):
    filters = frappe._dict(filters or {})
    columns = get_columns(filters)
    data = get_data(filters)
    return columns, data


def get_columns(filters):
    group_columns = {
        "date": {
            "label": _("Date"),
            "fieldtype": "Date",
            "fieldname": "date",
            "width": 150,
        },
        "employee": {
            "label": _("Employee Name"),
            "fieldtype": "Data",
            "fieldname": "employee",
            "width": 250
        },
    }
    columns = []
    
    columns.extend(group_columns.values())

    columns.extend(
        [
            {
                "label": _("Activity"),
                "fieldtype": "data",
                "fieldname": "activity",
                 "width": 200
            },
            {
                "label": _("Description"),
                "fieldtype": "Data",
                "fieldname": "description",
                "width": 250,
            },
            {"label": _("Working Hours"), "fieldtype": "Data", "fieldname": "working_hours", "width": 150},
        ]
    )

    return columns


def get_data(filters):
    columns = []

    # Fetch timesheet data
    sql_conditions = []
    from_date = filters.get("from_date")
    to_date =  filters.get("to_date")
    if filters.get("project"):
        sql_conditions.append(f"td.project = '{filters['project']}'")  
        project_doc = frappe.get_doc("Project", filters.get("project"))
        assignee = project_doc._assign
        assign_users =json.loads(assignee)
        employees = []
        for item in assign_users:
            emp_name, employee_name = frappe.get_value("Employee",{'user_id':item},["name","employee_name"])
            employee = {"name": emp_name,"employee_name": employee_name}
            employees.append(employee)
    else:
        employees = frappe.get_all('Employee', fields=['name','employee_name'])
        
    from datetime import datetime, timedelta

    # Sample filter dictionary
    filters = {
        "from_date": "2024-05-01",
        "to_date": "2024-05-10"
    }

    from_date = datetime.strptime(from_date, "%Y-%m-%d")
    to_date = datetime.strptime(to_date, "%Y-%m-%d")

    current_date = from_date
    while current_date <= to_date:
        date_row = {
            'date':current_date.strftime("%Y-%m-%d"),
            "indent": 0,
            "is_group": 1,
        }
        columns.append(date_row)
        for employee in employees:
            row = {}
            emp_color = employee.get("employee_name")+" "+employee.get("name")
            row["employee"] = f"<font color ='red'>{emp_color}</font>"
            record = get_timesheet_data(employee.get("name"),current_date.strftime("%Y-%m-%d"))
            if record:
                total_hours = frappe.get_value("Timesheet", {"employee": employee.get("name")}, "total_hours")
                columns.append({"employee":employee.get("employee_name")+" "+employee.get("name"),"working_hours":"Total Hours: "+str(total_hours)})
                for rec in record:
                    columns.append({"activity":rec.get("activity"),"description":rec.get("task_d"),"working_hours":rec.get("working_hours"),"indent": 1,"is_group": 0})
            else:
                columns.append(row)
        current_date += timedelta(days=1)
    return columns


def get_timesheet_data(emp_id,date):
    where_clause = "WHERE ts.employee ='{}' AND DATE(td.from_time) = '{}'".format(emp_id,date)
    sql_query = f"""
        SELECT
            ts.name AS timesheet,
            CONCAT_WS(' ', ts.employee_name, ts.employee) as employee,
            td.project,
            td.hours AS working_hours,
            td.description AS task_d,
            td.activity_type AS activity,
            ts.total_hours,
            COALESCE(ts.name, '') AS timesheet,
            CASE WHEN ts.name IS NULL THEN 0 ELSE 1 END AS is_timesheet_filled
        FROM
            `tabTimesheet` ts
        LEFT JOIN
            `tabTimesheet Detail` td ON ts.name = td.parent
        {where_clause}
    """
    timesheet_data = frappe.db.sql(sql_query,as_dict=1)
    return timesheet_data