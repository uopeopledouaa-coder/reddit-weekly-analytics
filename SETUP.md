# 🚀 Reddit Weekly Analytics - Quick Start Guide

## ⏱️ 5-Minute Setup

This guide will get you up and running in **5 minutes**!

### Step 1: Get Reddit API Credentials (2 min) 🤖

1. Go to https://www.reddit.com/prefs/apps
2. Click **"Create an app"** or **"Create another app"**
3. Fill in:
   - **name**: reddit-weekly-analytics
   - **app type**: script
4. Click **Create app**
5. You'll see your credentials:
   - **Client ID**: Below the app name (highlighted)
   - **Client Secret**: Click the "secret" button
6. **Copy both values** 📋

### Step 2: Create Google Cloud Project (2 min) 📊

1. Go to https://console.cloud.google.com/
2. Click **"Create a Project"**
3. Name: `reddit-analytics`
4. Click **Create**
5. Wait for activation (1-2 min)
6. Go to **APIs & Services** → **Library**
7. Search for **"Google Sheets API"**
8. Click the result → **Enable**

### Step 3: Create Service Account (1 min) 🔑

1. Go to **APIs & Services** → **Credentials**
2. Click **Create Credentials** → **Service Account**
3. Fill in:
   - **Service account name**: reddit-analytics
4. Click **Create and continue**
5. Click **Create key**
6. Choose **JSON**
7. A file downloads automatically
8. **Open it** and **copy ALL contents** (entire JSON)

### Step 4: Add GitHub Secrets (5 min) 🔐

1. Go to your GitHub repo
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret** for each:

#### Secret 1: REDDIT_CLIENT_ID
- **Name**: `REDDIT_CLIENT_ID`
- **Value**: Your Client ID from Step 1
- Click **Add secret**

#### Secret 2: REDDIT_CLIENT_SECRET
- **Name**: `REDDIT_CLIENT_SECRET`
- **Value**: Your Client Secret from Step 1
- Click **Add secret**

#### Secret 3: SUBREDDIT_NAME
- **Name**: `SUBREDDIT_NAME`
- **Value**: `python` (or any subreddit you want to track)
- Click **Add secret**

#### Secret 4: GOOGLE_SHEET_NAME
- **Name**: `GOOGLE_SHEET_NAME`
- **Value**: `Reddit Weekly Analytics`
- Click **Add secret**

#### Secret 5: GOOGLE_APPLICATION_CREDENTIALS
- **Name**: `GOOGLE_APPLICATION_CREDENTIALS`
- **Value**: Paste the **entire JSON file** from Step 3
- Click **Add secret**

✅ **You're done!**

---

## 🎬 Running the Script

### Automatic (Every Monday) ✅

The workflow runs automatically **every Monday at 8:00 AM UTC**.

To verify it works:
1. Go to **Actions** tab in your repo
2. Click **Reddit Weekly Analytics**
3. You should see runs listed

### Manual Trigger 🎯

To run it now:
1. Go to **Actions** tab
2. Click **Reddit Weekly Analytics**
3. Click **Run workflow**
4. Click **Run workflow** button
5. Wait 1-2 minutes

### Check Results 📈

1. After workflow completes, go to Google Drive
2. Find **"Reddit Weekly Analytics"** Google Sheet
3. You'll see:
   - Weekly summary (Total Posts, Score, Comments, etc.)
   - Top 10 posts
   - All posts data

---

## 🐛 Troubleshooting

### ❌ Workflow failed?

1. Click on the failed run in **Actions**
2. Check the logs for error messages
3. Common issues:
   - **"credentials not configured"** → Check GitHub Secrets (typos?)
   - **"Connection error"** → Check internet/Reddit API status
   - **"Sheet not found"** → Google credentials might be wrong

### ❌ No data in Google Sheet?

1. Check subreddit name is correct (no spaces, exact match)
2. Try running manually first
3. Check workflow logs for errors

### ❌ GitHub Secrets not working?

1. Make sure you're in the right repo
2. Check spelling exactly matches (`REDDIT_CLIENT_ID` not `reddit_client_id`)
3. Try deleting and re-adding the secret

---

## 📱 Next Steps

1. **Monitor results**: Check your Google Sheet weekly
2. **Customize**: Edit `reddit_stats.py` to track different metrics
3. **Share**: Share the Google Sheet with others
4. **Analyze**: Use Google Sheet's built-in charts

---

## 📚 Full Documentation

See [README.md](./README.md) for complete documentation.

---

## ⚡ Key Points

✅ All credentials are **private** (stored in GitHub Secrets)  
✅ Runs **automatically** every Monday  
✅ Data updates in **Google Sheets**  
✅ **Free** to use (Reddit & Google APIs have free tiers)  
✅ **No sensitive data** in repository  

---

**Have questions?** Check the README or open an Issue! 🙋
