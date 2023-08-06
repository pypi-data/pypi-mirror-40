from abc import ABCMeta
from collections import defaultdict
from typing import List, Callable, Tuple

import numpy as np

from lfa_toolbox.core.mf.free_shape_mf import FreeShapeMF
from lfa_toolbox.core.rules.default_fuzzy_rule import DefaultFuzzyRule
from lfa_toolbox.core.rules.fuzzy_rule import FuzzyRule

COA_func = (lambda v, m: np.sum(np.multiply(v, m)) / np.sum(m), "COA_func")
OR_max = (np.max, "OR_max")
AND_min = (np.min, "AND_min")
MIN = (np.min, "MIN")

ERR_MSG_MUST_PREDICT = "you must use predict() at least once"


def must_use_predict_before(func):
    def wrapper(*args):
        that = args[0]
        if that._last_crisp_values is None:
            raise ValueError(ERR_MSG_MUST_PREDICT)
        to_return = func(that)
        return to_return

    return wrapper


class RuleActivationRange:
    """
    A rule activation is valid between the range MIN and MAX
    """

    MIN = 0.0
    MAX = 1.0


class FIS(metaclass=ABCMeta):
    def __init__(
        self,
        aggr_func: Callable,
        defuzz_func: Tuple[Callable, str],
        rules: List[FuzzyRule],
        default_rule: DefaultFuzzyRule = None,
    ):
        """
        Create a Mamdani Fuzzy Inference System where aggregation function,
        defuzzification function, rules and default rule are defined by the
        caller (you). All rules have the same weight.

        :param aggr_func: aggregation function. Can be any function that takes
        lists of floats and returns a float. Most of the time, numpy.max
        is the function you want to use.

        :param defuzz_func: defuzzification function. Can be any
        Tuple[Callable, str] object. Callable is the defuzzification function
        and str is a user-defined label. The signature of the defuzzification
        function must be like f(v, m) where v are the rules activation and m
        are consequent values. For example, the rule r0 is fully activated so
        v[0] = 1.0 and r1 is only half activated so v[1] = 0.5. The consequent
        for the first rule was "then out is HIGH(100)" and for the second rule
        it was "then out is LOW(0)". Let's say that f() implements the COA
        defuzzification method then the output is "(1.0*100 + 0.5*0)/(1.0+0.5)".
        Pre-defined defuzzification functions are already implemented in
        this class such as COA_func.

        :param rules: List of FuzzyRule. It supports rules with multiples
        consequents as long as all rules use each defined consequent. For
        example it is invalid to have the first rule with 1 consequent and the
        other with 2. The caller (you) must take care of this by theirself.

        :param default_rule: if desired, a default rule can be set
        """
        self._aggr_func = aggr_func
        self._defuzz_func = defuzz_func
        self._rules = rules
        self._default_rule = default_rule

        # used by FISViewer, useless for the computation itself
        self._last_crisp_values = None
        self._implicated_consequents = None
        self._aggregated_consequents = None
        self._defuzzified_outputs = None

    @property
    def rules(self):
        return self._rules

    @property
    def default_rule(self):
        return self._default_rule

    @property
    @must_use_predict_before
    def last_crisp_values(self):
        return self._last_crisp_values

    @property
    @must_use_predict_before
    def last_implicated_consequents(self):
        return self._implicated_consequents

    @property
    @must_use_predict_before
    def last_aggregated_consequents(self):
        return self._aggregated_consequents

    @property
    @must_use_predict_before
    def last_defuzzified_outputs(self):
        return self._defuzzified_outputs

    def describe(self):
        [print(r) for r in self.rules]
        if self.default_rule is not None:
            print(self.default_rule)

    def predict(self, crisp_values):
        self._last_crisp_values = crisp_values
        """

        :param crisp_values: a dict where keys are variables name and values are
        variables values. Example: {"temperature": 19, "sunshine": 60}
        :return:
        """

        rules_implicated_cons = defaultdict(list)

        # initial value can be set to 0 because activation values are in [0, 1]
        max_ant_act = RuleActivationRange.MIN

        # Fuzzify and activate inputs then implicate consequents for each rule
        for r in self._rules:
            fuzzified_inputs = r.fuzzify(crisp_values)
            antecedents_activation = r.activate(fuzzified_inputs)
            max_ant_act = max(max_ant_act, antecedents_activation)
            implicated_consequents = r.implicate(antecedents_activation)

            for lv_name, lv_impl_mf in implicated_consequents.items():
                rules_implicated_cons[lv_name].extend(lv_impl_mf)

        self._handle_default_rule(max_ant_act, rules_implicated_cons)

        # Aggregate consequents
        self._aggregated_consequents = self._aggregate(rules_implicated_cons)

        # save implicated consequents to use it in the visualizations
        self._implicated_consequents = rules_implicated_cons

        # Defuzzify
        return self._defuzzify()

    def _handle_default_rule(self, max_ant_act, rules_implicated_cons):
        if self._default_rule is None:
            return

        act_value = RuleActivationRange.MAX - max_ant_act
        implicated_consequents = self._default_rule.implicate(act_value)
        for lv_name, lv_impl_mf in implicated_consequents.items():
            rules_implicated_cons[lv_name].extend(lv_impl_mf)

    def _aggregate(self, rules_implicated_cons):
        """
        Aggregate each consequent (grouped by output variables)
        :param rules_implicated_cons: implicated (i.e. after rule activation)
        consequents of this system's rules.

        :return: a dict where keys are output variables name and where values
        are aggregated fuzzy sets.
        """
        aggregated_consequents = {}
        for out_v_name, out_v_mf in rules_implicated_cons.items():
            aggregated_consequents[out_v_name] = self._aggregate_cons(*out_v_mf)
        return aggregated_consequents

    def _aggregate_cons(self, *out_var_mf):
        """
        Aggregate a given consequent (represented by one or more membership
        functions) together.

        :param out_var_mf: a list of membership functions for a given output
        variable.

        :return: the aggregated fuzzy set, represented by a FreeShapeMF since
        the result can be a MF of any shape.
        """
        all_in_values = np.concatenate([mf.in_values for mf in out_var_mf])
        min_in, max_in = np.min(all_in_values), np.max(all_in_values)

        aggregated_mf_values = []

        aggregated_in_values = np.linspace(min_in, max_in, 50)
        for x in aggregated_in_values:
            fuzzified_x = [mf.fuzzify(x) for mf in out_var_mf]
            mf = self._aggr_func(fuzzified_x)
            aggregated_mf_values.append(mf)

        return FreeShapeMF(
            in_values=aggregated_in_values, mf_values=aggregated_mf_values
        )

    def _defuzzify(self):
        """
        Defuzzify the output variable(s) into crisp values. Must be run after
        aggregation.

        :return: a dict of crisp values where keys are variables names and
        values are discrete/crisp output values
        """
        defuzzified_outputs = {}
        for out_v_name, out_v_mf in self._aggregated_consequents.items():
            defuzzified_outputs[out_v_name] = self._defuzzify_cons(out_v_mf)
        self._defuzzified_outputs = defuzzified_outputs
        return defuzzified_outputs

    def _defuzzify_cons(self, aggr_mf):
        """
        Defuzzify an aggregated membership function using the user-defined
        aggregation function.

        :param aggr_mf: aggregated membership function to defuzzify
        :return: crisp value for this MF
        """
        return self._defuzz_func[0](aggr_mf.in_values, aggr_mf.mf_values)
