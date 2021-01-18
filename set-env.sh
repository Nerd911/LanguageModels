SRC=${BASH_SOURCE[0]}
if [[ -L $SRC ]]; then
    SRC=`readlink -e $SRC`
fi

export REPO_TOP_DIR="$( cd "$( dirname "$SRC" )" && pwd )"

export PYTHONPATH=$PYTHONPATH:$REPO_TOP_DIR

export PATH=$PATH:$REPO_TOP_DIR/bin
