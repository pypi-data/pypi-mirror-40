# -*- coding: utf-8 -*-
import numpy as np
import scipy.sparse as sp

from matplotlib import pyplot as plt

DATATYPE = np.float64


def operator(generators, indices_of_generators, weights, operator_type='fast'):
    """Create a LinearOperator object.

    This method defines the object that describes the linear operator by means
    of its fundamental components. These components are a set of generators, a
    table that encodes the non-zero entries of the operator and indexes the
    proper generator in each entry and another table that encodes the weight
    applied to each called generator in the linear operator.

    Each block of entries of the linear operator A is given by

        .. math:: A[k\cdot i\dots k\cdot(i+1), j] = g_{T_{i,j}} \cdot w_{i,j}

    where `k` is the length of the generators, `T` is the table of indices and
    `w` is the table of weights.

    Args:
        generators : np.array where each row is a generator.
        indices_of_generators : COO sparse matrix that tells which generator is
            called where in the linear operator.
        weights : COO sparse matrix that encodes the weight applied to each
            generator indexed by indices_of_generators. It has the same
            dimension as indices_of_generators.
        operator_type (optional): string
            Operator type to use. Accepted values are ``'fast'`` and
            ``'reference'``. The latter is intended to be used only for testing
            purposes. (default = `fast`).

    Returns:
        talon.core.LinearOperator: the wanted linear operator.

    Raises:
        ValueError: If `reference_type` is not ``'fast'`` or ``'reference'``.
    """

    args = (generators, indices_of_generators, weights)

    if operator_type == 'fast':
        return FastLinearOperator(*args)

    elif operator_type == 'reference':
        return LinearOperator(*args)

    raise ValueError('Invalid reference type {}. Should be "fast" or '
                     '"reference"'.format(operator_type))


def spy(linear_operator, **kwargs):
    """Spy a LinearOperator Object.

    This method is the equivalent of matplotlib.pyplot.spy where the considered
    matrix is the full matrix corresponding to a LinearOperator object.

    Args:
        linear_operator : LinearOperator object to be spied.
        **kwargs : arbitrary keyword arguments that are compatible with
            ``matplotlib.pyplot.spy``.

    Returns:
        matplotlib.pyplot.spy plot of `linear_operator`.

    Raises:
        ValueError: If in kwargs the `precision` variable is passed and not
            assigned to ``'present'``.
    """
    if 'precision' in kwargs.keys() and not kwargs['precision'] == 'present':
        raise ValueError('"precision" argument must be equal to "present"'
                         'or omitted.')
    else:
        kwargs['precision'] = 'present'
        return plt.spy(linear_operator._indices_of_generators, **kwargs)


