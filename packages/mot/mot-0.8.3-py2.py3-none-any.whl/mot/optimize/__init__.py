from mot.lib.cl_function import SimpleCLFunction
from mot.configuration import CLRuntimeInfo
from mot.lib.kernel_data import Array, Scalar, CompositeArray, Struct, LocalMemory
from mot.lib.utils import all_elements_equal, get_single_value
from mot.library_functions import Powell, Subplex, NMSimplex, LevenbergMarquardt
from mot.optimize.base import OptimizeResults
import numpy as np

__author__ = 'Robbert Harms'
__date__ = '2018-08-01'
__maintainer__ = 'Robbert Harms'
__email__ = 'robbert.harms@maastrichtuniversity.nl'
__licence__ = 'LGPL v3'


def minimize(func, x0, data=None, method=None,
             lower_bounds=None, upper_bounds=None,
             nmr_observations=None, cl_runtime_info=None, options=None,
             jacobian_func=None):
    """Minimization of one or more variables.

    For an easy wrapper of function maximization, see :func:`maximize`.

    Args:
        func (mot.lib.cl_function.CLFunction): A CL function with the signature:

            .. code-block:: c

                double <func_name>(local const mot_float_type* const x,
                                   void* data,
                                   local mot_float_type* objective_list);

            The objective list needs to be filled when the provided pointer is not null. It should contain
            the function values for each observation. This list is used by non-linear least-squares routines,
            and will be squared by the least-square optimizer. This is only used by the ``Levenberg-Marquardt`` routine.

        x0 (ndarray): Initial guess. Array of real elements of size (n, p), for 'n' problems and 'p'
            independent variables.
        data (mot.lib.kernel_data.KernelData): the kernel data we will load. This is returned to the likelihood function
            as the ``void* data`` pointer.
        method (str): Type of solver.  Should be one of:
            - 'Levenberg-Marquardt'
            - 'Nelder-Mead'
            - 'Powell'
            - 'Subplex'

            If not given, defaults to 'Powell'.
        lower_bounds (tuple): per parameter a lower bound, if given, the optimizer ensures ``a <= x`` with
            a the lower bound and x the parameter. If not given, -infinity is assumed for all parameters.
            Each tuple element can either be a scalar or a vector. If a vector is given the first dimension length
            should match that of the parameters.
        upper_bounds (tuple): per parameter an upper bound, if given, the optimizer ensures ``x >= b`` with
            b the upper bound and x the parameter. If not given, +infinity is assumed for all parameters.
            Each tuple element can either be a scalar or a vector. If a vector is given the first dimension length
            should match that of the parameters.
        nmr_observations (int): the number of observations returned by the optimization function.
            This is only needed for the ``Levenberg-Marquardt`` method.
        cl_runtime_info (mot.configuration.CLRuntimeInfo): the CL runtime information
        options (dict): A dictionary of solver options. All methods accept the following generic options:
            - patience (int): Maximum number of iterations to perform.

        jacobian_func (mot.lib.cl_function.CLFunction): a CL function to compute the Jacobian of the objective function.
            This should have the signature:

            .. code-block:: c

                void compute_jacobian(local mot_float_type* model_parameters,
                                      void* data,
                                      local mot_float_type* fvec,
                                      global mot_float_type* const fjac);

            With as input:

            * model_parameters: (nmr_params,) the current point around which we want to know the Jacobian
            * data: the current modeling data, used by the objective function
            * fvec: (nmr_observations,), the function values corresponding to the current model parameters
            * fjac: (nmr_parameters, nmr_observations), the memory location for the Jacobian


            This function is only used by the Levenberg-Marquardt algorithm. If not given, we will use a numerical
            derivative.

    Returns:
        mot.optimize.base.OptimizeResults:
            The optimization result represented as a ``OptimizeResult`` object.
            Important attributes are: ``x`` the solution array.
    """
    if not method:
        method = 'Powell'

    cl_runtime_info = cl_runtime_info or CLRuntimeInfo()

    if len(x0.shape) < 2:
        x0 = x0[..., None]

    lower_bounds = _bounds_to_array(lower_bounds or np.ones(x0.shape[1]) * -np.inf)
    upper_bounds = _bounds_to_array(upper_bounds or np.ones(x0.shape[1]) * np.inf)

    if method == 'Powell':
        return _minimize_powell(func, x0, cl_runtime_info, lower_bounds, upper_bounds, data=data, options=options)
    elif method == 'Nelder-Mead':
        return _minimize_nmsimplex(func, x0, cl_runtime_info, lower_bounds, upper_bounds, data=data, options=options)
    elif method == 'Levenberg-Marquardt':
        return _minimize_levenberg_marquardt(func, x0, nmr_observations, cl_runtime_info, lower_bounds, upper_bounds,
                                             data=data, options=options, jacobian_func=jacobian_func)
    elif method == 'Subplex':
        return _minimize_subplex(func, x0, cl_runtime_info, lower_bounds, upper_bounds, data=data, options=options)
    raise ValueError('Could not find the specified method "{}".'.format(method))


