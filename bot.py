import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.environ.get("8550413186:AAEM5QgWc-MDDUMC7B9pj0bEpeao3uI05xI")
CHANNEL_ID = "@Shadownet_plus"
CARD_NUMBER = "5859471124157979"
CRYPTO_WALLET = "TUeJitgJQrE72vffctcoz4LWhZ9XW2TyNz"
SUPPORT_USERNAME = "@Shadownet_S"
PLANS = {
    "1month": {"name": "یک ماهه", "options": [
        {"name": "۳۰ گیگ", "price": 135},
        {"name": "۴۵ گیگ", "price": 203},
        {"name": "۷۰ گیگ", "price": 315},
        {"name": "۱۰۰ گیگ", "price": 450}]},
    "2month": {"name": "دو ماهه", "options": [
        {"name": "۳۰ گیگ", "price": 150},
        {"name": "۴۵ گیگ", "price": 225},
        {"name": "۷۰ گیگ", "price": 350},
        {"name": "۱۰۰ گیگ", "price": 500},
        {"name": "۱۲۰ گیگ", "price": 600},
        {"name": "۱۵۰ گیگ", "price": 750}]},
    "3month": {"name": "سه ماهه", "options": [
        {"name": "۳۰ گیگ", "price": 150},
        {"name": "۴۵ گیگ", "price": 225},
        {"name": "۷۰ گیگ", "price": 350},
        {"name": "۱۰۰ گیگ", "price": 500},
        {"name": "۱۲۰ گیگ", "price": 600},
        {"name": "۱۵۰ گیگ", "price": 750},
        {"name": "۱۷۰ گیگ", "price": 850},
        {"name": "۲۰۰ گیگ", "price": 1000}]}
}
users = {}
def get_user(uid):
    if uid not in users:
        users[uid] = {"points": 0, "wallet": 0, "referrals": 0, "referred_by": None}
    return users[uid]
async def check_joined(update, context):
    try:
        uid = update.effective_user.id
        m = await context.bot.get_chat_member(CHANNEL_ID, uid)
        return m.status in ["member", "administrator", "creator"]
    except:
        return False
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    user = get_user(uid)
    if context.args and context.args[0].startswith("ref_"):
        rid = int(context.args[0].split("_")[1])
        if rid != uid and user["referred_by"] is None:
            user["referred_by"] = rid
            get_user(rid)["referrals"] += 1
    joined = await check_joined(update, context)
    if not joined:
        kb = [[InlineKeyboardButton("📢 عضویت در کانال", url=f"https://t.me/{CHANNEL_ID.replace('@','')}")],
              [InlineKeyboardButton("✅ عضو شدم", callback_data="check_join")]]
        await update.message.reply_text("⚠️ برای استفاده از ربات باید عضو کانال بشی!", reply_markup=InlineKeyboardMarkup(kb))
        return
    await show_menu(update, context)
async def show_menu(update, context, edit=False):
    kb = [
        [InlineKeyboardButton("🛒 خرید اشتراک", callback_data="buy")],
        [InlineKeyboardButton("🎁 تست رایگان", callback_data="free_test")],
        [InlineKeyboardButton("💎 باشگاه مشتریان", callback_data="club")],
        [InlineKeyboardButton("👥 زیرمجموعه گیری", callback_data="referral")],
        [InlineKeyboardButton("🆘 پشتیبانی", callback_data="support")],
    ]
    text = "🌐 *به ShadowNet VPN خوش اومدی!*\n\nاز منوی زیر انتخاب کن:"
    if edit:
        await update.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")
    else:
        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")
