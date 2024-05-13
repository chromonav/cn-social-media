# Copyright (c) 2024, rahul and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document

class ContentInspiration(Document):
    def validate(self):
        # Check for status changes and update accordingly (optional)
        if self.status == 'Rejected':
            # Perform actions based on rejection
            pass
        elif self.status == 'Accepted':
            # Perform actions based on acceptance
            pass
