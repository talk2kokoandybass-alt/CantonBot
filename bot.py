import httpx
from aiogram import Bot, Dispatcher, types, utils

# --- CONFIG ---
TOKEN = "8289262375:AAEej81xDwPJsuwrxqZYK-XTFQ5CaQZre54"
ADS_ID = "bot-28626"
SUPA_URL = "https://sjjlzmaqxrzrrbqikjaa.supabase.co/rest/v1"
SUPA_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNqamx6bWFxeHJ6cnJicWlramFhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzcxMTg2NjUsImV4cCI6MjA5MjY5NDY2NX0.OSqefYbZW8-G9XGlw1x8xFcpAdpXfqVFLwUgATYhFLg"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
headers = {"apikey": SUPA_KEY, "Authorization": f"Bearer {SUPA_KEY}", "Content-Type": "application/json"}

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_id = message.from_user.id
    ref_by = message.get_args()

    async with httpx.AsyncClient() as client:
        # 1. Check/Register User
        check = await client.get(f"{SUPA_URL}/users?id=eq.{user_id}", headers=headers)
        if not check.json():
            await client.post(f"{SUPA_URL}/users", headers=headers, json={"id": user_id, "refs": 0})
            if ref_by and ref_by.isdigit() and int(ref_by) != user_id:
                await client.post(f"{SUPA_URL}/rpc/increment_refs", headers=headers, json={"row_id": int(ref_by)})

        # 2. Get Count
        res = await client.get(f"{SUPA_URL}/users?id=eq.{user_id}&select=refs", headers=headers)
        count = res.json()[0]['refs'] if res.json() else 0

    link = f"https://t.me/cantonclaim_bot?start={user_id}"
    ad_url = f"https://adsgram.ai/api/v1/ad?blockId={ADS_ID}&userId={user_id}"

    await message.answer(
        f"🚀 **Canton ($CC) Priority Claim Assistant**\n\n"
        f"Status: **Network Congested (94%)**\n"
        f"Your Referrals: **{count}/5**\n\n"
        f"To bypass the queue, you must invite 5 active users.\n\n"
        f"🔗 Your Link: `{link}`\n\n"
        f"👉 [VERIFY WALLET STATUS]({ad_url})",
        parse_mode="Markdown"
    )

if __name__ == '__main__':
    print("Bot is starting (Light Mode)...")
    utils.executor.start_polling(dp, skip_updates=True)
    
