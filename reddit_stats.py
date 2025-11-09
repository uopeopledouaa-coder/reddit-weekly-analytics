#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reddit Weekly Analytics Script
Automatically fetches Reddit posts, analyzes engagement, and exports to Google Sheets
"""

import os
import praw
import pandas as pd
from datetime import datetime, timedelta
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json

# ===== CONFIGURATION =====
REDDIT_CLIENT_ID = os.environ.get('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = os.environ.get('REDDIT_CLIENT_SECRET')
REDDIT_USER_AGENT = 'RedditWeeklyAnalytics/1.0'
SUBREDDIT_NAME = os.environ.get('SUBREDDIT_NAME', 'python')  # Default: python

GOOGLE_SHEET_NAME = os.environ.get('GOOGLE_SHEET_NAME', 'Reddit Weekly Analytics')
GOOGLE_CREDS_JSON = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')

# ===== REDDIT DATA FETCHING =====
def fetch_reddit_posts(subreddit_name, days=7, limit=1000):
    """
    Fetch posts from a subreddit for the last 'days' days
    """
    print(f"[INFO] Connecting to Reddit API...")
    reddit = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent=REDDIT_USER_AGENT
    )
    
    subreddit = reddit.subreddit(subreddit_name)
    now = datetime.utcnow()
    start_of_week = now - timedelta(days=days)
    
    posts_data = []
    print(f"[INFO] Fetching posts from r/{subreddit_name}...")
    
    for submission in subreddit.new(limit=limit):
        created_date = datetime.utcfromtimestamp(submission.created_utc)
        if created_date < start_of_week:
            continue
        
        posts_data.append({
            'id': submission.id,
            'title': submission.title,
            'score': submission.score,
            'num_comments': submission.num_comments,
            'author': str(submission.author),
            'created_utc': submission.created_utc,
            'created_date': created_date.strftime('%Y-%m-%d %H:%M:%S'),
            'url': f"https://reddit.com{submission.permalink}",
            'selftext': submission.selftext[:200] if submission.selftext else '',
        })
    
    print(f"[INFO] Fetched {len(posts_data)} posts from the last {days} days")
    return pd.DataFrame(posts_data)

# ===== ANALYTICS =====
def analyze_engagement(df):
    """
    Perform statistical analysis on Reddit posts
    """
    if df.empty:
        print("[WARNING] No data to analyze")
        return {}
    
    # Top posts by score
    top_posts = df.nlargest(10, 'score')[['title', 'score', 'num_comments', 'url']]
    
    # Engagement metrics
    total_posts = len(df)
    total_score = df['score'].sum()
    total_comments = df['num_comments'].sum()
    avg_score = df['score'].mean()
    avg_comments = df['num_comments'].mean()
    
    # Engagement rate (simple formula)
    engagement_rate = (total_score + total_comments) / total_posts if total_posts > 0 else 0
    
    analytics = {
        'total_posts': total_posts,
        'total_score': int(total_score),
        'total_comments': int(total_comments),
        'avg_score': round(avg_score, 2),
        'avg_comments': round(avg_comments, 2),
        'engagement_rate': round(engagement_rate, 2),
        'top_posts': top_posts
    }
    
    print(f"[INFO] Analytics completed:")
    print(f"  - Total Posts: {total_posts}")
    print(f"  - Total Score: {int(total_score)}")
    print(f"  - Engagement Rate: {round(engagement_rate, 2)}")
    
    return analytics

# ===== GOOGLE SHEETS EXPORT =====
def export_to_google_sheets(df, analytics, sheet_name):
    """
    Export data to Google Sheets with weekly worksheet
    """
    print(f"[INFO] Connecting to Google Sheets...")
    
    # Setup credentials
    if GOOGLE_CREDS_JSON:
        creds_dict = json.loads(GOOGLE_CREDS_JSON)
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    else:
        print("[ERROR] Google credentials not found")
        return
    
    gc = gspread.authorize(credentials)
    
    # Open or create spreadsheet
    try:
        sheet = gc.open(sheet_name)
    except:
        print(f"[INFO] Creating new spreadsheet: {sheet_name}")
        sheet = gc.create(sheet_name)
        sheet.share('', perm_type='anyone', role='reader')  # Make it readable
    
    # Create worksheet for current week
    now = datetime.utcnow()
    week_name = now.strftime("%Y-W%W")
    
    try:
        worksheet = sheet.worksheet(week_name)
        print(f"[INFO] Worksheet '{week_name}' already exists, clearing it...")
        worksheet.clear()
    except:
        print(f"[INFO] Creating new worksheet: {week_name}")
        worksheet = sheet.add_worksheet(title=week_name, rows=1000, cols=20)
    
    # Write analytics summary
    row = 1
    worksheet.update_acell(f'A{row}', 'REDDIT WEEKLY ANALYTICS')
    row += 1
    worksheet.update_acell(f'A{row}', f'Week: {week_name}')
    row += 1
    worksheet.update_acell(f'A{row}', f'Generated: {now.strftime("%Y-%m-%d %H:%M:%S")} UTC')
    row += 2
    
    worksheet.update_acell(f'A{row}', 'SUMMARY METRICS')
    row += 1
    for key, value in analytics.items():
        if key != 'top_posts':
            worksheet.update_acell(f'A{row}', key.replace('_', ' ').title())
            worksheet.update_acell(f'B{row}', str(value))
            row += 1
    
    row += 2
    worksheet.update_acell(f'A{row}', 'TOP 10 POSTS')
    row += 1
    
    # Write top posts
    headers = ['Title', 'Score', 'Comments', 'URL']
    for col, header in enumerate(headers, start=1):
        worksheet.update_cell(row, col, header)
    row += 1
    
    for idx, post in analytics['top_posts'].iterrows():
        worksheet.update_cell(row, 1, post['title'][:100])
        worksheet.update_cell(row, 2, int(post['score']))
        worksheet.update_cell(row, 3, int(post['num_comments']))
        worksheet.update_cell(row, 4, post['url'])
        row += 1
    
    row += 2
    worksheet.update_acell(f'A{row}', 'ALL POSTS')
    row += 1
    
    # Write all posts data
    all_headers = list(df.columns)
    for col, header in enumerate(all_headers, start=1):
        worksheet.update_cell(row, col, header)
    row += 1
    
    for idx, post_row in df.iterrows():
        for col, value in enumerate(post_row, start=1):
            worksheet.update_cell(row, col, str(value))
        row += 1
        if row > 999:  # Prevent overflow
            print("[WARNING] Reached row limit, truncating data")
            break
    
    print(f"[SUCCESS] Data exported to Google Sheets: {sheet.url}")
    return sheet.url

# ===== MAIN EXECUTION =====
def main():
    """
    Main execution function
    """
    print("="*50)
    print("Reddit Weekly Analytics - Starting...")
    print("="*50)
    
    # Validate configuration
    if not REDDIT_CLIENT_ID or not REDDIT_CLIENT_SECRET:
        print("[ERROR] Reddit credentials not configured")
        return
    
    if not GOOGLE_CREDS_JSON:
        print("[ERROR] Google Sheets credentials not configured")
        return
    
    # Fetch data
    df = fetch_reddit_posts(SUBREDDIT_NAME, days=7, limit=1000)
    
    if df.empty:
        print("[WARNING] No posts found for analysis")
        return
    
    # Analyze
    analytics = analyze_engagement(df)
    
    # Export
    sheet_url = export_to_google_sheets(df, analytics, GOOGLE_SHEET_NAME)
    
    print("="*50)
    print(f"[SUCCESS] Process completed!")
    print(f"[INFO] View results: {sheet_url}")
    print("="*50)

if __name__ == "__main__":
    main()
