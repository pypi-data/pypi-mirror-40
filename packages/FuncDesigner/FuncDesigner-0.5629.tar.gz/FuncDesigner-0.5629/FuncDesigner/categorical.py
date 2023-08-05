#PythonSum = sum
import numpy as np, copy

def categoricalAttribute(oof, attr):
    
    #################
    # ! TODO: vectorize the funcs
    #################
    
    
    from ooFun import oofun
    L = len(oof.domain)
    if not hasattr(oof, 'aux_domain'):
        oof.aux_domain = copy.copy(oof.domain)
        ind_numeric = [j for j, elem in enumerate(oof.aux_domain[0]) if type(elem) not in (str, np.str_)]
        if len(ind_numeric):
            ind_first_numeric = ind_numeric[0]
            oof.aux_domain.sort(key = lambda elem: elem[ind_first_numeric])
        oof.domain = np.arange(len(oof.domain))
    ind = oof.fields.index(attr)
    
    # usually oof.aux_domain is python list or tuple
    dom = np.array([oof.aux_domain[j][ind] for j in range(L)])
    aux_domain_dict = dict((elem, j) for j, elem in enumerate(dom.tolist()))
#    assert 0
#    reversed_aux_domain_dict = dict((j, elem) for j, elem in enumerate(dom))
    
    f = lambda x: dom[np.asarray(x, int) if isinstance(x, np.ndarray) else int(x)]
#    def f(x):
##        print('1:', x.shape)
#        input()
##        print('2:', dom[np.asarray(x, int) if isinstance(x, np.ndarray) else int(x)].shape)
#        return dom[np.asarray(x, int) if isinstance(x, np.ndarray) else int(x)]
    
    
    f_numerical = lambda x: [aux_domain_dict[el] for el in dom[np.asarray(x, int)]] \
    if isinstance(x, np.ndarray) else aux_domain_dict[dom[int(x)]]
#    def f_numerical(x):
#        
#        r = [aux_domain_dict[el] for el in dom[np.asarray(x, int)]] \
#        if isinstance(x, np.ndarray) else aux_domain_dict[dom[int(x)]]
##        print('3:', x.shape)
##        print('4:', r.shape)
#        return r
    
    
    
    
    r = oofun(f, oof, engine = attr, vectorized = False, domain = dom)
    r._is_categorical_field = True
    r.aux_domain_dict = aux_domain_dict
    r._interval_ = lambda domain, dtype: categorical_interval(r, oof, domain, dtype)
    
    # ascending, descending, none
    r._sort_order = \
    'a' if np.all(dom[1:] >= dom[:-1]) \
    else 'd' if np.all(dom[1:] <= dom[:-1]) \
    else 'n'
    
    r.numerical = oofun(f_numerical, oof, vectorized = False, engine = attr+'_sorted_enumerated')
    r.numerical._interval_ = r._interval_
    
    return r

def categorical_interval(r, oof, domain, dtype):
#    print('iter:', domain._p.iter)
#    print(domain, r.domain)
    l_ind, u_ind = np.asarray(domain[oof], int)
#    print('l_ind:', l_ind)
#    print('u_ind:', u_ind)
    s = l_ind.size
    
    cond_numerical = type(r.domain[0]) in (str, np.string_)
    if cond_numerical:
        variable_domain = r.domain
    else:
        variable_domain = np.arange(len(r.domain)) # TODO: rework it, don't create new each time
    
    
    if r._sort_order == 'a':
        vals = np.vstack((variable_domain[l_ind], variable_domain[u_ind]))
    elif r._sort_order == 'd':
        vals = np.vstack((variable_domain[u_ind], variable_domain[l_ind]))
    else:
        vals = np.zeros((2, s), dtype)
        U_ind = u_ind + 1 # not inplace for more safety
        # TODO: mb rework or remove the cycle (improve by vectorization if possible)
        for j in range(s):
            tmp = variable_domain[l_ind[j]:U_ind[j]]
            vals[0, j], vals[1, j] = tmp.min(), tmp.max()
#        print(tmp.max() - tmp.min(), '\n')
    definiteRange = True
#    print('vals:', vals)
    return vals, definiteRange