async def btn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    uid = q.from_user.id
    user = get_user(uid)
    data = q.data
    if data == "check_join":
        if await check_joined(update, context):
            await show_menu(q, context, edit=True)
        else:
            await q.answer("هنوز عضو نشدی!", show_alert=True)
        return
    if data == "buy":
        kb = [[InlineKeyboardButton("📅 یک ماهه", callback_data="plan_1month")],
              [InlineKeyboardButton("📅 دو ماهه", callback_data="plan_2month")],
              [InlineKeyboardButton("📅 سه ماهه", callback_data="plan_3month")],
              [InlineKeyboardButton("🔙 برگشت", callback_data="back")]]
        await q.edit_message_text("📦 نوع اشتراک رو انتخاب کن:", reply_markup=InlineKeyboardMarkup(kb))
    elif data.startswith("plan_"):
        pk = data[5:]
        plan = PLANS[pk]
        kb = [[InlineKeyboardButton(f"{o['name']} - {o['price']} تومن", callback_data=f"order_{pk}_{i}")] for i,o in enumerate(plan["options"])]
        kb.append([InlineKeyboardButton("🔙 برگشت", callback_data="buy")])
        await q.edit_message_text(f"📋 پلن {plan['name']}:", reply_markup=InlineKeyboardMarkup(kb))
    elif data.startswith("order_"):
        parts = data.split("_")
        idx = int(parts[-1])
        pk = "_".join(parts[1:-1])
        opt = PLANS[pk]["options"][idx]
        pts = user["points"]
        disc = 15 if pts>=100 else 10 if pts>=60 else 5 if pts>=30 else 0
        fp = opt["price"]*(100-disc)//100
        text = f"🛒 *سفارش:*\n📦 {PLANS[pk]['name']} - {opt['name']}\n💰 {opt['price']} تومن\n" + (f"🎉 تخفیف: {disc}٪\n" if disc else "") + f"💵 نهایی: {fp} تومن\n\n💳 روش پرداخت:"
        kb = [[InlineKeyboardButton("💳 کارت به کارت", callback_data=f"card_{pk}_{idx}")],
              [InlineKeyboardButton("₿ کریپتو", callback_data=f"crypto_{pk}_{idx}")],
              [InlineKeyboardButton("🔙 برگشت", callback_data=f"plan_{pk}")]]
        await q.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")
    elif data.startswith("card_"):
        await q.edit_message_text(f"💳 *کارت به کارت:*\n\nشماره کارت:\n`{CARD_NUMBER}`\n\nرسید رو بفرست! ✅", parse_mode="Markdown", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 برگشت", callback_data="buy")]]))
    elif data.startswith("crypto_"):
        await q.edit_message_text(f"₿ *کریپتو TRC20:*\n\n`{CRYPTO_WALLET}`\n\nهش تراکنش رو بفرست! ✅", parse_mode="Markdown", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 برگشت", callback_data="buy")]]))
    elif data == "free_test":
        await q.edit_message_text("🎁 *تست رایگان:*\n\n۱۰۰ مگ رایگان!\n\nبا پشتیبانی تماس بگیر 👇", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("💬 پشتیبانی", url=f"https://t.me/{SUPPORT_USERNAME.replace('@','')}")],[InlineKeyboardButton("🔙 برگشت", callback_data="back")]]), parse_mode="Markdown")
    elif data == "club":
        pts = user["points"]
        lv = "🥇 طلایی - ۱۵٪ تخفیف" if pts>=100 else "🥈 نقره‌ای - ۱۰٪ تخفیف" if pts>=60 else "🥉 برنزی - ۵٪ تخفیف" if pts>=30 else "🔰 عادی"
        await q.edit_message_text(f"💎 *باشگاه مشتریان:*\n\nامتیاز: {pts} ⭐\nسطح: {lv}\n\nهر ۵۰ تومن = ۱۰ امتیاز", parse_mode="Markdown", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 برگشت", callback_data="back")]]))
    elif data == "referral":
        rl = f"https://t.me/shadownetvpn_bot?start=ref_{uid}"
        await q.edit_message_text(f"👥 *زیرمجموعه:*\n\nلینک:\n`{rl}`\n\nزیرمجموعه: {user['referrals']} نفر\nکیف پول: {user['wallet']} تومن\n\nهر خرید = ۱۰٪ کمیسیون! 💰", parse_mode="Markdown", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 برگشت", callback_data="back")]]))
    elif data == "support":
        await q.edit_message_text("🆘 *پشتیبانی:*", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("💬 پشتیبانی", url=f"https://t.me/{SUPPORT_USERNAME.replace('@','')}")],[InlineKeyboardButton("🔙 برگشت", callback_data="back")]]), parse_mode="Markdown")
    elif data == "back":
        await show_menu(q, context, edit=True)
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(btn))
    print("✅ ربات شروع کرد!")
    app.run_polling()
if __name__ == "__main__":
    main()

