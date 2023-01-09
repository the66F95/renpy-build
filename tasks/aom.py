from renpybuild.model import task, Context

@task(kind="host", platforms="all")
def download(c : Context):
    c.clean("{{ tmp }}/source/aom")
    c.chdir("{{ tmp }}/source")

    c.run("git clone --branch v3.5.0 https://aomedia.googlesource.com/aom")

@task(platforms="all")
def build(c : Context):
    c.clean()

    c.run("""
        {{ cmake }}
        -DCMAKE_INSTALL_PREFIX={{install}}
        -DCONFIG_AV1_ENCODER=0
        -DCONFIG_LIBYUV=0
        -DENABLE_EXAMPLES=0
        -DENABLE_TOOLS=0
        -DENABLE_TESTS=0
        {{ tmp }}/source/aom
        """)

    try:
        c.run("{{ make }}")
    except:
        c.run("make VERBOSE=1")

    c.run("make install")