def _bounds_to_array(bounds):
    """Create a CompositeArray to hold the bounds."""
    elements = []
    for value in bounds:
        if all_elements_equal(value):
            elements.append(Scalar(get_single_value(value), ctype='mot_float_type'))
        else:
            elements.append(Array(value, ctype='mot_float_type', as_scalar=True))
    return CompositeArray(elements, 'mot_float_type', address_space='local')


def maximize(func, x0, nmr_observations, **kwargs):
    """Maximization of a function.

    This wraps the objective function to take the negative of the computed values and passes it then on to one
    of the minimization routines.

    Args:
        func (mot.lib.cl_function.CLFunction): A CL function with the signature:

            .. code-block:: c

                double <func_name>(local const mot_float_type* const x,
                                   void* data,
                                   local mot_float_type* objective_list);

            The objective list needs to be filled when the provided pointer is not null. It should contain
            the function values for each observation. This list is used by non-linear least-squares routines,
            and will be squared by the least-square optimizer. This is only used by the ``Levenberg-Marquardt`` routine.

        x0 (ndarray): Initial guess. Array of real elements of size (n, p), for 'n' problems and 'p'
            independent variables.
        nmr_observations (int): the number of observations returned by the optimization function.
        **kwargs: see :func:`minimize`.
    """
    wrapped_func = SimpleCLFunction.from_string('''
        double _negate_''' + func.get_cl_function_name() + '''(
                local mot_float_type* x,
                void* data, 
                local mot_float_type* objective_list){

            double return_val = ''' + func.get_cl_function_name() + '''(x, data, objective_list);    

            if(objective_list){
                const uint nmr_observations = ''' + str(nmr_observations) + ''';
                uint local_id = get_local_id(0);
                uint workgroup_size = get_local_size(0);

                uint observation_ind;
                for(uint i = 0; i < (nmr_observations + workgroup_size - 1) / workgroup_size; i++){
                    observation_ind = i * workgroup_size + local_id;

                    if(observation_ind < nmr_observations){
                        objective_list[observation_ind] *= -1;    
                    }
                }
            }
            return -return_val;
        }
    ''', dependencies=[func])
    kwargs['nmr_observations'] = nmr_observations
    return minimize(wrapped_func, x0, **kwargs)


def get_minimizer_options(method):
    """Return a dictionary with the default options for the given minimization method.

    Args:
        method (str): the name of the method we want the options off

    Returns:
        dict: a dictionary with the default options
    """
    if method == 'Powell':
        return {'patience': 2,
                'patience_line_search': None,
                'reset_method': 'EXTRAPOLATED_POINT'}

    elif method == 'Nelder-Mead':
        return {'patience': 200,
                'alpha': 1.0, 'beta': 0.5, 'gamma': 2.0, 'delta': 0.5, 'scale': 0.1,
                'adaptive_scales': True}

    elif method == 'Levenberg-Marquardt':
        return {'patience': 250, 'step_bound': 100.0, 'scale_diag': 1, 'usertol_mult': 30}

    elif method == 'Subplex':
        return {'patience': 10,
                'patience_nmsimplex': 100,
                'alpha': 1.0, 'beta': 0.5, 'gamma': 2.0, 'delta': 0.5, 'scale': 1.0, 'psi': 0.0001, 'omega': 0.01,
                'adaptive_scales': True,
                'min_subspace_length': 'auto',
                'max_subspace_length': 'auto'}

    raise ValueError('Could not find the specified method "{}".'.format(method))


