# 杭电图书馆抢座脚本

## 使用说明

1. 克隆本项目

    ```bash
    git clone git@github.com:LitttleHeroZZZX/hdu-library-booker.git
    cd hdu-library-booker
    ```

2. 安装依赖项

    ```bash
    pip install -r requirements.txt
    ```

3. 运行脚本

    ```bash
    python hdu-booker.py --config config.yaml --show_log false
    ```

4. 接下来可按照脚本提示添加座位愉快抢座啦~

## 功能说明

本脚本具备以下功能：

* 自动登录
* 自动保存，自动加载上次抢座列表
* 多座位抢座
  * 由于提交频率过高会封号，故设置默认抢座间隔为5秒，且未开启并行抢座
* 批量修改抢座时间
  * 可批量修改抢座时间，免去重复添加抢座列表
* 定时抢座
  * 支持设置在指定时间开启抢座


## 注意事项

**本脚本仅限用于个人抢座，请勿恶意囤座位**  
配置文件config.yaml-settings参数interval为抢课请求间隔，默认为5，请勿修改过小，有封号风险（一周），后果自负

## 联系作者

关于本脚本的一切问题，请联系作者：[zzzx@hdu.edu.cn](mailto:zzzx@hdu.edu.cn)
