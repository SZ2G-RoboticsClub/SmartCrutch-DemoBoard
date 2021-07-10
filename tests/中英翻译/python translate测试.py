from translate import Translator


# 在任何两种语言之间，中文翻译成英文
translator= Translator(from_lang="chinese",to_lang="english")
translation = translator.translate("深圳市第二高级中学")
print(translation)