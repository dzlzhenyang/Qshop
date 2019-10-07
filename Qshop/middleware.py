from django.utils.deprecation import MiddlewareMixin
from Qshop.settings import ERROR_PATH
from django.http import HttpResponse
from CeleryTask.tasks import ding_send_message
import time


class MiddleWareTest(MiddlewareMixin):
    def process_request(self, request):
        # request.META返回的是一个字典格式，它中的键REMOTE_ADDR:远程地址，对应的值为连入该项目的主机ip
        print(request.META)
        request_ip = request.META["REMOTE_ADDR"]
        # 写入对应的主机ip
        if request_ip == "":
            return HttpResponse("你被禁了！")
        print("我是process_request")

    def process_view(self, request, callback, callback_args, callback_kwargs):
        """
        :param request: 请求
        :param callback: 对应视图中的函数
        :param callback_args: 视图函数的参数，元组类型
        :param callback_kwargs: 视图函数的参数，字典类型
        :return:
        """
        print("我是process_view")
        print(callback)

    # def process_exception(self, request, exception):
    #     if exception:
    #         with open(ERROR_PATH, "a") as f:
    #             now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    #             content = "%s:%s" % (now, exception)
    #             f.write(content)
    #             ding_send_message.delay(content)
    #         return HttpResponse("您的代码出错，出错内容为: <br> %s" % exception)
    # 只有当views函数中返回的对象中具有render方法，才会执行process_template_response
    def process_template_response(self, request, response):
        print("我是process_template_response")
        # 必须有返回值
        return HttpResponse("123")

    def process_response(self, request, response):
        print("我是process_response")
        print(response)
        # 必须有返回值
        return response
