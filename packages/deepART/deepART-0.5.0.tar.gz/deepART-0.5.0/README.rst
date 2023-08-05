pyART
============

pyART is a Python module that aims to facilitate the application of family
of Adaptive Resonance Theory (ART) neural network in solving machine learning problems.
By design, ART neural networks supports returning the reasons for which predictions are made
by the networks. As such, this class of neural network is a natural fit for application
in an environment where trustworthy and auditable machine learning model is essential.

pyART accentuate this property of ART neural networks by incorporating
this into its design philosophy.

*All pyART predictions are returned with accompanying reasons.*


Website:


Installation
------------

Dependencies
~~~~~~~~~~~~

pyART requires:

- Python (>= 3.6)
- NumPy (>= 1.15.1)


User installation
~~~~~~~~~~~~~~~~~

Install using ``pip`` ::

    pip install .


Getting Started:
----------------
The basic architecture of ART neural network consist of a comparison field F1
layer, recognition field F2 layer, long term memory traces  that connect the
layers, gain control subsystem and a orientating subsystem. These are
implemented as a class in pyART.

Here is an example of using fuzzy ART model ::

    from pyART import fuzzyART

    network = fuzzyART.FuzzyART(n=3, m=50, rho=0.85, beta=0.5)

where ::

    n is the number of dimension of input
    m is the number of nodes in the F2 layer
    rho is the vigilance parameter
    beta is the learning rate

You can generate some random clusters and cluster them using fuzzyART

To generate dataset ::

    from pyART import dataset

    sample_data = dataset.Clusters3d(nclusters=4)

    #training loop for the network
    epochs = 10
    for _ in range(epochs)
      for I in sample_data.data_normalized:
            Z, k = network.predict(I.ravel())

Cluster the data using the trained fuzzyART network ::

    pred = []

    for I in sample_data.data_normalized:
            Z, k = network.predict(I.ravel())
            if not k==None:
                pred.append(k)
            else:
                pred.append(-1)

Visualize the clusters ::

    import matplotlib.pyplot as plt
    from matplotlib import cm

    fig = plt.figure(figsize=(8,8))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_title("Clustering Results ",fontsize=14)
    ax.set_xlabel("X",fontsize=12)
    ax.set_ylabel("Y",fontsize=12)
    ax.set_ylabel("Z",fontsize=12)
    ax.grid(True,linestyle='-',color='0.75')
    # scatter with colormap mapping to predicted class
    color = [c+1 for c in pred]
    ax.scatter(sample_data.data_normalized[...,0],sample_data.data_normalized[...,1],sample_data.data_normalized[...,2],s=100,c=color, marker = '*', cmap = cm.jet_r );
    plt.show()


Development
-----------

We welcome new contributors that are passionate about ART neural network.


Important links
~~~~~~~~~~~~~~~

- Official source code repo:
- Download releases:
- Issue tracker:

Source code
~~~~~~~~~~~

You can check the latest sources with the command::

    git clone

Setting up a development environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



Testing
~~~~~~~

The package can be tested at the source code directory using::

    python setup.py test


Submitting a Pull Request
~~~~~~~~~~~~~~~~~~~~~~~~~



Project History
---------------

The project was started under the Cognitive Analytics Solution Centre
in Deloitte Singapore. This project was started as an initiative to
develop applied cognitive technologies to be employed in a regulated
environment where trustworthy artificial intelligence is a essential.


Help and Support
----------------

Documentation
~~~~~~~~~~~~~


Communication
~~~~~~~~~~~~~

- Website:

Citation
~~~~~~~~

We appreciate citation when you use pyART in any publication.
