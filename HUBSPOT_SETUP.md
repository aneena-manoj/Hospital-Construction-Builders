# HubSpot CRM Integration Setup Guide

## 🎯 Overview

The SE Builders AI Platform now integrates seamlessly with HubSpot CRM, automatically syncing:

- **Client conversations** → HubSpot Contacts with notes
- **Cost estimates** → HubSpot Deals
- **Safety issues** → HubSpot Tasks

---

## 📋 Prerequisites

1. **HubSpot Account** (Free or Paid)
2. **API Access** (Available on all HubSpot plans)
3. **Python environment** with the SE Builders AI Platform installed

---

## 🚀 Setup Instructions

### Step 1: Get Your HubSpot API Key

1. Log in to your HubSpot account
2. Click the **Settings** icon (gear icon in the top right)
3. Navigate to **Integrations** → **API Key**
4. Click **Create API key** (or copy existing key)
5. Copy your API key (keep it secure!)

### Step 2: Install HubSpot SDK

```bash
pip install hubspot-api-client
```

Or if using the project dependencies:

```bash
pip install -e .
```

### Step 3: Configure Environment Variables

Add your HubSpot API key to your `.env` file:

```bash
# .env file

GOOGLE_API_KEY=your_google_api_key_here
HUBSPOT_API_KEY=your_hubspot_api_key_here
```

**Important**:
- Make sure `.env` is in your `.gitignore`
- Never commit API keys to version control
- Each team member should have their own `.env` file

### Step 4: Restart the Application

```bash
streamlit run app.py
```

### Step 5: Verify Connection

1. Open the app in your browser
2. Check the sidebar - you should see **"✅ HubSpot Connected"**
3. Navigate to **📊 HubSpot CRM** to verify full access

---

## ✨ Features

### 1. Client Assistant → HubSpot Contacts

**What it does:**
- Saves chat conversations as HubSpot contacts
- Adds conversation transcript as notes
- Tracks AI interaction dates

**How to use:**
1. Have a conversation with a client in the **Client Assistant**
2. Click **"💾 Save to HubSpot CRM"** in the sidebar
3. Enter client's email and optional details
4. Click **"Save to HubSpot"**

**Result in HubSpot:**
- New contact created (or existing updated)
- Conversation added as a note
- Lead source tagged as "AI Chat Assistant"

---

### 2. Cost Estimator → HubSpot Deals

**What it does:**
- Creates deals from cost estimates
- Associates deals with contacts
- Captures project details (facility type, size, location, timeline)

**How to use:**
1. Generate a cost estimate
2. Scroll to **"💾 Save to HubSpot CRM"** section
3. Enter client email and details
4. Choose:
   - **"💼 Create Deal"** - Creates deal + contact
   - **"👤 Save Contact Only"** - Just saves contact info

**Result in HubSpot:**
- New deal created with estimated value
- Deal properties include:
  - Facility type
  - Square footage
  - Location
  - Timeline
  - Project details
- Contact associated with deal
- Estimate added as contact note

---

### 3. Safety Scanner → HubSpot Tasks

**What it does:**
- Creates tasks for safety hazards
- Prioritizes by severity (Critical/Moderate/Minor)
- Sets due dates based on urgency

**How to use:**
1. Upload and scan site photos
2. After analysis, click **"📝 Create Safety Tasks"**
3. Optionally assign to a project manager's email
4. Tasks are automatically created for each hazard

**Result in HubSpot:**
- Task created for each hazard found
- Priority set by severity:
  - Critical → HIGH priority, due in 1 day
  - Moderate → MEDIUM priority, due in 3 days
  - Minor → LOW priority, due in 7 days
- Task includes:
  - Project name
  - Location
  - Full hazard description
  - OSHA references
  - Recommended actions

---

## 📊 HubSpot CRM Manager Dashboard

Navigate to **📊 HubSpot CRM** to:

### Overview Tab
- View integration statistics
- See recent activity
- Track contacts, deals, and tasks created

### Quick Actions Tab
- Manually create contacts
- Create deals
- Create tasks
- Direct access to common workflows

### Settings Tab
- View API configuration status
- Access HubSpot directly
- Troubleshooting tips

---

## 🔧 Configuration Options

### Custom Properties (Optional)

You can add custom properties to your HubSpot objects:

**In `modules/hubspot_integration.py`:**

```python
# Add custom properties when creating contacts
hubspot.create_or_update_contact(
    email="client@example.com",
    additional_properties={
        "custom_field_1": "value",
        "custom_field_2": "value"
    }
)
```

### Deal Stages

