import time
import schedule
import re
import lmstudio as lms
from datetime import datetime

# Import tools
# (Make sure tools.py is in the same folder)
from tools import fetch_rss_headlines, save_to_markdown, push_to_github

# Connect to Local LLM
model = lms.llm("deepseek/deepseek-r1-0528-qwen3-8b")


def clean_ai_response(text: str) -> str:
    """
    Removes <think> tags often output by reasoning models like DeepSeek.
    """
    clean_text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
    return clean_text.strip()


def job():
    print(f"\n⏰ Job Triggered at {time.strftime('%H:%M:%S')}")

    # --- STEP 1: Fetch Data ---
    print("1. Fetching news...")
    raw_news = fetch_rss_headlines()

    if "No headlines" in raw_news:
        print("❌ No news found. Skipping cycle.")
        return

    # --- STEP 2: AI Processing ---
    print("2. Generating Summary...")

    # UPDATED PROMPT: Asked for ## headers to avoid conflict with Jekyll Title
    prompt = (
        f"You are a tech news editor. Here is the raw data:\n{raw_news}\n\n"
        "TASK: Write a short, punchy 'Smart Brevity' newsletter update for each news article.\n"
        "RULES:\n"
        "- Use standard Markdown.\n"
        "- Start with a catchy sub-headline (use ##), NOT a main header (#).\n"
        "- Group stories by theme.\n"
        "- Include the links.\n"
        "- NO introduction text. Just start writing."
    )

    try:
        response = model.respond(prompt)
        raw_output = response.content

        # Clean the output
        cleaned_text = clean_ai_response(raw_output)

        if not cleaned_text:
            print("❌ Error: AI returned empty text after cleaning.")
            return

        # --- STEP 3: INJECT JEKYLL FRONT MATTER ---
        # This is critical for Jekyll to render the post
        current_time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S -0800")
        display_title_time = datetime.now().strftime("%H:%M")

        front_matter = f"""---
layout: post
title: "AI News Update - {display_title_time}"
date: {current_time_str}
---

"""
        # Combine Header + Body
        final_post_content = front_matter + cleaned_text

        # --- STEP 4: Save File ---
        print("3. Saving to Markdown...")
        # We pass the full content (header + body) to the save tool
        saved_filename = save_to_markdown(final_post_content)
        print(f"   Saved as: {saved_filename}")

        # --- STEP 5: Upload ---
        print("4. Pushing to GitHub...")
        git_result = push_to_github()
        print(git_result)

        print("✅ Cycle Complete.")

    except Exception as e:
        print(f"❌ Error during job: {e}")


if __name__ == "__main__":
    print("--- AI News Agent Started ---")
    print("Running initial test job now...")

    # Run once immediately to verify everything works
    job()

    # Schedule for every hour
    schedule.every().hour.do(job)

    print("\nWaiting for next scheduled run... (Press Ctrl+C to stop)")
    while True:
        schedule.run_pending()
        time.sleep(1)