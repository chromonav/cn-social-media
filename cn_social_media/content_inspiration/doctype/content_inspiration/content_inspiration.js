// Copyright (c) 2024, rahul and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Content Inspiration", {
// 	refresh(frm) {

// 	},
// });




frappe.ui.form.on('Content Inspiration', {
  refresh(frm) {
    // Add click event handlers for the buttons

    frm.add_custom_button(__('Reject'), function() {
      frappe.confirm(__('Are you sure you want to reject this content inspiration?'), function() {
        // Show "Rejected" message and potentially update document state
        frappe.msgprint(__('Content Inspiration Rejected'), 'success');

        // Update document state if needed (optional)
        // frm.set_value('status', 'Rejected');
        // frm.save();
      });
    });

    frm.add_custom_button(__('Accept'), function() {
      frappe.confirm(__('Are you sure you want to accept this content inspiration?'), function() {
        // Show "Accepted" message and potentially update document state
        frappe.msgprint(__('Content Inspiration Accepted'), 'success');

        // Update document state if needed (optional)
        // frm.set_value('status', 'Accepted');
        // frm.save();
      });
    });
  }
});
