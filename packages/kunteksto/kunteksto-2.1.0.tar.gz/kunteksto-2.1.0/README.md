# Kunteksto

=======================================================

**Kunteksto** is a tool for helping domain experts, data creators and data users translate their simple CSV formatted data files into semantically enhanced formats. This provides a path for existing data to be used in conjunction with the emerging *data-centric, model first* approach in analysis, general artificial intelligence and decision support systems. This approach opens the door for the change to a *data-centric* world as opposed to the *application-centric* one we have now. This new approach enables automatic interoperability avoiding the data quality issues created through data cleaning and massaging. 

The importance of this capability and improved data quality is discussed in foundational S3Model https://datainsights.tech/S3Model documentation and references. However, detailed understanding of S3Model is not required to understand and use the power of Kunteksto. Addtional information on the data-centric movement can be found in the References below. 

What is 'Context' for your data?

It is the combination of ontological, temporal and spatial semantics that describes the deeper meaning of your data allowing you to share 'information' instead of just 'data'.

# Installation

See the instructions in the documentation or online at https://datainsights.tech/Kunteksto/index.html

# References

The limits of deep learning https://blog.keras.io/the-limitations-of-deep-learning.html 

The future of deep learning https://blog.keras.io/the-future-of-deep-learning.html


# Development

- Install Anaconda (Python 3.7+)
- Open a terminal.
- Clone the repository.
- Create the development virtual environment: $ conda env create -f Kunteksto/dev_environment.yml
- Activate the environment according to the instructions displayed in the terminal.
- Change to the Kunteksto directory: $ cd Kunteksto/kunteksto
- Run the Kunteksto dev server: $ ./kunteksto.sh
- In a browser go to: http://127.0.0.1:7659/ 

When making changes and testing locally you should;
build the package: $ python3 setup.py sdist bdist_wheel
Then perform a local install: $ pip install e .

