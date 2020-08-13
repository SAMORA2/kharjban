import matplotlib.pyplot as plt

from src.db.db_operations import visualize_asset


def show_plot(id):
    my_plot = visualize_asset(id)[0]
    category = [x for x in visualize_asset(id)[1]]
    if my_plot:
        try:

            length = len(my_plot)
            middle_index = length // 2
            x = my_plot[middle_index:]
            y = my_plot[:middle_index]

            plt.plot(x, y, '--bD')
            labels = [f'({i+1}) {{{category[i]}}}  {x} Rial' for i, x in enumerate(y)]
            for label, x_axis, y_axis in zip(labels, x, y):
                plt.annotate(label, xy=(x_axis, y_axis),
                             bbox=dict(boxstyle='round,pad=0.4',
                                       fc='yellow',
                                       alpha=2)),

            plt.title('Payment records')
            plt.show()
            return True
        except:
            return False
    else:
        print('\nNothing Found ! (NO PAYMENT)\n')
