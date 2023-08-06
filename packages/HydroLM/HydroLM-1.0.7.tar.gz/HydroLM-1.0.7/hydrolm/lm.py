# -*- coding: utf-8 -*-
"""
Functions/Class for regressions.
"""
import numpy as np
import statsmodels.api as sm
import pandas as pd
from itertools import combinations
from scipy import log, exp, mean, stats, special
from statsmodels.tools import eval_measures
from copy import copy as cp
from hydrolm.util import autocorr_est, tsreg

eval_measures_names = ['bias', 'iqr', 'maxabs', 'meanabs', 'medianabs', 'mse', 'rmse', 'stde', 'vare']
neval_measures_names = ['meanabs', 'medianabs', 'mse', 'rmse']
single_plots_names = ['plot_ccpr', 'plot_regress_exog', 'plot_fit']
multi_plots_names = ['plot_ccpr_grid', 'plot_partregress_grid', 'influence_plot']
cols = ['y', 'nrmse', 'mane', 'Adj R2', 'nobs', 'y range', 'f value', 'f p value', 'x sites', 'y intercept', 'x slopes']

class LM(object):
    """
    Class to handle predictive linear models. Only OLS and RLM are supported at the moment.

    Parameters
    ----------
    x : DataFrame
        With header names as the variable names and can be with or without a DateTimeIndex.
    y : DataFrame
        With header names as the variable names and can be with or without a DateTimeIndex.

    Returns
    -------
    LM class
    """

    def __init__(self, x, y):
        """
        Function to load in the data.

        Parameters
        ----------
        x : DataFrame
            With header names as the variable names and can be with or without a DateTimeIndex.
        y : DataFrame
            With header names as the variable names and can be with or without a DateTimeIndex.

        Returns
        -------
        LM class
        """
        if (not isinstance(x, pd.DataFrame)) | (not isinstance(y, pd.DataFrame)):
            raise TypeError('x and y must be DataFrames')
        x_names = x.columns.values
        y_names = y.columns.values

        if isinstance(x.index, pd.DatetimeIndex) & isinstance(y.index, pd.DatetimeIndex):
            self.timeindex = True
        elif len(x) == len(y):
            self.timeindex = False
            xy = pd.concat([x, y], axis=1)
            xy1 = xy.dropna()
            x = xy1[x_names].copy()
            y = xy1[y_names].copy()
        else:
            raise ValueError('The x and y DataFrames must either have a DateTimeIndex or must be the same length.')

        self.x = x
        self.y = y
        self.y_names = y_names
        self.x_names = x_names

    def copy(self):
        return cp(self)

    def __repr__(self):
        if hasattr(self, 'summary_df'):
            return repr(self.summary_df)
        else:
            return repr(pd.concat([self.x, self.y], axis=1))

    def __getitem__(self, key):
        n3 = self.sm[key].summary()
        return n3

    def _summary_df(self):
        sm1 = self.copy()
        res_list = []
        nrmse = sm1.nrmse()
        mane = sm1.mane()
        for y in sm1.sm:
            if sm1.sm[y] is not None:
                nrmse1 = nrmse[y]
                mane1 = mane[y]
                adjr2 = round(sm1.sm[y].rsquared_adj, 3)
                nobs = sm1.sm[y].nobs
                y_range = sm1.sm_xy[y]['y_orig'].max() - sm1.sm_xy[y]['y_orig'].min()
                x_sites = ', '.join(sm1.sm_xy[y]['x_orig'].columns.tolist())
                fvalue = round(sm1.sm[y].fvalue, 3)
                fpvalue = round(sm1.sm[y].f_pvalue, 3)
                params1 = sm1.sm[y].params.round(5).tolist()
                intercept = params1[0]
                x_slopes = ', '.join([str(i) for i in params1[1:]])

                site_res = [y, nrmse1, mane1, adjr2, nobs, y_range, fvalue, fpvalue, x_sites, intercept, x_slopes]
                res_list.append(site_res)
        res_site = pd.DataFrame(res_list, columns=cols).set_index('y')

        return res_site


    def predict(self, model='ols', n_ind=1, x_transform=None, y_transform=None, min_obs=10, autocorr=None):
        """
        Function to perform an OLS on the contained dataset.

        Parameters
        ----------
        model : str
            The type of linear model to run. Options are ols and rlm.
        n_ind : int
            Number of independent variables to choose from.
        x_transform : str or None
            Should the x variables be transformed to be more normal? Options are either None, 'log', or 'boxcox'.
        y_transform : str or None
            Should the y variables be transformed to be more normal? Options are either None, 'log', or 'boxcox'.
        min_obs : int
            Minimum number of combined x and y data to perform the OLS.
        autocorr : float or None
            The autocorrelation value that will be used to sample the data for the regression. This is meant to reduce the dependence in sucessive values. For example, if continuous time series is used as input, then there will be a strong dependent relationship between adjacent values. Setting an autocorr value will sample at a frequency to greatly reduce the interdependence. Recommended values would be 0.05 or 0.1 (depending on data availability).

        Returns
        -------
        LM class with Statsmodels results contained within.
        """
        model1 = self.copy()
        y_names = model1.y_names
        x_names = model1.x_names

        if isinstance(autocorr, float):
            auto_dict = autocorr_est(model1.x, autocorr)
            print(auto_dict)

        best1 = {}
