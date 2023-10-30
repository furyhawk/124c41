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

bash Miniconda3-py310_22.11.1-1-Linux-x86_64.sh 
conda list
conda config --add channels conda-forge
conda config --describe
conda config --set auto_activate_base false
conda update --all
pip --disable-pip-version-check list --outdated --format=json | python -c "import json, sys; print('\n'.join([x['name'] for x in json.load(sys.stdin)]))" | xargs -n1 pip install -U
conda update conda
conda install --file requirements.txt -c conda-forge
pip install -r requirements.txt

# archlinux
 echo "[ -f /opt/miniconda3/etc/profile.d/conda.sh ] && source /opt/miniconda3/etc/profile.d/conda.sh" >> ~/.zshrc
 

# ubuntu
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm -rf ~/miniconda3/miniconda.sh

source ~/miniconda3/etc/profile.d/conda.sh
conda init zsh
```


