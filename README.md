# Ubyssey Dispatch Theme

## Installation

We recommend working inside a virtualenv, but it's not required.

```bash
# Create a new folder for the virtual environment
mkdir ubyssey-dev
virtualenv ubyssey-dev
cd ubyssey-dev

# Activate the virtualenv
source bin/activate
```

Clone the `ubyssey-dispatch-theme` repository:

```bash
git clone https://github.com/ubyssey-dispatch-theme
cd ubyssey-dispatch-theme
```

Install the required Python packages with pip:

```bash
pip install -r requirements.txt
```

*INSERT PROJECT SETTINGS & DATABASE INSTRUCTIONS*


### Static files

Install the required Node packages with npm:

```bash
cd ubyssey/static
npm install
```

Install a global verison of gulp (if you don't have it already) and build the static files:

```bash
npm install -g gulp
gulp
```

### Running the server


