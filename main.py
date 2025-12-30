import time
import schedule
import lmstudio as lms

# Import the specific tools we need
from tools import fetch_rss_headlines, save_to_markdown, push_to_github

# Connect to the local model
# Ensure this exact model ID matches what is LOADED in LM Studio
model = lms.llm("deepseek/deepseek-r1-0528-qwen3-8b")


def job():
    print(f"\n⏰ Job Triggered at {time.strftime('%H:%M:%S')}")

    # STEP 1: Fetch
    print("1. Fetching news manually...")
    raw_news = fetch_rss_headlines()

    if "No headlines" in raw_news:
        print("❌ No news found. Skipping.")
        return

    # STEP 2: Summarize
    print("2. Sending to AI for summarization...")
    prompt = (
        f"Here is a list of raw RSS headlines from various sources:\n{raw_news}\n\n"
        "TASK: Create a 'Smart Brevity' style newsletter.\n"
        "- Start with one catchy main headline.\n"
        "- Group stories by topic if possible.\n"
        "- Use bullet points with the links provided.\n"
        "- Keep the tone professional but punchy.\n"
        "- Do not use 'Here is the summary'—just start writing the newsletter."
    )

    try:
        # We use .respond() to get a direct text string
        response = model.respond(prompt)
        summary_text = response.content
        print(f"🤖 AI Output generated ({len(summary_text)} chars).")

        # STEP 3: Save to Markdown
        print("3. Saving to Markdown...")
        save_result = save_to_markdown(summary_text)
        print(save_result)

        # STEP 4: Push to GitHub
        print("4. Syncing with Website...")
        git_result = push_to_github()
        print(git_result)

        print("✅ Cycle Complete.")

    except Exception as e:
        print(f"❌ Error during AI processing: {e}")


if __name__ == "__main__":
    print("--- News Pipeline Started ---")

    # Run immediately to test functionality
    job()

    # Schedule the job to run every hour
    schedule.every().hour.do(job)

    print("Waiting for next schedule... (Press Ctrl+C to stop)")
    while True:
        schedule.run_pending()
        time.sleep(1)