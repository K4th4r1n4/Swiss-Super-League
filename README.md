# Swiss-Super-League
Some historical analysis of the Swiss Super League.

### Installation of packages
This project manages its dependencies using pip.
It requires Python >=3.10.6. You can ensure that
you are using a valid Python version by running

<pre><code>python3 --version
</code></pre>

You can install all the required packages as follows:

Regular install
````commandline
python3 -m pip install  .
````

Create virtual environment using `Makefile`
````commandline
make
````

Clean-up
````commandline
make clean
````

### Documentation
You can auto-generate the documentation of the `src` package by 
running

````commandline
make docs
````

which will generate the documentation in HTML format into the `docs` directory.
