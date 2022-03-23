# Swiss-Super-League
Some historical analysis of the Swiss Super League.

### Installation of packages
This project manages its dependencies using pip.
It requires Python >=3.8.10, <4.0.0 (3.9.7 recommended). You can ensure that
you are using a valid Python version by running

<pre><code>python --version
</code></pre>

You can install all the required packages as follows:

<pre><code>python -m pip install -r requirements.txt
</code></pre>

### Documentation
You can auto-generate the documentation of the `src` package by 
running

<pre><code>pdoc3 src/ -o docs/ --html
</code></pre>

which will generate the documentation in HTML format into the `docs` directory.
