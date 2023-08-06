# coding=utf-8
import collections

import matplotlib.pylab as plt
import numpy as np
import scipy.cluster.hierarchy as sch
import seaborn as sns
from scipy import stats
from scipy.spatial import distance
from sklearn.cluster import KMeans


def clustering_hierarchical(df, cols, k=2, linkage_method='complete', fcluster_criterion='maxclust', color_threshold=2,
                            plot_dendrogram=False):
    """
    Performs a hierarchical clustering using scipy [1]_.

    Parameters
    ----------
    df : dataframe
        Input data frame
    cols : array_like
        List of columns to be considered from the data frame
    k : int
        Number of clusters
    linkage_method : str, optional
        Methods for calculating the distance between the clusters [2]_
    fcluster_criterion : str, optional
        The criterion to use in forming flat clusters [3]_
    color_threshold : float, optional
        Cut threshold to show different colors for different clusters [4]_
    plot_dendrogram : bool, optional
        When True, plots the dendrogram

    Returns
    -------
    clusters : array_like
        List with the cluster assigned to each line
    cluster_distribution: dict
        Dictionary with the count on the number of data points per cluster
    centroids : array_like
        List of all the centroids
    sum_intra_cluster_distances : float
        Sum of Squares of distances of the data points to their cluster center
    sum_inter_cluster_distances : float
        Sum of Squares of distances among all the centroids

    Notes
    -----
    Some references about the error metrics and how to better define the number of clusters [5]_ [6]_

    References
    ----------
    .. [1] Hierarchical clustering (scipy.cluster.hierarchy)
       https://docs.scipy.org/doc/scipy/reference/cluster.hierarchy.html

    .. [2] scipy.cluster.hierarchy.linkage
       https://docs.scipy.org/doc/scipy-0.18.1/reference/generated/scipy.cluster.hierarchy.linkage.html

    .. [3] scipy.cluster.hierarchy.fcluster
       https://docs.scipy.org/doc/scipy-0.18.1/reference/generated/scipy.cluster.hierarchy.fcluster.html

    .. [4] scipy.cluster.hierarchy.dendrogram
       https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.cluster.hierarchy.dendrogram.html

    .. [5] Data Mining Clustering
       http://wwwis.win.tue.nl/~tcalders/teaching/datamining09/slides/DM09-07-Clustering.pdf

    .. [6] Clustering Methods
       https://www.cs.swarthmore.edu/~meeden/cs63/s16/reading/Clustering.pdf

    Examples
    --------
    >>> import mdspy
    >>> import pandas as pd
    >>> dataset = [[1, 1], [1, 2], [1, 2], [5, 10], [2, 10]]
    >>> df_clustering = pd.DataFrame(dataset)
    >>> df_clustering.columns = ['col1', 'col2']
    >>> mdspy.analytics.clustering_hierarchical(df_clustering, ['col1', 'col2'], 2)
    {'clusters': [1, 1, 1, 2, 2], 'sum_intra_cluster_distances': 5.16666667,
    'sum_inter_cluster_distances': 75.694444444444443, 'centroids': [[1.0, 1.6666666666666667], [3.5, 10.0]],
    'cluster_distribution': {1: 3, 2: 2}}
    >>> mdspy.analytics.clustering_hierarchical(df_clustering, ['col1', 'col2'], 2, color_threshold=5, \
                                                plot_dendrogram=True)
    {'clusters': [1, 1, 1, 2, 2], 'sum_intra_cluster_distances':  5.16666667,
    'sum_inter_cluster_distances': 75.694444444444443, 'centroids': [[1.0, 1.6666666666666667], [3.5, 10.0]],
    'cluster_distribution': {1: 3, 2: 2}}

    """

    d = sch.distance.pdist(df[cols])
    z = sch.linkage(d, method=linkage_method)
    t = list(sch.fcluster(z, k, criterion=fcluster_criterion))
    cluster_distribution = dict(collections.Counter(t))

    df['clusters'] = t

    # calculate the centroids
    centroids = []
    centroids_reference = {}
    for c in list(set(t)):
        centroid = df[df['clusters'] == c][cols].mean(axis=0).values
        centroids_reference[c] = [centroid]
        centroids.append(list(centroid))

    # calculate the errors
    sum_intra_cluster_distances = 0
    for k, v in df.iterrows():
        sum_intra_cluster_distances += distance.cdist(centroids_reference[v['clusters']], [v[cols].values],
                                                      'euclidean') ** 2.0
    sum_intra_cluster_distances = sum_intra_cluster_distances[0][0]
    sum_inter_cluster_distances = (np.sum(distance.cdist(centroids, centroids, 'euclidean')) / 2.0) ** 2.0

    # plotting the dendrogram
    if plot_dendrogram:
        sns.set_style('whitegrid')
        p = sch.dendrogram(z, color_threshold=color_threshold)
        plt.show()

    return {'clusters': t, 'cluster_distribution': cluster_distribution, 'centroids': centroids,
            'sum_intra_cluster_distances': sum_intra_cluster_distances,
            'sum_inter_cluster_distances': sum_inter_cluster_distances}


