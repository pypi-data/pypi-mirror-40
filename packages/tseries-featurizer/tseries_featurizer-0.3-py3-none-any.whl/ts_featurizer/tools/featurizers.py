from base import BaseFeaturizer


class TimeFeaturizer(BaseFeaturizer):

	def __init__(self, config=None, ):
		super(TimeFeaturizer, self).__init__(config, )


class FrequencyFeaturizer(BaseFeaturizer):

	def __init__(self, config=None, ):
		super(FrequencyFeaturizer, self).__init__(config, )

	def _apply_featurization(self, key, exec):
		return super()._apply_featurization(key, exec)


class AutoRegressionFeaturizer(BaseFeaturizer):

	def __init__(self, config=None, ):
		super(AutoRegressionFeaturizer, self).__init__(config, )


class WaveletFeaturizer(BaseFeaturizer):

	def __init__(self, config=None, ):
		super(WaveletFeaturizer, self).__init__(config, )
