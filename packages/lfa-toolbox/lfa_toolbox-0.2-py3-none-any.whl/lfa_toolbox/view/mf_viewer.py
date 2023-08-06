from matplotlib.ticker import MaxNLocator

from lfa_toolbox.core.mf.free_shape_mf import FreeShapeMF
from lfa_toolbox.core.mf.lin_piece_wise_mf import LinPWMF
from lfa_toolbox.core.mf.singleton_mf import SingletonMF
from lfa_toolbox.view.viewer import Viewer


class MembershipFunctionViewer(Viewer):
    def __init__(
            self, mf: FreeShapeMF, label="", ax=None, color=None, alpha=None,
            draw_not=False
    ):
        super(MembershipFunctionViewer, self).__init__(ax)
        self._mf = mf
        self._label = label
        self._color = color
        self._alpha = alpha
        self._draw_not = draw_not

        # draw SingletonMF horizontal line to be more visible
        if isinstance(self._mf, SingletonMF):
            in_val = self._mf.in_values[0]
            mf_val = self._mf.mf_values[0]
            self._ax.plot([in_val, in_val], [0, mf_val], "r", c=self._color)

        self.get_plot(self._ax)

    def fuzzify(self, in_value):
        fuzzified = self._mf.fuzzify(in_value)

        self._ax.plot([in_value], [fuzzified], "ro")
        self._ax.plot([in_value, in_value], [0, fuzzified], "r")

    def get_plot(self, ax):
        xs, ys = self._mf.in_values, self._mf.mf_values

        if self._draw_not:
            ys = 1.0 - ys

        ax.scatter(xs, ys, s=5, label=self._label, c=self._color,
                   alpha=self._alpha)
        ax.plot(xs, ys, c=self._color, alpha=self._alpha)
        ax.set_xlabel(self._label, fontsize="small")

        ax.xaxis.set_major_locator(MaxNLocator(5))
        ax.yaxis.set_major_locator(MaxNLocator(5))
        return ax


if __name__ == "__main__":
    from matplotlib import pyplot as plt

    fig, ax = plt.subplots()

    mf = LinPWMF([17, 0], [20, 1], [26, 1], [29, 0])
    mfv = MembershipFunctionViewer(mf, ax=ax, label="N/A")
    mfv.fuzzify(22.5)

    plt.legend()
    plt.show()
