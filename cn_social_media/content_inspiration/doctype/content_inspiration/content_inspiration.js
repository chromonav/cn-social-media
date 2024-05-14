// Copyright (c) 2024, Hybrowlabs Technologies and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Content Inspiration", {
// 	refresh(frm) {

// 	},
// });


frappe.ui.form.on('Content Inspiration', {
    refresh: function(frm) {
        frm.fields_dict['accept'].$input.click(function() {
            frappe.prompt([
                {'fieldname': 'field1', 'fieldtype': 'Data', 'label': 'Hook title'},
                {'fieldname': 'field2', 'fieldtype': 'Select', 'label': 'Social Media Account', 'reqd': 1},
                {'fieldname': 'field1', 'fieldtype': 'Text', 'label': 'Notes'},
            ],
            function(values){
                frappe.msgprint('You entered ' + values.field1 + ' and ' + values.field2);
            },
            'New Post',
            'Create Post'
            )
        });

        
        frm.fields_dict['reject'].$input.click(function() {
            frappe.msgprint('You clicked on Reject');
        });
    }
});