def _clean_options(method, provided_options):
    """Clean the given input options.

    This will make sure that all options are present, either with their default values or with the given values,
    and that no other options are present then those supported.

    Args:
        method (str): the method name
        provided_options (dict): the given options

    Returns:
        dict: the resulting options dictionary
    """
    provided_options = provided_options or {}
    default_options = get_minimizer_options(method)

    result = {}

    for name, default in default_options.items():
        if name in provided_options:
            result[name] = provided_options[name]
        else:
            result[name] = default_options[name]
    return result


def _minimize_powell(func, x0, cl_runtime_info, lower_bounds, upper_bounds, data=None, options=None):
    """
    Options:
        patience (int): Used to set the maximum number of iterations to patience*(number_of_parameters+1)
        reset_method (str): one of 'EXTRAPOLATED_POINT' or 'RESET_TO_IDENTITY' lower case or upper case.
        patience_line_search (int): the patience of the searching algorithm. Defaults to the
            same patience as for the Powell algorithm itself.
    """
    options = _clean_options('Powell', options)

    nmr_problems = x0.shape[0]
    nmr_parameters = x0.shape[1]

    eval_func = SimpleCLFunction.from_string('''
        double evaluate(local mot_float_type* x, void* data){
            local mot_float_type* lower_bounds = ((_powell_eval_func_data*)data)->lower_bounds;
            local mot_float_type* upper_bounds = ((_powell_eval_func_data*)data)->upper_bounds;
            local int* out_of_bounds = ((_powell_eval_func_data*)data)->out_of_bounds;
            
            if(get_local_id(0) == 0){
                *out_of_bounds = 0;
                
                for(int i = 0; i < ''' + str(nmr_parameters) + '''; i++){
                    if(x[i] <= lower_bounds[i] || x[i] >= upper_bounds[i]){
                        *out_of_bounds = 1;
                        break;
                    }
                }
            }
            barrier(CLK_LOCAL_MEM_FENCE);
            if(*out_of_bounds){
                return INFINITY;
            }
        
            return ''' + func.get_cl_function_name() + '''(x, ((_powell_eval_func_data*)data)->data, 0);
        }
    ''', dependencies=[func])

    optimizer_func = Powell(eval_func, nmr_parameters, **options)

    kernel_data = {'model_parameters': Array(x0, ctype='mot_float_type', mode='rw'),
                   'data': Struct({'data': data,
                                   'lower_bounds': lower_bounds,
                                   'upper_bounds': upper_bounds,
                                   'out_of_bounds': LocalMemory('int', 1)}, '_powell_eval_func_data')}
    kernel_data.update(optimizer_func.get_kernel_data())

    return_code = optimizer_func.evaluate(
        kernel_data, nmr_problems,
        use_local_reduction=all(env.is_gpu for env in cl_runtime_info.cl_environments),
        cl_runtime_info=cl_runtime_info)

    return OptimizeResults({'x': kernel_data['model_parameters'].get_data(),
                            'status': return_code})


