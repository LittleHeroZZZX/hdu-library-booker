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

## 注意事项

**本脚本仅限用于个人抢座，请勿恶意囤座位**    
配置文件config.yaml-settings参数incident为抢课请求间隔，默认为5，请勿修改过小，有封号风险（一周），后果自负
