import numpy as np
try:
    import matplotlib.pyplot as plt
    matplotlib_available = True
except RuntimeError:
    matplotlib_available = False


def Spectrum(object):
    """A mass spectrum."""
    def __init__(self, mz=[], i=[]):
        """Initialize the spectrum.
        
        Args:
            mz (iterable): Recorded mass over charge ratios.
            i (iterable): Recorded intensities.
        """
        self.mz = np.array(mz)
        self.i = np.array(intensity)
    
    def read(self, path):
        pass

    def write(self, path):
        pass

    def plot(self,
             plt_style='dark_background',
             peak_color='greenyellow',
             show=True):
        """Make a simple visualization of a mass spectrum.
        
        Args:
            plt_style (str): The style of the matplotlib visualization. Check https://matplotlib.org/gallery/style_sheets/style_sheets_reference.html
            peak_color (str): A color to visualize the peaks.
            show (bool): Show the figure, or just add it to the canvas.
        """
        if matplotlib_available:
            plt.style.use(plt_style)
            plt.vlines(x=self.mz,
                       ymin=[0],
                       ymax=self.i,
                       colors=peak_color)
            if show:
                plt.show()
        else:
            print("Install matplotlib to use this function.")