def _minimize_nmsimplex(func, x0, cl_runtime_info, lower_bounds, upper_bounds, data=None, options=None):
    """Use the Nelder-Mead simplex method to calculate the optimimum.

    The scales should satisfy the following constraints:

        .. code-block:: python

            alpha > 0
            0 < beta < 1
            gamma > 1
            gamma > alpha
            0 < delta < 1

    Options:
        patience (int): Used to set the maximum number of iterations to patience*(number_of_parameters+1)
        scale (double): the scale of the initial simplex, default 1.0
        alpha (double): reflection coefficient, default 1.0
        beta (double): contraction coefficient, default 0.5
        gamma (double); expansion coefficient, default 2.0
        delta (double); shrinkage coefficient, default 0.5
        adaptive_scales (boolean): if set to True we use adaptive scales instead of the default scale values.
            This sets the scales to:

            .. code-block:: python

                n = <# parameters>

                alpha = 1
                beta  = 0.75 - 1.0 / (2 * n)
                gamma = 1 + 2.0 / n
                delta = 1 - 1.0 / n

            Following the paper [1]

    References:
        [1] Gao F, Han L. Implementing the Nelder-Mead simplex algorithm with adaptive parameters.
              Comput Optim Appl. 2012;51(1):259-277. doi:10.1007/s10589-010-9329-3.
    """
    options = _clean_options('Nelder-Mead', options)

    nmr_problems = x0.shape[0]
    nmr_parameters = x0.shape[1]

    eval_func = SimpleCLFunction.from_string('''
        double evaluate(local mot_float_type* x, void* data){
            local mot_float_type* lower_bounds = ((_nmsimplex_eval_func_data*)data)->lower_bounds;
            local mot_float_type* upper_bounds = ((_nmsimplex_eval_func_data*)data)->upper_bounds;
            
            if(get_local_id(0) == 0){
                for(int i = 0; i < ''' + str(nmr_parameters) + '''; i++){
                    x[i] = clamp(x[i], lower_bounds[i], upper_bounds[i]);
                }
            }
            barrier(CLK_LOCAL_MEM_FENCE);
            
            return ''' + func.get_cl_function_name() + '''(x, ((_nmsimplex_eval_func_data*)data)->data, 0);
        }
    ''', dependencies=[func])

    optimizer_func = NMSimplex('evaluate', nmr_parameters, dependencies=[eval_func], **options)

    kernel_data = {'model_parameters': Array(x0, ctype='mot_float_type', mode='rw'),
                   'data': Struct({'data': data,
                                   'lower_bounds': lower_bounds,
                                   'upper_bounds': upper_bounds}, '_nmsimplex_eval_func_data')}
    kernel_data.update(optimizer_func.get_kernel_data())

    return_code = optimizer_func.evaluate(
        kernel_data, nmr_problems,
        use_local_reduction=all(env.is_gpu for env in cl_runtime_info.cl_environments),
        cl_runtime_info=cl_runtime_info)

    return OptimizeResults({'x': kernel_data['model_parameters'].get_data(),
                            'status': return_code})


