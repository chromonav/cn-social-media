// Copyright (c) 2024, Hybrowlabs Technologies and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Content Inspiration", {
// 	refresh(frm) {

// 	},
// });


frappe.ui.form.on('Content Inspiration', {
    refresh: function(frm) {
        // Check if the document is saved
        if (!frm.doc.__islocal) {
            // Accept button click event
            frm.add_custom_button(__('Accept'), function(){
                frappe.prompt([
                    {'fieldname': 'hook_title', 'fieldtype': 'Data', 'label': 'Hook Title'},
                    {'fieldname': 'social_media_account', 'fieldtype': 'Link', 'label': 'Social Media Account', 'reqd': 1, 'options': 'Social Media Account'},
                    {'fieldname': 'notes', 'fieldtype': 'Text', 'label': 'Notes'},
                ],
                function(values){
                    frappe.msgprint('You entered ' + values.hook_title + ', ' + values.social_media_account + ', and ' + values.notes);
 
                    // Create a new document
                    var doc = frappe.model.get_new_doc('Social Media Post');
 
                    // Set the fields
                    doc.social_media_title = values.hook_title;
                    doc.social_media_account = values.social_media_account;
                    doc.content_inspiration_synopsis = values.notes;
 
                    // Insert the document
                    frappe.call({
                        method: 'frappe.client.insert',
                        args: {
                            doc: doc
                        },
                        callback: function(response) {
                            if (!response.exc) {
                                frappe.msgprint('Record inserted successfully into Social Media Post');
                            }
                        }
                    });
                },
                'New Post',
                'Create Post'
                );
            });
 
            // Reject button click event
            frm.add_custom_button(__('Reject'), function(){
                frappe.msgprint('You clicked on Reject');
            });
        }
    }
 });
 