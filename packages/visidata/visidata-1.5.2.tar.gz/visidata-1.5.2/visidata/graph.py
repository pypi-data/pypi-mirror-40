from visidata import *

option('color_graph_axis', 'bold', 'color for graph axis labels')

Sheet.addCommand('.', 'plot-column', 'vd.push(GraphSheet(sheet.name+"_graph", sheet, rows, keyCols, [cursorCol]))')
Sheet.addCommand('g.', 'plot-numerics', 'vd.push(GraphSheet(sheet.name+"_graph", sheet, rows, keyCols, numericCols(nonKeyVisibleCols)))')


def numericCols(cols):
    # isNumeric from describe.py
    return [c for c in cols if isNumeric(c)]


class InvertedCanvas(Canvas):
    def zoomTo(self, bbox):
        super().zoomTo(bbox)
        self.fixPoint(Point(self.plotviewBox.xmin, self.plotviewBox.ymax), bbox.xymin)

    def plotpixel(self, x, y, attr, row=None):
        y = self.plotviewBox.ymax-y
        self.pixels[y][x][attr].append(row)

    def scaleY(self, canvasY):
        'returns plotter y coordinate, with y-axis inverted'
        plotterY = super().scaleY(canvasY)
        return (self.plotviewBox.ymax-plotterY+4)

    def canvasH(self, plotterY):
        return (self.plotviewBox.ymax-plotterY)/self.yScaler

    @property
    def canvasMouse(self):
        p = super().canvasMouse
        p.y = self.visibleBox.ymin + (self.plotviewBox.ymax-self.plotterMouse.y)/self.yScaler
        return p

# swap directions of up/down
InvertedCanvas.addCommand(None, 'go-up', 'sheet.cursorBox.ymin += cursorBox.h')
InvertedCanvas.addCommand(None, 'go-down', 'sheet.cursorBox.ymin -= cursorBox.h')
InvertedCanvas.addCommand(None, 'go-top', 'sheet.cursorBox.ymin = visibleBox.ymax')
InvertedCanvas.addCommand(None, 'go-bottom', 'sheet.cursorBox.ymin = visibleBox.ymin')
InvertedCanvas.addCommand(None, 'next-page', 't=(visibleBox.ymax-visibleBox.ymin); sheet.cursorBox.ymin -= t; sheet.visibleBox.ymin -= t; refresh()')
InvertedCanvas.addCommand(None, 'prev-page', 't=(visibleBox.ymax-visibleBox.ymin); sheet.cursorBox.ymin += t; sheet.visibleBox.ymin += t; refresh()')

InvertedCanvas.addCommand(None, 'go-down-small', 'sheet.cursorBox.ymin -= canvasCharHeight')
InvertedCanvas.addCommand(None, 'go-up-small', 'sheet.cursorBox.ymin += canvasCharHeight')

InvertedCanvas.addCommand(None, 'resize-cursor-shorter', 'sheet.cursorBox.h -= canvasCharHeight')
InvertedCanvas.addCommand(None, 'resize-cursor-taller', 'sheet.cursorBox.h += canvasCharHeight')


# provides axis labels, legend
class GraphSheet(InvertedCanvas):
    def __init__(self, name, sheet, rows, xcols, ycols, **kwargs):
        super().__init__(name, sheet, sourceRows=rows, **kwargs)

        self.xcols = xcols
        self.ycols = [ycol for ycol in ycols if isNumeric(ycol)] or fail('%s is non-numeric' % '/'.join(yc.name for yc in ycols))

    @asyncthread
    def reload(self):
        nerrors = 0
        nplotted = 0

        self.reset()

        status('loading data points')
        catcols = [c for c in self.xcols if not isNumeric(c)]
        numcols = numericCols(self.xcols)
        for ycol in self.ycols:
            for rownum, row in enumerate(Progress(self.sourceRows, 'plotting')):  # rows being plotted from source
                try:
                    k = tuple(c.getValue(row) for c in catcols) if catcols else (ycol.name,)

                    # convert deliberately to float (to e.g. linearize date)
                    graph_x = float(numcols[0].type(numcols[0].getValue(row))) if numcols else rownum
                    graph_y = ycol.type(ycol.getValue(row))

                    attr = self.plotColor(k)
                    self.point(graph_x, graph_y, attr, row)
                    nplotted += 1
                except Exception:
                    nerrors += 1
                    if options.debug:
                        raise


        status('loaded %d points (%d errors)' % (nplotted, nerrors))

        self.setZoom(1.0)
        self.refresh()

    def setZoom(self, zoomlevel=None):
        super().setZoom(zoomlevel)
        self.createLabels()

    def add_y_axis_label(self, frac):
        amt = self.visibleBox.ymin + frac*self.visibleBox.h
        srccol = self.ycols[0]
        txt = srccol.format(srccol.type(amt))

        # plot y-axis labels on the far left of the canvas, but within the plotview height-wise
        attr = colors.color_graph_axis
        self.plotlabel(0, self.plotviewBox.ymin + (1.0-frac)*self.plotviewBox.h, txt, attr)

    def add_x_axis_label(self, frac):
        amt = self.visibleBox.xmin + frac*self.visibleBox.w
        txt = ','.join(xcol.format(xcol.type(amt)) for xcol in self.xcols if isNumeric(xcol))

        # plot x-axis labels below the plotviewBox.ymax, but within the plotview width-wise
        attr = colors.color_graph_axis
        xmin = self.plotviewBox.xmin + frac*self.plotviewBox.w
        if frac == 1.0:
            # shift rightmost label to be readable
            xmin -= max(len(txt)*2 - self.rightMarginPixels+1, 0)

        self.plotlabel(xmin, self.plotviewBox.ymax+4, txt, attr)

    def createLabels(self):
        self.gridlabels = []

        # y-axis
        self.add_y_axis_label(1.00)
        self.add_y_axis_label(0.75)
        self.add_y_axis_label(0.50)
        self.add_y_axis_label(0.25)
        self.add_y_axis_label(0.00)

        # x-axis
        self.add_x_axis_label(1.00)
        self.add_x_axis_label(0.75)
        self.add_x_axis_label(0.50)
        self.add_x_axis_label(0.25)
        self.add_x_axis_label(0.00)

        # TODO: if 0 line is within visible bounds, explicitly draw the axis
        # TODO: grid lines corresponding to axis labels

        xname = ','.join(xcol.name for xcol in self.xcols if isNumeric(xcol)) or 'row#'
        self.plotlabel(0, self.plotviewBox.ymax+4, '%*s»' % (int(self.leftMarginPixels/2-2), xname), colors.color_graph_axis)
