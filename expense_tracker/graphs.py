import matplotlib
matplotlib.use('Agg')
# First two lines are to prevent errors when running matplotlib on a Django server
import matplotlib.pyplot as plt
import numpy as np
from django.db.models import Sum
# io provides an in-memory file-like object
from io import BytesIO
import urllib, base64
import emoji

from .models import Expense, Category

# Global values for all graphs
CHART_COLORS = [
            "#84ACFA",
            "#83BDF7",
            "#8BCBFC",
            "#7CD7F7",
            "#90E6FC",
            "#A8EEFF",
]
FONT_SIZE = 14.5


def get_chart_data(request, mon_exp_sum, year, month) -> list[list]:
    spent_per_category: dict = {}
    all_categories = Category.objects.all()
    # For each category aggregate the sum spent
    for category in all_categories:
        spent_per_category[str(category)] = Expense.objects.filter(date__year=year, date__month=month).filter(category=category).filter(created_by=request.user.id).aggregate(Sum('amount'))['amount__sum'] or 0
    spent_per_category['Monthly bills'] = mon_exp_sum
    # Make sure items with None category are included in the piechart
    spent_per_category['No category'] = Expense.objects.filter(date__year=year, date__month=month).filter(created_by=request.user.id).filter(category=None).aggregate(Sum('amount'))['amount__sum'] or 0
    # Make a list of tuples of all non 0 values, then sort them based on the value
    spent_per_category_non_null: list[tuple] = [(key, spent_per_category[key]) for key in spent_per_category.keys() if spent_per_category[key] > 0]
    spent_per_category_sorted: list[tuple] = sorted(spent_per_category_non_null, key=lambda x: x[1], reverse=True)
    # Get a list of values from the tuples [1] index, and labels from [0]
    money_values: np.array = np.array([tup[1] for tup in spent_per_category_sorted])
    category_labels: list[str] = [tup[0] for tup in spent_per_category_sorted]
    # Remove emoji to prevent problems with matplotlib labels
    category_labels = list(map(lambda label: emoji.replace_emoji(label, replace=''), category_labels))
    return [category_labels, money_values]


def pie_chart(category_labels, money_values) -> bytes:
    # make a correct length list of zeroes with a 0.2 at index [0]
    explode: list[float | int] = [0] * (len(money_values)-1)
    explode.insert(0, 0.2)
    plt.pie(
        money_values, 
        labels=category_labels,
        explode=explode, 
        shadow=True, 
        labeldistance=0.7,
        colors=CHART_COLORS,
        textprops={
            'fontsize': FONT_SIZE
        },
        wedgeprops={
            'edgecolor': CHART_COLORS[0],
            'linewidth': 1,
            'linestyle': 'solid',
            'antialiased': True,
        }
    )

    # Instantiate a new 'file-like object' in memory, then save the figure to it
    buf = BytesIO()
    plt.tight_layout()
    # Save to buffer
    plt.savefig(buf, format='png', transparent=True)
    buf.seek(0)
    # Encode
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    plt.close()
    return uri


def bar_chart(category_labels, money_values, currency) -> bytes:
    fig, ax = plt.subplots(figsize =(6.4, 4.8))
    # Use a horizontal bar plot
    ax.barh(category_labels, money_values, color=CHART_COLORS, linewidth=1, linestyle='solid', edgecolor=CHART_COLORS[0])
    # Remove spines
    for i in ['top', 'bottom', 'left', 'right']:
        ax.spines[i].set_visible(False)
    # Remove Ticks
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')
    # Add padding between axes and labels
    ax.xaxis.set_tick_params(pad = 5)
    ax.yaxis.set_tick_params(pad = 10)
    plt.xticks(fontsize=FONT_SIZE)
    plt.yticks(fontsize=FONT_SIZE)
    # Add x, y gridlines
    ax.grid(b = True, color ='black', linestyle ='-', linewidth = 0.5, alpha = 0.3)
    ax.set_axisbelow(True)
    # Show highest values first
    ax.invert_yaxis()
    # Add value labels to the midway point
    for i in ax.patches:
        # if bar is small use custom positioning, else center label at 50%.
        largest_bar_width = ax.patches[0].get_width()
        is_small_bar = (i.get_width() * 4) < largest_bar_width
        label_align = 'center' if not is_small_bar else 'left'
        label_x = (i.get_width() * 0.5) if not is_small_bar else (largest_bar_width*0.02)
        plt.text(label_x, i.get_y()+0.5,
            str(currency) + " " + f"{round((i.get_width()), 2):,.2f}",
            fontsize = FONT_SIZE, color ='black', ha=label_align)

    # Instantiate a new 'file-like object' in memory, then save the figure to it
    buf = BytesIO()
    plt.tight_layout()
    # Save to buffer
    plt.savefig(buf, format='png', transparent=True)
    buf.seek(0)
    # Encode
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    plt.close()
    return uri
