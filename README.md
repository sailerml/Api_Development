# Api_Development
the basic AIGC api
提供AIGC各类接口代码， 具体原理与代码讲解可关注公众号——walle优选笔记

## 0.基于whisper框架的离线语音接口开发
   具体代码参考0_whisper_api.py，可支持异步调用;接口文档见《语音识别接口说明文档》

## 1.基于fastspeech2框架的语音合成接口开发
具体代码参考1_fastspeech2_t2s_api，可支持异步调用；接口文档见《语音合成接口说明文档》

### 1) 运行环境
python 版本一定要 3.9，具体参考requiments.txt

### 2) 已训练完成的模型路径
   模型包括 fastspeech_model、hifigan_model、prosody_model
   
   百度网盘链接：https://pan.baidu.com/s/1PzjQecaANCoXeIvisyWyeg 
   提取码：2twv

   下载后放置路径如下：
   - 8000.pth.tar ---> output/ckpt/biaobei/
   - generator_universal.pth.tar ---> hifigan/
   - best_model.pt ---> transformer/prosody_model/

### 3) 接口文件
具体代码参考1_fastspeech2_t2s_api/t2s_api.py
