from ipywidgets import widgets
from .floatview import Floatview
from .plotly.scatter import GlueScatterPlotly
from .plotly.scatter3d import GlueScatter3DPlotly
from .plotly.contour import GlueContourPlotly
from .plotly.table import GlueTablePlotly
from .plotly.histogram import GlueHistogramPlotly
from .plotly.parallelcoordinates import GlueParallelCoordinatesPlotly
from .plotly.errorbar import GlueErrorBarPlotly
from .plotly.polyfit import GluePolyFitPlotly
from .plotly.line import GlueLinePlotly
from .plotly.image import GlueImagePlotly
from glue import core as gcore

import itertools

class GlueManager:
    data = None
    scatter = []
    debug = None
    selection = []
    views = []    
    parent = None

    def __init__(self, data):
        self.scatter = []
        self.scatter3D = []
        self.tables = []
        self.data = data
        self.parent = None
        self.debug = widgets.Output()
        self.selection = []
        
    def setNewData(self, data):
        self.data = data

    def setParent(self, parent):    
        if isinstance(parent, GlueManagerWidget):
            self.parent = parent
        
    def newView(self, type="scatter", components=[], title="New View", **kwargs):
        only_subsets = kwargs.get('only_subsets', False)
        if (self.parent is not None):
            kwargs.setdefault('modal', self.parent.modal)
        if (self.debug is not None):
            kwargs.setdefault('debug', self.debug)
                
        gp = None
        if (type == "scatter"):
            if len(components) == 1:
                mdimensions = [[components[0],components[0]]]
            elif len(components) == 2:
                mdimensions = [[components[0],components[1]]]
            else:
                mdimensions = list(itertools.combinations(components, 2))
            for dimensions in mdimensions:
                mode = "tab-after"
                if (len(self.scatter) == 0):
                    mode = "split-bottom"
                    
                gp = GlueScatterPlotly(self.data, dimensions, title=title, **kwargs)
                self.scatter.append(gp);
                gp.setParent(self)

        elif (type == "errorbar"):
            if len(components) == 1:
                mdimensions = [[components[0],components[0]]]
            elif len(components) == 2:
                mdimensions = [[components[0],components[1]]]
            else:
                mdimensions = list(itertools.combinations(components, 2))
            for dimensions in mdimensions:
                mode = "tab-after"
                if (len(self.scatter) == 0):
                    mode = "split-bottom"                    
                gp = GlueErrorBarPlotly(self.data, dimensions, title=title, **kwargs)
                self.tables.append(gp);
                gp.setParent(self)
                
        elif (type == "composed_polyfit_2d" or type == "composed_polyfit_3d"):
            mode = "tab-after"                        
            degree = 2
            if (type == "composed_polyfit_3d"):
                degree = 3
            if (len(self.tables) == 0):
                mode = "split-right"               
            gp = GluePolyFitPlotly(self.data, components, degree, title=title, **kwargs)                
            self.tables.append(gp);
            gp.setParent(self)
            
        elif (type == "scatter3D"):
            if len(components) == 1:
                mdimensions = [[components[0],components[0],components[0]]]
            elif len(components) == 2:
                mdimensions = [[components[0],components[0],components[1]]]
            else:
                mdimensions = list(itertools.combinations(components, 3))
            for dimensions in mdimensions:
                mode = "tab-after"
                if (len(self.scatter3D) == 0):
                    mode = "split-right"
                gp = GlueScatter3DPlotly(self.data, dimensions, title=title, **kwargs)
                self.scatter3D.append(gp);
                gp.setParent(self)
                
        elif (type == "contour"):
            if len(components) == 1:
                mdimensions = [[components[0],components[0]]]
            elif len(components) == 2:
                mdimensions = [[components[0],components[1]]]
            else:
                mdimensions = list(itertools.combinations(components, 2))
            for dimensions in mdimensions:
                mode = "tab-after"
                if (len(self.scatter) == 0):
                    mode = "split-bottom"
                gp = GlueContourPlotly(self.data, dimensions, title=title, **kwargs)
                self.scatter.append(gp);
                gp.setParent(self)

                
        elif (type == "table"):
            mode = "tab-after"            
            if (len(self.tables) == 0):
                mode = "split-right"
                
            gp = GlueTablePlotly(self.data, components, title=title, **kwargs)
            self.tables.append(gp);
            gp.setParent(self)

        elif (type == "parallels"):
            mode = "tab-after"            
            if (len(self.scatter) == 0):
                mode = "split-bottom"                
            gp = GlueParallelCoordinatesPlotly(self.data, components, title=title, **kwargs)
            self.tables.append(gp);
            gp.setParent(self)

        elif (type == "histogram"):   
            for dimension in components:
                mode = "tab-after"            
                if (len(self.tables) == 0):
                    mode = "split-right"
                gp = GlueHistogramPlotly(self.data, [dimension], title=title, **kwargs)
                self.tables.append(gp);
                gp.setParent(self)
                
                
        elif (type == "composed_errorbar"):
            mode = "tab-after"
            if (len(self.scatter) == 0):
                mode = "split-bottom"                    
            gp = GlueErrorBarPlotly(self.data, components, title=title, **kwargs)
            self.tables.append(gp);
            gp.setParent(self)
                
        elif (type == "composed_scatter"):
            mode = "tab-after"            
            if (len(self.tables) == 0):
                mode = "split-right"               
            gp = GlueScatterPlotly(self.data, components, title=title, **kwargs)                
            self.tables.append(gp);
            gp.setParent(self)
            
        elif (type == "composed_errorbar"):
            mode = "tab-after"            
            if (len(self.tables) == 0):
                mode = "split-right"               
            gp = GlueScatterPlotly(self.data, components, title=title, **kwargs)                
            self.tables.append(gp);
            gp.setParent(self)            
            
                
        elif (type == "composed_lines"):
            mode = "tab-after"
            if (len(self.scatter) == 0):
                mode = "split-bottom"                    
            gp = GlueLinePlotly(self.data, components, title=title, **kwargs)
            self.tables.append(gp);
            gp.setParent(self)

        elif (type == "image"):
            if len(components) == 1:
                mdimensions = [[components[0],components[0],components[0]]]
            elif len(components) == 2:
                mdimensions = [[components[0],components[0],components[1]]]
            else:
                mdimensions = [[components[0],components[1],components[2]]]
                mode = "tab-after"
            if (len(self.scatter) == 0):
                mode = "split-bottom"                    
            gp = GlueImagePlotly(self.data, components, title=title, **kwargs)
            self.tables.append(gp);
            gp.setParent(self)

        #if gp is not None:
        #    self.views.append({'type':type,'components':components,'title':title, 'kwargs':kwargs })

        return gp

    
    def listPlots(self):    
        return ["scatter","composed_scatter","composed_errorbar","composed_lines","errorbar","scatter3D","contour","table","parallels", "histogram", "composed_polyfit_2d", "composed_polyfit_3d","image"]
            

    def printInDebug(self, var):
        if self.debug is not None:
            with self.debug:
                print (var);
                
    def updateSelection(self,ids):
        self.selection = ids
        for view in self.scatter3D:
            view.updateSelection(ids)
        for view in self.scatter:
            view.updateSelection(ids)
        for view in self.tables:
            view.updateSelection(ids)

    def updateTraces(self):
        for view in self.scatter3D:
            view.updateRender()
        for view in self.scatter:
            view.updateRender()
        for view in self.tables:
            view.updateRender()

    def createSubsetFromSelection(self, label = 'data'):
        if (len(self.selection) > 0):
            state = gcore.subset.ElementSubsetState(indices=self.selection)
            self.data.new_subset(state, label=label)
            self.updateTraces()
            if isinstance(self.parent, GlueManagerWidget):
                self.parent.updateSubsets()
        
        
    def deleteSubsetFromSelection(self, labels):
        for label in labels:
            value = next((i for i in self.data.subsets if i.label == label), None)
            if (value is not None):
                value.delete()
        self.updateTraces()                
        if isinstance(self.parent, GlueManagerWidget):
            self.parent.updateSubsets()                


