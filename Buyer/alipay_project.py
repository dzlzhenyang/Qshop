from alipay import AliPay

alipay_public_key_string = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA6OqrpXSPjFVifdQ7GP4Sk/crDzb6sjpVmES3OKIs3CNl/XtkgLh3blzUBS+4hvSEZj1wgrxZisNaDhIxgyUwgJjViEFVsvIPzIC7edtbigkaobkuzDahinH2P+x4+DkmAQNuZfQJ/dRC9bC06Zg32U90YqK2498Dy7al0DrbY6feNnMrZKogrFjgr7+wOo1/UtazrN+sH21ol9AY5qdJfsjE0xCY321daFMBUVufitZsibYt9ZYOJQwshn25L79C8FINaxtK1IN7/TVjQ45uqgAjTvAebUs8N841XN6mEeaRof72aJO5F51N5nYGinm4RsAOuwNIMQDNipSeP3eduwIDAQAB
-----END PUBLIC KEY-----"""
alipay_private_key_string = """-----BEGIN RSA PRIVATE KEY-----
MIIEpQIBAAKCAQEA6OqrpXSPjFVifdQ7GP4Sk/crDzb6sjpVmES3OKIs3CNl/XtkgLh3blzUBS+4hvSEZj1wgrxZisNaDhIxgyUwgJjViEFVsvIPzIC7edtbigkaobkuzDahinH2P+x4+DkmAQNuZfQJ/dRC9bC06Zg32U90YqK2498Dy7al0DrbY6feNnMrZKogrFjgr7+wOo1/UtazrN+sH21ol9AY5qdJfsjE0xCY321daFMBUVufitZsibYt9ZYOJQwshn25L79C8FINaxtK1IN7/TVjQ45uqgAjTvAebUs8N841XN6mEeaRof72aJO5F51N5nYGinm4RsAOuwNIMQDNipSeP3eduwIDAQABAoIBADY4KqzhbWkllz/jX755pql7KDLqgYFrwvEnTd+JIRg9xUg0qTituF+gjFqIuVPxJ8EFHGPSpKWAxD3yTkRRK/FDorGNQ/3cC4F3lizPu4duhxyOly5CqWgpD0HiMmbWJtqlidWB8bF87/lxoSufm6Citl0fs6NoDuIlKoRGrzuLLpywpp8UrPn29fkiZEMs+NBedLKASXvEZFK2oPhieE8Qosbxq7uovZHAj2uVjoqDzmJ/mdHoPpQYh1zMIr+2op1twFnT0DnRFm/+RzkAtFpYYTsE+mTgpK0PlH3iqMZCph2qtrBfxvoR9A1pB2/KL+fujnYk6OdQ7qZWasCwO8ECgYEA+ughkDAiDweAh0TYWrsbO8WF9MVqB2WZvz9b0eVT3jimkohSq0DuvDbGcTxPTAOQVXplZjjaONmarMOgBdDHkQWOG/UfFyBA+MARz/dZoHaRpHV5NEBlXB1+Z1MrApB0Pu/yofM7u4BjobrxM/6AiqMW7nr/uTU3ELLmG6GFFpcCgYEA7aUNOK0Gl1891mVCZNefb8MoqBEgEHRTMK0+698JTkB6w/Oto9SnSNH//dKmIduJ3gkKOwaqpFuRQabiin8pmBMILO/xBoEXaqeDkl67oQtZF0qpKi2EqG5GpnqdG8VzMHVbU1UmvAyr8bfZ2cg4i7UjUDrbKubzHlCMh1SZ2n0CgYEAn9PMxX+TwoUh34kAVNOJZorNaP10LCARTx06DTuLMCxgF0mVd5eWO/iccjdbv+0pPPoJq5Mdl0cuW00GG45CAeRLAQ4k7uNR3+Lhtds3kZrV7bATNDCtIH99LK5y4GBKXGkW4wkBDNCdJsHhsiA1m5qGGgXp7f2zBQUgxYsfLyMCgYEAhZQvGFp5yABrG+YTKefh4MqMQdxOb7FTSZs4MRFPg8LOvvJr+hkAZvhTsnMDmyhyGHJwY7ldlcE6pvKNiFfuI2MfR1Mf4g4SAYtjc5T4Vo+wZl07NVAcryg9YjqtsPyNwQFWckL84Nsmk1pKhBX9YtpQnTpYE4d5xOJ1+2Pcj2kCgYEA4ULlgpyEU3FxLQv6RbXwgsQrdUsOLg0uuXoCEGVbqSVFbwd5NYNf6WEqP98wXGWLEvKI/MD0DI2paurtajEysvNqd7svCEmCwl/BlKzCNj+bKkW3f1FImpBFrBrIObRdOJAMBeh3MUpMTExXC4QdVFQyDfuB+4gqqoWZasP4Uio=
-----END RSA PRIVATE KEY-----"""
# 实例化支付
alipy = AliPay(
    appid="2016101200667716",
    app_notify_url=None,
    app_private_key_string=alipay_private_key_string,
    alipay_public_key_string=alipay_public_key_string,
    sign_type="RSA2"
)
# 实例化订单,网页支付的订单
order_string = alipy.api_alipay_trade_page_pay(
    out_trade_no="100000000",  # 订单号
    total_amount=str(100.5),  # 支付金额
    subject="生鲜交易",  # 支付主题
    return_url=None,
    notify_url=None
)
# 拼接收款地址 = 支付宝网关+ 订单返回参数
result = "https://openapi.alipaydev.com/gateway.do?" + order_string
print(result)
