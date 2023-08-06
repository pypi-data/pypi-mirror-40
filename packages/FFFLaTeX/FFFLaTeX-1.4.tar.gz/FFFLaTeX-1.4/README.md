## Installation
You will need python 3.6+ and pip

```bash
> pip install --upgrade FFFLaTeX
```

## Launching the script

Just as you would launch any other python script after installation:

``` bash
> FFFLaTeX
```

## Output tex file

The tex file for the FFF XXX will be located under a new folder FFFXXX where you used the FFFLaTeX command, as FFFXXX.tex

This lets you directly modify and compile the tex file under its own folder without dealing with multiple outputs

```bash
> FFFLaTeX
....
> 277
....
> ls
....... ./FFF277/
```

You can also use the command line directly as of 1.4

```bash
> FFFLaTeX 277
....
> ls
....... ./FFF277/
```

## Configuration

You can now configure both the LaTeX templates per tag but also use an hybrid scripting system!

This hybrid system lets you call any registered python function from the configSymbol.py file at specific points in your LaTeX templates, allowing you to generate your document dynamically!

![Config scheme][./Config system.PNG]

The LaTeX templates can be modified in the configLaTeX.py file

The linking and function declarations can be modified in the configSymbol.py