import csv

import frappe
from frappe.auth import cint

def execute():
    create_email_account()
def create_email_account():
    """
    Tạo Email Account từ file CSV
    """
    try:
        account_file_path = frappe.get_app_path("airplane_mode", "install/data_template", "email_account_noreplyf59dd9.csv")

        with open(account_file_path, newline='', encoding='utf-8') as csvfile:
            account_reader = csv.DictReader(csvfile)
            for row in account_reader:
                create_single_email_account(row)

        frappe.db.commit()
        return "Đã tạo xong Email Account từ file CSV"

    except FileNotFoundError:
        print(f"Không tìm thấy file email_account_noreplyf59dd9.csv")
        return "Không tìm thấy file email_account_noreplyf59dd9.csv"
    except Exception as e:
        error_msg = f"Lỗi khi tạo Email Account: {str(e)}"
        print(error_msg)
        frappe.logger().error(error_msg)
        return error_msg

import frappe

def create_single_email_account(row):
    try:
        email_id = row.get("Email Address")

        if not email_id:
            return

        # check tồn tại
        if frappe.db.exists("Email Account", {"email_id": email_id}):
            frappe.logger().info(f"Đã tồn tại: {email_id}")
            return

        doc = frappe.get_doc({
            "doctype": "Email Account",

            "email_account_name": row.get("Email Account Name"),
            "email_id": email_id,
            "password": row.get("Password", "BB/bBhU5FhpH2Of+F/WlekNnh0zIpFSxsEotrvWztt+p"),
            "domain":row.get("Domain", ""),
            "service": row.get("Service", ""),

            #authentication
            "auth_method": row.get("Method") or "Basic",
			"awaiting_password": cint(row.get("Awaiting password")) or 0,
			"ascii_encode_password": cint(row.get("Use ASCII encoding for password")) or 0,
			"login_id_is_different": cint(row.get("Use different Email ID")) or 1,
			"login_id": row.get("Alternative Email ID") or "AKIA52QKLLYOM7QQUKNZ",
            # incoming
            "enable_incoming": cint(row.get("Enable Incoming")) or 0,
            "email_server": row.get("Incoming Server"),
            "incoming_port": cint(row.get("Port")),
			"attachment_limit": cint(row.get("Attachment Limit (MB)")) or 25,
			"email_sync_option": row.get("Email Sync Option") or "UNSEEN",
			"initial_sync_count": cint(row.get("Initial Sync Count")) or 250,

            # outgoing
            "enable_outgoing": cint(row.get("Enable Outgoing")) or 1,
            "smtp_server": row.get("Outgoing Server") or "email-smtp.us-east-1.amazonaws.com",
            "smtp_port": cint(row.get("smtp_port")) or 465,
			"use_ssl_for_outgoing": cint(row.get("use_ssl_for_outgoing")) or 1,
			"always_use_account_email_id_as_sender": cint(row.get("Always use this email address as sender address")) or 1,
			"always_use_account_name_as_sender_name": cint(row.get("Always use this name as sender name")) or 1,
			"send_unsubscribe_message": cint(row.get("Send unsubscribe message in email")) or 1,
			"track_email_status": cint(row.get("Track Email Status")) or 1,
            # flags
            "default_incoming": cint(row.get("Default Incoming")) or 0,
            "default_outgoing": cint(row.get("Default Outgoing")) or 1,

            #documents to link
            "notify_if_unreplied": cint(row.get("Notify if unreplied")),
            "unreplied_for_mins": cint(row.get("Notify if unreplied for (in mins)")),
            "send_notification_to": row.get("Send Notification to"),

        })

        doc.insert(ignore_permissions=True)

        frappe.logger().info(f"✅ Created: {email_id}")

    except Exception as e:
        frappe.log_error(
            title="Create Email Account Error",
            message=f"{row}\n\n{str(e)}"
        )
