from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
def token(name,seconds):
    s=Serializer('anisha@2003',seconds)
    return s.dumps({'user':name}).decode('utf-8')
