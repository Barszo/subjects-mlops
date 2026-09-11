"""Lokalne rozszerzenie IPython dostarczające magię komórkową ``%%skip``.

Uzycie w notebooku:

    %load_ext skip_kernel_extension

    %%skip True
    # ta komórka zostanie pominięta

Wyrazenie po ``%%skip`` jest ewaluowane w przestrzeni nazw notebooka. Gdy jest
prawdziwe (domyślnie ``True``), komórka nie zostaje wykonana.
"""

from IPython.core.magic import register_cell_magic


def skip(line, cell):
    """Pomija wykonanie komórki, gdy wyrazenie w ``line`` jest prawdziwe."""
    ipython = get_ipython()  # noqa: F821 - dostarczane przez IPython w runtime
    should_skip = eval(line, ipython.user_ns) if line.strip() else True
    if should_skip:
        return
    ipython.run_cell(cell)


def load_ipython_extension(ipython):
    """Rejestruje magię ``%%skip`` przy ``%load_ext skip_kernel_extension``."""
    ipython.register_magic_function(skip, magic_kind="cell", magic_name="skip")
