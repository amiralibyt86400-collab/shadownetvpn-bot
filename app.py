import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.environ.get("8550413186:AAG-Euvc1zJS3mlIJwVNHE1nUpEektsxr60")
CHANNEL = "@Shadownet_plus"
CARD = "5859471124157979"
WALLET = "TUeJitgJQrE72vffctcoz4LWhZ9XW2TyNz"
SUPPORT = "@Shadownet_S"

PLANS = {
    "1m": {"name": "یک ماهه", "items": [
        {"name": "۳۰ گیگ", "price": 135},
        {"name": "۴۵ گیگ", "price": 203},
        {"name": "۷۰ گیگ", "price": 315},
        {"name": "۱۰۰ گیگ", "price": 450}
    ]},
    "2m": {"name": "دو ماهه", "items": [
        {"name": "۳۰ گیگ", "price": 150},
        {"name": "۴۵ گیگ", "price": 225},
        {"name": "۷۰ گیگ", "price": 350},
        {"name": "۱۰۰ گیگ", "price": 500},
        {"name": "۱۲۰ گیگ", "price": 600},
        {"name": "۱۵۰ گیگ", "price": 750}
    ]},
    "3m": {"name": "سه ماهه", "items": [
        {"name": "۳۰ گیگ", "price": 150},
        {"name": "۴۵ گیگ", "price": 225},
        {"name": "۷۰ گیگ", "price": 350},
        {"name": "۱۰۰ گیگ", "price": 500},
        {"name": "۱۲۰ گیگ", "price": 600},
        {"name": "۱۵۰ گیگ", "price": 750},
        {"name": "۱۷۰ گیگ", "price": 850},
        {"name": "۲۰۰ گیگ", "price": 1000}
    ]}
}

users = {}

def get_user(uid):
    if uid not in users:
        users[uid] = {"points": 0, "wallet": 0, "referrals": 0}
    return users[uid]

async def check_channel(update, context):
    try:
        member = await context.bot.get_chat_member(CHANNEL, update.effective_user.id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_channel(update, context):
        kb = [[InlineKeyboardButton("📢 کانال", url=f"https://t.me/{CHANNEL.replace('@','')}")],
              [InlineKeyboardButton("✅ عضو شدم", callback_data="join")]]
        await update.message.reply_text("⚠️ اول عضو کانال شو!", reply_markup=InlineKeyboardMarkup(kb))
        return
    await main_menu(update, context)

async def main_menu(update, context, edit=False):
    kb = [[InlineKeyboardButton("🛒 خرید", callback_data="buy")],
          [InlineKeyboardButton("🎁 تست رایگان", callback_data="test")],
          [InlineKeyboardButton("💎 باشگاه", callback_data="club")],
          [InlineKeyboardButton("👥 معرف", callback_data="ref")],
          [InlineKeyboardButton("🆘 پشتیبانی", callback_data="support")]]
    text = "🌐 *ShadowNet VPN*\n\nمنو رو انتخاب کن:"
    if edit:
        await update.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")
    else:
        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    uid = query.from_user.id
    user = get_user(uid)
    data = query.data

    if data == "join":
        if await check_channel(update, context):
            await main_menu(query, context, edit=True)
        else:
            await query.answer("هنوز عضو نشدی!", show_alert=True)
        return

    if data == "buy":
        kb = [[InlineKeyboardButton("۱ ماهه", callback_data="p_1m")],
              [InlineKeyboardButton("۲ ماهه", callback_data="p_2m")],
              [InlineKeyboardButton("۳ ماهه", callback_data="p_3m")],
              [InlineKeyboardButton("🔙", callback_data="back")]]
        await query.edit_message_text("📦 مدت زمان:", reply_markup=InlineKeyboardMarkup(kb))

    elif data.startswith("p_"):
        pk = data[2:]
        plan = PLANS[pk]
        kb = [[InlineKeyboardButton(f"{item['name']} - {item['price']} تومن", callback_data=f"order_{pk}_{i}")] 
              for i, item in enumerate(plan["items"])]
        kb.append([InlineKeyboardButton("🔙", callback_data="buy")])
        await query.edit_message_text(f"📋 {plan['name']}:", reply_markup=InlineKeyboardMarkup(kb))

    elif data.startswith("order_"):
        parts = data.split("_")
        pk = "_".join(parts[1:-1])
        idx = int(parts[-1])
        item = PLANS[pk]["items"][idx]
        
        discount = 0
        if user["points"] >= 100:
            discount = 15
        elif user["points"] >= 60:
            discount = 10
        elif user["points"] >= 30:
            discount = 5
        
        final = item["price"] * (100 - discount) // 100
        
        text = f"🛒 *سفارش:*\n{PLANS[pk]['name']} - {item['name']}\n{item['price']} تومن\n"
        if discount:
            text += f"تخفیف: {discount}٪\n"
        text += f"*نهایی: {final} تومن*"
        
        kb = [[InlineKeyboardButton("💳 کارت", callback_data=f"card_{pk}_{idx}")],
              [InlineKeyboardButton("₿ کریپتو", callback_data=f"crypto_{pk}_{idx}")],
              [InlineKeyboardButton("🔙", callback_data=f"p_{pk}")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

    elif data.startswith("card_"):
        await query.edit_message_text(f"💳 *شماره کارت:*\n`{CARD}`\n\nرسید رو بفرست!", 
                                     parse_mode="Markdown", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙", callback_data="buy")]]))

    elif data.startswith("crypto_"):
        await query.edit_message_text(f"₿ *آدرس ولت:*\n`{WALLET}`\n\nهش تراکنش رو بفرست!", 
                                     parse_mode="Markdown", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙", callback_data="buy")]]))

    elif data == "test":
        await query.edit_message_text("🎁 *تست رایگان*\n\n۱۰۰ مگ رایگان\n\nبا پشتیبانی تماس بگیر:", 
                                     reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("💬", url=f"https://t.me/{SUPPORT.replace('@','')}")],
                                                                        [InlineKeyboardButton("🔙", callback_data="back")]]), parse_mode="Markdown")

    elif data == "club":
        pts = user["points"]
        level = "🥇 طلایی (۱۵٪)" if pts >= 100 else "🥈 نقره (۱۰٪)" if pts >= 60 else "🥉 برنزی (۵٪)" if pts >= 30 else "🔰 عادی"
        await query.edit_message_text(f"💎 *باشگاه*\n\nامتیاز: {pts} ⭐\nسطح: {level}\n\nهر ۵۰ تومن = ۱۰ امتیاز", 
                                     parse_mode="Markdown", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙", callback_data="back")]]))

    elif data == "ref":
        ref_link = f"https://t.me/shadownetvpn_bot?start=ref_{uid}"
        await query.edit_message_text(f"👥 *لینک معرف:*\n`{ref_link}`\n\nزیرمجموعه: {user['referrals']}\n\nهر خرید = ۱۰٪ کمیسیون", 
                                     parse_mode="Markdown", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙", callback_data="back")]]))

    elif data == "support":
        await query.edit_message_text("🆘 *پشتیبانی*", 
                                     reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("💬", url=f"https://t.me/{SUPPORT.replace('@','')}")],
                                                                        [InlineKeyboardButton("🔙", callback_data="back")]]), parse_mode="Markdown")

    elif data == "back":
        await main_menu(query, context, edit=True)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_click))
    print("✅ ربات شروع کرد!")
    app.run_polling()

if __name__ == "__main__":
    main()
