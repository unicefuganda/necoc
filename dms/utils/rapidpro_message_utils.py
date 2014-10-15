
def clean_text(message):
    split_message = message.split(' ')
    return filter(lambda x: x.strip(), split_message)

