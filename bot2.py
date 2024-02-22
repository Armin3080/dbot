from telegram.ext import Updater, CommandHandler
import subprocess

# متغیر گلوبال برای نگه‌داشتن پردازه فعلی
current_process = None

# تابعی که با دستور /run فراخوانی می‌شود
def run_script(update, context):
    global current_process
    
    if current_process and current_process.poll() is None:
        update.message.reply_text('یک فایل پایتون دیگر در حال اجرا است. لطفاً منتظر بمانید یا آن را لغو کنید.')
        return
    
    # اجرای فایل پایتون
    process = subprocess.Popen(['python', 'script.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    current_process = process
    update.message.reply_text('فایل پایتون در حال اجرا است. جهت لغو اجرا دستور /cancel را ارسال کنید.')
    
    # گرفتن خروجی از فرآیند
    stdout, stderr = process.communicate()
    output = stdout.decode() if stdout else stderr.decode()
    
    # ارسال خروجی به کاربر
    update.message.reply_text(output)

# تابعی که با دستور /cancel فراخوانی می‌شود
def cancel_script(update, context):
    global current_process
    
    if current_process and current_process.poll() is None:
        current_process.terminate()
        update.message.reply_text('اجرای فایل پایتون کنسل شد.')
    else:
        update.message.reply_text('هیچ فایل پایتونی در حال اجرا نیست.')

def main():
    # توکن ربات تلگرامی خود را وارد کنید
    token = '6077795668:AAGcdtB1SvIAkk4BLf8NggGOYFKfgLataTg'
    updater = Updater(token, use_context=True)
    dp = updater.dispatcher
    
    # اضافه کردن دستور /run به ربات
    dp.add_handler(CommandHandler('run', run_script))
    
    # اضافه کردن دستور /cancel به ربات
    dp.add_handler(CommandHandler('cancel', cancel_script))
    
    # شروع برنامه
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
