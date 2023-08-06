from statsmodels.tsa.arima_model import ARIMA, ARMA
import numpy as np
from tools import get_possible_orders
import pandas as pd
import warnings


def get_orders_aic(order, data):
	"""

	:param order:
	:param data:
	:return:
	"""
	aic = float('inf')
	data.name = str(data.name)
	p, q, c = None, None, None
	try:
		with warnings.catch_warnings():
			warnings.filterwarnings("ignore")
			arima_mod = ARIMA(data, order).fit(disp=0)
			aic = arima_mod.aic
			p, q, c = arima_mod.arparams, arima_mod.maparams, arima_mod.params.const
	except (ValueError, np.linalg.LinAlgError) as e:

		pass

	return aic, (p, q, [c])


def get_best_order(data, max_coeffs):
	"""

	:param data:
	:param max_coeffs:
	:return:
	"""
	best_score, best_cfg = float("inf"), None
	orders = get_possible_orders([max_coeffs, max_coeffs], max_coeffs)
	orders = np.concatenate((np.insert(orders, 1, 1, axis=1), np.insert(orders, 1, 0, axis=1)), )

	for order in orders:
		aic, _ = get_orders_aic(order, data)
		if aic < best_score:
			best_score, best_cfg = aic, order

	if best_score == float("inf"):
		best_cfg = [0, 0, 0]

	return best_cfg


def get_generic_AR(data, max_coeffs, all_data, fit_model=None, test=False):
	"""

	:param data:
	:param max_coeffs:
	:param all_data:
	:param fit_model:
	:param test:
	:return:
	"""
	df_params = pd.DataFrame()
	param_dict = dict()
	data_name = data.name
	if not test:
		fit_model = get_best_order(data, max_coeffs)

	for column in all_data:
		col_data = all_data[column].dropna()
		_, best_params = get_orders_aic(fit_model, col_data)
		if best_params[0] is None:
			# TODO Hau tratatu egin behar da eta ikusi zergatik gertatzen den.
			continue
		param_dict[column] = best_params
		df_params[column] = [item for sublist in best_params for item in sublist]

	std_sum = df_params.T.std().sum()
	params = param_dict[data_name]

	ret = {'best_order': fit_model, 'score': std_sum, 'constant': params[2][0]}
	to_dict = lambda params, title: {f'{title}_{index}': param for index, param in enumerate(params)}
	ar_params = to_dict(params[0], 'ar_params')
	ma_params = to_dict(params[1], 'ma_params')
	ret.update({**ar_params, **ma_params})

	return ret
