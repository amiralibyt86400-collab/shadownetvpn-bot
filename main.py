import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.environ.get("8550413186:AAEM5QgWc-MDDUMC7B9pj0bEpeao3uI05xI")
CHANNEL_ID = "@Shadownet_plus"
CARD = "5859471124157979"
WALLET = "TUeJitgJQrE72vffctcoz4LWhZ9XW2TyNz"
SUPPORT = "@Shadownet_S"

PLANS = {
    "1m": {"n": "یک ماهه", "opts": [{"n": "۳۰ گیگ", "p": 135}, {"n": "۴۵ گیگ", "p": 203}, {"n": "۷۰ گیگ", "p": 315}, {"n": "۱۰۰ گیگ", "p": 450}]},
    "2m": {"n": "دو ماهه", "opts": [{"n": "۳۰ گیگ", "p": 150}, {"n": "۴۵ گیگ", "p": 225}, {"n": "۷۰ گیگ", "p": 350}, {"n": "۱۰۰ گیگ", "p": 500}, {"n": "۱۲۰ گیگ", "p": 600}, {"n": "۱۵۰ گیگ", "p": 750}]},
    "3m": {"n": "سه ماهه", "opts": [{"n": "۳۰ گیگ", "p": 150}, {"n": "۴۵ گیگ", "p": 225}, {"n": "۷۰ گیگ", "p": 350}, {"n": "۱۰۰ گیگ", "p": 500}, {"n": "۱۲۰ گیگ", "p": 600}, {"n": "۱۵۰ گیگ", "p": 750}, {"n": "۱۷۰ گیگ", "p": 850}, {"n": "۲۰۰ گیگ", "p": 1000}]}
}

users = {}

def get_user(u):
    if u not in users: users[u] = {"pts": 0, "wal": 0, "ref": 0, "ref_by": None}
    return users[u]

async def chk_join(upd, ctx):
    try:
        m = await ctx.bot.get_chat_member(CHANNEL_ID, upd.effective_user.id)
        return m.status in ["member", "administrator", "creator"]
    except: return False

async def start(upd: Update, ctx: ContextTypes.DEFAULT_TYPE):
    u = upd.effective_user.id
    usr = get_user(u)
    if ctx.args and ctx.args[0].startswith("ref_"):
        r = int(ctx.args[0].split("_")[1])
        if r != u and usr["ref_by"] is None:
            usr["ref_by"] = r
            get_user(r)["ref"] += 1
    if not await chk_join(upd, ctx):
        kb = [[InlineKeyboardButton("📢 کانال", url=f"https://t.me/{CHANNEL_ID.replace('@','')}")], [InlineKeyboardButton("✅ شدم", callback_data="j")]]
        await upd.message.reply_text("⚠️ عضو کانال بشو!", reply_markup=InlineKeyboardMarkup(kb))
        return
    await show_menu(upd, ctx)

async def show_menu(upd, ctx, e=False):
    kb = [[InlineKeyboardButton("🛒 خرید", callback_data="b")], [InlineKeyboardButton("🎁 تست", callback_data="t")], [InlineKeyboardButton("💎 باشگاه", callback_data="c")], [InlineKeyboardButton("👥 معرف", callback_data="r")], [InlineKeyboardButton("🆘 پشتیبانی", callback_data="s")]]
    if e: await upd.edit_message_text("🌐 *خوش اومدی!*\n\nمنو رو انتخاب کن:", reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")
    else: await upd.message.reply_text("🌐 *خوش اومدی!*\n\nمنو رو انتخاب کن:", reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

async def btn(upd: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = upd.callback_query
    await q.answer()
    u = q.from_user.id
    usr = get_user(u)
    d = q.data
    
    if d == "j":
        if await chk_join(upd, ctx): await show_menu(q, ctx, e=True)
        else: await q.answer("هنوز نشدی!", show_alert=True)
        return
    
    if d == "b":
        kb = [[InlineKeyboardButton("1️⃣", callback_data="p_1m")], [InlineKeyboardButton("2️⃣", callback_data="p_2m")], [InlineKeyboardButton("3️⃣", callback_data="p_3m")], [InlineKeyboardButton("🔙", callback_data="bk")]]
        await q.edit_message_text("📦 نوع اشتراک:", reply_markup=InlineKeyboardMarkup(kb))
    elif d.startswith("p_"):
        pk = d[2:]
        p = PLANS[pk]
        kb = [[InlineKeyboardButton(f"{o['n']} - {o['p']} تومن", callback_data=f"ord_{pk}_{i}")] for i,o in enumerate(p["opts"])] + [[InlineKeyboardButton("🔙", callback_data="b")]]
        await q.edit_message_text(f"📋 {p['n']}:", reply_markup=InlineKeyboardMarkup(kb))
    elif d.startswith("ord_"):
        pt = d.split("_")
        idx = int(pt[-1])
        pk = "_".join(pt[1:-1])
        opt = PLANS[pk]["opts"][idx]
        disc = 15 if usr["pts"]>=100 else 10 if usr["pts"]>=60 else 5 if usr["pts"]>=30 else 0
        fp = opt["p"]*(100-disc)//100
        txt = f"🛒 *سفارش:*\n{PLANS[pk]['n']} - {opt['n']}\n{opt['p']} تومن\n" + (f"تخفیف: {disc}٪\n" if disc else "") + f"نهایی: {fp} تومن"
        kb = [[InlineKeyboardButton("💳", callback_data=f"c_{pk}_{idx}")], [InlineKeyboardButton("₿", callback_data=f"cr_{pk}_{idx}")], [InlineKeyboardButton("🔙", callback_data=f"p_{pk}")]]
        await q.edit_message_text(txt, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")
    elif d.startswith("c_"):
        await q.edit_message_text(f"💳:\n`{CARD}`", parse_mode="Markdown", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙", callback_data="b")]]))
    elif d.startswith("cr_"):
        await q.edit_message_text(f"₿:\n`{WALLET}`", parse_mode="Markdown", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙", callback_data="b")]]))
    elif d == "t":
        await q.edit_message_text("🎁 تست رایگان 100 مگ", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("💬", url=f"https://t.me/{SUPPORT.replace('@','')}")], [InlineKeyboardButton("🔙", callback_data="bk")]]))
    elif d == "c":
        pt = usr["pts"]
        lv = "🥇 طلایی" if pt>=100 else "🥈 نقره" if pt>=60 else "🥉 برنزی" if pt>=30 else "🔰 عادی"
        await q.edit_message_text(f"💎 باشگاه\nامتیاز: {pt}\nسطح: {lv}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙", callback_data="bk")]]))
    elif d == "r":
        rl = f"https://t.me/shadownetvpn_bot?start=ref_{u}"
        await q.edit_message_text(f"👥\n`{rl}`\nزیرمجموعه: {usr['ref']}", parse_mode="Markdown", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙", callback_data="bk")]]))
    elif d == "s":
        await q.edit_message_text("🆘", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("💬", url=f"https://t.me/{SUPPORT.replace('@','')}")], [InlineKeyboardButton("🔙", callback_data="bk")]]))
    elif d == "bk":
        await show_menu(q, ctx, e=True)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(btn))
    print("✅ ربات شروع کرد!")
    app.run_polling()

if __name__ == "__main__":
    main()
