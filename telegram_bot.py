from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

from automation.job_scraper import scrape_jobs, save_to_excel
from automation.agent_brain import get_agent_json

TOKEN = "8764798136:AAEeM82TRhT460rbB47jozNGmlLexGmh8Cs"


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text

    await update.message.reply_text("🧠 Understanding your request...")

    # STEP 1: Use Gemma (LLM)
    data = get_agent_json(user_input)

    if not data:
        await update.message.reply_text("❌ Agent failed to understand request")
        return

    role = data.get("role", "data analyst")
    location = data.get("location", "Hyderabad")

    await update.message.reply_text(f"🔍 Scraping {role} jobs in {location}...")

    # STEP 2: Scrape jobs
    jobs = scrape_jobs(role, location, max_jobs=20)

    if len(jobs) == 0:
        await update.message.reply_text("⚠️ No jobs found. Try another query.")
        return

    # STEP 3: Save Excel
    save_to_excel(jobs, filename="output/jobs.xlsx")

    await update.message.reply_text(f"✅ Found {len(jobs)} jobs")

    # STEP 4: Send file
    try:
        with open("output/jobs.xlsx", "rb") as file:
            await update.message.reply_document(file)
    except:
        await update.message.reply_text("❌ Failed to send file")


app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT, handle_message))

print("🚀 Bot is running...")
app.run_polling()
