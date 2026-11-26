from frostslot.recovery_neighbors.estimator import weighted_percentile


def test_nearest_defrost_quantile_uses_mass_not_average():
    assert weighted_percentile([(15, 0.12), (19, 0.7), (55, 0.18)], 0.67) == 19
    assert weighted_percentile([(15, 0.12), (19, 0.7), (55, 0.18)], 0.95) == 55
