import time
import schedule
import lmstudio as lms

# --- UPDATE IMPORTS HERE ---
from tools import fetch_rss_headlines, save_to_csv, save_to_markdown, push_to_github

# Connect to the local model
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
        f"Here is a list of raw RSS headlines:\n{raw_news}\n\n"
        "TASK: Summarize these into a 'Smart Brevity' style update.\n"
        "- Use a bold headline.\n"
        "- Use bullet points with the links.\n"
        "- Keep it under 200 words."
    )

    try:
        response = model.respond(prompt)
        summary_text = response.content
        print(f"🤖 AI Output generated.")

        # STEP 3: Save to Markdown (CHANGED)
        print("3. Saving to Markdown...")
        # We use the new markdown tool instead of the CSV one
        save_result = save_to_markdown(summary_text)
        print(save_result)

        # STEP 4: Push to GitHub (NEW)
        print("4. Syncing with Website...")
        git_result = push_to_github()
        print(git_result)

        print("✅ Cycle Complete.")

    except Exception as e:
        print(f"❌ Error during AI processing: {e}")


if __name__ == "__main__":
    print("--- News Pipeline Started ---")

    # Run immediately to test
    job()

    schedule.every().hour.do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)