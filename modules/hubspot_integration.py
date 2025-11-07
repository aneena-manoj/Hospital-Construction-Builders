"""
HubSpot Integration Utilities for SE Builders AI Platform

This module provides functions to integrate with HubSpot CRM:
- Contact management
- Deal creation and tracking
- Task creation for follow-ups
- Activity logging
"""

import os
from datetime import datetime, timedelta
from typing import Optional, Dict, List
import streamlit as st

try:
    from hubspot import HubSpot
    from hubspot.crm.contacts import SimplePublicObjectInput, ApiException
    HUBSPOT_AVAILABLE = True
except ImportError:
    HUBSPOT_AVAILABLE = False


class HubSpotIntegration:
    """HubSpot CRM Integration for SE Builders"""

    def __init__(self):
        """Initialize HubSpot client"""
        self.api_key = os.getenv("HUBSPOT_API_KEY")

        if not self.api_key:
            self.client = None
            self.enabled = False
        else:
            try:
                self.client = HubSpot(api_key=self.api_key)
                self.enabled = True
            except Exception as e:
                st.warning(f"HubSpot initialization failed: {e}")
                self.client = None
                self.enabled = False

    def is_enabled(self) -> bool:
        """Check if HubSpot integration is enabled"""
        return self.enabled and HUBSPOT_AVAILABLE

    # ==================== CONTACT MANAGEMENT ====================

    def create_or_update_contact(
        self,
        email: str,
        firstname: str = "",
        lastname: str = "",
        phone: str = "",
        company: str = "",
        additional_properties: Dict = None
    ) -> Optional[str]:
        """
        Create or update a contact in HubSpot

        Args:
            email: Contact email (required)
            firstname: First name
            lastname: Last name
            phone: Phone number
            company: Company name
            additional_properties: Additional HubSpot properties

        Returns:
            Contact ID if successful, None otherwise
        """
        if not self.is_enabled():
            return None

        properties = {
            "email": email,
            "firstname": firstname or email.split('@')[0],
            "lastname": lastname,
            "phone": phone,
            "company": company,
            "lead_source": "SE Builders AI Platform",
            "hs_lead_status": "NEW"
        }

        # Add additional properties
        if additional_properties:
            properties.update(additional_properties)

        # Remove empty values
        properties = {k: v for k, v in properties.items() if v}

        try:
            # Search for existing contact by email
            search_results = self.client.crm.contacts.search_api.do_search(
                public_object_search_request={
                    "filter_groups": [{
                        "filters": [{
                            "propertyName": "email",
                            "operator": "EQ",
                            "value": email
                        }]
                    }]
                }
            )

            if search_results.total > 0:
                # Update existing contact
                contact_id = search_results.results[0].id
                contact_update = SimplePublicObjectInput(properties=properties)
                self.client.crm.contacts.basic_api.update(
                    contact_id=contact_id,
                    simple_public_object_input=contact_update
                )
                return contact_id
            else:
                # Create new contact
                contact_input = SimplePublicObjectInput(properties=properties)
                result = self.client.crm.contacts.basic_api.create(
                    simple_public_object_input=contact_input
                )
                return result.id

        except Exception as e:
            st.error(f"HubSpot contact error: {str(e)}")
            return None

    def add_note_to_contact(
        self,
        contact_id: str,
        note_body: str
    ) -> bool:
        """
        Add a note to a contact

        Args:
            contact_id: HubSpot contact ID
            note_body: Note content

        Returns:
            True if successful
        """
        if not self.is_enabled():
            return False

        try:
            # Create note (simplified for v8)
            note_input = SimplePublicObjectInput(
                properties={
                    "hs_note_body": note_body,
                    "hs_timestamp": datetime.now().isoformat()
                }
            )
            # Create engagement (note)
            note_result = self.client.crm.objects.notes.basic_api.create(
                simple_public_object_input=note_input
            )

            # Associate note with contact
            try:
                self.client.crm.objects.notes.associations_api.create(
                    note_id=note_result.id,
                    to_object_type="contacts",
                    to_object_id=contact_id
                )
            except:
                pass  # Association may fail but note is created

            return True
        except Exception as e:
            st.error(f"Failed to add note: {str(e)}")
            return False

    # ==================== DEAL MANAGEMENT ====================

    def create_deal(
        self,
        deal_name: str,
        amount: float,
        deal_stage: str = "appointmentscheduled",
        contact_email: str = None,
        additional_properties: Dict = None
    ) -> Optional[str]:
        """
        Create a deal in HubSpot

        Args:
            deal_name: Name of the deal
            amount: Deal amount in USD
            deal_stage: HubSpot deal stage ID or name
            contact_email: Associate deal with this contact
            additional_properties: Additional deal properties

        Returns:
            Deal ID if successful
        """
        if not self.is_enabled():
            return None

        properties = {
            "dealname": deal_name,
            "amount": str(amount),
            "dealstage": deal_stage,
            "pipeline": "default",
            "closedate": (datetime.now() + timedelta(days=90)).strftime("%Y-%m-%d"),
            "deal_source": "SE Builders AI Platform"
        }

        if additional_properties:
            properties.update(additional_properties)

        try:
            # Create deal input object
            deal_input = SimplePublicObjectInput(properties=properties)

            # Create the deal
            deal = self.client.crm.deals.basic_api.create(
                simple_public_object_input=deal_input
            )

            # Associate with contact if email provided
            if contact_email:
                contact_id = self.create_or_update_contact(email=contact_email)
                if contact_id:
                    try:
                        self.client.crm.deals.associations_api.create(
                            deal_id=deal.id,
                            to_object_type="contacts",
                            to_object_id=contact_id
                        )
                    except:
                        pass  # Association may fail but deal is created

            return deal.id

        except Exception as e:
            st.error(f"Failed to create deal: {str(e)}")
            return None

    def associate_deal_to_contact(
        self,
        deal_id: str,
        contact_id: str
    ) -> bool:
        """Associate a deal with a contact"""
        if not self.is_enabled():
            return False

        try:
            self.client.crm.deals.associations_api.create(
                deal_id=deal_id,
                to_object_type="contacts",
                to_object_id=contact_id,
                association_type="deal_to_contact"
            )
            return True
        except Exception as e:
            st.error(f"Failed to associate deal: {str(e)}")
            return False

    # ==================== TASK MANAGEMENT ====================

    def create_task(
        self,
        subject: str,
        notes: str,
        due_date: datetime = None,
        priority: str = "MEDIUM",
        contact_email: str = None
    ) -> Optional[str]:
        """
        Create a task in HubSpot

        Args:
            subject: Task subject/title
            notes: Task description
            due_date: When task is due
            priority: HIGH, MEDIUM, or LOW
            contact_email: Associate with this contact

        Returns:
            Task ID if successful
        """
        if not self.is_enabled():
            return None

        if due_date is None:
            due_date = datetime.now() + timedelta(days=7)

        # Convert to milliseconds timestamp
        due_timestamp = int(due_date.timestamp() * 1000)

        properties = {
            "hs_task_subject": subject,
            "hs_task_body": notes,
            "hs_task_status": "NOT_STARTED",
            "hs_task_priority": priority,
            "hs_timestamp": str(due_timestamp)
        }

        try:
            # Create task input
            task_input = SimplePublicObjectInput(properties=properties)

            # Create task
            task = self.client.crm.objects.tasks.basic_api.create(
                simple_public_object_input=task_input
            )

            # Associate with contact if provided
            if contact_email:
                contact_id = self.create_or_update_contact(email=contact_email)
                if contact_id:
                    self.client.crm.objects.tasks.associations_api.create(
                        task_id=task.id,
                        to_object_type="contacts",
                        to_object_id=contact_id,
                        association_type="task_to_contact"
                    )

            return task.id

        except Exception as e:
            st.error(f"Failed to create task: {str(e)}")
            return None

    # ==================== UTILITY FUNCTIONS ====================

    def log_chat_conversation(
        self,
        contact_email: str,
        conversation_history: List[Dict],
        conversation_summary: str = ""
    ) -> bool:
        """
        Log an AI chat conversation to HubSpot

        Args:
            contact_email: Contact's email
            conversation_history: List of messages
            conversation_summary: Summary of the conversation

        Returns:
            True if successful
        """
        if not self.is_enabled():
            return False

        # Create or update contact
        contact_id = self.create_or_update_contact(
            email=contact_email,
            additional_properties={
                "last_ai_interaction": datetime.now().strftime("%Y-%m-%d"),
                "ai_interaction_count": "1"  # Would need to increment
            }
        )

        if not contact_id:
            return False

        # Format conversation as note
        note_body = f"**AI Chat Conversation Summary**\n\n{conversation_summary}\n\n---\n\n**Full Transcript:**\n\n"

        for msg in conversation_history[-10:]:  # Last 10 messages
            role = "🤖 AI Assistant" if msg['role'] == 'assistant' else "👤 Client"
            note_body += f"\n**{role}:**\n{msg['content']}\n"

        # Add note to contact
        return self.add_note_to_contact(contact_id, note_body)

    def log_cost_estimate(
        self,
        contact_email: str,
        estimate_data: Dict,
        estimate_text: str,
        estimated_value: float
    ) -> Optional[str]:
        """
        Log a cost estimate as a HubSpot deal

        Args:
            contact_email: Contact's email
            estimate_data: Estimate input data
            estimate_text: Generated estimate text
            estimated_value: Estimated project cost

        Returns:
            Deal ID if successful
        """
        if not self.is_enabled():
            return None

        deal_name = f"{estimate_data.get('facility_type', 'Project')} - {estimate_data.get('location', 'TBD')}"

        # Create contact first
        contact_id = self.create_or_update_contact(
            email=contact_email,
            additional_properties={
                "project_type": estimate_data.get('facility_type', ''),
                "project_location": estimate_data.get('location', '')
            }
        )

        # Create deal
        deal_id = self.create_deal(
            deal_name=deal_name,
            amount=estimated_value,
            deal_stage="appointmentscheduled",
            contact_email=contact_email,
            additional_properties={
                "facility_type": estimate_data.get('facility_type', ''),
                "square_footage": str(estimate_data.get('square_footage', 0)),
                "project_location": estimate_data.get('location', ''),
                "project_timeline": estimate_data.get('timeline', '')
            }
        )

        # Add estimate as note
        if deal_id and contact_id:
            note = f"**Cost Estimate Generated**\n\n{estimate_text[:500]}...\n\n[Full estimate attached in documents]"
            self.add_note_to_contact(contact_id, note)

        return deal_id

    def log_safety_issue(
        self,
        project_name: str,
        location: str,
        severity: str,
        description: str,
        contact_email: str = None
    ) -> Optional[str]:
        """
        Create a task for a safety issue

        Args:
            project_name: Project name
            location: Issue location
            severity: CRITICAL, MODERATE, or MINOR
            description: Issue description
            contact_email: Optional contact to assign

        Returns:
            Task ID if successful
        """
        if not self.is_enabled():
            return None

        priority_map = {
            "CRITICAL": "HIGH",
            "MODERATE": "MEDIUM",
            "MINOR": "LOW"
        }

        priority = priority_map.get(severity, "MEDIUM")

        # Due date based on severity
        due_days = {
            "CRITICAL": 1,
            "MODERATE": 3,
            "MINOR": 7
        }

        due_date = datetime.now() + timedelta(days=due_days.get(severity, 7))

        subject = f"🚨 {severity} Safety Issue: {project_name}"

        notes = f"""
**Project:** {project_name}
**Location:** {location}
**Severity:** {severity}
**Detected:** {datetime.now().strftime("%Y-%m-%d %H:%M")}

**Description:**
{description}

**Action Required:**
Immediate inspection and remediation required.

---
*Detected by SE Builders AI Safety Scanner*
"""

        return self.create_task(
            subject=subject,
            notes=notes,
            due_date=due_date,
            priority=priority,
            contact_email=contact_email
        )