Default deal stages used:
- `appointmentscheduled` - Default for new estimates
- `qualifiedtobuy`
- `presentationscheduled`
- `decisionmakerboughtin`
- `contractsent`
- `closedwon`
- `closedlost`

You can customize these in the HubSpot CRM Manager or by modifying the integration code.

---

## 🐛 Troubleshooting

### Issue: "⚠️ HubSpot Not Configured"

**Solution:**
1. Check that `HUBSPOT_API_KEY` is in your `.env` file
2. Verify the API key is correct (no extra spaces)
3. Restart the Streamlit app
4. Check that `.env` is in the same directory as `app.py`

### Issue: "HubSpot SDK not installed"

**Solution:**
```bash
pip install hubspot-api-client
```

### Issue: API key errors or authentication failures

**Solution:**
1. Verify your API key in HubSpot settings
2. Check if the key was recently rotated
3. Try generating a new API key
4. Ensure you have API access on your HubSpot plan

### Issue: Rate limit exceeded

**Solution:**
- HubSpot free plans have rate limits (typically 100 requests per 10 seconds)
- Wait a few minutes before retrying
- Consider upgrading your HubSpot plan for higher limits
- Batch operations when possible

### Issue: Properties not showing in HubSpot

**Solution:**
1. Check if custom properties exist in HubSpot
2. Create custom properties in HubSpot Settings → Properties
3. Use exact property names (case-sensitive)
4. Verify property types match (text, number, date, etc.)

---

## 📚 API Reference

### Main Functions

#### `create_or_update_contact(email, firstname, lastname, ...)`
Creates or updates a HubSpot contact

#### `create_deal(deal_name, amount, deal_stage, ...)`
Creates a new deal

#### `create_task(subject, notes, due_date, priority, ...)`
Creates a task

#### `log_chat_conversation(contact_email, conversation_history, ...)`
Logs an AI chat conversation

#### `log_cost_estimate(contact_email, estimate_data, ...)`
Logs a cost estimate as a deal

#### `log_safety_issue(project_name, severity, description, ...)`
Creates a task for a safety issue

---

## 🔐 Security Best Practices

1. **Never commit `.env` to version control**
   ```bash
   # Add to .gitignore
   .env
   ```

2. **Rotate API keys regularly**
   - Every 90 days recommended
   - Immediately if compromised

3. **Use separate keys per environment**
   - Development key
   - Production key
   - Test key

4. **Restrict API key permissions** (if available in your HubSpot plan)

5. **Monitor API usage**
   - Check HubSpot API logs regularly
   - Set up alerts for unusual activity

---

## 📈 Benefits

✅ **Automatic lead capture** - Never lose a potential client
✅ **Complete conversation history** - All interactions logged
✅ **Pipeline tracking** - Cost estimates become deals automatically
✅ **Safety compliance** - Critical issues tracked and assigned
✅ **Time savings** - Eliminate manual data entry
✅ **Better follow-up** - Tasks ensure nothing is forgotten
✅ **Unified data** - AI insights + CRM in one place

---

## 🎓 Training Resources

### For Your Team

1. **Client Assistant Users:**
   - Always get client email during conversations
   - Use "Save to HubSpot" for qualified leads
   - Add notes about client needs

2. **Estimators:**
   - Create deals for every estimate generated
   - Include client contact info
   - Set appropriate deal stage

3. **Safety Managers:**
   - Scan sites regularly
   - Create tasks for all critical issues
   - Assign to responsible team members

### Best Practices

- **Consistent data entry**: Use standardized formats for phone, company names
- **Regular sync**: Save conversations and estimates as they happen
- **Follow up**: Check HubSpot tasks daily
- **Update statuses**: Move deals through pipeline as projects progress

---

## 🆘 Support

### Getting Help

1. Check this documentation first
2. Review the in-app help in **📊 HubSpot CRM → Settings tab**
3. Check HubSpot's API documentation: https://developers.hubspot.com/docs/api/overview
4. Contact your HubSpot support team for HubSpot-specific issues

### Feedback & Feature Requests

Have ideas for improving the integration? Want new features? Let us know!

---

## 📝 Changelog

### Version 1.0 (Current)
- ✅ Basic contact creation
- ✅ Deal creation from estimates
- ✅ Task creation for safety issues
- ✅ Conversation logging
- ✅ HubSpot CRM Manager dashboard

### Roadmap (Future)
- 🔜 Two-way sync (read from HubSpot)
- 🔜 Email automation
- 🔜 Custom reports
- 🔜 Bulk import/export
- 🔜 Advanced analytics

---

**Happy CRM-ing! 🚀**