#        best_xy = {}
        best_xy_orig = {}
        predict_dict = {}
        for yi in y_names:
            if model1.timeindex:
                both1 = tsreg(pd.concat([model1.x, model1.y[yi]], axis=1, join='inner'))
            else:
                both1 = pd.concat([model1.x, model1.y[yi]], axis=1)

            if both1.empty | (len(both1) < min_obs):
                print('Dep variable ' + str(yi) + ' has no or not enough data available to run the OLS. Returning None...')
                best1.update({yi: None})
                continue

            combos = set(combinations(x_names, n_ind))

            models = {}
#            models_mae = {}
            fvalues_list = []
            xy_orig_dict = {}
            xy_trans_dict = {}
            boxcox_x_dict = {}
            boxcox_y_dict = {}
            for xi in combos:
                x_set = list(xi)
                full_set = list(x_set)
                full_set.extend([yi])
                if isinstance(autocorr, float):
                    auto1 = int(np.ceil(np.mean([auto_dict[i] for i in xi])))
                    xy_df1 = both1[::(auto1-1)][full_set].dropna()
                else:
                    xy_df1 = both1[full_set].dropna()
                if xy_df1.empty | (len(xy_df1) < min_obs):
                    continue
                x_df = xy_df1[x_set]
                y_df = xy_df1[yi]

                if isinstance(x_transform, str):
                    if x_transform == 'log':
                        x_df_trans = x_df.apply(log)
                    elif x_transform == 'boxcox':
                        x_bc1 = x_df.apply(stats.boxcox)
                        x_df_trans = x_bc1.apply(lambda x: pd.Series(x[0])).T
                        x_df_trans.index = x_df.index
                        x_lambda = x_bc1.apply(lambda x: x[1]).tolist()
                        boxcox_x_dict.update({xi: x_lambda})
                    else:
                        raise ValueError('x_transform must be either log or boxocx')
                else:
                    x_df_trans = x_df.copy()
                if isinstance(y_transform, str):
                    if y_transform == 'log':
                        y_df_trans = y_df.apply(log)
                    elif y_transform == 'boxcox':
                        y_bc1 = stats.boxcox(y_df)
                        y_df_trans = pd.Series(y_bc1[0])
                        y_df_trans.index = y_df.index
                        y_lambda = y_bc1[1]
                        boxcox_y_dict.update({xi: y_lambda})
                    else:
                        raise ValueError('y_transform must be either log or boxocx')
                else:
                    y_df_trans = y_df.copy()

                xy_orig_dict.update({xi: {'x_orig': x_df, 'y_orig': y_df}})
                xy_trans_dict.update({xi: {'x_trans': x_df_trans, 'y_trans': y_df_trans}})

                x_df_trans = sm.add_constant(x_df_trans, has_constant='add')

                if model == 'ols':
                    modelb = sm.OLS(y_df_trans, x_df_trans, missing='drop').fit()
                    fvalue = modelb.fvalue
                elif model == 'rlm':
                    modelb = sm.RLM(y_df_trans, x_df_trans, missing='drop').fit()
                    A = np.identity(len(modelb.params))
                    A = A[1:,:]
                    fvalue = modelb.f_test(A).fvalue[0][0]

                fvalues_list.append([xi, np.round(fvalue, 2)])
                models.update({xi: modelb})

#                mae1 = eval_measures.rmse(model.predict(), y_df)
#                models_mae.update({np.round(mae1, 6): xi})

            if not models:
                print('Not enough data available for regression, returning None.')
                return None

#            best_x = models_mae[np.min(list(models_mae.keys()))]
            fvalue_df = pd.DataFrame(fvalues_list, columns=['x', 'fvalue'])
            fvalue_df.set_index('x', inplace=True)
            best_x = fvalue_df.fvalue.idxmax()
            bestm = models[best_x]
            best1.update({yi: bestm})
#            best_xy.update({yi: xy_dict[yi]})

            predict1 = bestm.predict()
            if isinstance(y_transform, str):
                if y_transform == 'log':
                    predict1 = exp(predict1)
                elif y_transform == 'boxcox':
                    y_lambda = boxcox_y_dict[best_x]
                    predict1 = special.inv_boxcox(predict1, y_lambda)

            xy_orig = xy_orig_dict[best_x].copy()
            xy_trans = xy_trans_dict[best_x].copy()
            xy_both = xy_orig.copy()
            xy_both.update(xy_trans)
            best_xy_orig.update({yi: xy_both})
            predict_dict.update({yi: predict1})

        setattr(model1, 'sm', best1)
        setattr(model1, 'sm_xy', best_xy_orig)
