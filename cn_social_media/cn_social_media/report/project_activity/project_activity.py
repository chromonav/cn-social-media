import frappe
from frappe import _
from frappe.model.docstatus import DocStatus
from frappe.utils import * 


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
    sql_conditions = []
    
    if filters.get("employee"):
        sql_conditions.append(f"ts.employee = '{filters['employee']}'")

    if filters.get("from_date"):
        sql_conditions.append(f"DATE(td.from_time) >= DATE('{filters['from_date']}')")

    if filters.get("to_date"):
        sql_conditions.append(f"DATE(td.to_time) <= DATE('{filters['to_date']}')")
    
    if filters.get("project"):
        sql_conditions.append(f"td.project = '{filters['project']}'")    


    where_clause = " AND ".join(sql_conditions)
    sql_query = f"""
        SELECT
            ts.name AS timesheet,
            e.name AS employee,
            ts.employee_name,
            td.from_time AS date,
            td.project,
            td.hours AS working_hours,
            td.description AS task_d,
            td.activity_type AS activity,
            ts.total_hours
        FROM
            `tabEmployee` e
        LEFT JOIN
            `tabTimesheet` ts ON e.name = ts.employee
        LEFT JOIN
            `tabTimesheet Detail` td ON ts.name = td.parent
        {'WHERE e.custom_check_timesheet_filled=1 AND ' + where_clause if where_clause else ''}
    """


    # print(sql_query)
    data = frappe.db.sql(sql_query,as_dict=1)
    frappe.logger("ss").exception(data)
    print(data)
    return group_by(data)


def group_by(data):
    unique_dates = list(set([getdate(row.get('date')) for row in data]))
    grouped_data = []
    for date in sorted(unique_dates):
        date_row = {
            'date':date,
            "indent": 0,
            "is_group": 1,
        }
        grouped_data.append(date_row)
        employee_available_on_that_date= set([(row.get('employee'),row.get('employee_name')) for row in data if getdate(row.get('date')) == getdate(date)])
        for employee in employee_available_on_that_date:
            child_data =[]
            total_hours = 0
            for row in data:
                if row.get('employee') != employee[0]:
                    continue
                if getdate(row.get('date')) != getdate(date):
                    continue
                total_hours += float(row.get('working_hours'))
                _row = {}
                _row['employee'] = None
                _row['date'] = None
                _row['activity'] = row.get('activity')
                _row['description'] = row.get('task_d')
                _row["indent"] = 1
                _row['working_hours'] = str(row.get('working_hours')) + ' Hrs'
                _row["is_group"] = 0
                child_data.append(_row)
                
            data_row_employee = {
                "employee": employee[1]+' ('+employee[0]+')',
                "employee_id": employee[0],
                "activity":f"",
                "description": 'Total Hours: '+ str(total_hours),
                "indent": 0,
                "is_group": 1,
            } 
            grouped_data.append(data_row_employee)  
            grouped_data.extend(child_data)
    # print(grouped_data)
    return grouped_data

