import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

import os
TOKEN = os.environ.get("8550413186:AAHCJcFJbyZL4cI8CnXQbOnaYVJMj93G_qw")
ADMIN_ID = 8358016499
CHANNEL_ID = "@Shadownet_plus"
CARD_NUMBER = "5859471124157979"
CRYPTO_WALLET = "TUeJitgJQrE72vffctcoz4LWhZ9XW2TyNz"
SUPPORT_USERNAME = "@Shadownet_S"

PLANS = {
    "1month": {
        "name": "یک ماهه",
        "options": [
            {"name": "۳۰ گیگ", "price": 135},
            {"name": "۴۵ گیگ", "price": 203},
            {"name": "۷۰ گیگ", "price": 315},
            {"name": "۱۰۰ گیگ", "price": 450},
        ]
    },
    "2month": {
        "name": "دو ماهه",
        "options": [
            {"name": "۳۰ گیگ", "price": 150},
            {"name": "۴۵ گیگ", "price": 225},
            {"name": "۷۰ گیگ", "price": 350},
            {"name": "۱۰۰ گیگ", "price": 500},
            {"name": "۱۲۰ گیگ", "price": 600},
            {"name": "۱۵۰ گیگ", "price": 750},
        ]
    },
    "3month": {
        "name": "سه ماهه",
        "options": [
            {"name": "۳۰ گیگ", "price": 150},
            {"name": "۴۵ گیگ", "price": 225},
            {"name": "۷۰ گیگ", "price": 350},
            {"name": "۱۰۰ گیگ", "price": 500},
            {"name": "۱۲۰ گیگ", "price": 600},
            {"name": "۱۵۰ گیگ", "price": 750},
            {"name": "۱۷۰ گیگ", "price": 850},
            {"name": "۲۰۰ گیگ", "price": 1000},
        ]
    }
}

users = {}

def get_user(user_id):
    if user_id not in users:
        users[user_id] = {"points": 0, "wallet": 0, "referrals": 0, "referred_by": None, "joined": False}
    return users[user_id]

