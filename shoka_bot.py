from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    filters, ConversationHandler, ContextTypes
)

BOT_TOKEN = "7666433350:AAEtnztPRm2s4olljqaOLiSl0Lyr08u9Y-o"
ADMIN_ID = 1571446410

(NAME, PHONE, NATIONAL_ID, MARITAL, ADDRESS, BIRTHDAY, JOB, PLAN, POSTAL, BENEFICIARY_ID, BENEFICIARY_BIRTHDAY) = range(11)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام! 👋\nبه ربات ثبت‌نام بیمه سرمایه‌گذاری شوکا خوش اومدید.\n\n"
        "لطفا به سوالات زیر پاسخ بدید تا ثبت‌نام شما انجام بشه.\n\n"
        "🟢 برای شروع، نام و نام خانوادگی خود را ارسال کنید:"
    )
    return NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['name'] = update.message.text
    await update.message.reply_text("شماره تماس را وارد کنید:")
    return PHONE

async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['phone'] = update.message.text
    await update.message.reply_text("کد ملی را وارد کنید:")
    return NATIONAL_ID

async def get_national_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['national_id'] = update.message.text
    keyboard = [["متاهل"], ["مجرد"]]
    await update.message.reply_text(
        "وضعیت تاهل خود را انتخاب کنید:",
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    )
    return MARITAL

async def get_marital(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['marital'] = update.message.text
    await update.message.reply_text("آدرس خود را وارد کنید:")
    return ADDRESS

async def get_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['address'] = update.message.text
    await update.message.reply_text("تاریخ تولد خود را وارد کنید (مثال: 1370/05/12):")
    return BIRTHDAY

async def get_birthday(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['birthday'] = update.message.text
    await update.message.reply_text("شغل خود را وارد کنید:")
    return JOB

async def get_job(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['job'] = update.message.text
    keyboard = [["ماهانه"], ["سالانه"], ["یکجا"]]
    await update.message.reply_text(
        "لطفا طرح مورد نظر خود را انتخاب کنید:",
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    )
    return PLAN

async def get_plan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['plan'] = update.message.text
    await update.message.reply_text("کد پستی خود را وارد کنید:")
    return POSTAL

async def get_postal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['postal'] = update.message.text
    await update.message.reply_text("کد ملی ذینفع در صورت فوت را وارد کنید:")
    return BENEFICIARY_ID

async def get_beneficiary_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['beneficiary_id'] = update.message.text
    await update.message.reply_text("تاریخ تولد ذینفع را وارد کنید (مثال: 1390/03/10):")
    return BENEFICIARY_BIRTHDAY

async def get_beneficiary_birthday(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['beneficiary_birthday'] = update.message.text

    info = context.user_data
    message = (
        f"📝 اطلاعات ثبت شده:\n\n"
        f"👤 نام: {info['name']}\n"
        f"📞 شماره تماس: {info['phone']}\n"
        f"🆔 کد ملی: {info['national_id']}\n"
        f"💍 وضعیت تاهل: {info['marital']}\n"
        f"🏠 آدرس: {info['address']}\n"
        f"🎂 تاریخ تولد: {info['birthday']}\n"
        f"💼 شغل: {info['job']}\n"
        f"📅 طرح انتخابی: {info.get('plan', 'ثبت نشده')}\n"
        f"📮 کد پستی: {info['postal']}\n"
        f"👨‍👩‍👦‍👦 کد ملی ذینفع: {info['beneficiary_id']}\n"
        f"🎂 تولد ذینفع: {info['beneficiary_birthday']}"
    )
    await context.bot.send_message(chat_id=ADMIN_ID, text=message)
    await update.message.reply_text(
        "✅ اطلاعات شما با موفقیت ثبت شد.\n"
        "لینک پرداخت به زودی از طرف شرکت برای شما ارسال می‌شود.\n\n"
        "ممنون از اعتمادتون 🙏"
    )
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("فرآیند لغو شد.")
    return ConversationHandler.END

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
            NATIONAL_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_national_id)],
            MARITAL: [MessageHandler(filters.Regex("^(متاهل|مجرد)$"), get_marital)],
            ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_address)],
            BIRTHDAY: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_birthday)],
            JOB: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_job)],
            PLAN: [MessageHandler(filters.Regex("^(ماهانه|سالانه|یکجا)$"), get_plan)],
            POSTAL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_postal)],
            BENEFICIARY_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_beneficiary_id)],
            BENEFICIARY_BIRTHDAY: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_beneficiary_birthday)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        allow_reentry=True,
    )

    app.add_handler(conv_handler)
    app.run_polling()

if __name__ == "__main__":
    main()