class LinearOperator:
    def __init__(self, generators, indices_of_generators, weights):
        """Linear operator that maps tractography to signal space.
        The linear operator can be used to compute products with a vector.

        Args:
            generators : np.array where each row is a generator.
            indices_of_generators : COO sparse matrix that tells which
                generator is called where in the linear operator.
            weights : COO sparse matrix that encodes the weight applied to each
                generator indexed by indices_of_generators. It has the same
                dimension as indices_of_generators.
        Raises:
            TypeError: If `generators` is not a numpy ndarray of float.
            TypeError: If `indices_of_generators` is not a COO scipy matrix.
            TypeError: If `weights` is not a COO scipy matrix of float64.
            ValueError: If `weights` does not have the same dimension
                as indices_of_generators.
            ValueError: If `weights` and `indices_of_generators` don't have the
                same sparsity pattern.
        """
        if not isinstance(generators, np.ndarray):
            raise TypeError('Expected type for "generators" is np.ndarray.')
        if not generators.dtype == DATATYPE:
            raise TypeError(
                'Expected dtype for "generators" is {}.'.format(str(DATATYPE)))

        self._generators = generators

        if not sp.isspmatrix_coo(indices_of_generators):
            raise (TypeError(
                'Expected type for "indices_of_generators" is '
                'scipy.sparse.coo_matrix.'))

        self._indices_of_generators = indices_of_generators.astype(int)

        if not sp.isspmatrix_coo(weights):
            raise (TypeError('Expected type for "weights" is np.ndarray.'))
        if not weights.dtype == DATATYPE:
            raise TypeError(
                'Expected dtype for "weights" is {}.'.format(str(DATATYPE)))
        if not weights.shape == indices_of_generators.shape:
            raise ValueError(
                '"indices_of_generators" and "weights" must have the same'
                ' dimension')
        if not (
                len(weights.data) == len(indices_of_generators.data) and
                np.array_equal(weights.col, indices_of_generators.col) and
                np.array_equal(weights.row, indices_of_generators.row)):
            raise ValueError(
                '"indices_of_generators" and "weights" must have the same'
                ' sparsity pattern')

        self._weights = weights

    @property
    def columns(self):
        """int: Returns the indices of the nonzero columns."""
        return self._indices_of_generators.col

    @property
    def nb_generators(self):
        """int: Number of generators."""
        return self._generators.shape[0]

    @property
    def generator_length(self):
        """int: length of each generator (constant across generators)."""
        return self._generators.shape[1]

    @property
    def generators(self):
        """np.ndarray: Returns the generators of the linear operator."""
        return self._generators

    @property
    def indices(self):
        """np.ndarray: Returns the generator indices."""
        return self._indices_of_generators.data

    @property
    def nb_data(self):
        """int: Number of data points."""
        return self._indices_of_generators.shape[0]

    @property
    def nb_atoms(self):
        """int: Number of atoms (columns) in the linear operator."""
        return self._indices_of_generators.shape[1]

    @property
    def rows(self):
        """int: Returns the indices of the nonzero rows."""
        return self._indices_of_generators.row

    @property
    def shape(self):
        """:tuple of int: Shape of the linear operator.

        The shape is given by the number of rows and columns of the linear
        operator. The number of rows is equal to the number of data points
        times the length of the generators. The number of columns is equal to
        the number of atoms.
        """
        return self.nb_data * self.generator_length, self.nb_atoms

    @property
    def transpose(self):
        """TransposedLinearOperator: the transpose of the linear operator."""
        return TransposedLinearOperator(self)

    @property
    def T(self):
        return self.transpose

    @property
    def weights(self):
        """np.ndarray: The weights of the nonzero elements"""
        return self._weights.data

    def __matmul__(self, x):
        if not type(x) is np.ndarray:
            raise TypeError('Expected type for "x" is np.ndarray.')
        if not len(x) == self.shape[1]:
            raise ValueError('Dimension mismatch (%s != %s)'
                             % (len(x), self.shape[1]))

        product = np.zeros(self.shape[0], dtype=DATATYPE)
        for row, column, weighted_generator in self:
            tmp = weighted_generator * x[column]
            product[self.generator_length * row:
                    self.generator_length * (row + 1)] += tmp
        return product

    def todense(self):
        """Return the dense matrix associated to the linear operator.

        Note:
            The output of this method can be very memory heavy to store. Use at
            your own risk.

        Returns:
            ndarray: full matrix representing the linear operator.
        """
        dense = np.zeros(self.shape, dtype=DATATYPE)
        length = self.generator_length
        for row, column, generator in self:
            dense[length * row: length * (row + 1), column] = generator

        return dense

    def __iter__(self):
        indices = self._indices_of_generators
        rows, cols, data = indices.row, indices.col, indices.data
        weights = self._weights.data
        for r, c, idx, w in zip(rows, cols, data, weights):
            yield r, c, self._generators[idx, :] * w


