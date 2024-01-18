#
#   Allows to generate the graphs and images
#


##################################################################################################################################
#
#   IMPORTS
#
##################################################################################################################################

#
import matplotlib.pyplot as pdfplt
import plotext as txtplt
import logging
# * hide mathlotlib warnings
logging.getLogger('matplotlib.font_manager').disabled = True

##################################################################################################################################
#
#   FUNCTIONS
#
##################################################################################################################################


def drawPDFLineGraph(x_values, y_values, x_label, y_label, title, filename):
    pdfplt.plot(x_values, y_values)
    pdfplt.title(title)
    pdfplt.xlabel(x_label)
    pdfplt.ylabel(y_label)
    pdfplt.grid(True)
    pdfplt.savefig(filename+".pdf")
    pdfplt.clf()
    return

# ----------------------------------------------------------------


def drawPDFBarGraph(x_values, y_values, x_label, y_label, title, filename):
    pdfplt.bar(x_values, y_values, color='blue', width=0.3)
    pdfplt.title(title)
    pdfplt.xlabel(x_label)
    pdfplt.ylabel(y_label)
    pdfplt.grid(True)
    pdfplt.savefig(filename+".pdf")
    pdfplt.clf()
    return

# ----------------------------------------------------------------


def drawPDFPointsGraph(x_values, y_values, x_label, y_label, title, filename):
    pdfplt.scatter(x_values, y_values, color='blue')
    pdfplt.title(title)
    pdfplt.xlabel(x_label)
    pdfplt.ylabel(y_label)
    pdfplt.grid(True)
    pdfplt.savefig(filename+".pdf")
    pdfplt.clf()
    return

# ----------------------------------------------------------------


def drawTXTLineGraph(x_values, y_values, x_label, y_label, title, filename):
    txtplt.plot(x_values, y_values)
    txtplt.plot_size(100, 50)
    txtplt.title(title)
    txtplt.xlabel(x_label)
    txtplt.ylabel(y_label)
    txtplt.grid(True, True)
    txtplt.build()
    txtplt.save_fig(filename+".txt")
    txtplt.cld()
    return

# ----------------------------------------------------------------


def drawTXT2LineGraph(x_values, y_values, label, x_values_2, y_values_2, label_2, x_label, y_label, title, filename):
    txtplt.plot(x_values, y_values, label=label, marker="fhd")
    txtplt.plot(x_values_2, y_values_2, label=label_2,)
    txtplt.plot_size(100, 50)
    txtplt.title(title)
    txtplt.xlabel(x_label)
    txtplt.ylabel(y_label)
    txtplt.grid(True, True)
    txtplt.build()
    txtplt.save_fig(filename+".txt")
    txtplt.cld()
    return

# ----------------------------------------------------------------


def drawTXTBarGraph(x_values, y_values, x_label, y_label, title, filename):
    txtplt.bar(x_values, y_values)
    txtplt.plot_size(100, 50)
    txtplt.title(title)
    txtplt.xlabel(x_label)
    txtplt.ylabel(y_label)
    txtplt.save_fig(filename+".txt")
    txtplt.build()
    return

# ----------------------------------------------------------------


def drawTXTPointsGraph(x_values, y_values, x_label, y_label, title, filename):
    txtplt.scatter(x_values, y_values)
    txtplt.plot_size(100, 50)
    txtplt.title(title)
    txtplt.xlabel(x_label)
    txtplt.ylabel(y_label)
    txtplt.save_fig(filename+".txt")
    txtplt.build()
    return

# ----------------------------------------------------------------


def writeTXTFile(lines, file_path):
    file = open(file_path, "w")
    file.writelines(lines)
    file.close()

# ----------------------------------------------------------------


def writeJSONFile(json_object, file_path):
    file = open(file_path, "w")
    file.write(json_object)
    file.close()