# ==================== GLOBAL INSTANCE ====================

# Create a global instance to be used across modules
hubspot = HubSpotIntegration()


# ==================== HELPER FUNCTIONS ====================

def show_hubspot_status():
    """Display HubSpot integration status in sidebar"""
    if not HUBSPOT_AVAILABLE:
        st.sidebar.warning("⚠️ HubSpot SDK not installed")
        st.sidebar.code("pip install hubspot-api-client")
        return False

    if hubspot.is_enabled():
        st.sidebar.success("✅ HubSpot Connected")
        return True
    else:
        st.sidebar.warning("⚠️ HubSpot Not Configured")
        st.sidebar.info("Add HUBSPOT_API_KEY to .env file")
        return False


def extract_estimated_cost(estimate_text: str) -> float:
    """
    Extract estimated cost from generated estimate text

    Args:
        estimate_text: Generated estimate text

    Returns:
        Estimated cost as float
    """
    import re

    # Look for patterns like "$1,234,567" or "Total: $XXX"
    patterns = [
        r'Total.*?\$[\d,]+',
        r'TOTAL.*?\$[\d,]+',
        r'Estimated Cost.*?\$[\d,]+',
        r'\$[\d,]{6,}'  # At least 6 digits (100,000+)
    ]

    for pattern in patterns:
        match = re.search(pattern, estimate_text, re.IGNORECASE)
        if match:
            # Extract just the number
            number_str = re.search(r'[\d,]+', match.group()).group()
            return float(number_str.replace(',', ''))

    # Default fallback
    return 0.0
