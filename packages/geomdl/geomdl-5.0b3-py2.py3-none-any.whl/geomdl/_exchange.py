"""
.. module:: _exchange
    :platform: Unix, Windows
    :synopsis: Helper functions for exchange module

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

import math
from . import abstract, NURBS, multi, compatibility, utilities


def process_template(file_src):
    """ Process Jinja2 template input

    :param file_src: file contents
    :type file_src: str
    """
    def tmpl_sqrt(x):
        """ Square-root of 'x' """
        return math.sqrt(x)

    def tmpl_cubert(x):
        """ Cube-root of 'x' """
        return x ** (1.0 / 3.0) if x >= 0 else -(-x) ** (1.0 / 3.0)

    def tmpl_pow(x, y):
        """ 'x' to the power 'y' """
        return math.pow(x, y)

    # Check if it is possible to import 'jinja2'
    try:
        import jinja2
    except ImportError:
        print("Please install 'jinja2' package to use templated input: pip install jinja2")
        return

    # Replace jinja2 template tags for compatibility
    fsrc = file_src.replace("{%", "<%").replace("%}", "%>").replace("{{", "<{").replace("}}", "}>")

    # Generate Jinja2 environment
    env = jinja2.Environment(
        loader=jinja2.BaseLoader(),
        trim_blocks=True,
        block_start_string='<%', block_end_string='%>',
        variable_start_string='<{', variable_end_string='}>'
    ).from_string(fsrc)

    # Load custom functions into the Jinja2 environment
    template_funcs = dict(
        knot_vector=utilities.generate_knot_vector,
        sqrt=tmpl_sqrt,
        cubert=tmpl_cubert,
        pow=tmpl_pow,
    )
    for k, v in template_funcs.items():
        env.globals[k] = v

    # Process Jinja2 template functions & variables inside the input file
    return env.render()


def read_file(file_name, **kwargs):
    binary = kwargs.get('binary', False)
    skip_lines = kwargs.get('skip_lines', 0)
    callback = kwargs.get('callback', None)
    try:
        with open(file_name, 'rb' if binary else 'r') as fp:
            for _ in range(skip_lines):
                next(fp)
            content = fp.read() if callback is None else callback(fp)
        return content
    except IOError as e:
        print("An error occurred: {}".format(e.args[-1]))
        raise e
    except Exception:
        raise


def write_file(file_name, content, **kwargs):
    binary = kwargs.get('binary', False)
    callback = kwargs.get('callback', None)
    try:
        with open(file_name, 'wb' if binary else 'w') as fp:
            fp.write(content) if callback is None else callback(fp, content)
        return True
    except IOError as e:
        print("An error occurred: {}".format(e.args[-1]))
        raise e
    except Exception:
        raise


def import_smesh_single(file_name):
    """ Generates a NURBS surface from a surface mesh file.

    :param file_name: smesh file to read
    :type file_name: str
    :return: a NURBS surface
    :rtype: NURBS.Surface
    """
    try:
        with open(file_name, 'r') as fp:
            content = fp.readlines()
            content = [x.strip().split() for x in content]
    except IOError as e:
        print("An error occurred: {}".format(e.args[-1]))
        raise e
    except Exception:
        raise

    # 1st line defines the dimension and it must be 3
    if int(content[0][0]) != 3:
        raise TypeError("Input smesh file" + str(file_name) + " is not a surface")

    # Create a NURBS surface instance and fill with the data read from smesh file
    surf = NURBS.Surface()

    # 2nd line is the degrees
    surf.degree_u = int(content[1][0])
    surf.degree_v = int(content[1][1])

    # 3rd line is the number of weighted control points in u and v directions
    dim_u = int(content[2][0])
    dim_v = int(content[2][1])
    ctrlpts_end = 5 + (dim_u * dim_v)

    # Starting from 6th line, we have the weighted control points
    ctrlpts_smesh = content[5:ctrlpts_end]

    # smesh files have the control points in u-row order format
    ctrlpts = compatibility.flip_ctrlpts_u(ctrlpts_smesh, dim_u, dim_v)

    # smesh files store control points in format (x, y, z, w) -- Rhino format
    ctrlptsw = compatibility.generate_ctrlptsw(ctrlpts)

    # Set control points
    surf.set_ctrlpts(ctrlptsw, dim_u, dim_v)

    # 4th and 5th lines are knot vectors
    surf.knotvector_u = [float(u) for u in content[3]]
    surf.knotvector_v = [float(v) for v in content[4]]

    # Return the surface instance
    return surf


def import_dict_crv(data):
    shape = NURBS.Curve()
    shape.degree = data['degree']
    shape.ctrlpts = data['control_points']['points']
    if 'weights' in data['control_points']:
        shape.weights = data['control_points']['weights']
    shape.knotvector = data['knotvector']
    if 'delta' in data:
        shape.delta = data['delta']
    if 'name' in data:
        shape.name = data['name']
    return shape


def export_dict_crv(obj):
    data = dict(
        degree=obj.degree,
        knotvector=list(obj.knotvector),
        control_points=dict(
            points=obj.ctrlpts
        ),
        delta=obj.delta
    )
    try:
        data['control_points']['weights'] = list(obj.weights)
    except AttributeError:
        # Not a NURBS curve
        pass
    return data


def import_dict_surf(data):
    shape = NURBS.Surface()
    shape.degree_u = data['degree_u']
    shape.degree_v = data['degree_v']
    shape.ctrlpts_size_u = data['size_u']
    shape.ctrlpts_size_v = data['size_v']
    shape.ctrlpts = data['control_points']['points']
    if 'weights' in data['control_points']:
        shape.weights = data['control_points']['weights']
    shape.knotvector_u = data['knotvector_u']
    shape.knotvector_v = data['knotvector_v']
    if 'delta' in data:
        shape.delta = data['delta']
    if 'name' in data:
        shape.name = data['name']
    return shape


def export_dict_surf(obj):
    data = dict(
        degree_u=obj.degree_u,
        degree_v=obj.degree_v,
        knotvector_u=list(obj.knotvector_u),
        knotvector_v=list(obj.knotvector_v),
        size_u=obj.ctrlpts_size_u,
        size_v=obj.ctrlpts_size_v,
        control_points=dict(
            points=obj.ctrlpts
        ),
        delta=obj.delta
    )
    try:
        data['control_points']['weights'] = list(obj.weights)
    except AttributeError:
        # Not a NURBS curve
        pass
    return data


def import_text_data(content, sep, col_sep=";", two_dimensional=False):
    lines = content.strip().split("\n")
    ctrlpts = []
    if two_dimensional:
        # Start reading file
        size_u = 0
        size_v = 0
        for line in lines:
            # Remove whitespace
            line = line.strip()
            # Convert the string containing the coordinates into a list
            control_point_row = line.split(col_sep)
            # Clean and convert the values
            size_v = 0
            for cpr in control_point_row:
                ctrlpts.append([float(c.strip()) for c in cpr.split(sep)])
                size_v += 1
            size_u += 1

        # Return control points, size in u- and v-directions
        return ctrlpts, size_u, size_v
    else:
        # Start reading file
        for line in lines:
            # Remove whitespace
            line = line.strip()
            # Clean and convert the values
            ctrlpts.append([float(c.strip()) for c in line.split(sep)])

        # Return control points
        return ctrlpts


def export_text_data(obj, sep, col_sep=";", two_dimensional=False):
    result = ""
    if two_dimensional:
        for i in range(0, obj.ctrlpts_size_u):
            line = ""
            for j in range(0, obj.ctrlpts_size_v):
                for idx, coord in enumerate(obj.ctrlpts2d[i][j]):
                    if idx:  # check for the first element
                        line += sep
                    line += str(coord)
                if j != obj.ctrlpts_size_v - 1:
                    line += col_sep
                else:
                    line += "\n"
            result += line
    else:
        # B-spline or NURBS?
        try:
            ctrlpts = obj.ctrlptsw
        except AttributeError:
            ctrlpts = obj.ctrlpts
        # Loop through points
        for pt in ctrlpts:
            result += sep.join(str(c) for c in pt) + "\n"

    return result


def import_dict_str(file_src, delta, callback, tmpl):
    mapping = {'curve': import_dict_crv, 'surface': import_dict_surf}

    # Process template
    if tmpl:
        file_src = process_template(file_src)
    # Execute callback function
    imported_data = callback(file_src)

    # Process imported data
    ret_list = []
    for data in imported_data['shape']['data']:
        temp = mapping[imported_data['shape']['type']](data)
        if 0.0 < delta < 1.0:
            temp.delta = delta
        ret_list.append(temp)

    # Return imported data
    return ret_list


def export_dict_str(obj, callback):
    count = 1
    if isinstance(obj, abstract.Curve):
        export_type = "curve"
        data = [export_dict_crv(obj)]
    elif isinstance(obj, abstract.Surface):
        export_type = "surface"
        data = [export_dict_surf(obj)]
    elif isinstance(obj, multi.CurveContainer):
        export_type = "curve"
        data = [export_dict_crv(o) for o in obj]
        count = len(obj)
    elif isinstance(obj, multi.SurfaceContainer):
        export_type = "surface"
        data = [export_dict_surf(o) for o in obj]
        count = len(obj)
    else:
        raise NotADirectoryError("Object type is not defined for dict export")

    # Create the dictionary
    data = dict(
        shape=dict(
            type=export_type,
            count=count,
            data=tuple(data)
        )
    )

    # Execute callback function
    exported_data = callback(data)

    return exported_data
