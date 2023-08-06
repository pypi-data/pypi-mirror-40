# jupyterlab-zip

Zip and Download folders in Jupyterlab

## Install

Install the Jupyter Notebook server extension under `PREFIX` (e.g., the active
virtualenv or conda env).

```
pip install jupyterlab-zip
```

Then install the JupyterLab frontend extension.

```
jupyter labextension install @chatter92/jupyterlab-zip
jupyter serverextension enable --py jupyterlab-zip
```

### Install Alternatives

You can use `jupyter serverextension` commands to enable and disable the
server extension in different contexts, e.g.:

```
jupyter serverextension enable --py jupyterlab-zip --user
jupyter serverextension disable --py jupyterlab-zip --sys-prefix
```