def _minimize_subplex(func, x0, cl_runtime_info, lower_bounds, upper_bounds, data=None, options=None):
    """Variation on the Nelder-Mead Simplex method by Thomas H. Rowan.

    This method uses NMSimplex to search subspace regions for the minimum. See Rowan's thesis titled
    "Functional Stability analysis of numerical algorithms" for more details.

     The scales should satisfy the following constraints:

        .. code-block:: python

            alpha > 0
            0 < beta < 1
            gamma > 1
            gamma > alpha
            0 < delta < 1

    Options:
        patience (int): Used to set the maximum number of iterations to patience*(number_of_parameters+1)
        patience_nmsimplex (int): The maximum patience for each subspace search.
            For each subspace search we set the number of iterations to patience*(number_of_parameters_subspace+1)
        scale (double): the scale of the initial simplex, default 1.0
        alpha (double): reflection coefficient, default 1.0
        beta (double): contraction coefficient, default 0.5
        gamma (double); expansion coefficient, default 2.0
        delta (double); shrinkage coefficient, default 0.5
        psi (double): subplex specific, simplex reduction coefficient, default 0.001.
        omega (double): subplex specific, scaling reduction coefficient, default 0.01
        min_subspace_length (int): the minimum subspace length, defaults to min(2, n).
            This should hold: (1 <= min_s_d <= max_s_d <= n and min_s_d*ceil(n/nsmax_s_dmax) <= n)
        max_subspace_length (int): the maximum subspace length, defaults to min(5, n).
            This should hold: (1 <= min_s_d <= max_s_d <= n and min_s_d*ceil(n/max_s_d) <= n)

        adaptive_scales (boolean): if set to True we use adaptive scales instead of the default scale values.
            This sets the scales to:

            .. code-block:: python

                n = <# parameters>

                alpha = 1
                beta  = 0.75 - 1.0 / (2 * n)
                gamma = 1 + 2.0 / n
                delta = 1 - 1.0 / n

    References:
        [1] Gao F, Han L. Implementing the Nelder-Mead simplex algorithm with adaptive parameters.
              Comput Optim Appl. 2012;51(1):259-277. doi:10.1007/s10589-010-9329-3.
    """
    options = _clean_options('Subplex', options)

    nmr_problems = x0.shape[0]
    nmr_parameters = x0.shape[1]

    eval_func = SimpleCLFunction.from_string('''
        double evaluate(local mot_float_type* x, void* data){
            local mot_float_type* lower_bounds = ((_subplex_eval_func_data*)data)->lower_bounds;
            local mot_float_type* upper_bounds = ((_subplex_eval_func_data*)data)->upper_bounds;
            
            if(get_local_id(0) == 0){
                for(int i = 0; i < ''' + str(nmr_parameters) + '''; i++){
                    x[i] = clamp(x[i], lower_bounds[i], upper_bounds[i]);
                }
            }
            barrier(CLK_LOCAL_MEM_FENCE);
            return ''' + func.get_cl_function_name() + '''(x, ((_subplex_eval_func_data*)data)->data, 0);
        }
    ''', dependencies=[func])

    optimizer_func = Subplex(eval_func, nmr_parameters, **options)

    kernel_data = {'model_parameters': Array(x0, ctype='mot_float_type', mode='rw'),
                   'data': Struct({'data': data,
                                   'lower_bounds': lower_bounds,
                                   'upper_bounds': upper_bounds}, '_subplex_eval_func_data')}
    kernel_data.update(optimizer_func.get_kernel_data())

    return_code = optimizer_func.evaluate(
        kernel_data, nmr_problems,
        use_local_reduction=all(env.is_gpu for env in cl_runtime_info.cl_environments),
        cl_runtime_info=cl_runtime_info)

    return OptimizeResults({'x': kernel_data['model_parameters'].get_data(),
                            'status': return_code})


def _minimize_levenberg_marquardt(func, x0, nmr_observations, cl_runtime_info,
                                  lower_bounds, upper_bounds,
                                  data=None, options=None, jacobian_func=None):
    options = _clean_options('Levenberg-Marquardt', options)

    nmr_problems = x0.shape[0]
    nmr_parameters = x0.shape[1]

    if nmr_observations < x0.shape[1]:
        raise ValueError('The number of instances per problem must be greater than the number of parameters')

    eval_func = SimpleCLFunction.from_string('''
        void evaluate(local mot_float_type* x, void* data, local mot_float_type* result){
            local mot_float_type* lower_bounds = ((_lm_eval_func_data*)data)->lower_bounds;
            local mot_float_type* upper_bounds = ((_lm_eval_func_data*)data)->upper_bounds;
            local int* out_of_bounds = ((_lm_eval_func_data*)data)->out_of_bounds;
            
            if(get_local_id(0) == 0){
                *out_of_bounds = 0;
                
                for(int i = 0; i < ''' + str(nmr_parameters) + '''; i++){
                    if(x[i] <= lower_bounds[i] || x[i] >= upper_bounds[i]){
                        for(int j = 0; j < ''' + str(nmr_observations) + '''; j++){
                            result[j] = INFINITY;    
                        }
                        *out_of_bounds = 1;
                        break;
                    }
                }
            }
            barrier(CLK_LOCAL_MEM_FENCE);
            if(*out_of_bounds){
                return;
            }
            
            ''' + func.get_cl_function_name() + '''(x, ((_lm_eval_func_data*)data)->data, result);
        }
    ''', dependencies=[func])

    if not jacobian_func:
        jacobian_eval_func = SimpleCLFunction.from_string('''
            void _jacobian_evaluate(local mot_float_type* x, void* data, local mot_float_type* result){
                ''' + func.get_cl_function_name() + '''(x, ((_lm_eval_func_data*)data)->data, result);
            }
        ''', dependencies=[func])
        jacobian_func = get_numerical_jacobian_func(jacobian_eval_func, nmr_parameters, nmr_observations)

    optimizer_func = LevenbergMarquardt(eval_func, nmr_parameters, nmr_observations, jacobian_func, **options)

    kernel_data = {'model_parameters': Array(x0, ctype='mot_float_type', mode='rw'),
                   'data': Struct({'data': data,
                                   'lower_bounds': lower_bounds,
                                   'upper_bounds': upper_bounds,
                                   'out_of_bounds': LocalMemory('int', 1)}, '_lm_eval_func_data')}
    kernel_data.update(optimizer_func.get_kernel_data())

    return_code = optimizer_func.evaluate(
        kernel_data, nmr_problems,
        use_local_reduction=all(env.is_gpu for env in cl_runtime_info.cl_environments),
        cl_runtime_info=cl_runtime_info)

    return OptimizeResults({'x': kernel_data['model_parameters'].get_data(),
                            'status': return_code})


