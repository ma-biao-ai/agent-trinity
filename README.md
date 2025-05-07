# Trinity

**Trinity** is a `compact agent team architecture` designed to reliably complete tasks while ensuring output quality. This worker-checker-arbitrator triad overcomes the limitations of single-agent systems where errors may go undetected.
If needed, it can be extended with a restorer.worker do the input task, and checker check the result, and arbitrator arbitrate the result. If needed, restorer restore the environment.  
This architecture is developed based on the [**Agno**](https://github.com/agno-agi/agno)  

**The Trinity architecture's concept can be applied to any other agent framework. Compared to a single agent, Trinity serves as a more effective task executor.**

## Architecture
![trinity-architecture](trinity.png)


## usage
+ linux
    + install necessary lib
    ``` bash
    # python version need > 3.10
    sudo apt install python3.11
    # If the system has multiple Python versions, execute the following command; otherwise, skip it.（find python3.11 position: which python3.11）
    sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1
    sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 2
    sudo update-alternatives --config python3
    # install venv
    sudo apt install python3.11-venv
    # install npm
    sudo apt install nodejs npm
    # verify npm env
    node --version
    npm --version
    ```
    + python venv 
    ``` bash
    # start python venv
    python3 -m venv myvenv
    source myvenv/bin/activate
    # install necessary lib in python venv
    pip install -U agno openai mcp mcp[cli] uv
    ```
    + use agno and trinity
    ``` bash
    # choose your model, and write api key in activate, like deepseek
    export DEEPSEEK_API_KEY=sk-***************(your api key)
    # start python venv
    source myvenv/bin/activate
    # run an agno example
    python3 cookbook/models/deepseek/basic.py 
    # run trinity example
    python3 example/excel_trinity/excel_trinity_demo.py
    ```