async def check_joined(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    try:
        member = await context.bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False
      async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = get_user(user_id)

    if context.args and context.args[0].startswith("ref_"):
        referrer_id = int(context.args[0].split("_")[1])
        if referrer_id != user_id and user["referred_by"] is None:
            user["referred_by"] = referrer_id
            get_user(referrer_id)["referrals"] += 1

    joined = await check_joined(update, context)
    if not joined:
        keyboard = [[InlineKeyboardButton("📢 عضویت در کانال", url=f"https://t.me/{CHANNEL_ID.replace('@', '')}")],
                    [InlineKeyboardButton("✅ عضو شدم", callback_data="check_join")]]
        await update.message.reply_text(
            "⚠️ برای استفاده از ربات باید اول عضو کانال ما بشی!\n\n"
            "👇 روی دکمه کلیک کن و عضو شو:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    await show_main_menu(update, context)

async def show_main_menu(update, context, edit=False):
    keyboard = [
        [InlineKeyboardButton("🛒 خرید اشتراک", callback_data="buy")],
        [InlineKeyboardButton("🎁 تست رایگان", callback_data="free_test")],
        [InlineKeyboardButton("💎 باشگاه مشتریان", callback_data="club")],
        [InlineKeyboardButton("👥 زیرمجموعه گیری", callback_data="referral")],
        [InlineKeyboardButton("🆘 پشتیبانی", callback_data="support")],
    ]
    text = "🌐 *به ShadowNet VPN خوش اومدی!*\n\nاز منوی زیر انتخاب کن:"
    if edit:
        await update.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
    else:
        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    user = get_user(user_id)
    data = query.data

    if data == "check_join":
        joined = await check_joined(update, context)
        if joined:
            await show_main_menu(query, context, edit=True)
        else:
            await query.answer("هنوز عضو نشدی! اول عضو کانال شو ✅", show_alert=True)
        return

    joined = await check_joined(update, context)
    if not joined:
        keyboard = [[InlineKeyboardButton("📢 عضویت در کانال", url=f"https://t.me/{CHANNEL_ID.replace('@', '')}")],
                    [InlineKeyboardButton("✅ عضو شدم", callback_data="check_join")]]
        await query.edit_message_text(
            "⚠️ باید اول عضو کانال ما بشی!",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    if data == "buy":
        keyboard = [
            [InlineKeyboardButton("📅 یک ماهه", callback_data="plan_1month")],
            [InlineKeyboardButton("📅 دو ماهه", callback_data="plan_2month")],
            [InlineKeyboardButton("📅 سه ماهه", callback_data="plan_3month")],
            [InlineKeyboardButton("🔙 برگشت", callback_data="back")],
        ]
        await query.edit_message_text("📦 نوع اشتراک رو انتخاب کن:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data.startswith("plan_"):
        plan_key = data[5:]
        plan = PLANS[plan_key]
        keyboard = []
        for i, opt in enumerate(plan["options"]):
            keyboard.append([InlineKeyboardButton(
                f"{opt['name']} - {opt['price']} تومن",
                callback_data=f"order_{plan_key}_{i}"
            )])
        keyboard.append([InlineKeyboardButton("🔙 برگشت", callback_data="buy")])
        await query.edit_message_text(f"📋 پلن {plan['name']} رو انتخاب کن:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data.startswith("order_"):
        parts = data.split("_")
        idx = int(parts[-1])
        plan_key = "_".join(parts[1:-1])
        plan = PLANS[plan_key]
        opt = plan["options"][idx]

        discount = 0
        points = user["points"]
        if points >= 100:
            discount = 15
        elif points >= 60:
            discount = 10
        elif points >= 30:
            discount = 5

        final_price = opt["price"] * (100 - discount) // 100

        text = (
            f"🛒 *سفارش شما:*\n"
            f"📦 پلن: {plan['name']} - {opt['name']}\n"
            f"💰 قیمت: {opt['price']} تومن\n"
            + (f"🎉 تخفیف باشگاه: {discount}٪\n" if discount > 0 else "")
            + f"💵 مبلغ نهایی: {final_price} تومن\n\n"
            f"💳 *روش پرداخت رو انتخاب کن:*"
        )
        keyboard = [
            [InlineKeyboardButton("💳 کارت به کارت", callback_data=f"pay_card_{plan_key}_{idx}")],
            [InlineKeyboardButton("₿ کریپتو", callback_data=f"pay_crypto_{plan_key}_{idx}")],
            [InlineKeyboardButton("🔙 برگشت", callback_data=f"plan_{plan_key}")],
        ]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
    elif data.startswith("pay_card_"):
        await query.edit_message_text(
            f"💳 *پرداخت کارت به کارت:*\n\n"
            f"شماره کارت:\n`{CARD_NUMBER}`\n\n"
            f"بعد از پرداخت رسید رو برام بفرست تا کانفیگت رو بدم! ✅",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 برگشت", callback_data="buy")]])
        )

    elif data.startswith("pay_crypto_"):
        await query.edit_message_text(
            f"₿ *پرداخت کریپتو (TRC20):*\n\n"
            f"آدرس ولت:\n`{CRYPTO_WALLET}`\n\n"
            f"بعد از پرداخت هش تراکنش رو بفرست! ✅",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 برگشت", callback_data="buy")]])
        )

    elif data == "free_test":
        await query.edit_message_text(
            "🎁 *تست رایگان:*\n\n"
            "۱۰۰ مگ حجم رایگان برای تست!\n\n"
            "برای دریافت با پشتیبانی در تماس باش 👇",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("💬 پشتیبانی", url=f"https://t.me/{SUPPORT_USERNAME.replace('@', '')}")],
                [InlineKeyboardButton("🔙 برگشت", callback_data="back")]
            ]),
            parse_mode="Markdown"
        )

    elif data == "club":
        points = user["points"]
        if points >= 100:
            level = "🥇 طلایی"
            discount = "۱۵٪ تخفیف + ۱ گیگ هدیه"
        elif points >= 60:
            level = "🥈 نقره‌ای"
            discount = "۱۰٪ تخفیف"
        elif points >= 30:
            level = "🥉 برنزی"
            discount = "۵٪ تخفیف"
        else:
            level = "🔰 عادی"
            discount = "هنوز تخفیف نداری"

        await query.edit_message_text(
            f"💎 *باشگاه مشتریان ShadowNet:*\n\n"
            f"امتیاز شما: {points} ⭐\n"
            f"سطح: {level}\n"
            f"مزایا: {discount}\n\n"
            f"به ازای هر ۵۰ تومن خرید = ۱۰ امتیاز",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 برگشت", callback_data="back")]]),
        )

    elif data == "referral":
        ref_link = f"https://t.me/shadownetvpn_bot?start=ref_{user_id}"
        referrals = user["referrals"]
        wallet = user["wallet"]
        await query.edit_message_text(
            f"👥 *زیرمجموعه گیری:*\n\n"
            f"لینک اختصاصی شما:\n`{ref_link}`\n\n"
            f"تعداد زیرمجموعه: {referrals} نفر\n"
            f"کیف پول: {wallet} تومن\n\n"
            f"به ازای هر خرید زیرمجموعه = ۱۰٪ کمیسیون برای شما! 💰",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 برگشت", callback_data="back")]]),
        )

    elif data == "support":
        await query.edit_message_text(
            "🆘 *پشتیبانی ShadowNet:*\n\n"
            "برای ارتباط با پشتیبانی کلیک کن 👇",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("💬 پشتیبانی", url=f"https://t.me/{SUPPORT_USERNAME.replace('@', '')}")],
                [InlineKeyboardButton("🔙 برگشت", callback_data="back")]
            ]),
            parse_mode="Markdown"
        )

    elif data == "back":
        await show_main_menu(query, context, edit=True)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("✅ ربات ShadowNet شروع کرد!")
    app.run_polling()

if __name__ == "__main__":
    main()