def clustering_density(df, cols, k, n_jobs=1, n_init=10, random_state=None):
    """
    Performs a density clustering using K-Means. The implementation uses sklearn [1]_.

    Parameters
    ----------
    df : dataframe
        Input data frame
    cols : array_like
        List of columns to be considered from the data frame
    k : int
        Number of clusters
    n_jobs : int, optional
        The number of jobs to use for the computation. This works by computing each of the n_init runs in parallel.
        If -1 all CPUs are used.
    n_init : int, optional
        Number of time the k-means algorithm will be run with different centroid seeds. The final results will be the
        best output of n_init consecutive runs in terms of inertia.
    random_state : int, optional
        The generator used to initialize the centers. If an integer is given, it fixes the seed.

    Returns
    -------
    clusters : array_like
        List with the cluster assigned to each line
    cluster_distribution: dict
        Dictionary with the count on the number of data points per cluster
    centroids : array_like
        List of all the centroids
    sum_intra_cluster_distances : float
        Sum of Squares of distances of the data points to their cluster center
    sum_inter_cluster_distances : float
        Sum of Squares of distances among all the centroids

    Notes
    -----
    Some references about the error metrics and how to better define the number of clusters [2]_ [3]_

    References
    ----------
    .. [1] sklearn.cluster.KMeans
       http://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html

    .. [2] Data Mining Clustering
       http://wwwis.win.tue.nl/~tcalders/teaching/datamining09/slides/DM09-07-Clustering.pdf

    .. [3] Clustering Methods
       https://www.cs.swarthmore.edu/~meeden/cs63/s16/reading/Clustering.pdf


    Examples
    --------
    >>> import mdspy
    >>> import pandas as pd
    >>> mdspy.analytics.clustering_density(pd.DataFrame([[1, 1], [1, 2], [1, 2], [5, 10], [2, 10]]), 2)
    {'clusters': [0, 0, 0, 1, 1], 'sum_inter_cluster_distances': 8.7002554240921253,
    'centroids': [[1.0, 1.6666666666666665], [3.5, 10.0]], 'sum_intra_cluster_distances': 5.1666666666666661,
    'cluster_distribution': {0: 2, 1: 3}}
    >>> mdspy.analytics.clustering_density(pd.DataFrame([[1, 1], [1, 2], [1, 2], [5, 10], [2, 10]]), 2, 4, 50, 42))
    {'clusters': [1, 1, 1, 0, 0], 'sum_inter_cluster_distances': 8.7002554240921253,
    'centroids': [[3.5, 10.0], [1.0, 1.6666666666666665]], 'sum_intra_cluster_distances': 5.1666666666666661,
    'cluster_distribution': {0: 2, 1: 3}}
    """

    # set a random seed
    if random_state is None:
        random_state = np.random.random_integers(1000)
    kmeans = KMeans(k, n_jobs=n_jobs, n_init=n_init, random_state=random_state)
    kmeans.fit_transform(df[cols])
    T = list(kmeans.labels_)
    cluster_distribution = dict(collections.Counter(T))
    sum_intra_cluster_distances = kmeans.inertia_
    centroids = kmeans.cluster_centers_.tolist()
    sum_inter_cluster_distances = (np.sum(distance.cdist(centroids, centroids, 'euclidean')) / 2.0) ** 2.0

    return {'clusters': T, 'cluster_distribution': cluster_distribution, 'centroids': centroids,
            'sum_intra_cluster_distances': sum_intra_cluster_distances,
            'sum_inter_cluster_distances': sum_inter_cluster_distances}


def correlation(x, y):
    """
    Calculates a Pearson correlation coefficient and the p-value for testing non-correlation.

    Parameters
    ----------
    x : array_like
        Input sequences
    y : array_like
        Input sequences

    Returns
    -------
    pearson_correlation_coefficient : float
        Pearson's correlation coefficient
    interpretation : string
        Pearson's correlation coefficient interpretation

    Notes
    -----
    Following a table that explain the interpretation of the Pearson's correlation coefficient [1]_

    +---------------+-------------------------------+
    | Coefficient   | Strength of Relationship      |
    +===============+===============================+
    | [0.7, 1.0]    | Strong positive correlation   |
    +---------------+-------------------------------+
    | [0.5, 0.7[    | Moderate positive correlation |
    +---------------+-------------------------------+
    | [0.3, 0.5[    | Weak positive correlation     |
    +---------------+-------------------------------+
    | ]-0.3, 0.3[   | No correlation                |
    +---------------+-------------------------------+
    | [-0.3, -0.5[  | Weak negative correlation     |
    +---------------+-------------------------------+
    | [-0.5, -0.7[  | Moderate negative correlation |
    +---------------+-------------------------------+
    | [-0.7, -1.0]  | Strong negative correlation   |
    +---------------+-------------------------------+

    References
    ----------
    .. [1] Scatterplots and Correlation. Based on Chapter 4 of The Basic Practice of Statistics (6th ed.)
       https://www.westga.edu/academics/research/vrc/assets/docs/scatterplots_and_correlation_notes.pdf

    Examples
    --------
    >>> import mdspy
    >>> mdspy.analytics.correlation([1.0, 2.0, 2.0], [1.0, 2.0, 2.0])
    (1.0, 'Strong positive correlation')
    """

    r_row, p_value = stats.pearsonr(x, y)

    if r_row >= 0.7:
        interpretation = 'Strong positive correlation'
    elif r_row >= 0.5:
        interpretation = 'Moderate positive correlation'
    elif r_row >= 0.3:
        interpretation = 'Weak positive correlation'
    elif r_row <= -0.7:
        interpretation = 'Strong negative correlation'
    elif r_row <= -0.5:
        interpretation = 'Moderate negative correlation'
    elif r_row <= -0.3:
        interpretation = 'Weak negative correlation'
    else:
        interpretation = 'No correlation'

    return {'pearson_correlation_coefficient': r_row, 'interpretation': interpretation}
