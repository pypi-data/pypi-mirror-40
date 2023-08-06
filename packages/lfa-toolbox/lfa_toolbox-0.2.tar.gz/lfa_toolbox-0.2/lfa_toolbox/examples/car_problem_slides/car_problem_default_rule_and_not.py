from lfa_toolbox.core.fis.fis import AND_min, MIN
from lfa_toolbox.core.fis.singleton_fis import SingletonFIS
from lfa_toolbox.core.lv.linguistic_variable import LinguisticVariable
from lfa_toolbox.core.mf.lin_piece_wise_mf import LinPWMF
from lfa_toolbox.core.mf.singleton_mf import SingletonMF
from lfa_toolbox.core.rules.default_fuzzy_rule import DefaultFuzzyRule
from lfa_toolbox.core.rules.fuzzy_rule import FuzzyRule
from lfa_toolbox.core.rules.fuzzy_rule_element import Antecedent, Consequent
from lfa_toolbox.view.fis_surface import show_surface


def car_accel_problem():
    car_speed = LinguisticVariable(
        name="speed",
        ling_values_dict={
            "slow": LinPWMF([-0.2, 1], [0, 0]),
            "ok": LinPWMF([-0.2, 0], [0, 1], [0.15, 0]),
            "fast": LinPWMF([0, 0], [0.15, 1], [1, 1], [2, 0]),
        },
    )

    car_acc = LinguisticVariable(
        name="speed_change",
        ling_values_dict={
            "slowing": LinPWMF([-0.3, 1], [0, 0]),
            "constant": LinPWMF([-0.3, 0], [0, 1], [0.3, 0]),
            "rising": LinPWMF([0, 0], [0.3, 1]),
        },
    )

    car_action = LinguisticVariable(
        name="action",
        ling_values_dict={
            "release": SingletonMF(-1),
            "nothing": SingletonMF(0),
            "push": SingletonMF(1),
        },
    )

    car_rules = [
        FuzzyRule(
            ant_act_func=AND_min,
            ants=[
                Antecedent(car_speed, "fast"),
                Antecedent(car_acc, "slowing", is_not=True),
            ],
            cons=[Consequent(car_action, "release")],
            impl_func=MIN,
        ),
        FuzzyRule(
            ant_act_func=AND_min,
            ants=[
                Antecedent(car_speed, "slow"),
                Antecedent(car_acc, "rising", is_not=True),
            ],
            cons=[Consequent(car_action, "push")],
            impl_func=MIN,
        ),
    ]

    default_rule = DefaultFuzzyRule(
        cons=[Consequent(car_action, "nothing")], impl_func=MIN
    )

    fis = SingletonFIS(rules=car_rules, default_rule=default_rule)
    input_values = {"speed": 1, "speed_change": 0.22}
    fis.predict(input_values)

    # fisv = FISViewer(fis)
    # # # # fisv.save("/tmp/out.png")
    # fisv.show()

    return fis


if __name__ == "__main__":
    fis = car_accel_problem()
    show_surface(
        fis,
        x_label="speed",
        y_label="speed_change",
        z_label="action",
        n_pts=15,
        x_range=(-1, 1),
        y_range=(-1, 1),
        z_range=(-1, 1),
    )
