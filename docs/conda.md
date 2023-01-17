# conda cheat sheet

```shell
conda update -n base conda

conda remove --name myenv --all
conda env remove -n tf2

conda init powershell

conda env create -f environment.yml
conda env export > environment.yml

conda create --name myenv python=3.10
conda install --file requirements.txt
conda install --file requirements.txt -c conda-forge
conda create --name tft --clone 311

pip install -r /path/to/requirements.txt
pip install --upgrade --force-reinstall -r requirements.txt

python -m ipykernel install --user --name myenv --display-name "Python (myenv)"

conda clean -a

conda install -y -c apple tensorflow-deps
pip install tensorflow-macos tensorflow-metal

```


