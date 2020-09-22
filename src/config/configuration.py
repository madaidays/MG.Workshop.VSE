REGEX = [{'regex': r'\+[0-9XY]+\/\+[0-9XY]+', 'token': '<UPTURN>'},
         {'regex': r'\-[0-9XY]+\/\-[0-9XY]+', 'token': '<DOWNTURN>'},
         {'regex': r'[\+\-][0-9XY]+\/[\+\-][0-9XY]+', 'token': '<MODIFIER>'},
         {'regex': r'[0-9XY]+\/[0-9XY]+', 'token': '<TOKEN>'},
         {'regex': r'({([0-9\/A-Z])+})+:', 'token': '<COST>:'},
         {'regex': r'({([0-9\/A-Z])+})+', 'token': '<MANA>'}]

VSE = {
    'max_words': 30,
    'tokenizer_n_words': 3043,
    "ignore_tokens": [' ', '<', '>'],
    "buffer_size": 1000,
    "batch_size": 64,
    "units": 512,
    "embedding_dim": 256,
    "epochs": 400
}
