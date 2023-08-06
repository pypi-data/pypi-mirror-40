# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Chart(Component):
    """A Chart component.


Keyword arguments:
- id (string; optional): The ID of this component, used to identify dash components
in callbacks. The ID needs to be unique across all of the
components in an app.
- style (dict; optional): Defines CSS styles which will override styles previously set.
- className (string; optional): Often used with CSS to style elements with common properties.
- height (string | number; optional)
- width (string | number; optional)
- graphID (string; optional)
- chartType (a value equal to: 'AnnotationChart', 'AreaChart', 'BarChart', 'BubbleChart', 'Calendar', 'CandlestickChart', 'ColumnChart', 'ComboChart', 'DiffChart', 'DonutChart', 'Gantt', 'Gauge', 'GeoChart', 'Histogram', 'LineChart', 'Line', 'Bar', 'Map', 'OrgChart', 'PieChart', 'Sankey', 'ScatterChart', 'SteppedAreaChart', 'Table', 'Timeline', 'TreeMap', 'WaterfallChart', 'WordTree'; optional)
- options (dict; optional)
- data (list | dict; optional)
- mapsApiKey (string; optional)

Available events: """
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, style=Component.UNDEFINED, className=Component.UNDEFINED, height=Component.UNDEFINED, width=Component.UNDEFINED, graphID=Component.UNDEFINED, chartType=Component.UNDEFINED, options=Component.UNDEFINED, data=Component.UNDEFINED, mapsApiKey=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'style', 'className', 'height', 'width', 'graphID', 'chartType', 'options', 'data', 'mapsApiKey']
        self._type = 'Chart'
        self._namespace = 'dash_google_charts/_components'
        self._valid_wildcard_attributes =            []
        self.available_events = []
        self.available_properties = ['id', 'style', 'className', 'height', 'width', 'graphID', 'chartType', 'options', 'data', 'mapsApiKey']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Chart, self).__init__(**args)

    def __repr__(self):
        if(any(getattr(self, c, None) is not None
               for c in self._prop_names
               if c is not self._prop_names[0])
           or any(getattr(self, c, None) is not None
                  for c in self.__dict__.keys()
                  if any(c.startswith(wc_attr)
                  for wc_attr in self._valid_wildcard_attributes))):
            props_string = ', '.join([c+'='+repr(getattr(self, c, None))
                                      for c in self._prop_names
                                      if getattr(self, c, None) is not None])
            wilds_string = ', '.join([c+'='+repr(getattr(self, c, None))
                                      for c in self.__dict__.keys()
                                      if any([c.startswith(wc_attr)
                                      for wc_attr in
                                      self._valid_wildcard_attributes])])
            return ('Chart(' + props_string +
                   (', ' + wilds_string if wilds_string != '' else '') + ')')
        else:
            return (
                'Chart(' +
                repr(getattr(self, self._prop_names[0], None)) + ')')
