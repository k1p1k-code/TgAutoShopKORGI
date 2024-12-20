import json

PATH='data/settings.json'

async def get_texts() -> str:
    
    return (json.load((open(PATH, 'r', encoding='UTF-8'))))['text'] 

async def edit_text(text, value) -> str:
    data=json.load((open(PATH, 'r', encoding='UTF-8')))
    data['text'][text]=value
    json.dump(data, open(PATH, 'w', encoding='UTF-8'), indent=4)