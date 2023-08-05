"""
.. module:: abstract
    :platform: Unix, Windows
    :synopsis: Provides abstract base classes for parametric shapes

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

import copy
import abc
import six
import warnings
from .evaluators import AbstractEvaluator
from .tessellate import AbstractTessellate
from . import vis
from . import helpers
from . import utilities
from . import voxelize


class Curve(six.with_metaclass(abc.ABCMeta, object)):
    """ Abstract base class (ABC) for parametric curves.

    The Curve ABC is inherited from abc.ABCMeta class which is included in Python standard library by default. Due to
    differences between Python 2 and 3 on defining a metaclass, the compatibility module ``six`` is employed. Using
    ``six`` to set metaclass allows users to use the abstract classes in a correct way.

    The abstract base classes in this module are implemented using a feature called Python Properties. This feature
    allows users to use some of the functions as if they are class fields. You can also consider properties as a
    pythonic way to set getters and setters. You will see "getter" and "setter" descriptions on the documentation of
    these properties.

    The Curve ABC allows users to set the *FindSpan* function to be used in evaluations with ``find_span_func`` keyword
    as an input to the class constructor. NURBS-Python includes a binary and a linear search variation of the FindSpan
    function in the ``helpers`` module.
    You may also implement and use your own *FindSpan* function. Please see the ``helpers`` module for details.

    Code segment below illustrates a possible implementation of Curve abstract base class:

    .. code-block:: python

        from geomdl import abstract

        class MyCurveClass(abstract.Curve):
            def __init__(self, **kwargs):
            super(MyCurveClass, self).__init__(**kwargs)
            # Add your constructor code here

            def evaluate(self, **kwargs):
                # Implement this function
                pass

            def evaluate_single(self, uv):
                # Implement this function
                pass

            def evaluate_list(self, uv_list):
                # Implement this function
                pass

            def derivatives(self, u, v, order, **kwargs):
                # Implement this function
                pass

    The properties and functions defined in the abstract base class will be automatically available in the subclasses.
    """

    def __init__(self, **kwargs):
        self._array_type = list
        self._iter_index = 0  # iterator index
        self._name = "Curve"  # descriptor field
        self._rational = False  # defines whether the curve is rational or not
        self._degree = 0  # degree
        self._knot_vector = self._init_var(self._array_type)  # knot vector
        self._control_points = self._init_var(self._array_type)  # control points
        self._delta = 0.01  # evaluation delta
        self._curve_points = self._init_var(self._array_type)  # evaluated points
        self._dimension = 0  # dimension of the curve
        self._vis_component = None  # visualization component
        self._bounding_box = self._init_var(self._array_type)  # bounding box
        self._evaluator = None  # evaluator instance
        self._precision = 18  # number of decimal places to round to
        self._span_func = kwargs.get('find_span_func', helpers.find_span_linear)  # default "find_span" function
        self._kv_normalize = kwargs.get('normalize_kv', True)  # normalize knot vector
        self._cache = {}  # cache dictionary

    def __iter__(self):
        self._iter_index = 0
        return self

    def next(self):
        return self.__next__()

    def __next__(self):
        if self._iter_index > 0:
            raise StopIteration
        self._iter_index += 1
        return self

    def __len__(self):
        return 1

    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result

    def __deepcopy__(self, memo):
        # Don't copy self reference
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        # Don't copy the cache
        memo[id(self._cache)] = self._cache.__new__(dict)
        # Copy all other attributes
        for k, v in self.__dict__.items():
            setattr(result, k, copy.deepcopy(v, memo))
        return result

    def __str__(self):
        return self.name

    __repr__ = __str__

    def _init_var(self, arr_type):
        """ Initializes the arrays.

        :param arr_type: array type
        """
        if callable(arr_type):
            return arr_type()
        else:
            return None

    @property
    def name(self):
        """ Curve descriptor (as a string or a number).

        Descriptor field allows users to assign an identification to the curve object. The identification can be a
        string or a number.

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets the descriptor
        :setter: Sets the descriptor
        :type: str or int
        """
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def evaluator(self):
        """ Curve evaluator.

        Evaluators allow users to use different algorithms for B-Spline and NURBS evaluations. Please see the
        documentation on ``Evaluator`` classes.

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets the current Evaluator instance
        :setter: Sets the evaluator
        """
        return self._evaluator

    @evaluator.setter
    def evaluator(self, value):
        if not isinstance(value, AbstractEvaluator):
            raise TypeError("The evaluator must be an instance of AbstractEvaluator")
        value._span_func = self._span_func
        self._evaluator = value

    @property
    def rational(self):
        """ True if the curve is rational.

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Returns True is the curve is rational (NURBS)
        :type: bool
        """
        return self._rational

    @property
    def dimension(self):
        """ Dimension of the curve.

        Dimension will be automatically estimated from the first element of the control points array.

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets the dimension of the curve, e.g. 2D, 3D, etc.
        :type: integer
        """
        if self._rational:
            return self._dimension - 1
        return self._dimension

    @property
    def order(self):
        """ Order.

        Defined as ``order = degree + 1``

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets the order
        :setter: Sets the order
        :type: integer
        """
        return self.degree + 1

    @order.setter
    def order(self, value):
        self.degree = value - 1

    @property
    def degree(self):
        """ Degree.

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets the degree
        :setter: Sets the degree
        :type: integer
        """
        return self._degree

    @degree.setter
    def degree(self, value):
        val = int(value)
        if val < 0:
            raise ValueError("Degree cannot be less than zero")

        # Clean up the curve points list
        self.reset(evalpts=True)

        # Set degree
        self._degree = val

    @property
    def knotvector(self):
        """ Knot vector.

        The knot vector will be normalized to [0, 1] domain if the class is initialized with ``normalize_kv=True``
        argument.

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets the knot vector
        :setter: Sets the knot vector
        """
        return tuple(self._knot_vector)

    @knotvector.setter
    def knotvector(self, value):
        if self.degree == 0 or self._control_points is None or len(self._control_points) == 0:
            raise ValueError("Set degree and control points first")

        # Check knot vector validity
        if not utilities.check_knot_vector(self.degree, value, len(self._control_points)):
            raise ValueError("Input is not a valid knot vector")

        # Clean up the curve points lists
        self.reset(evalpts=True)

        # Set knot vector
        self._knot_vector = utilities.normalize_knot_vector(value, decimals=self._precision) \
            if self._kv_normalize else value

    @property
    def ctrlpts(self):
        """ Control points.

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets the control points
        :setter: Sets the control points
        """
        return self._control_points

    @ctrlpts.setter
    def ctrlpts(self, value):
        self._control_points = value

    @property
    def ctrlpts_size(self):
        """ Number of control points.

        :getter: Gets number of control points
        """
        return len(self._control_points)

    @property
    def evalpts(self):
        """ Evaluated points.

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets the coordinates of the evaluated points
        """
        if self._curve_points is None or len(self._curve_points) == 0:
            self.evaluate()

        return self._curve_points

    @property
    def sample_size(self):
        """ Sample size.

        Sample size defines the number of evaluated points to generate. It also sets the ``delta`` property.

        The following figure illustrates the working principles of sample size property:

        .. math::

            \\underbrace {\\left[ {{u_{start}}, \\ldots ,{u_{end}}} \\right]}_{{n_{sample}}}

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets sample size
        :setter: Sets sample size
        :type: int
        """
        return int(1.0 / self.delta) + 1

    @sample_size.setter
    def sample_size(self, value):
        if not isinstance(value, int):
            raise ValueError("Sample size must be an integer value")

        if self.knotvector is None or len(self.knotvector) == 0 or self.degree == 0:
            warnings.warn("Cannot determine the delta value. Please set knot vector and degree before sample size.")
            return

        # To make it operate like linspace, we have to know the starting and ending points.
        start = self.knotvector[self.degree]
        stop = self.knotvector[-(self.degree+1)]

        # Set delta value
        self.delta = (stop - start) / float(value - 1)

    @property
    def delta(self):
        """ Evaluation delta.

        Evaluation delta corresponds to the *step size* while ``evaluate`` function iterates on the knot vector to
        generate curve points. Decreasing step size results in generation of more curve points.
        Therefore; smaller the delta value, smoother the curve.

        The following figure illustrates the working principles of the delta property:

        .. math::

            \\left[{{u_{start}},{u_{start}} + \\delta ,({u_{start}} + \\delta ) + \\delta , \\ldots ,{u_{end}}} \\right]

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets the delta value
        :setter: Sets the delta value
        :type: float
        """
        return self._delta

    @delta.setter
    def delta(self, value):
        # Delta value for surface evaluation should be between 0 and 1
        if float(value) <= 0 or float(value) >= 1:
            raise ValueError("Curve evaluation delta should be between 0.0 and 1.0")

        # Clean up the curve points list
        self.reset(evalpts=True)

        # Set new delta value
        self._delta = float(value)

    @property
    def vis(self):
        """ Visualization component.

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets the visualization component
        :setter: Sets the visualization component
        """
        return self._vis_component

    @vis.setter
    def vis(self, value):
        if not isinstance(value, vis.VisAbstract):
            warnings.warn("Visualization component is NOT an instance of VisAbstract class")
            return
        self._vis_component = value

    @property
    def bbox(self):
        """ Bounding box.

        Evaluates the bounding box of the curve and returns the minimum and maximum coordinates.

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets bounding box
        :type: tuple
        """
        if self._bounding_box is None or len(self._bounding_box) == 0:
            self._bounding_box = utilities.evaluate_bounding_box(self.ctrlpts)

        return tuple(self._bounding_box)

    @property
    def data(self):
        """ Returns a dictionary containing all shape data.

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.
        """
        return dict(
            rational=self.rational,
            dimension=self.dimension,
            degree=self._degree,
            knotvector=self._knot_vector,
            size=self.ctrlpts_size,
            control_points=self._control_points
        )

    def set_ctrlpts(self, ctrlpts, **kwargs):
        """ Sets control points and checks if the data is consistent.

        This method is designed to provide a consistent way to set control points whether they are weighted or not.
        It directly sets the control points member of the class, and therefore it doesn't return any values.
        The input will be an array of coordinates. If you are working in the 3-dimensional space, then your coordinates
        will be an array of 3 elements representing *(x, y, z)* coordinates.

        It accepts a keyword argument ``array_init`` which defaults to a ``list`` of size ``len(ctrlpts)``
        where ``ctrlpts`` is the input list of control points. ``array_init`` keyword argument may be used to input
        other types of arrays to this method.

        The following example illustrates a way to use a NumPy array with this method.

        .. code-block:: python

            # Import numpy
            import numpy as np

            # Assuming that "ctrlpts" is a NumPy array of a shape (x,y) where x == len(ctrlpts) and y == len(ctrlpts[0])
            curve.set_ctrlpts(ctrlpts, array_init=np.zeros(ctrlpts.shape, dtype=np.float32))

        :param ctrlpts: input control points as a list of coordinates
        :type ctrlpts: list
        """
        # Degree must be set before setting the control points
        if self.degree <= 0:
            raise ValueError("Set the degree first")

        if len(ctrlpts) < self.degree + 1:
            raise ValueError("Number of control points should be at least degree + 1")

        # Keyword arguments
        array_init = kwargs.get('array_init', [[] for _ in range(len(ctrlpts))])

        # Clean up the curve and control points lists
        self.reset(ctrlpts=True, evalpts=True)

        # Estimate dimension by checking the size of the first element
        self._dimension = len(ctrlpts[0])

        ctrlpts_float = array_init
        for idx, cpt in enumerate(ctrlpts):
            if not isinstance(cpt, (list, tuple)):
                raise ValueError("Element number " + str(idx) + " is not a list")
            if len(cpt) is not self._dimension:
                raise ValueError("The input must be " + str(self._dimension) + " dimensional list - " + str(cpt) +
                                 " is not a valid control point")
            # Convert to list of floats
            ctrlpts_float[idx] = [float(coord) for coord in cpt]

        self._control_points = ctrlpts_float

    # Runs visualization component to render the curve
    def render(self, **kwargs):
        """ Renders the curve using the visualization component

        The visualization component must be set using :py:attr:`~vis` property before calling this method.

        Keyword Arguments:
            * ``cpcolor``: sets the color of the control points polygon
            * ``evalcolor``: sets the color of the curve
            * ``bboxcolor``: sets the color of the bounding box
            * ``filename``: saves the plot with the input name
            * ``plot``: a flag to control displaying the plot window. *Default: True*
            * ``extras``: adds line plots to the figure. *Default: None*

        ``plot`` argument is useful when you would like to work on the command line without any window context.
        If ``plot`` flag is False, this method saves the plot as an image file (.png file where possible) and disables
        plot window popping out. If you don't provide a file name, the name of the image file will be pulled from the
        configuration class.

        ``extras`` argument can be used to add extra line plots to the figure. This argument expects a list of dicts
        in the format described below:

        .. code-block:: python

            [
                dict(  # line plot 1
                    points=[[1, 2, 3], [4, 5, 6]],  # list of points
                    name="My line Plot 1",  # name displayed on the legend
                    color="red",   # color of the line plot
                    size=6.5  # size of the line plot
                ),
                dict(  # line plot 2
                    points=[[7, 8, 9], [10, 11, 12]],  # list of points
                    name="My line Plot 2",  # name displayed on the legend
                    color="navy",   # color of the line plot
                    size=12.5  # size of the line plot
                )
            ]
        """
        if not self._vis_component:
            warnings.warn("No visualization component has been set")
            return

        cpcolor = kwargs.get('cpcolor', 'blue')
        evalcolor = kwargs.get('evalcolor', 'black')
        bboxcolor = kwargs.get('bboxcolor', 'darkorange')
        filename = kwargs.get('filename', None)
        plot_visible = kwargs.get('plot', True)
        extra_plots = kwargs.get('extras', None)

        # Check all parameters are set
        self._check_variables()

        # Check if the curve has been evaluated
        if self._curve_points is None or len(self._curve_points) == 0:
            self.evaluate()

        # Clear the visualization component
        self._vis_component.clear()

        # Control points
        self._vis_component.add(ptsarr=self.ctrlpts, name="Control Points", color=cpcolor, plot_type='ctrlpts')

        # Evaluated points
        self._vis_component.add(ptsarr=self.evalpts, name=self.name, color=evalcolor, plot_type='evalpts')

        # Bounding box
        self._vis_component.add(ptsarr=self.bbox, name="Bounding Box", color=bboxcolor, plot_type='bbox')

        # User-defined plots
        if extra_plots is not None:
            for ep in extra_plots:
                self._vis_component.add(ptsarr=ep['points'], name=ep['name'],
                                        color=(ep['color'], ep['size']), plot_type='extras')

        # Data requested by the visualization module
        if self._vis_component.plot_types['others']:
            vis_other = self._vis_component.plot_types['others'].split(",")
            for vo in vis_other:
                vo_clean = vo.strip()
                # Send center point of the parametric space to the visualization module
                if vo_clean == "midpt":
                    midprm = (max(self.knotvector) + min(self.knotvector)) / 2.0
                    midpt = self.evaluate_single(midprm)
                    self._vis_component.add(ptsarr=[midpt], plot_type=vo_clean)

        # Plot the curve
        self._vis_component.render(fig_save_as=filename, display_plot=plot_visible)

    def reset(self, **kwargs):
        """ Resets control points and/or evaluated points.

        Keyword Arguments:
            * ``evalpts``: if True, then resets evaluated points
            * ``ctrlpts`` if True, then resets control points

        """
        reset_ctrlpts = kwargs.get('ctrlpts', False)
        reset_evalpts = kwargs.get('evalpts', False)

        if reset_ctrlpts:
            self._control_points = self._init_var(self._array_type)
            self._bounding_box = self._init_var(self._array_type)

        if reset_evalpts:
            self._curve_points = self._init_var(self._array_type)

    # Checks whether the curve evaluation is possible or not
    def _check_variables(self):
        works = True
        param_list = []
        if self.degree == 0:
            works = False
            param_list.append('degree')
        if self._control_points is None or len(self._control_points) == 0:
            works = False
            param_list.append('ctrlpts')
        if self.knotvector is None or len(self.knotvector) == 0:
            works = False
            param_list.append('knotvector')
        if not works:
            raise ValueError("Please set the following variables before evaluation: " + ",".join(param_list))

    @abc.abstractmethod
    def evaluate(self, **kwargs):
        """ Evaluates the parametric curve.

        .. note::

            This is an abstract method and it must be implemented in the subclass.

        """
        # Check all parameters are set before the curve evaluation
        self._check_variables()

        # Should implement the evaluation functionality
        pass

    @abc.abstractmethod
    def evaluate_single(self, param):
        """ Evaluates the parametric curve at the given parameter.

        .. note::

            This is an abstract method and it must be implemented in the subclass.

        :param param: parameter
        """
        # Check all parameters are set before the evaluation
        self._check_variables()

        # Should implement the evaluation functionality
        pass

    @abc.abstractmethod
    def evaluate_list(self, param_list):
        """ Evaluates the parametric curve for an input range of parameters.

        .. note::

            This is an abstract method and it must be implemented in the subclass.

        :param param_list: array of parameters
        """
        # Check all parameters are set before the evaluation
        self._check_variables()

        # Should implement the evaluation functionality
        pass

    @abc.abstractmethod
    def derivatives(self, u, order, **kwargs):
        """ Evaluates the derivatives of the parametric curve at parameter u.

        .. note::

            This is an abstract method and it must be implemented in the subclass.

        :param u: parameter value
        :type u: float
        :param order: derivative order
        :type order: int
        """
        # Check all parameters are set before the curve evaluation
        self._check_variables()

        # Check u parameters are correct
        utilities.check_params(u)

        # Should implement the derivatives functionality
        pass


class Surface(six.with_metaclass(abc.ABCMeta, object)):
    """ Abstract base class (ABC) for parametric surfaces.

    The Surface ABC is inherited from abc.ABCMeta class which is included in Python standard library by default. Due to
    differences between Python 2 and 3 on defining a metaclass, the compatibility module ``six`` is employed. Using
    ``six`` to set metaclass allows users to use the abstract classes in a correct way.

    The abstract base classes in this module are implemented using a feature called Python Properties. This feature
    allows users to use some of the functions as if they are class fields. You can also consider properties as a
    pythonic way to set getters and setters. You will see "getter" and "setter" descriptions on the documentation of
    these properties.

    The Surface ABC allows users to set the *FindSpan* function to be used in evaluations with ``find_span_func``
    keyword as an input to the class constructor. NURBS-Python includes a binary and a linear search variation of the
    FindSpan function in the ``helpers`` module.
    You may also implement and use your own *FindSpan* function. Please see the ``helpers`` module for details.

    Code segment below illustrates a possible implementation of Surface abstract base class:

    .. code-block:: python

        from geomdl import abstract

        class MySurfaceClass(abstract.Surface):
            def __init__(self, **kwargs):
            super(MySurfaceClass, self).__init__(**kwargs)
            # Add your constructor code here

            def evaluate(self, **kwargs):
                # Implement this function
                pass

            def evaluate_single(self, uv):
                # Implement this function
                pass

            def evaluate_list(self, uv_list):
                # Implement this function
                pass

            def derivatives(self, u, v, order, **kwargs):
                # Implement this function
                pass

    The properties and functions defined in the abstract base class will be automatically available in the subclasses.
    """

    def __init__(self, **kwargs):
        self._array_type = list
        self._iter_index = 0  # iterator index
        self._degree = [0, 0]  # degree
        self._knot_vector = [self._init_array(self._array_type), self._init_array(self._array_type)]  # knot vector
        self._control_points_size = [0, 0]  # control points array length
        self._delta = [0.05, 0.05]  # evaluation delta
        self._name = "Surface"  # descriptor field
        self._rational = False  # defines whether the surface is rational or not
        self._control_points = self._init_array(self._array_type)  # control points, 1-D array (v-order)
        self._control_points2D = self._init_array(self._array_type)  # control points, 2-D array [u][v]
        self._surface_points = self._init_array(self._array_type)  # evaluated points
        self._dimension = 0  # dimension of the surface
        self._vis_component = None  # visualization component
        self._tsl_component = None  # tessellation component
        self._bounding_box = self._init_array(self._array_type)  # bounding box
        self._evaluator = None  # evaluator instance
        self._precision = 18  # number of decimal places to round to
        self._span_func = kwargs.get('find_span_func', helpers.find_span_linear)  # default "find_span" function
        self._kv_normalize = kwargs.get('normalize_kv', True)  # normalize knot vectors
        self._cache = {}  # cache dictionary
        # Advanced functionality
        self._trims = self._init_array(self._array_type)  # trim curves

    def __iter__(self):
        self._iter_index = 0
        return self

    def next(self):
        return self.__next__()

    def __next__(self):
        if self._iter_index > 0:
            raise StopIteration
        self._iter_index += 1
        return self

    def __len__(self):
        return 1

    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result

    def __deepcopy__(self, memo):
        # Don't copy self reference
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        # Don't copy the cache
        memo[id(self._cache)] = self._cache.__new__(dict)
        # Copy all other attributes
        for k, v in self.__dict__.items():
            setattr(result, k, copy.deepcopy(v, memo))
        return result

    def __str__(self):
        return self.name

    __repr__ = __str__

    def _init_array(self, arr_type, **kwargs):
        """ Initializes the arrays.

        :param arr_type: array type
        """
        if callable(arr_type):
            return arr_type()
        else:
            return None

    @property
    def name(self):
        """ Surface descriptor (as a string or a number).

        Descriptor field allows users to assign an identification to the surface object. The identification can be a
        string or a number.

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets the descriptor
        :setter: Sets the descriptor
        :type: str or int
        """
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def evaluator(self):
        """ Surface evaluator.

        Evaluators allow users to use different algorithms for B-Spline and NURBS evaluations. Please see the
        documentation on ``Evaluator`` classes.

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Prints the name of the evaluator and returns the current Evaluator instance
        :setter: Sets the evaluator
        """
        return self._evaluator

    @evaluator.setter
    def evaluator(self, value):
        if not isinstance(value, AbstractEvaluator):
            raise TypeError("The evaluator must be an instance of Abstract.Evaluator")
        value._span_func = self._span_func
        self._evaluator = value

    @property
    def rational(self):
        """ True if the surface is rational.

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Returns True if the surface is rational (NURBS)
        :type: bool
        """
        return self._rational

    @property
    def dimension(self):
        """ Dimension of the surface.

        Dimension will be automatically estimated from the first element of the control points array.

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets the dimension of the surface
        :type: integer
        """
        if self._rational:
            return self._dimension - 1
        return self._dimension

    @property
    def order_u(self):
        """ Order for the u-direction.

        Defined as ``order = degree + 1``

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets order for the u-direction
        :setter: Sets order for the u-direction
        :type: integer
        """
        return self.degree_u + 1

    @order_u.setter
    def order_u(self, value):
        self.degree_u = value - 1

    @property
    def order_v(self):
        """ Order for the v-direction.

        Defined as ``order = degree + 1``

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets surface order for the v-direction
        :setter: Sets surface order for the v-direction
        :type: integer
        """
        return self.degree_v + 1

    @order_v.setter
    def order_v(self, value):
        self.degree_v = value - 1

    @property
    def degree_u(self):
        """ Degree for the u-direction.

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets degree for the u-direction
        :setter: Sets degree for the u-direction
        :type: integer
        """
        return self._degree[0]

    @degree_u.setter
    def degree_u(self, value):
        val = int(value)
        if val <= 0:
            raise ValueError("Degree cannot be less than zero")
        # Clean up the surface points
        self.reset(evalpts=True)
        # Set degree u
        self._degree[0] = int(value)

    @property
    def degree_v(self):
        """ Degree for the v-direction.

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets degree for the v-direction
        :setter: Sets degree for the v-direction
        :type: integer
        """
        return self._degree[1]

    @degree_v.setter
    def degree_v(self, value):
        val = int(value)
        if val <= 0:
            raise ValueError("Degree cannot be less than zero")
        # Clean up the surface points
        self.reset(evalpts=True)
        # Set degree v
        self._degree[1] = val

    @property
    def knotvector_u(self):
        """ Knot vector for the u-direction.

        The knot vector will be normalized to [0, 1] domain if the class is initialized with ``normalize_kv=True``
        argument.

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets knot vector for the u-direction
        :setter: Sets knot vector for the u-direction
        """
        return tuple(self._knot_vector[0])

    @knotvector_u.setter
    def knotvector_u(self, value):
        if self.degree_u == 0 or self.ctrlpts_size_u == 0:
            raise ValueError("Set degree and control points first for the u-direction")

        # Check knot vector validity
        if not utilities.check_knot_vector(self.degree_u, value, self.ctrlpts_size_u):
            raise ValueError("Input is not a valid knot vector for the u-direction")

        # Clean up the surface points
        self.reset(evalpts=True)

        # Set knot vector
        self._knot_vector[0] = utilities.normalize_knot_vector(value, decimals=self._precision) \
            if self._kv_normalize else value

    @property
    def knotvector_v(self):
        """ Knot vector for the v-direction.

        The knot vector will be normalized to [0, 1] domain if the class is initialized with ``normalize_kv=True``
        argument.

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets knot vector for the v-direction
        :setter: Sets knot vector for the v-direction
        """
        return tuple(self._knot_vector[1])

    @knotvector_v.setter
    def knotvector_v(self, value):
        if self.degree_v == 0 or self.ctrlpts_size_v == 0:
            raise ValueError("Set degree and control points first for the v-direction")

        # Check knot vector validity
        if not utilities.check_knot_vector(self.degree_v, value, self.ctrlpts_size_v):
            raise ValueError("Input is not a valid knot vector for the v-direction")

        # Clean up the surface points
        self.reset(evalpts=True)

        # Set knot vector
        self._knot_vector[1] = utilities.normalize_knot_vector(value, decimals=self._precision) \
            if self._kv_normalize else value

    @property
    def ctrlpts(self):
        """ 1-dimensional array of control points.

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets the control points
        :setter: Sets the control points
        """
        return self._control_points

    @ctrlpts.setter
    def ctrlpts(self, value):
        self._control_points = value

    @property
    def ctrlpts2d(self):
        """ 2-dimensional control points.

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets the control points as a 2-dimensional array in [u][v] format
        :setter: Sets the control points as a 2-dimensional array in [u][v] format
        """
        return self._control_points2D

    @ctrlpts2d.setter
    def ctrlpts2d(self, value):
        self._control_points2D = value

    @property
    def ctrlpts_size(self):
        """ Total number of control points.

        :getter: Gets the total number of control points
        :type: int
        """
        res = 1
        for sz in self._control_points_size:
            res *= sz
        return res

    @property
    def ctrlpts_size_u(self):
        """ Number of control points for the u-direction.

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets number of control points for the u-direction
        :setter: Sets number of control points for the u-direction
        """
        return self._control_points_size[0]

    @ctrlpts_size_u.setter
    def ctrlpts_size_u(self, value):
        if not isinstance(value, int):
            raise TypeError("Number of control points for the u-direction must be an integer number")
        if value <= 0:
            raise ValueError("Control points size cannot be less than and equal to zero")

        # Assume that user is doing this right
        self._control_points_size[0] = value

    @property
    def ctrlpts_size_v(self):
        """ Number of control points for the v-direction.

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets number of control points on the v-direction
        :setter: Sets number of control points on the v-direction
        """
        return self._control_points_size[1]

    @ctrlpts_size_v.setter
    def ctrlpts_size_v(self, value):
        if not isinstance(value, int):
            raise TypeError("Number of control points on the v-direction must be an integer number")
        if value <= 0:
            raise ValueError("Control points size cannot be less than and equal to zero")

        # Assume that user is doing this right
        self._control_points_size[1] = value

    @property
    def evalpts(self):
        """ Evaluated surface points.

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets the coordinates of the evaluated points
        """
        if self._surface_points is None or len(self._surface_points) == 0:
            self.evaluate()

        return self._surface_points

    @property
    def sample_size_u(self):
        """ Sample size for the u-direction.

        Sample size defines the number of surface points to generate. It also sets the ``delta_u`` property.

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets sample size for the u-direction
        :setter: Sets sample size for the u-direction
        :type: int
        """
        return int(1.0 / self.delta_u) + 1

    @sample_size_u.setter
    def sample_size_u(self, value):
        if not isinstance(value, int):
            raise ValueError("Sample size must be an integer value")

        if (self.knotvector_u is None or len(self.knotvector_u) == 0) or self.degree_u == 0:
            warnings.warn("Cannot determine 'delta_u' value. Please set knot vectors and degrees before sample size.")
            return

        # To make it operate like linspace, we have to know the starting and ending points.
        start_u = self.knotvector_u[self.degree_u]
        stop_u = self.knotvector_u[-(self.degree_u+1)]

        # Set delta values
        self.delta_u = (stop_u - start_u) / float(value - 1)

    @property
    def sample_size_v(self):
        """ Sample size for the v-direction.

        Sample size defines the number of surface points to generate. It also sets the ``delta_v`` property.

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets sample size for the v-direction
        :setter: Sets sample size for the v-direction
        :type: int
        """
        return int(1.0 / self.delta_v) + 1

    @sample_size_v.setter
    def sample_size_v(self, value):
        if not isinstance(value, int):
            raise ValueError("Sample size must be an integer value")

        if (self.knotvector_v is None or len(self.knotvector_v) == 0) or self.degree_v == 0:
            warnings.warn("Cannot determine 'delta_v' value. Please set knot vectors and degrees before sample size.")
            return

        # To make it operate like linspace, we have to know the starting and ending points.
        start_v = self.knotvector_v[self.degree_v]
        stop_v = self.knotvector_v[-(self.degree_v+1)]

        # Set delta values
        self.delta_v = (stop_v - start_v) / float(value - 1)

    @property
    def sample_size(self):
        """ Sample size for both u- and v-directions.

        Sample size defines the number of surface points to generate. It also sets the ``delta`` property.

        The following figure illustrates the working principles of sample size property:

        .. math::

            \\underbrace {\\left[ {{u_{start}}, \\ldots ,{u_{end}}} \\right]}_{{n_{sample}}}

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets sample size as a tuple of values corresponding to u- and v-directions
        :setter: Sets sample size for both u- and v-directions
        :type: int
        """
        sample_size_u = int(1.0 / self.delta_u) + 1
        sample_size_v = int(1.0 / self.delta_v) + 1
        return sample_size_u, sample_size_v

    @sample_size.setter
    def sample_size(self, value):
        if (self.knotvector_u is None or len(self.knotvector_u) == 0) or self.degree_u == 0 or\
                (self.knotvector_v is None or len(self.knotvector_v) == 0 or self.degree_v == 0):
            warnings.warn("Cannot determine 'delta' value. Please set knot vectors and degrees before sample size.")
            return

        # To make it operate like linspace, we have to know the starting and ending points.
        start_u = self.knotvector_u[self.degree_u]
        stop_u = self.knotvector_u[-(self.degree_u+1)]
        start_v = self.knotvector_v[self.degree_v]
        stop_v = self.knotvector_v[-(self.degree_v+1)]

        # Set delta values
        self.delta_u = (stop_u - start_u) / float(value - 1)
        self.delta_v = (stop_v - start_v) / float(value - 1)

    @property
    def delta_u(self):
        """ Evaluation delta for the u-direction.

        Evaluation delta corresponds to the *step size* while ``evaluate()`` function iterates on the knot vector to
        generate surface points. Decreasing step size results in generation of more surface points.
        Therefore; smaller the delta value, smoother the surface.

        Please note that ``delta_u`` and ``sample_size_u`` properties correspond to the same variable with different
        descriptions. Therefore, setting ``delta_u`` will also set ``sample_size_u``.

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets evaluation delta for the u-direction
        :setter: Sets evaluation delta for the u-direction
        :type: float
        """
        return self._delta[0]

    @delta_u.setter
    def delta_u(self, value):
        # Delta value for surface evaluation should be between 0 and 1
        if float(value) <= 0 or float(value) >= 1:
            raise ValueError("Surface evaluation delta (u-direction) must be between 0.0 and 1.0")

        # Clean up the surface points
        self.reset(evalpts=True)

        # Set new delta value
        self._delta[0] = float(value)

    @property
    def delta_v(self):
        """ Evaluation delta for the v-direction.

        Evaluation delta corresponds to the *step size* while ``evaluate()`` function iterates on the knot vector to
        generate surface points. Decreasing step size results in generation of more surface points.
        Therefore; smaller the delta value, smoother the surface.

        Please note that ``delta_v`` and ``sample_size_v`` properties correspond to the same variable with different
        descriptions. Therefore, setting ``delta_v`` will also set ``sample_size_v``.

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets evaluation delta for the v-direction
        :setter: Sets evaluation delta for the v-direction
        :type: float
        """
        return self._delta[1]

    @delta_v.setter
    def delta_v(self, value):
        # Delta value for surface evaluation should be between 0 and 1
        if float(value) <= 0 or float(value) >= 1:
            raise ValueError("Surface evaluation delta (v-direction) should be between 0.0 and 1.0")

        # Clean up the surface points
        self.reset(evalpts=True)

        # Set new delta value
        self._delta[1] = float(value)

    @property
    def delta(self):
        """ Evaluation delta for both u- and v-directions.

        Evaluation delta corresponds to the *step size* while ``evaluate()`` function iterates on the knot vector to
        generate surface points. Decreasing step size results in generation of more surface points.
        Therefore; smaller the delta value, smoother the surface.

        Please note that ``delta`` and ``sample_size`` properties correspond to the same variable with different
        descriptions. Therefore, setting ``delta`` will also set ``sample_size``.

        The following figure illustrates the working principles of the delta property:

        .. math::

            \\left[{{u_{0}},{u_{start}} + \\delta ,({u_{start}} + \\delta ) + \\delta , \\ldots ,{u_{end}}} \\right]

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets evaluation delta as a tuple of values corresponding to u- and v-directions
        :setter: Sets evaluation delta for both u- and v-directions
        :type: float
        """
        return self.delta_u, self.delta_v

    @delta.setter
    def delta(self, value):
        if isinstance(value, (int, float)):
            self.delta_u = value
            self.delta_v = value
        elif isinstance(value, (list, tuple)):
            if len(value) == 2:
                self.delta_u = value[0]
                self.delta_v = value[1]
            else:
                raise ValueError("Surface requires 2 delta values")
        else:
            raise ValueError("Cannot set delta. Please input a numeric value or a list or tuple with 2 numeric values")

    @property
    def vis(self):
        """ Visualization component.

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets the visualization component
        :setter: Sets the visualization component
        """
        return self._vis_component

    @vis.setter
    def vis(self, value):
        if not isinstance(value, vis.VisAbstract):
            warnings.warn("Visualization component must be an instance of VisAbstract class")
            return

        self._vis_component = value

    @property
    def tessellator(self):
        """ Tessellation component.

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets the tessellation component
        :setter: Sets the tessellation component
        """
        return self._tsl_component

    @tessellator.setter
    def tessellator(self, value):
        if not isinstance(value, AbstractTessellate):
            warnings.warn("Tessellation component must be an instance of Abstract.Tessellate class")
            return

        self._tsl_component = value

    @property
    def bbox(self):
        """ Bounding box.

        Evaluates the bounding box of the surface and returns the minimum and maximum coordinates.

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets the surface bounding box
        """
        if self._bounding_box is None or len(self._bounding_box) == 0:
            self._bounding_box = utilities.evaluate_bounding_box(self.ctrlpts)

        return tuple(self._bounding_box)

    @property
    def trims(self):
        """ Trim curves.

        Trim curves are introduced to the surfaces on the parametric space. It should be an array (or list, tuple, etc.)
        and they are integrated to the existing visualization system.

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets the array of trim curves
        :setter: Sets the array of trim curves
        """
        return self._trims

    @trims.setter
    def trims(self, value):
        self._trims = value

    @property
    def data(self):
        """ Returns a dictionary containing all shape data.

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.
        """
        return dict(
            rational=self.rational,
            dimension=self.dimension,
            degree=self._degree,
            knotvector=self._knot_vector,
            size=self._control_points_size,
            control_points=self._control_points
        )

    def set_ctrlpts(self, ctrlpts, size_u, size_v, **kwargs):
        """ Sets the control points and checks if the data is consistent.

        This method is designed to provide a consistent way to set control points whether they are weighted or not.
        It directly sets the control points member of the class, and therefore it doesn't return any values.
        The input will be an array of coordinates. If you are working in the 3-dimensional space, then your coordinates
        will be an array of 3 elements representing *(x, y, z)* coordinates.

        This method also generates 2D control points in *[u][v]* format which can be accessed via :py:attr:`~ctrlpts2d`.

        You may initialize the 1-dimensional and 2-dimensional arrays via ``array_init`` and ``array_init2d`` keyword
        arguments. Please see :py:meth:`.Curve.set_ctrlpts()` for details.

        .. note::

            The v index varies first. That is, a row of v control points for the first u value is found first.
            Then, the row of v control points for the next u value.

        :param ctrlpts: input control points as a list of coordinates
        :type ctrlpts: list
        :param size_u: number of control points for the u-direction
        :type size_u: int
        :param size_v: number of control points for the v-direction
        :type size_v: int
        """
        # Degrees must be set before setting the control points
        if self.degree_u <= 0 or self.degree_v <= 0:
            raise ValueError("Set the degrees first")

        # Check array size validity
        if size_u < self.degree_u + 1:
            raise ValueError("Number of control points on the u-direction should be at least degree + 1")
        if size_v < self.degree_v + 1:
            raise ValueError("Number of control points on the v-direction should be at least degree + 1")

        # Keyword arguments
        array_init = kwargs.get('array_init', [[] for _ in range(len(ctrlpts))])
        array_init2d = kwargs.get('array_init2d', [[[] for _ in range(size_v)] for _ in range(size_u)])

        # Clean up the surface and control points
        self.reset(evalpts=True, ctrlpts=True)

        # Estimate dimension by checking the size of the first element
        self._dimension = len(ctrlpts[0])

        # Check the dimensions of the input control points array and type cast to float
        ctrlpts_float = array_init
        for idx, cpt in enumerate(ctrlpts):
            if not isinstance(cpt, (list, tuple)):
                raise ValueError("Element number " + str(idx) + " is not a list")
            if len(cpt) is not self._dimension:
                raise ValueError("The input must be " + str(self._dimension) + " dimensional list - " + str(cpt) +
                                 " is not a valid control point")
            ctrlpts_float[idx] = [float(coord) for coord in cpt]

        # Generate a 2-dimensional list of control points
        ctrlpts_float2d = array_init2d
        for i in range(0, size_u):
            for j in range(0, size_v):
                ctrlpts_float2d[i][j] = ctrlpts_float[j + (i * size_v)]

        # Set the new control points
        self._control_points = ctrlpts_float
        self._control_points2D = ctrlpts_float2d

        # Set u and v sizes
        self.ctrlpts_size_u = size_u
        self.ctrlpts_size_v = size_v

    # Runs visualization component to render the surface
    def render(self, **kwargs):
        """ Renders the surface using the visualization component.

        The visualization component must be set using :py:attr:`~vis` property before calling this method.

        Keyword Arguments:
            * ``cpcolor``: sets the color of the control points grid
            * ``evalcolor``: sets the color of the surface
            * ``trimcolor``: sets the color of the trim curves
            * ``filename``: saves the plot with the input name
            * ``plot``: a flag to control displaying the plot window. *Default: True*
            * ``extras``: adds line plots to the figure. *Default: None*
            * ``colormap``: sets the colormap of the surface

        The ``plot`` argument is useful when you would like to work on the command line without any window context.
        If ``plot`` flag is False, this method saves the plot as an image file (.png file where possible) and disables
        plot window popping out. If you don't provide a file name, the name of the image file will be pulled from the
        configuration class.

        ``extras`` argument can be used to add extra line plots to the figure. This argument expects a list of dicts
        in the format described below:

        .. code-block:: python

            [
                dict(  # line plot 1
                    points=[[1, 2, 3], [4, 5, 6]],  # list of points
                    name="My line Plot 1",  # name displayed on the legend
                    color="red",   # color of the line plot
                    size=6.5  # size of the line plot
                ),
                dict(  # line plot 2
                    points=[[7, 8, 9], [10, 11, 12]],  # list of points
                    name="My line Plot 2",  # name displayed on the legend
                    color="navy",   # color of the line plot
                    size=12.5  # size of the line plot
                )
            ]

        Please note that ``colormap`` argument can only work with visualization classes that support colormaps. As an
        example, please see :py:class:`.VisMPL.VisSurfTriangle()` class documentation. This method expects a single
        colormap input.
        """
        if not self._vis_component:
            warnings.warn("No visualization component has been set")
            return

        cpcolor = kwargs.get('cpcolor', 'blue')
        evalcolor = kwargs.get('evalcolor', 'green')
        bboxcolor = kwargs.get('bboxcolor', 'darkorange')
        trimcolor = kwargs.get('trimcolor', 'black')
        filename = kwargs.get('filename', None)
        plot_visible = kwargs.get('plot', True)
        extra_plots = kwargs.get('extras', None)

        # Get colormap and convert to a list
        surf_cmap = kwargs.get('colormap', None)
        surf_cmap = [surf_cmap] if surf_cmap else []

        # Check all parameters are set
        self._check_variables()

        # Check if the surface has been evaluated
        if self._surface_points is None or len(self._surface_points) == 0:
            self.evaluate()

        # Clear the visualization component
        self._vis_component.clear()

        # Add control points
        if self._vis_component.plot_types['ctrlpts'] == 'points':
            self._vis_component.add(ptsarr=self.ctrlpts, name="Control Points", color=cpcolor, plot_type='ctrlpts')

        # Add control points as quads
        if self._vis_component.plot_types['ctrlpts'] == 'quads':
            ctrlpts_quads = utilities.make_quad(self.ctrlpts, self.ctrlpts_size_u, self.ctrlpts_size_v)
            self._vis_component.add(ptsarr=ctrlpts_quads, name="Control Points", color=cpcolor, plot_type='ctrlpts')

        # Add control points as a quad mesh
        if self._vis_component.plot_types['ctrlpts'] == 'quadmesh':
            ctrlpts_quads = utilities.make_quad_mesh(self.ctrlpts, self.ctrlpts_size_u, self.ctrlpts_size_v)
            self._vis_component.add(ptsarr=ctrlpts_quads, name="Control Points", color=cpcolor, plot_type='ctrlpts')

        # Add surface points
        if self._vis_component.plot_types['evalpts'] == 'points':
            self._vis_component.add(ptsarr=self.evalpts, name=self.name, color=evalcolor, plot_type='evalpts')

        # Add surface points as quads
        if self._vis_component.plot_types['evalpts'] == 'quads':
            evalpts_quads = utilities.make_quad(self.evalpts, self.sample_size_u, self.sample_size_v)
            self._vis_component.add(ptsarr=evalpts_quads, name=self.name, color=evalcolor, plot_type='evalpts')

        # Add surface points as vertices and triangles
        if self._vis_component.plot_types['evalpts'] == 'triangles':
            self.tessellate()
            self._vis_component.add(ptsarr=[self.tessellator.vertices, self.tessellator.triangles],
                                    name=self.name, color=evalcolor, plot_type='evalpts')

        # Visualize the trim curve
        for idx, trim in enumerate(self._trims):
            self._vis_component.add(ptsarr=self.evaluate_list(trim.evalpts),
                                    name="Trim Curve " + str(idx + 1), color=trimcolor, plot_type='trimcurve')

        # Bounding box
        self._vis_component.add(ptsarr=self.bbox, name="Bounding Box", color=bboxcolor, plot_type='bbox')

        # User-defined plots
        if extra_plots is not None:
            for ep in extra_plots:
                self._vis_component.add(ptsarr=ep['points'], name=ep['name'],
                                        color=(ep['color'], ep['size']), plot_type='extras')

        # Data requested by the visualization module
        if self._vis_component.plot_types['others']:
            vis_other = self._vis_component.plot_types['others'].split(",")
            for vo in vis_other:
                vo_clean = vo.strip()
                # Send center point of the parametric space to the visualization module
                if vo_clean == "midpt":
                    midprm_u = (max(self.knotvector_u) + min(self.knotvector_u)) / 2.0
                    midprm_v = (max(self.knotvector_v) + min(self.knotvector_v)) / 2.0
                    midpt = self.evaluate_single((midprm_u, midprm_v))
                    self._vis_component.add(ptsarr=[midpt], plot_type=vo_clean)

        # Plot the surface
        self._vis_component.render(fig_save_as=filename, display_plot=plot_visible, colormap=surf_cmap)

    def tessellate(self, **kwargs):
        """ Tessellates the surface.

        Keyword arguments are directly passed to the tessellation component.
        """
        # No need to re-tessellate if we have already tessellated the surface
        if self._tsl_component.vertices is not None and self._tsl_component.triangles is not None:
            return

        # Call tessellation component for vertex and triangle generation
        self._tsl_component.tessellate(self.evalpts, self.sample_size_u, self.sample_size_v, trims=self.trims, **kwargs)

        # Re-evaluate vertex coordinates
        for idx in range(len(self._tsl_component.vertices)):
            self._tsl_component.vertices[idx].data = self.evaluate_single(self._tsl_component.vertices[idx].uv)

    def reset(self, **kwargs):
        """ Resets control points and/or evaluated points.

        Keyword Arguments:
            * ``evalpts``: if True, then resets evaluated points
            * ``ctrlpts`` if True, then resets control points

        """
        reset_ctrlpts = kwargs.get('ctrlpts', False)
        reset_evalpts = kwargs.get('evalpts', False)

        if reset_ctrlpts:
            self._control_points = self._init_array(self._array_type)
            self._control_points2D = self._init_array(self._array_type)
            self._control_points_size[0] = 0
            self._control_points_size[1] = 0
            self._bounding_box = self._init_array(self._array_type)

        if reset_evalpts:
            self._surface_points = self._init_array(self._array_type)

        # Reset vertices and triangles
        self._tsl_component.reset()

    # Checks whether the surface evaluation is possible or not
    def _check_variables(self):
        works = True
        param_list = []
        if self.degree_u == 0:
            works = False
            param_list.append('degree_u')
        if self.degree_v == 0:
            works = False
            param_list.append('degree_v')
        if self._control_points is None or len(self._control_points) == 0:
            works = False
            param_list.append('ctrlpts')
        if self.knotvector_u is None or len(self.knotvector_u) == 0:
            works = False
            param_list.append('knotvector_u')
        if self.knotvector_v is None or len(self.knotvector_v) == 0:
            works = False
            param_list.append('knotvector_v')
        if not works:
            raise ValueError("Please set the following variables before evaluation: " + ",".join(param_list))

    @abc.abstractmethod
    def evaluate(self, **kwargs):
        """ Evaluates the parametric surface.

        .. note::

            This is an abstract method and it must be implemented in the subclass.

        """
        # Check all parameters are set before the evaluation
        self._check_variables()

        # Should implement the evaluation functionality
        pass

    @abc.abstractmethod
    def evaluate_single(self, param):
        """ Evaluates the parametric surface at the given (u, v) parameter.

        .. note::

            This is an abstract method and it must be implemented in the subclass.

        :param param: parameter (u, v)
        """
        # Check all parameters are set before the evaluation
        self._check_variables()

        # Should implement the evaluation functionality
        pass

    @abc.abstractmethod
    def evaluate_list(self, param_list):
        """ Evaluates the parametric surface for an input range of (u, v) parameters.

        .. note::

            This is an abstract method and it must be implemented in the subclass.

        :param param_list: array of parameters (u, v)
        """
        # Check all parameters are set before the evaluation
        self._check_variables()

        # Should implement the evaluation functionality
        pass

    @abc.abstractmethod
    def derivatives(self, u, v, order, **kwargs):
        """ Evaluates the derivatives of the parametric surface at parameter (u, v).

        .. note::

            This is an abstract method and it must be implemented in the subclass.

        :param u: parameter on the u-direction
        :type u: float
        :param v: parameter on the v-direction
        :type v: float
        :param order: derivative order
        :type order: int
        """
        # Check all parameters are set before the evaluation
        self._check_variables()

        # Check u and v parameters are correct
        utilities.check_params(u, v)

        # Should implement the derivatives functionality here
        pass


class Volume(six.with_metaclass(abc.ABCMeta, object)):
    """ Abstract base class (ABC) for parametric volumes.

    The Volume ABC is inherited from abc.ABCMeta class which is included in Python standard library by default. Due to
    differences between Python 2 and 3 on defining a metaclass, the compatibility module ``six`` is employed. Using
    ``six`` to set metaclass allows users to use the abstract classes in a correct way.

    The abstract base classes in this module are implemented using a feature called Python Properties. This feature
    allows users to use some of the functions as if they are class fields. You can also consider properties as a
    pythonic way to set getters and setters. You will see "getter" and "setter" descriptions on the documentation of
    these properties.

    The Volume ABC allows users to set the *FindSpan* function to be used in evaluations with ``find_span_func``
    keyword as an input to the class constructor. NURBS-Python includes a binary and a linear search variation of the
    FindSpan function in the ``helpers`` module.
    You may also implement and use your own *FindSpan* function. Please see the ``helpers`` module for details.

    Code segment below illustrates a possible implementation of Volume abstract base class:

    .. code-block:: python

        from geomdl import abstract

        class MyVolumeClass(abstract.Volume):
            def __init__(self, **kwargs):
            super(MyVolumeClass, self).__init__(**kwargs)
            # Add your constructor code here

            def evaluate(self, **kwargs):
                # Implement this function
                pass

            def evaluate_single(self, uvw):
                # Implement this function
                pass

            def evaluate_list(self, uvw_list):
                # Implement this function
                pass

    The properties and functions defined in the abstract base class will be automatically available in the subclasses.
    """

    def __init__(self, **kwargs):
        self._array_type = list
        self._iter_index = 0  # iterator index
        self._degree = [0, 0, 0]  # degree
        self._knot_vector = [self._init_array(self._array_type),
                             self._init_array(self._array_type),
                             self._init_array(self._array_type)]  # knot vector
        self._control_points_size = [0, 0, 0]  # control points array length
        self._delta = [0.1, 0.1, 0.1]  # evaluation delta
        self._name = "Volume"  # descriptor field
        self._rational = False  # defines whether the surface is rational or not
        self._control_points = self._init_array(self._array_type)  # control points, 1-D array (w-order)
        self._eval_points = self._init_array(self._array_type)  # evaluated points
        self._dimension = 0  # dimension of the volume
        self._vis_component = None  # visualization component
        self._bounding_box = self._init_array(self._array_type)  # bounding box
        self._evaluator = None  # evaluator instance
        self._precision = 18  # number of decimal places to round to
        self._span_func = kwargs.get('find_span_func', helpers.find_span_linear)  # default "find_span" function
        self._kv_normalize = kwargs.get('normalize_kv', True)  # normalize knot vectors
        self._cache = {}  # cache dictionary

    def __iter__(self):
        self._iter_index = 0
        return self

    def next(self):
        return self.__next__()

    def __next__(self):
        if self._iter_index > 0:
            raise StopIteration
        self._iter_index += 1
        return self

    def __len__(self):
        return 1

    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result

    def __deepcopy__(self, memo):
        # Don't copy self reference
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        # Don't copy the cache
        memo[id(self._cache)] = self._cache.__new__(dict)
        # Copy all other attributes
        for k, v in self.__dict__.items():
            setattr(result, k, copy.deepcopy(v, memo))
        return result

    def __str__(self):
        return self.name

    __repr__ = __str__

    def _init_array(self, arr_type, **kwargs):
        """ Initializes the arrays.

        :param arr_type: array type
        """
        if callable(arr_type):
            return arr_type()
        else:
            return None

    @property
    def name(self):
        """ Volume descriptor (as a string or a number).

        Descriptor field allows users to assign an identification to the volume object. The identification can be a
        string or a number.

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets the descriptor
        :setter: Sets the descriptor
        :type: str or int
        """
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def evaluator(self):
        """ Volume evaluator.

        Evaluators allow users to use different algorithms for B-Spline and NURBS evaluations. Please see the
        documentation on ``Evaluator`` classes.

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Prints the name of the evaluator and returns the current Evaluator instance
        :setter: Sets the evaluator
        """
        return self._evaluator

    @evaluator.setter
    def evaluator(self, value):
        if not isinstance(value, AbstractEvaluator):
            raise TypeError("The evaluator must be an instance of Abstract.Evaluator")
        value._span_func = self._span_func
        self._evaluator = value

    @property
    def rational(self):
        """ True if the volume is rational.

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Returns True if the surface is rational (NURBS)
        :type: bool
        """
        return self._rational

    @property
    def dimension(self):
        """ Dimension of the volume.

        Dimension will be automatically estimated from the first element of the control points array.

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets the dimension of the surface
        :type: integer
        """
        if self._rational:
            return self._dimension - 1
        return self._dimension

    @property
    def order_u(self):
        """ Order for the u-direction.

        Defined as ``order = degree + 1``

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets the surface order for u-direction
        :setter: Sets the surface order for u-direction
        :type: integer
        """
        return self.degree_u + 1

    @order_u.setter
    def order_u(self, value):
        self.degree_u = value - 1

    @property
    def order_v(self):
        """ Order for the v-direction.

        Defined as ``order = degree + 1``

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets the surface order for v-direction
        :setter: Sets the surface order for v-direction
        :type: integer
        """
        return self.degree_v + 1

    @order_v.setter
    def order_v(self, value):
        self.degree_v = value - 1

    @property
    def order_w(self):
        """ Order for the w-direction.

        Defined as ``order = degree + 1``

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets the surface order for v-direction
        :setter: Sets the surface order for v-direction
        :type: integer
        """
        return self.degree_w + 1

    @order_w.setter
    def order_w(self, value):
        self.degree_w = value - 1

    @property
    def degree_u(self):
        """ Degree for the u-direction.

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets degree for the u-direction
        :setter: Sets degree for the u-direction
        :type: integer
        """
        return self._degree[0]

    @degree_u.setter
    def degree_u(self, value):
        val = int(value)
        if val <= 0:
            raise ValueError("Degree cannot be less than zero")
        # Clean up the surface points
        self.reset(evalpts=True)
        # Set degree u
        self._degree[0] = int(value)

    @property
    def degree_v(self):
        """ Degree for the v-direction.

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets degree for the v-direction
        :setter: Sets degree for the v-direction
        :type: integer
        """
        return self._degree[1]

    @degree_v.setter
    def degree_v(self, value):
        val = int(value)
        if val <= 0:
            raise ValueError("Degree cannot be less than zero")
        # Clean up the surface points
        self.reset(evalpts=True)
        # Set degree v
        self._degree[1] = val

    @property
    def degree_w(self):
        """ Degree for the w-direction.

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets degree for the w-direction
        :setter: Sets degree for the w-direction
        :type: integer
        """
        return self._degree[2]

    @degree_w.setter
    def degree_w(self, value):
        val = int(value)
        if val <= 0:
            raise ValueError("Degree cannot be less than zero")
        # Clean up the surface points
        self.reset(evalpts=True)
        # Set degree v
        self._degree[2] = val

    @property
    def knotvector_u(self):
        """ Knot vector for the u-direction.

        The knot vector will be normalized to [0, 1] domain if the class is initialized with ``normalize_kv=True``
        argument.

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets knot vector for the u-direction
        :setter: Sets knot vector for the u-direction
        """
        return tuple(self._knot_vector[0])

    @knotvector_u.setter
    def knotvector_u(self, value):
        if self.degree_u == 0 or self.ctrlpts_size_u == 0:
            raise ValueError("Set degree and control points first on the u-direction")

        # Check knot vector validity
        if not utilities.check_knot_vector(self.degree_u, value, self.ctrlpts_size_u):
            raise ValueError("Input is not a valid knot vector on the u-direction")

        # Clean up the surface points
        self.reset(evalpts=True)

        # Set knot vector
        self._knot_vector[0] = utilities.normalize_knot_vector(value, decimals=self._precision) \
            if self._kv_normalize else value

    @property
    def knotvector_v(self):
        """ Knot vector for the v-direction.

        The knot vector will be normalized to [0, 1] domain if the class is initialized with ``normalize_kv=True``
        argument.

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets knot vector for the v-direction
        :setter: Sets knot vector for the v-direction
        """
        return tuple(self._knot_vector[1])

    @knotvector_v.setter
    def knotvector_v(self, value):
        if self.degree_v == 0 or self.ctrlpts_size_v == 0:
            raise ValueError("Set degree and control points first on the v-direction")

        # Check knot vector validity
        if not utilities.check_knot_vector(self.degree_v, value, self.ctrlpts_size_v):
            raise ValueError("Input is not a valid knot vector on the v-direction")

        # Clean up the surface points
        self.reset(evalpts=True)

        # Set knot vector
        self._knot_vector[1] = utilities.normalize_knot_vector(value, decimals=self._precision) \
            if self._kv_normalize else value

    @property
    def knotvector_w(self):
        """ Knot vector for the w-direction.

        The knot vector will be normalized to [0, 1] domain if the class is initialized with ``normalize_kv=True``
        argument.

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets knot vector for the w-direction
        :setter: Sets knot vector for the w-direction
        """
        return tuple(self._knot_vector[2])

    @knotvector_w.setter
    def knotvector_w(self, value):
        if self.degree_w == 0 or self.ctrlpts_size_w == 0:
            raise ValueError("Set degree and control points first for the w-direction")

        # Check knot vector validity
        if not utilities.check_knot_vector(self.degree_w, value, self.ctrlpts_size_w):
            raise ValueError("Input is not a valid knot vector for the w-direction")

        # Clean up the surface points
        self.reset(evalpts=True)

        # Set knot vector
        self._knot_vector[2] = utilities.normalize_knot_vector(value, decimals=self._precision) \
            if self._kv_normalize else value

    @property
    def ctrlpts(self):
        """ Control points.

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets the control points
        :setter: Sets the control points
        """
        return self._control_points

    @ctrlpts.setter
    def ctrlpts(self, value):
        self._control_points = value

    @property
    def ctrlpts_size(self):
        """ Total number of control points.

        :getter: Gets the total number of control points
        :type: int
        """
        res = 1
        for sz in self._control_points_size:
            res *= sz
        return res

    @property
    def ctrlpts_size_u(self):
        """ Number of control points for the u-direction.

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets number of control points for the u-direction
        :setter: Sets number of control points for the u-direction
        """
        return self._control_points_size[0]

    @ctrlpts_size_u.setter
    def ctrlpts_size_u(self, value):
        if not isinstance(value, int):
            raise TypeError("Number of control points for the u-direction must be an integer number")
        if value <= 0:
            raise ValueError("Control points size cannot be less than and equal to zero")

        # Assume that user is doing this right
        self._control_points_size[0] = value

    @property
    def ctrlpts_size_v(self):
        """ Number of control points for the v-direction.

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets number of control points for the v-direction
        :setter: Sets number of control points for the v-direction
        """
        return self._control_points_size[1]

    @ctrlpts_size_v.setter
    def ctrlpts_size_v(self, value):
        if not isinstance(value, int):
            raise TypeError("Number of control points for the v-direction must be an integer number")
        if value <= 0:
            raise ValueError("Control points size cannot be less than and equal to zero")

        # Assume that user is doing this right
        self._control_points_size[1] = value

    @property
    def ctrlpts_size_w(self):
        """ Number of control points for the w-direction.

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets number of control points for the w-direction
        :setter: Sets number of control points for the w-direction
        """
        return self._control_points_size[2]

    @ctrlpts_size_w.setter
    def ctrlpts_size_w(self, value):
        if not isinstance(value, int):
            raise TypeError("Number of control points for the w-direction must be an integer number")
        if value <= 0:
            raise ValueError("Control points size cannot be less than and equal to zero")

        # Assume that user is doing this right
        self._control_points_size[2] = value

    @property
    def evalpts(self):
        """ Evaluated points.

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets the coordinates of the evaluated points
        """
        if self._eval_points is None or len(self._eval_points) == 0:
            self.evaluate()

        return self._eval_points

    @property
    def sample_size_u(self):
        """ Sample size for the u-direction.

        Sample size defines the number of evaluated points to generate. It also sets the ``delta_u`` property.

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets sample size for the u-direction
        :setter: Sets sample size for the u-direction
        :type: int
        """
        return int(1.0 / self.delta_u) + 1

    @sample_size_u.setter
    def sample_size_u(self, value):
        if not isinstance(value, int):
            raise ValueError("Sample size must be an integer value")

        if (self.knotvector_u is None or len(self.knotvector_u) == 0) or self.degree_u == 0:
            warnings.warn("Cannot determine 'delta_u' value. Please set knot vectors and degrees before sample size.")
            return

        # To make it operate like linspace, we have to know the starting and ending points.
        start_u = self.knotvector_u[self.degree_u]
        stop_u = self.knotvector_u[-(self.degree_u + 1)]

        # Set delta values
        self.delta_u = (stop_u - start_u) / float(value - 1)

    @property
    def sample_size_v(self):
        """ Sample size for the v-direction.

        Sample size defines the number of evaluated points to generate. It also sets the ``delta_v`` property.

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets sample size for the v-direction
        :setter: Sets sample size for the v-direction
        :type: int
        """
        return int(1.0 / self.delta_v) + 1

    @sample_size_v.setter
    def sample_size_v(self, value):
        if not isinstance(value, int):
            raise ValueError("Sample size must be an integer value")

        if (self.knotvector_v is None or len(self.knotvector_v) == 0) or self.degree_v == 0:
            warnings.warn("Cannot determine 'delta_v' value. Please set knot vectors and degrees before sample size.")
            return

        # To make it operate like linspace, we have to know the starting and ending points.
        start_v = self.knotvector_v[self.degree_v]
        stop_v = self.knotvector_v[-(self.degree_v + 1)]

        # Set delta values
        self.delta_v = (stop_v - start_v) / float(value - 1)

    @property
    def sample_size_w(self):
        """ Sample size for the w-direction.

        Sample size defines the number of evaluated points to generate. It also sets the ``delta_w`` property.

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets sample size for the w-direction
        :setter: Sets sample size for the w-direction
        :type: int
        """
        return int(1.0 / self.delta_w) + 1

    @sample_size_w.setter
    def sample_size_w(self, value):
        if not isinstance(value, int):
            raise ValueError("Sample size must be an integer value")

        if (self.knotvector_w is None or len(self.knotvector_w) == 0) or self.degree_w == 0:
            warnings.warn("Cannot determine 'delta_w' value. Please set knot vectors and degrees before sample size.")
            return

        # To make it operate like linspace, we have to know the starting and ending points.
        start_w = self.knotvector_w[self.degree_w]
        stop_w = self.knotvector_w[-(self.degree_w + 1)]

        # Set delta values
        self.delta_w = (stop_w - start_w) / float(value - 1)

    @property
    def sample_size(self):
        """ Sample size for both u- and v-directions.

        Sample size defines the number of surface points to generate. It also sets the ``delta`` property.

        The following figure illustrates the working principles of sample size property:

        .. math::

            \\underbrace {\\left[ {{u_{start}}, \\ldots ,{u_{end}}} \\right]}_{{n_{sample}}}

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets sample size as a tuple of values corresponding to u-, v- and w-directions
        :setter: Sets sample size value for both u-, v- and w-directions
        :type: int
        """
        sample_size_u = int(1.0 / self.delta_u) + 1
        sample_size_v = int(1.0 / self.delta_v) + 1
        sample_size_w = int(1.0 / self.delta_w) + 1
        return sample_size_u, sample_size_v, sample_size_w

    @sample_size.setter
    def sample_size(self, value):
        if (self.knotvector_u is None or len(self.knotvector_u) == 0) or self.degree_u == 0 or \
                (self.knotvector_v is None or len(self.knotvector_v) == 0 or self.degree_v == 0) or \
                (self.knotvector_w is None or len(self.knotvector_w) == 0 or self.degree_w == 0):
            warnings.warn("Cannot determine 'delta' value. Please set knot vectors and degrees before sample size.")
            return

        # To make it operate like linspace, we have to know the starting and ending points.
        start_u = self.knotvector_u[self.degree_u]
        stop_u = self.knotvector_u[-(self.degree_u + 1)]
        start_v = self.knotvector_v[self.degree_v]
        stop_v = self.knotvector_v[-(self.degree_v + 1)]
        start_w = self.knotvector_w[self.degree_w]
        stop_w = self.knotvector_w[-(self.degree_w + 1)]

        # Set delta values
        self.delta_u = (stop_u - start_u) / float(value - 1)
        self.delta_v = (stop_v - start_v) / float(value - 1)
        self.delta_w = (stop_w - start_w) / float(value - 1)

    @property
    def delta_u(self):
        """ Evaluation delta for the u-direction.

        Evaluation delta corresponds to the *step size* while ``evaluate()`` function iterates on the knot vector to
        generate surface points. Decreasing step size results in generation of more surface points.
        Therefore; smaller the delta value, smoother the surface.

        Please note that ``delta_u`` and ``sample_size_u`` properties correspond to the same variable with different
        descriptions. Therefore, setting ``delta_u`` will also set ``sample_size_u``.

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets evaluation delta for the u-direction
        :setter: Sets evaluation delta for the u-direction
        :type: float
        """
        return self._delta[0]

    @delta_u.setter
    def delta_u(self, value):
        # Delta value should be between 0 and 1
        if float(value) <= 0 or float(value) >= 1:
            raise ValueError("Evaluation delta (u-direction) must be between 0.0 and 1.0")

        # Clean up evaluated points
        self.reset(evalpts=True)

        # Set new delta value
        self._delta[0] = float(value)

    @property
    def delta_v(self):
        """ Evaluation delta for the v-direction.

        Evaluation delta corresponds to the *step size* while ``evaluate()`` function iterates on the knot vector to
        generate surface points. Decreasing step size results in generation of more surface points.
        Therefore; smaller the delta value, smoother the surface.

        Please note that ``delta_v`` and ``sample_size_v`` properties correspond to the same variable with different
        descriptions. Therefore, setting ``delta_v`` will also set ``sample_size_v``.

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets evaluation delta for the v-direction
        :setter: Sets evaluation delta for the v-direction
        :type: float
        """
        return self._delta[1]

    @delta_v.setter
    def delta_v(self, value):
        # Delta value should be between 0 and 1
        if float(value) <= 0 or float(value) >= 1:
            raise ValueError("Evaluation delta (v-direction) should be between 0.0 and 1.0")

        # Clean up evaluated points
        self.reset(evalpts=True)

        # Set new delta value
        self._delta[1] = float(value)

    @property
    def delta_w(self):
        """ Evaluation delta for the w-direction.

        Evaluation delta corresponds to the *step size* while ``evaluate()`` function iterates on the knot vector to
        generate surface points. Decreasing step size results in generation of more surface points.
        Therefore; smaller the delta value, smoother the surface.

        Please note that ``delta_w`` and ``sample_size_w`` properties correspond to the same variable with different
        descriptions. Therefore, setting ``delta_w`` will also set ``sample_size_w``.

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets evaluation delta for the w-direction
        :setter: Sets evaluation delta for the w-direction
        :type: float
        """
        return self._delta[2]

    @delta_w.setter
    def delta_w(self, value):
        # Delta value should be between 0 and 1
        if float(value) <= 0 or float(value) >= 1:
            raise ValueError("Evaluation delta (w-direction) should be between 0.0 and 1.0")

        # Clean up evaluated points
        self.reset(evalpts=True)

        # Set new delta value
        self._delta[2] = float(value)

    @property
    def delta(self):
        """ Evaluation delta for u-, v- and w-directions.

        Evaluation delta corresponds to the *step size* while ``evaluate()`` function iterates on the knot vector to
        generate surface points. Decreasing step size results in generation of more surface points.
        Therefore; smaller the delta value, smoother the surface.

        Please note that ``delta`` and ``sample_size`` properties correspond to the same variable with different
        descriptions. Therefore, setting ``delta`` will also set ``sample_size``.

        The following figure illustrates the working principles of the delta property:

        .. math::

            \\left[{{u_{0}},{u_{start}} + \\delta ,({u_{start}} + \\delta ) + \\delta , \\ldots ,{u_{end}}} \\right]

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets evaluation delta as a tuple of values corresponding to u-, v- and w-directions
        :setter: Sets evaluation delta for u-, v- and w-directions
        :type: float
        """
        return self.delta_u, self.delta_v, self.delta_w

    @delta.setter
    def delta(self, value):
        if isinstance(value, (int, float)):
            self.delta_u = value
            self.delta_v = value
            self.delta_w = value
        elif isinstance(value, (list, tuple)):
            if len(value) == 3:
                self.delta_u = value[0]
                self.delta_v = value[1]
                self.delta_w = value[2]
            else:
                raise ValueError("Surface requires 3 delta values")
        else:
            raise ValueError("Cannot set delta. Please input a numeric value or a list or tuple with 3 numeric values")

    @property
    def bbox(self):
        """ Bounding box.

        Evaluates the bounding box of the volume and returns the minimum and maximum coordinates.

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets the volume bounding box
        """
        if self._bounding_box is None or len(self._bounding_box) == 0:
            self._bounding_box = utilities.evaluate_bounding_box(self.ctrlpts)

        return tuple(self._bounding_box)

    @property
    def vis(self):
        """ Visualization component.

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets the visualization component
        :setter: Sets the visualization component
        """
        return self._vis_component

    @vis.setter
    def vis(self, value):
        if not isinstance(value, vis.VisAbstract):
            warnings.warn("Visualization component must be an instance of VisAbstract class")
            return

        self._vis_component = value

    @property
    def data(self):
        """ Returns a dictionary containing all shape data.

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.
        """
        return dict(
            rational=self.rational,
            dimension=self.dimension,
            degree=self._degree,
            knotvector=self._knot_vector,
            size=self._control_points_size,
            control_points=self._control_points
        )

    def reset(self, **kwargs):
        """ Resets control points and/or evaluated points.

        Keyword Arguments:
            * ``evalpts``: if True, then resets evaluated points
            * ``ctrlpts`` if True, then resets control points

        """
        reset_ctrlpts = kwargs.get('ctrlpts', False)
        reset_evalpts = kwargs.get('evalpts', False)

        if reset_ctrlpts:
            self._control_points = self._init_array(self._array_type)
            self._control_points_size = [0, 0, 0]
            self._bounding_box = self._init_array(self._array_type)

        if reset_evalpts:
            self._eval_points = self._init_array(self._array_type)

    def _check_variables(self):
        """ Checks whether the evaluation is possible or not. """
        works = True
        param_list = []
        if self.degree_u == 0:
            works = False
            param_list.append('degree_u')
        if self.degree_v == 0:
            works = False
            param_list.append('degree_v')
        if self.degree_w == 0:
            works = False
            param_list.append('degree_w')
        if self._control_points is None or len(self._control_points) == 0:
            works = False
            param_list.append('ctrlpts')
        if self.knotvector_u is None or len(self.knotvector_u) == 0:
            works = False
            param_list.append('knotvector_u')
        if self.knotvector_v is None or len(self.knotvector_v) == 0:
            works = False
            param_list.append('knotvector_v')
        if self.knotvector_w is None or len(self.knotvector_w) == 0:
            works = False
            param_list.append('knotvector_w')
        if not works:
            raise ValueError("Please set the following variables before evaluation: " + ",".join(param_list))

    def set_ctrlpts(self, ctrlpts, size_u, size_v, size_w, **kwargs):
        """ Sets the control points and checks if the data is consistent.

        This method is designed to provide a consistent way to set control points whether they are weighted or not.
        It directly sets the control points member of the class, and therefore it doesn't return any values.
        The input will be an array of coordinates. If you are working in the 3-dimensional space, then your coordinates
        will be an array of 3 elements representing *(x, y, z)* coordinates.

        :param ctrlpts: input control points as a list of coordinates
        :type ctrlpts: list
        :param size_u: number of control points for the u-direction
        :type size_u: int
        :param size_v: number of control points for the v-direction
        :type size_v: int
        :param size_w: number of control points for the w-direction
        :type size_w: int
        """
        # Degrees must be set before setting the control points
        if self.degree_u <= 0 or self.degree_v <= 0 or self.degree_w <= 0:
            raise ValueError("Set the degrees first")

        # Check array size validity
        if size_u < self.degree_u + 1:
            raise ValueError("Number of control points on the u-direction should be at least degree + 1")
        if size_v < self.degree_v + 1:
            raise ValueError("Number of control points on the v-direction should be at least degree + 1")
        if size_w < self.degree_w + 1:
            raise ValueError("Number of control points on the w-direction should be at least degree + 1")

        # Keyword arguments
        array_init = kwargs.get('array_init', [[] for _ in range(len(ctrlpts))])

        # Clean up the surface and control points
        self.reset(evalpts=True, ctrlpts=True)

        # Estimate dimension by checking the size of the first element
        self._dimension = len(ctrlpts[0])

        # Check the dimensions of the input control points array and type cast to float
        ctrlpts_float = array_init
        for idx, cpt in enumerate(ctrlpts):
            if not isinstance(cpt, (list, tuple)):
                raise ValueError("Element number " + str(idx) + " is not a list")
            if len(cpt) is not self._dimension:
                raise ValueError("The input must be " + str(self._dimension) + " dimensional list - " + str(cpt) +
                                 " is not a valid control point")
            ctrlpts_float[idx] = [float(coord) for coord in cpt]

        # Set new control points
        self._control_points = ctrlpts_float

        # Set number of control points
        self.ctrlpts_size_u = size_u
        self.ctrlpts_size_v = size_v
        self.ctrlpts_size_w = size_w

    def render(self, **kwargs):
        """ Renders the volume using the visualization component.

        The visualization component must be set using :py:attr:`~vis` property before calling this method.

        Keyword Arguments:
            * ``cpcolor``: sets the color of the control points
            * ``evalcolor``: sets the color of the volume
            * ``filename``: saves the plot with the input name
            * ``plot``: a flag to control displaying the plot window. *Default: True*
            * ``extras``: adds line plots to the figure. *Default: None*
            * ``grid_size``: grid size for voxelization. *Default: (16, 16, 16)*
            * ``use_mp``: flag to activate multi-threaded voxelization. *Default: False*
            * ``num_procs``: number of concurrent processes for multi-threaded voxelization. *Default: 4*

        The ``plot`` argument is useful when you would like to work on the command line without any window context.
        If ``plot`` flag is False, this method saves the plot as an image file (.png file where possible) and disables
        plot window popping out. If you don't provide a file name, the name of the image file will be pulled from the
        configuration class.

        ``extras`` argument can be used to add extra line plots to the figure. This argument expects a list of dicts
        in the format described below:

        .. code-block:: python

            [
                dict(  # line plot 1
                    points=[[1, 2, 3], [4, 5, 6]],  # list of points
                    name="My line Plot 1",  # name displayed on the legend
                    color="red",   # color of the line plot
                    size=6.5  # size of the line plot
                ),
                dict(  # line plot 2
                    points=[[7, 8, 9], [10, 11, 12]],  # list of points
                    name="My line Plot 2",  # name displayed on the legend
                    color="navy",   # color of the line plot
                    size=12.5  # size of the line plot
                )
            ]
        """
        if not self._vis_component:
            warnings.warn("No visualization component has been set")
            return

        cpcolor = kwargs.get('cpcolor', 'blue')
        evalcolor = kwargs.get('evalcolor', 'green')
        bboxcolor = kwargs.get('bboxcolor', 'darkorange')
        filename = kwargs.get('filename', None)
        plot_visible = kwargs.get('plot', True)
        extra_plots = kwargs.get('extras', None)

        # Check all parameters are set
        self._check_variables()

        # Check if the volume has been evaluated
        if self._eval_points is None or len(self._eval_points) == 0:
            self.evaluate()

        # Clear the visualization component
        self._vis_component.clear()

        # Add control points
        if self._vis_component.plot_types['ctrlpts'] == 'points':
            self._vis_component.add(ptsarr=self.ctrlpts, name="Control Points", color=cpcolor, plot_type='ctrlpts')

        # Add evaluated points
        if self._vis_component.plot_types['evalpts'] == 'points':
            self._vis_component.add(ptsarr=self.evalpts, name=self.name, color=evalcolor, plot_type='evalpts')

        # Add evaluated points as voxels
        if self._vis_component.plot_types['evalpts'] == 'voxels':
            grid, filled = voxelize.voxelize(self, **kwargs)
            polygrid = voxelize.generate_faces(grid)
            self._vis_component.add(ptsarr=[polygrid, filled], name=self.name, color=evalcolor, plot_type='evalpts')

        # Bounding box
        self._vis_component.add(ptsarr=self.bbox, name="Bounding Box", color=bboxcolor, plot_type='bbox')

        # User-defined plots
        if extra_plots is not None:
            for ep in extra_plots:
                self._vis_component.add(ptsarr=ep['points'], name=ep['name'],
                                        color=(ep['color'], ep['size']), plot_type='extras')

        # Data requested by the visualization module
        if self._vis_component.plot_types['others']:
            vis_other = self._vis_component.plot_types['others'].split(",")
            for vo in vis_other:
                vo_clean = vo.strip()
                # Send center point of the parametric space to the visualization module
                if vo_clean == "midpt":
                    midprm_u = (max(self.knotvector_u) + min(self.knotvector_u)) / 2.0
                    midprm_v = (max(self.knotvector_v) + min(self.knotvector_v)) / 2.0
                    midprm_w = (max(self.knotvector_w) + min(self.knotvector_w)) / 2.0
                    midpt = self.evaluate_single((midprm_u, midprm_v, midprm_w))
                    self._vis_component.add(ptsarr=[midpt], plot_type=vo_clean)

        # Plot the volume
        self._vis_component.render(fig_save_as=filename, display_plot=plot_visible)

    @abc.abstractmethod
    def evaluate(self, **kwargs):
        """ Evaluates the parametric volume.

        .. note::

            This is an abstract method and it must be implemented in the subclass.

        """
        # Check all parameters are set before the evaluation
        self._check_variables()

        # Should implement the evaluation functionality
        pass

    @abc.abstractmethod
    def evaluate_single(self, param):
        """ Evaluates the parametric surface at the given (u, v, w) parameter.

        .. note::

            This is an abstract method and it must be implemented in the subclass.

        :param param: parameter pair (u, v, w)
        """
        # Check all parameters are set before the evaluation
        self._check_variables()

        # Should implement the evaluation functionality
        pass

    @abc.abstractmethod
    def evaluate_list(self, param_list):
        """ Evaluates the parametric volume for an input range of (u, v, w) parameter pairs.

        .. note::

            This is an abstract method and it must be implemented in the subclass.

        :param param_list: array of parameter pairs (u, v, w)
        """
        # Check all parameters are set before the evaluation
        self._check_variables()

        # Should implement the evaluation functionality
        pass
