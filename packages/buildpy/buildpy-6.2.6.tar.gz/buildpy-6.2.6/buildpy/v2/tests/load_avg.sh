#!/bin/bash
# @(#) -l

# set -xv
set -o nounset
set -o errexit
set -o pipefail
set -o noclobber

export IFS=$' \t\n'
export LANG=en_US.UTF-8
umask u=rwx,g=,o=


readonly tmp_dir="$(mktemp -d)"

finalize(){
   rm -fr "$tmp_dir"
}

trap finalize EXIT


cd "$tmp_dir"


cat <<EOF > build.py
#!/usr/bin/python

import os
import sys
import time

import buildpy.v2


os.environ["SHELL"] = "/bin/bash"
os.environ["SHELLOPTS"] = "pipefail:errexit:nounset:noclobber"
os.environ["PYTHON"] = sys.executable


dsl = buildpy.v2.DSL()
file = dsl.file
phony = dsl.phony
let = dsl.let
sh = dsl.sh
rm = dsl.rm


nx = 3
ny = 3
nz = 3
dt = 0.1


xs = ["x" + str(i) for i in range(nx)]
ys = ["y" + str(i) for i in range(ny)]
zs = ["z" + str(i) for i in range(nz)]


def getloadavg():
    return (3, None, None)

os.getloadavg = getloadavg


@phony("all", xs)
def _(j):
    # print(j)
    time.sleep(dt)

for x in xs:
    @let
    def _(x=x):
        @phony(x, [x + y for y in ys])
        def _(j):
            # print(j)
            time.sleep(dt)

        for y in ys:
            @let
            def _(y=y):
                @phony(x + y, [x + y + z for z in zs])
                def _(j):
                    # print(j)
                    time.sleep(dt)

                for z in zs:
                    @let
                    def _(z=z):
                        @phony(x + y + z, [])
                        def _(j):
                            # print(j)
                            time.sleep(dt)


if __name__ == '__main__':
    t1 = time.time()
    dsl.main(sys.argv)
    t2 = time.time()
    assert t2 - t1 > dt*(1 + nx*(1 + ny*(1 + nz)))
EOF

"$PYTHON" build.py -j20 -l2
