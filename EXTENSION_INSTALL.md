# ⚠️ REQUIRED: Install Terraform Extension First

## 🔴 CRITICAL STEP - DO THIS FIRST

Before running the pipeline, you **MUST** install the **Terraform Extension** from Azure DevOps Marketplace.

---

## ✅ Quick Install (2 minutes)

### Step 1: Go to Organization Settings
In Azure DevOps:
1. Click your **Organization** (top-left)
2. Click **Organization Settings** (bottom-left)

### Step 2: Open Extensions
1. In left menu, click **Extensions**
2. Click **Browse marketplace** (top-right)

### Step 3: Search and Install
1. Search for: `Terraform`
2. Find **"Terraform"** by **Microsoft DevLabs**
   - Should show 133,376+ installs
   - Should show "Free"
3. Click the extension
4. Click **Get it free** (top button)
5. Select your organization from dropdown
6. Click **Install**
7. **Wait 1-2 minutes** while Azure DevOps installs it

### Step 4: Verify Installation
1. Go back to **Extensions**
2. Look for **"Terraform"** in the installed list
3. Should show: ✅ **Green checkmark**
4. Should say: **Microsoft DevLabs** as publisher

---

## 🎯 What This Does

The Terraform extension provides:
- ✅ TerraformInstaller@0 task
- ✅ TerraformTaskV2@2 task  
- ✅ Azure backend integration
- ✅ State management support

**Without this extension, the pipeline won't run!**

---

## ❌ Error Without Extension

If you don't install it, you'll see:
```
A task is missing. The pipeline references a task called 'TerraformInstaller'
A task is missing. The pipeline references a task called 'TerraformTaskV2'
```

**This is the solution!**

---

## 🔗 Direct Link

Can't find it? Use this direct link:
https://marketplace.visualstudio.com/items?itemName=ms-devlabs.custom-terraform-tasks

Then:
1. Click **Get it free**
2. Select your organization
3. Click **Install**

---

## ✨ Done!

Once installed (usually takes 1-2 minutes), proceed with:
→ **[PIPELINE_SETUP.md](PIPELINE_SETUP.md)**

---

## 🆘 Still Having Issues?

### Extension Not Showing
- Clear browser cache (Ctrl+Shift+Delete)
- Wait 5 minutes
- Try different browser
- Refresh Azure DevOps

### Installation Stuck
- Check organization email for confirmation
- Try again in 5 minutes
- Contact Azure DevOps support

### Pipeline Still Failing
- Verify extension is in installed list
- Verify Service Connection exists
- Verify Variable Group exists
- Check pipeline YAML syntax

---

**👉 After installing extension, go to: [PIPELINE_SETUP.md](PIPELINE_SETUP.md)**

*Last Updated: January 27, 2026*