class GlueManagerWidget(widgets.Tab):
    gluemanager = None
    subsets = None
    debug = None
    plots = None
    subsetsui = None
    modal = False
    def __init__(self, gluemanager, modal=False, label=None):
        widgets.Tab.__init__(self);
        if isinstance(gluemanager, GlueManager):
            self.gluemanager = gluemanager
        elif isinstance(gluemanager, gcore.Data):
            self.gluemanager = GlueManager(gluemanager)
        else:
            self.gluemanager = GlueManager(gcore.Data(**gluemanager))

        if (label is not None):
            self.gluemanager.data.label=label
        
        self.gluemanager.setParent(self)
        self.subsets = self.createSubsetsPanel()
        self.plots = self.createPlotsPanel()
        self.modal = modal
        self.debug = self.gluemanager.debug
        
        self.children = [self.plots, self.subsets, self.debug]
        self.set_title(0, 'Plots')
        self.set_title(1, 'Subsets')
        self.set_title(2, 'Debug')
        if (self.modal):
            modal_window = Floatview(title = "GMW("+str(id(self))+")", mode = "split-top")  
            with modal_window:
                display(self)
        else:
            display(self)

    def createSubsetsPanel(self):
        self.subsetsui = widgets.SelectMultiple(
            options=[sset.label for sset in self.gluemanager.data.subsets],
            value=[],
            rows=4,
            disabled=False
        )
        self.subsetsui.layout = widgets.Layout(width='99%')

        bt = widgets.Button(
            description='Create new Subset.',
            disabled=False,
            button_style='', # 'success', 'info', 'warning', 'danger' or ''
            tooltip='createa new subset from current selection',
        )
        
        bt.layout = widgets.Layout(width='99%')

        tx = widgets.Text(
            value='',
            placeholder='new subset name',
            disabled=False
        )
        tx.layout = widgets.Layout(width='99%')

        bt.on_click(lambda e : GlueManagerWidget.createSubsetFromSelection(self, tx))

        dl = widgets.Button(
            description='remove selected Subsets',
            disabled=False,
            button_style='danger',
            tooltip='Removes active subsets from the data workspace',
        )
               
        dl.layout = widgets.Layout(width='99%')
        dl.on_click(lambda e : GlueManagerWidget.deleteSubsetFromSelection(self))


        sl = widgets.Button(
            description='Hide selected subsets',
            disabled=False,
            button_style='warning',
            tooltip='',
        )
        
        
        sl.layout = widgets.Layout(width='99%')

        vb = widgets.VBox([dl, sl])

        vb2 = widgets.VBox([tx, bt])

        hb1 = widgets.HBox([vb2,self.subsetsui,vb])


        vb3 = widgets.VBox([hb1])
        
        return vb3

    def createPlotsPanel(self):
        components = self.gluemanager.data.components
        pixel_component_ids = self.gluemanager.data.pixel_component_ids
        world_component_ids = self.gluemanager.data.world_component_ids
        
        v = []
        for k in components:
            if k not in world_component_ids: #k not in pixel_component_ids and
                kt = str(k)
                vv = widgets.ToggleButton(
                    value=False, tooltip=kt, description=kt
                )
                v.append(vv)

        tb = widgets.HBox(v)

        cr = widgets.Button(
            description='Create new visualization',
            disabled=False,
            button_style='',
            tooltip='',
        )

        views = self.gluemanager.listPlots()

        dd = widgets.Dropdown(
            options=views,
            value=views[0],
            disabled=False,
        )

        ss = widgets.Checkbox(
            value=False,
            description='Only subsets',
            disabled=False
        )

        tx = widgets.Text(
            value='',
            placeholder='New_Visualization',
            disabled=False
        )
        
        
        hb1 = widgets.HBox([dd,tx,ss,cr])
        vb1 = widgets.VBox([tb,hb1])
        
        from IPython.display import display
        cr.on_click(lambda e : GlueManagerWidget.createNewView(self,e, dd, tb.children, tx, ss))

        return vb1    
    def _repr_html_(self):
        return widgets.Tab._repr_html_(self)

    def createNewView(self,e,dd, tb, tx, ss):
        with self.debug:
            print("asdasd")
        list_comp = []
        for vv in tb:
            if vv.value == True:
                list_comp.append(vv.description)                        
        self.gluemanager.newView(dd.value, list_comp, tx.value, only_subsets=ss.value)
            
    def createSubsetFromSelection(self, tx):        
        self.gluemanager.createSubsetFromSelection(tx.value)

    def deleteSubsetFromSelection(self):
        self.gluemanager.deleteSubsetFromSelection(self.subsetsui.value)
        
    def updateSubsets(self):
        self.subsetsui.options = [sset.label for sset in self.gluemanager.data.subsets]
        