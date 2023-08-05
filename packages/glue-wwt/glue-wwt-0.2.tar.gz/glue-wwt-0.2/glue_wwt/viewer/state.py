from __future__ import absolute_import, division, print_function

from glue.external.echo import (CallbackProperty, ListCallbackProperty,
                                SelectionCallbackProperty,
                                keep_in_sync, delay_callback)

from glue.core import Data, Subset
from glue.core.data_combo_helper import ComponentIDComboHelper
from glue.viewers.common.state import ViewerState, LayerState


class WWTDataViewerState(ViewerState):

    foreground = SelectionCallbackProperty(default_index=1)
    background = SelectionCallbackProperty(default_index=8)
    foreground_opacity = CallbackProperty(1)
    galactic = CallbackProperty(False)

    layers = ListCallbackProperty()

    # For now we need to include this here otherwise when loading files, the
    # imagery layers are only available asynchronously and the session loading
    # fails.
    imagery_layers = ListCallbackProperty()

    def __init__(self, **kwargs):
        super(WWTDataViewerState, self).__init__()
        self.add_callback('layers', self._sync_all_attributes)
        self.add_callback('imagery_layers', self._update_imagery_layers)
        self.update_from_dict(kwargs)

    def _update_imagery_layers(self, *args):
        WWTDataViewerState.foreground.set_choices(self, self.imagery_layers)
        WWTDataViewerState.background.set_choices(self, self.imagery_layers)

    def _update_priority(self, name):
        if name == 'layers':
            return 2
        elif name == 'imagery_layers':
            return 1
        else:
            return 0

    def _sync_attributes_single(self, reference, layer_state):
        with delay_callback(layer_state, 'ra_att', 'dec_att'):
            layer_state.ra_att = reference.ra_att
            layer_state.dec_att = reference.dec_att

    def _sync_all_attributes(self, layers=None, reference=None):

        # Make sure attributes are in sync between datasets and subsets

        if reference is None:
            data_layers = [layer for layer in self.layers if isinstance(layer, Data)]
            subset_layers = [layer for layer in self.layers if isinstance(layer, Subset)]
            for data_layer in data_layers:
                for subset_layer in subset_layers:
                    self._sync_attributes_single(data_layer, subset_layer)
        elif isinstance(reference.layer, Data):
            reference_data = reference.layer
            for layer_state in self.layers:
                if isinstance(layer_state.layer, Subset) and layer_state.layer.data is reference.layer:
                    self._sync_attributes_single(reference, layer_state)
        elif isinstance(reference.layer, Subset):
            reference_data = reference.layer.data
            for layer_state in self.layers:
                if isinstance(layer_state.layer, Data) and layer_state.layer is reference_data:
                    self._sync_attributes_single(reference, layer_state)
                elif isinstance(layer_state.layer, Subset) and layer_state.layer.data is reference_data:
                    self._sync_attributes_single(reference, layer_state)


class WWTLayerState(LayerState):

    layer = CallbackProperty()
    ra_att = SelectionCallbackProperty(default_index=0)
    dec_att = SelectionCallbackProperty(default_index=1)
    color = CallbackProperty()
    size = CallbackProperty()
    alpha = CallbackProperty()
    zorder = CallbackProperty(0)
    visible = CallbackProperty(True)

    def __init__(self, viewer_state=None, **kwargs):

        super(WWTLayerState, self).__init__()

        self.viewer_state = viewer_state

        self.ra_att_helper = ComponentIDComboHelper(self, 'ra_att',
                                                    numeric=True,
                                                    categorical=False,
                                                    world_coord=True,
                                                    pixel_coord=False)
        self.dec_att_helper = ComponentIDComboHelper(self, 'dec_att',
                                                     numeric=True,
                                                     categorical=False,
                                                     world_coord=True,
                                                     pixel_coord=False)

        self.add_callback('layer', self._layer_changed)

        self.update_from_dict(kwargs)

        if isinstance(self.layer, Subset) and self.viewer_state is not None:
            for layer_state in self.viewer_state.layers:
                if self.layer.data is layer_state.layer:
                    self.viewer_state._sync_attributes_single(layer_state, self)
                    break

        self.add_callback('ra_att', self._att_changed)
        self.add_callback('dec_att', self._att_changed)

        self.color = self.layer.style.color
        self.alpha = self.layer.style.alpha
        self.size = self.layer.style.markersize

        self._sync_color = keep_in_sync(self, 'color', self.layer.style, 'color')
        self._sync_alpha = keep_in_sync(self, 'alpha', self.layer.style, 'alpha')
        self._sync_size = keep_in_sync(self, 'size', self.layer.style, 'markersize')

    def _update_priority(self, name):
        if name == 'layer':
            return 1
        else:
            return 0

    def _layer_changed(self, layer):
        self.ra_att_helper.set_multiple_data([self.layer])
        self.dec_att_helper.set_multiple_data([self.layer])

    def _att_changed(self, *args):
        self.viewer_state._sync_all_attributes(reference=self)
