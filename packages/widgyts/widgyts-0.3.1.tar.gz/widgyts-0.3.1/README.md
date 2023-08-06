widgyts
===============================

A fully client-side pan-and-zoom widget, using WebAssembly, for variable mesh
datasets from yt.  It runs in the browser, so once the data hits your notebook,
it's super fast and responsive!

If you'd like to dig into the Rust and WebAssembly portion of the code, you can
find it at https://github.com/data-exp-lab/rust-yt-tools/ and in the npm
package `@data-exp-lab/yt-tools`.

Check out our [SciPy 2018 talk](https://www.youtube.com/watch?v=5dl_m_6T2bU)
and the [associated slides](https://munkm.github.io/2018-07-13-scipy/) for more info!

Installation
------------

To install using pip from the most recent released version:

    $ pip install widgyts

To install using pip from this directory:

    $ git clone https://github.com/data-exp-lab/widgyts.git
    $ cd widgyts
    $ pip install .

For a development installation (requires npm),

    $ git clone https://github.com/data-exp-lab/widgyts.git
    $ cd widgyts
    $ pip install -e .
    $ jupyter serverextension enable --py --sys-prefix widgyts
    $ jupyter nbextension install --py --symlink --sys-prefix widgyts
    $ jupyter nbextension enable --py --sys-prefix widgyts

Note that in previous versions, serverextension was not provided and you were
required to set up your own mimetype in your local configuration.  This is no
longer the case and you are now able to use this server extension to set up the
correct wasm mimetype.

To install the jupyterlab extension, you will need to make sure you are on a
recent enough version of Jupyterlab, preferably 0.35 or above.  For a
development installation, do:

    $ jupyter labextension install js

To install the latest released version,

    $ jupyter labextension install @data-exp-lab/yt-widgets

Using
-----

To use this, you will need to have yt installed.  Importing it monkeypatches
the Slice and Projection objects, so you are now able to do:

```
#!python
import yt
import widgyts

ds = yt.load("data/IsolatedGalaxy/galaxy0030/galaxy0030")
s = ds.r[:,:,0.5]
s.display("density")
```

and for a projection:

```
#!python
ds = yt.load("data/IsolatedGalaxy/galaxy0030/galaxy0030")
p = ds.r[:].integrate("density", axis="x")
p.display()
```

There are a number of traits you can set on the resultant objects, as well.