def get_numerical_jacobian_func(eval_func, nmr_params, nmr_observations):
    """Get a numerical Jacobian function.

    This computes the Jacobian of the observations (function vector) with respect to the parameters.

    Args:
        eval_func (mot.lib.cl_function.CLFunction): the evaluation function
        nmr_params (int): the number of parameters
        nmr_observations (int): the number of observations (the length of the function vector).

    Returns:
        mot.lib.cl_function.CLFunction: CL function for numerically estimating the Jacobian.
    """
    return SimpleCLFunction.from_string(r'''
        void numerical_jacobian(local mot_float_type* model_parameters,
                                void* data,
                                local mot_float_type* fvec,
                                local mot_float_type* const fjac){
            /**
             * Compute the Jacobian for use in the LM method.
             *
             * This should place the output in the ``fjac`` matrix.
             *
             * Parameters:
             *
             *   model_parameters: (nmr_params,) the current point around which we want to know the Jacobian
             *   data: the current modeling data, used by the objective function
             *   fvec: (nmr_observations,), the function values corresponding to the current model parameters
             *   fjac: (nmr_parameters, nmr_observations), the memory location for the Jacobian
             */
            int i, j;
            uint observation_ind;
            mot_float_type temp, step;
            
            const uint nmr_observations = %(NMR_OBSERVATIONS)s;
            const mot_float_type EPS = 30 * MOT_EPSILON;
            
            uint local_id = get_local_id(0);
            uint workgroup_size = get_local_size(0);
            
            for (j = 0; j < %(NMR_PARAMS)s; j++) {
                step = max(EPS*EPS, EPS * fabs(model_parameters[j]));
                barrier(CLK_LOCAL_MEM_FENCE);
                
                if(get_local_id(0) == 0){
                    temp = model_parameters[j];
                    model_parameters[j] += step; /* replace temporarily */
                }
                barrier(CLK_LOCAL_MEM_FENCE);

                %(FUNCTION_NAME)s(model_parameters, data, fjac + j*nmr_observations);
            
                for(i = 0; i < (nmr_observations + workgroup_size - 1) / workgroup_size; i++){
                    observation_ind = i * workgroup_size + local_id;
                    if(observation_ind < nmr_observations){
                        fjac[j*nmr_observations + observation_ind] = (
                            fjac[j*nmr_observations + observation_ind] - fvec[observation_ind]) / step;
                    }
                }
                
                if(get_local_id(0) == 0){
                    model_parameters[j] = temp; /* restore */
                }
                barrier(CLK_LOCAL_MEM_FENCE);
            }
        }
    ''' % dict(FUNCTION_NAME=eval_func.get_cl_function_name(),
               NMR_PARAMS=nmr_params, NMR_OBSERVATIONS=nmr_observations), dependencies=[eval_func])
