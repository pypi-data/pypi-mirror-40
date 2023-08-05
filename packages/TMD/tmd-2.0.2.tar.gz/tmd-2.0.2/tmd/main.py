import matplotlib.pyplot as plt
import matplotlib.cm as cmx
import tmd
import view
import click
import numpy as np

@click.group()
def cli():
    '''A tool for morphology cut plane management'''


@cli.command(short_help='Compute a cut plane')
@click.argument('folder1', type=str, required=True)
@click.argument('folder2', type=str, required=True)
def distance(folder1, folder2):
    pop1 = tmd.io.load_population(folder1)
    pop2 = tmd.io.load_population(folder2)

    phs1 = [tmd.methods.get_ph_neuron(n, neurite_type='basal') for n in pop1.neurons]
    phs2 = [tmd.methods.get_ph_neuron(n, neurite_type='basal') for n in pop2.neurons]

    # Normalize the limits
    xlims, ylims = tmd.analysis.define_limits(phs1 + phs2)
    # Create average images for populations
    imgs1 = [tmd.analysis.persistence_image_data(p, xlims=xlims, ylims=ylims) for p in phs1]
    IMG1 = tmd.analysis.average_image(phs1, xlims=xlims, ylims=ylims)
    imgs2 = [tmd.analysis.persistence_image_data(p, xlims=xlims, ylims=ylims) for p in phs2]
    IMG2 = tmd.analysis.average_image(phs2, xlims=xlims, ylims=ylims)

    cmaps = plt.get_cmap('jet')
    # You can plot the images if you want to create pretty figures
    average_figure1 = view.plot.plot_img_basic(IMG1, title='', xlims=xlims, ylims=ylims, cmap=cmaps)
    average_figure2 = view.plot.plot_img_basic(IMG2, title='', xlims=xlims, ylims=ylims, cmap=cmaps)

    # Create the diffence between the two images
    DIMG = tmd.analysis.img_diff_data(IMG1, IMG2) # subtracts IMG2 from IMG1 so anything red IMG1 has more of it and anything blue IMG2 has more of it - or that's how it is supposed to be :)

    # Plot the difference between them
    diff_image = view.plot.plot_img_basic(DIMG, vmin=-1.0, vmax=1.0) # vmin, vmax important to see changes
    # Quantify the absolute distance between the two averages
    dist = np.sum(np.abs(DIMG))
    plt.show()
