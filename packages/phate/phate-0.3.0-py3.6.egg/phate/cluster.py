import graphtools
from sklearn.exceptions import NotFittedError
from sklearn.cluster import KMeans


def kmeans(phate_op, k=8):
    """KMeans on the PHATE potential

    Clustering on the PHATE operator as introduced in Moon et al.
    This is similar to spectral clustering.

    Parameters
    ----------

    phate_op : phate.PHATE
        Fitted PHATE operator
    k : int, optional (default: 8)
        Number of clusters

    Returns
    -------
    clusters : np.ndarray
        Integer array of cluster assignments
    """
    if phate_op.graph is not None:
        diff_potential = phate_op.calculate_potential()
        if isinstance(phate_op.graph, graphtools.graphs.LandmarkGraph):
            diff_potential = phate_op.graph.interpolate(diff_potential)
        return KMeans(k).fit_predict(diff_potential)
    else:
        raise NotFittedError("This PHATE instance is not fitted yet. Call "
                             "'fit' with appropriate arguments before "
                             "using this method.")
