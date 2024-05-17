// Copyright (c) 2024, Hybrowlabs Technologies and contributors
// For license information, please see license.txt

frappe.query_reports["Project Activity Report"] = {
	tree: true,
	initial_depth: 0,
	filters: [
		{
			fieldname: "project",
			label: __("Project"),
			fieldtype: "Link",
			options: "Project",
		
		},
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.nowdate()
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.add_days( frappe.datetime.nowdate(), 1)
		},
		{
			"fieldname": "employee",
			"label": __("Employee"),
			"fieldtype": "Link",
			"options": "Employee"
		},
	]
};
 