#        setattr(model1, 'sm_xy_base', best_xy_orig)
        setattr(model1, 'sm_predict', predict_dict)

        ### Create stat and plot functions
        for s in eval_measures_names:
            setattr(model1, s, model1._stat_err_gen(s))

        for ns in neval_measures_names:
            setattr(model1, 'n' + ns, model1._nstat_err_gen(ns))

        for sp in single_plots_names:
            setattr(model1, sp, model1._single_plots_gen(sp))

        for mp in multi_plots_names:
            setattr(model1, mp, model1._multi_plots_gen(mp))

        setattr(model1, 'mane', model1._mane_fun)

        ### Create summary df
        if model == 'ols':
            summ_df = model1._summary_df()
            setattr(model1, 'summary_df', summ_df)

        ### Return
        return model1

    def _stat_err_gen(self, fun_name):
        """

        """
        fun = getattr(eval_measures, fun_name)

        def stat_err_fun(y=None, round_dig=5):
            """
            Produces the associated Statsmodels eval_measures.

            Parameters
            ----------
            y: list, str, or None
                The name(s) of the dependent variable(s).
            round_dig: int
                The number of digits to round.

            Returns
            -------
            Dict
                Where the key is the y name associated with the stat.
            """
            if y is None:
                stat1 = {}
                for i in self.y_names:
                    stat1.update({i: fun(self.sm_xy[i]['y_orig'].values, self.sm_predict[i])})
            elif isinstance(y, list):
                stat1 = {}
                for i in y:
                    stat1.update({i: fun(self.sm_xy[i]['y_orig'].values, self.sm_predict[i])})
            elif isinstance(y, str):
                stat1 = {y: fun(self.sm_xy[y]['y_orig'].values, self.sm_predict[y])}

            if isinstance(round_dig, int):
                stat1 = {j: np.round(stat1[j], round_dig) for j in stat1}

            return stat1

        return stat_err_fun

    def _nstat_err_gen(self, fun_name):
        """

        """
        fun = getattr(eval_measures, fun_name)

        def nstat_err_fun(y=None, round_dig=5):
            """
            Produces the associated normalised Statsmodels eval_measures.

            Parameters
            ----------
            y: list, str, or None
                The name(s) of the dependent variable(s).
            round_dig: int
                The number of digits to round.

            Returns
            -------
            Dict
                Where the key is the y name associated with the stat.
            """
            if y is None:
                stat1 = {}
                for i in self.y_names:
                    stat1.update({i: fun(self.sm_xy[i]['y_orig'].values, self.sm_predict[i])/mean(self.sm_xy[i]['y_orig'].values)})
            elif isinstance(y, list):
                stat1 = {}
                for i in y:
                    stat1.update({i: fun(self.sm_xy[i]['y_orig'].values, self.sm_predict[i])/mean(self.sm_xy[i]['y_orig'].values)})
            elif isinstance(y, str):
                stat1 = {y: fun(self.sm_xy[y]['y_orig'].values, self.sm_predict[y])/mean(self.sm_xy[y]['y_orig'].values)}

            if isinstance(round_dig, int):
                stat1 = {j: np.round(stat1[j], round_dig) for j in stat1}

            return stat1

        return nstat_err_fun

    def _single_plots_gen(self, fun_name):
        """

        """
        plot_fun = getattr(sm.graphics, fun_name)

        def single_plot(y, x, **kwargs):
            """

            """
            if isinstance(y, str) & isinstance(x, str):
                plot1 = plot_fun(self.sm[y], x, **kwargs)
            return plot1

        return single_plot

    def _multi_plots_gen(self, fun_name):
        """

        """
        plot_fun = getattr(sm.graphics, fun_name)

        def multi_plot(y, **kwargs):
            """

            """
            if isinstance(y, str):
                plot1 = plot_fun(self.sm[y], **kwargs)
            return plot1

        return multi_plot

    def _mane_fun(self, y=None, round_dig=3):
        """
        Produces the mean absolute normalised error.

        Parameters
        ----------
        y: list, str, or None
            The name(s) of the dependent variable(s).
        round_dig: int
            The number of digits to round.

        Returns
        -------
        Dict
            Where the key is the y name associated with the stat.
        """
        if y is None:
            stat1 = {}
            for i in self.y_names:
                mane1 = mean(np.abs(self.sm_xy[i]['y_orig'].values - self.sm_predict[i])/(self.sm_xy[i]['y_orig'].values))
                stat1.update({i: mane1})
        elif isinstance(y, list):
            stat1 = {}
            for i in y:
                mane1 = mean(np.abs(self.sm_xy[i]['y_orig'].values - self.sm_predict[i])/(self.sm_xy[i]['y_orig'].values))
                stat1.update({i: mane1})
        elif isinstance(y, str):
            mane1 = mean(np.abs(self.sm_xy[y]['y_orig'].values - self.sm_predict[y])/(self.sm_xy[y]['y_orig'].values))
            stat1 = {y: mane1}

        if isinstance(round_dig, int):
            stat1 = {j: np.round(stat1[j], round_dig) for j in stat1}

        return stat1
