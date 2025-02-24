import os
import telegram
from telegram.ext import Updater, CommandHandler
import requests

# 从环境变量获取 Telegram Bot Token
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

# 查询 Tron 网络 USDT (TRC-20) 余额
def get_usdt_balance(address):
    try:
        # TronGrid API 端点（免费，无需 API 密钥）
        url = f"https://api.trongrid.io/v1/accounts/{address}"
        headers = {"Accept": "application/json"}
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            # 检查 TRC-20 代币数据是否存在
            trc20_tokens = data.get("data", [{}])[0].get("trc20", [])
            # USDT 的合约地址是 TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t
            usdt_balance = 0
            for token in trc20_tokens:
                if "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t" in token:
                    usdt_balance = int(token["TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"]) / 10**6  # USDT 有 6 位小数
                    break
            return usdt_balance
        else:
            return "无法获取余额，请检查地址或稍后重试"
    except Exception as e:
        return f"查询失败：{str(e)}"

# /start 命令
def start(update, context):
    user = update.message.from_user
    message = f"你好，{user.first_name}！我是 USDT 余额查询机器人。\n发送 /balance <TRON地址> 查询余额，例如：\n/balance TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

# /balance 命令
def balance(update, context):
    try:
        address = context.args[0]
        usdt_balance = get_usdt_balance(address)
        message = f"地址 {address} 的 USDT 余额为：{usdt_balance} USDT"
    except IndexError:
        message = "请提供一个 TRON 地址，例如：/balance TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

# 主函数
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("balance", balance))
    updater.start_polling()
    print("Bot is running...")
    updater.idle()

if __name__ == "__main__":
    main()