class FastLinearOperator(LinearOperator):

    def __init__(self, generators, indices_of_generators, weights):
        """A LinearOperator that computes products quickly.

        The FastLinearOperator class implements a linear operator optimized to
        compute matrix-vector products quickly. It is single threaded and
        written in pure Python, which makes it a good default choice for linear
        operators.

        Args:
            generators : np.array where each row is a generator.
            indices_of_generators : COO sparse matrix that tells which
                generator is called where in the linear operator.
            weights : COO sparse matrix that encodes the weight applied to each
                generator indexed by indices_of_generators. It has the same
                dimension as indices_of_generators.

        Raises:
            TypeError: If generators is not a numpy ndarray of float64.
            TypeError: If indices_of_generators is not a COO scipy matrix.
            TypeError: If weights is not a COO scipy matrix of float64.
            ValueError: if weights does not have the same dimension
                as indices_of_generators.
            ValueError: if weights and indices_of_generators don't have the
                same sparsity pattern.

        """

        super().__init__(generators, indices_of_generators, weights)

        # Find the indices of the row which are not empty. This allows the
        # linear performance to be independent of the number of empty rows.
        row_indices = np.unique(self.rows)

        # The product is computed row by row. Here, we precompute which
        # generators are multiplied by which weight and x, and where the
        # result is placed.
        row_elements = [np.where(self.rows == r)[0] for r in row_indices]

        # The indices of the generator, for each row.
        row_generators = [self.indices[r] for r in row_elements]

        # The indices of nonzero columns for each row.
        row_columns = [self.columns[r] for r in row_elements]

        # The weights of the nonzero elements for each row.
        row_weights = [self.weights[r] for r in row_elements]

        length = self.generator_length

        def row_slice(row):
            return slice(length * row, length * (row + 1))

        row_slices = [row_slice(r) for r in row_indices]

        self._row = list(zip(row_columns, row_generators, row_weights,
                             row_slices))

    @property
    def transpose(self):
        """TransposedFastLinearOperator: transpose of the linear operator."""
        return TransposedFastLinearOperator(self)

    @property
    def T(self):
        return self.transpose

    def __matmul__(self, x):
        """Matrix vector product (A @ x)

        Args:
            x: The right operand of the product. It's length must match the
                number of columns of the linear operator.

        Raises:
            TypeError : If x is not a numpy array.
            ValueError : If the length of x does not match the number of
                columns of the linear operator.

        """

        if not type(x) is np.ndarray:
            raise TypeError('Expected type for "x" is np.ndarray.')

        if not len(x) == self.shape[1]:
            raise ValueError('Dimension mismatch (%s != %s)'
                             % (len(x), self.shape[1]))

        product = np.zeros(self.shape[0], dtype=DATATYPE)

        for elements, generator_indices, weights, row_slice in self._row:
            row_x = x[elements] * weights
            row_generators = self.generators[generator_indices, :]
            product[row_slice] = np.dot(row_generators.T, row_x)

        return product


class TransposedLinearOperator:

    def __init__(self, linear_operator):
        """Transposed of a LinearOperator object.

        Args:
            linear_operator : the LinearOperator object of which the transpose
                is wanted.
        """
        self._linear_operator = linear_operator

    @property
    def shape(self):
        return self._linear_operator.shape[::-1]

    def __matmul__(self, y):
        if not type(y) is np.ndarray:
            raise TypeError('Expected type for "y" is np.ndarray.')
        if not len(y) == self.shape[1]:
            raise ValueError('Dimension mismatch (%s != %s)'
                             % (len(y), self.shape[1]))

        genlen = self._linear_operator.generator_length
        product = np.zeros(self.shape[0], dtype=DATATYPE)
        for row, col, weighted_generator in self._linear_operator:
            indices_range = range(genlen * row, genlen * (row + 1))
            product[col] += weighted_generator.dot(y[indices_range])
        return product


class TransposedFastLinearOperator:

    def __init__(self, linear_operator):
        """Transposed of a LinearOperator object.

        Args:
            linear_operator : the LinearOperator object of which the transpose
                is wanted.
        """
        self._linear_operator = linear_operator

    @property
    def shape(self):
        """:tuple of int: Shape of the transposed linear operator.

        The shape is the flipped version of the one of the original linear
        operator, as in the definition of transpose matrix.
        """
        return self._linear_operator.shape[::-1]

    def __matmul__(self, y):
        """Matrix vector product (A.T @ y)

        Args:
            y: The left operand of the product. It's length must match the
                number of columns of the transposed linear operator.

        Raises:
            TypeError if y is not a numpy array.
            ValueError if the length of y does not match the number of
                columns of the transposed linear operator.

        """

        if not type(y) is np.ndarray:
            raise TypeError('Expected type for "y" is np.ndarray.')

        if not len(y) == self.shape[1]:
            raise ValueError('Dimension mismatch (%s != %s)'
                             % (len(y), self.shape[1]))

        product = np.zeros(self.shape[0], dtype=DATATYPE)
        for (elements, generator_indices,
             weights, row_slice) in self._linear_operator._row:
            row_y = y[row_slice]
            row_generators = self._linear_operator.generators[
                             generator_indices, :]
            product[elements] += row_generators.dot(row_y) * weights

        return product
