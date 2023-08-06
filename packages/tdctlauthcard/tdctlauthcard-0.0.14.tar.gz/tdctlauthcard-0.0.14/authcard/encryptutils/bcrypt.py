import bcrypt

def encryptText(opts={}):
    saltRounds = opts.get('saltRounds',10)
    text = opts.get('text',"")
    textBytes = bytes(text, 'utf-8')
    hashBytes = bcrypt.hashpw(textBytes, bcrypt.gensalt(saltRounds))
    hash = hashBytes.decode("utf-8")
    return hash

def compareText(opts={}):    
    hash = opts.get('hash',"")
    text = opts.get('text',"")
    textBytes = bytes(text, 'utf-8')
    hashBytes = bytes(hash, 'utf-8')
    match = bcrypt.checkpw(textBytes,hashBytes)
    return match
