import matplotlib_terminal
import matplotlib.pyplot as plt
# Or in short:
# from matplotlib_terminal import plt


plt.plot([0, 1], [0, 1])
plt.plot([1, 0], [0, 1], lw=3)
plt.scatter([0], [.5])

plt.show()
plt.show('gamma') # Use RendererGamma-fast/noblock from img2unicode renderer
plt.show('block') # Use Renderer-fast/block from img2unicode 
plt.show('braille') # Use RendererGamma-fast/braille from img2unicode renderer
plt.close()