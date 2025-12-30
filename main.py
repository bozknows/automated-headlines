import time
import schedule
import re
import lmstudio as lms

# Import tools
from tools import fetch_rss_headlines, save_to_markdown, push_to_github

# Connect to Local LLM
model = lms.llm("deepseek/deepseek-r1-0528-qwen3-8b")


def clean_ai_response(text: str) -> str:
    """
    Removes <think> tags often output by reasoning models like DeepSeek.
    """
    # Regex to remove anything between <think> and </think>
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

    prompt = (
        f"You are a tech news editor. Here is the raw data:\n{raw_news}\n\n"
        "TASK: Write a short, punchy 'Smart Brevity' newsletter update.\n"
        "RULES:\n"
        "- Use standard Markdown (## for headers, * for bullets).\n"
        "- Start with a single catchy main headline (use #).\n"
        "- Group stories by theme.\n"
        "- Include the links.\n"
        "- NO introduction text (like 'Here is the summary'). Just start writing."
    )

    try:
        response = model.respond(prompt)
        raw_output = response.content

        # Clean the output (Remove "thinking" blocks)
        summary_text = clean_ai_response(raw_output)

        # Debugging: Show exactly what we got
        print(f"--- AI RESPONSE ({len(summary_text)} chars) ---")
        print(summary_text[:100] + "...")  # Print first 100 chars
        print("----------------------------------------------")

        if not summary_text:
            print("❌ Error: AI return empty text after cleaning.")
            return

        # --- STEP 3: Save File ---
        print("3. Saving to Markdown...")
        save_result = save_to_markdown(summary_text)
        print(save_result)

        # --- STEP 4: Upload ---
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