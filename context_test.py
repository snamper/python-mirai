from mirai import Direct

def is_startwith(string):
    """判断当前正在处理的消息是否以 string 为前缀
    """
    return Direct.Message\
        .message.messageChain.toString().startswith(string)