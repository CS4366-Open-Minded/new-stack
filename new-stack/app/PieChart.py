import matplotlib.pyplot as plt

def sentimentChart(pos, neg, neu, id):
    plt.clf()
    plt.title("Sentiment Analysis")
    # The slices will be ordered and plotted counter-clockwise.
    labels = 'Positive', 'Negative', 'Neutral'
    sizes = [pos, neg, neu]
    colors = ['green', 'red', 'grey']
    explode = (0, 0, 0)  # only "explode" the nth slice (i.e. 'Neutral')

    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=90)
    # Set aspect ratio to be equal so that pie is drawn as a circle.
    plt.axis('equal')


    #plt.show()
    

    plt.savefig("app/static/app/img/"+str(id)+".png")


