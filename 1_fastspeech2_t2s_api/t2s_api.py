from synthesize_all import SpeechSynthesis
import base64
import time,json
import threading
from gevent import monkey
from gevent.pywsgi import WSGIServer
from flask import Flask, request, jsonify, has_request_context, copy_current_request_context
from flask_cors import CORS
import traceback
import argparse
from concurrent.futures import Future, ThreadPoolExecutor
from functools import wraps
import asyncio
import wave


#这里写自己对应的路径位置
config_path = '/home/.../config/AISHELL3'   #参数配置路径
save_path = '/home/.../t2s_wav'             #生成音频存储路径

tts = SpeechSynthesis(config_path)

### # ——————————————————接口定义————————————————
app = Flask(__name__, static_folder="./static", static_url_path='')
CORS(app, supports_credentials=True)
### # ——————————————————————————————————————————
monkey.patch_all()
def run_async(func):
    @wraps(func)
    def _wrapper(*args, **kwargs):
        call_result = Future()

        def _run():
            loop = asyncio.new_event_loop()
            try:
                result = loop.run_until_complete(func(*args, **kwargs))
            except Exception as error:
                call_result.set_exception(error)
            else:
                call_result.set_result(result)
            finally:
                loop.close()

        loop_executor = ThreadPoolExecutor(max_workers=1)
        if has_request_context():
            _run = copy_current_request_context(_run)
        loop_future = loop_executor.submit(_run)
        loop_future.result()
        return call_result.result()
    return _wrapper


def ToBase64(file):
    with open(file, 'rb') as fileObj:
        image_data = fileObj.read()
        base64_data = base64.b64encode(image_data)
        string = base64_data.decode()
        return string


def t2s_process_api(inputjson):
    res = {
        'base64': '',
        'duration': ''  # 单位是s
    }
    s_time = time.time()
    text = inputjson['text']
    wavpath = tts.text2speech(text, save_path)
    wavefile = wave.open(wavpath)
    rate = wavefile.getframerate()
    frames = wavefile.getnframes()
    duration = frames / float(rate)  # 单位为s
    base64code = ToBase64(wavpath)
    # 验证base64编码是否有问题
    # decode_string = base64.b64decode(base64code)
    # wav_file = open(save_path+'/debug.wav', "wb")
    # print("write wav")
    # wav_file.write(decode_stjsonify, has_request_context, copy_current_request_contextring)
    # wav_file.close()
    res['base64'] = base64code
    res['duration'] = duration
    e_time = time.time()

    time_info = "{:.2f}".format(e_time - s_time)
    return res, time_info


@app.route('/api/sound/t2s', methods=['POST'])
@run_async
async def text_process():
    res_dict = {
        "Status": 200,
        "success": True,
        "result": {
        },
        "ErrorMessage": "None",
        "InfoMessage": "Received",
        "Debug": {
            "ErrorDetails": "",
            "TimeInfo": {
                "ApiTime": ""
            }
        }
    }
    try:
        data = json.loads(request.data)
    except Exception as e:
        res_dict["success"] = False
        res_dict["ErrorMessage"] = "Params Error"
        res_dict["Debug"]["ErrorDetails"] = str(e) + "\n" + traceback.format_exc()
        return json.dumps(res_dict), {"Content-Type": "application/json;charset=utf-8"}

    try:
        res, time_info = t2s_process_api(data)
        res_dict["Debug"]["TimeInfo"]['ApiTime'] = time_info
    except Exception as e:

        res_dict["success"] = False
        res_dict["ErrorMessage"] = "API Error"
        res_dict["Debug"]["ErrorDetails"] = str(e) + "\n" + traceback.format_exc()
        return json.dumps(res_dict), {"Content-Type": "application/json;charset=utf-8"}
    res_dict["result"] = res

    return json.dumps(res_dict), {"Content-Type": "application/json;charset=utf-8"}


inputjson = {
    'text': '我是机器人瓦力'
}

if __name__ == '__main__':
    # 这里是测试代码
    # res,timeinfo = t2s_process_api(inputjson)
    #
    # print(res)
    # print(timeinfo)

    # 这里是正式运行代码
    address = "0.0.0.0"
    port = 5001
    http_server = WSGIServer((address, port), app)
    print("api start: {}:{}".format(address, port))
    http_server.serve_forever()