// This file is a mini-library that translates JSON messages into actions
// on the WWT side. The reason for having this in its own file is that
// we can then use it for both the Jupyter widget and other front-ends such
// as the Qt one.

function wwt_apply_json_message(wwt, msg) {

  if (!wwt.hasOwnProperty('annotations')) {
    wwt.annotations = {};
    wwt.layers = {};
  }

  switch(msg['event']) {

    case 'clear_annotations':
      return wwt.clearAnnotations();
      break;

    case 'get_dec':
      return wwt.getDec();
      break;

    case 'get_ra':
      return wwt.getRA();
      break;

    case 'load_tour':
      wwt.loadTour(msg['url']);
      break;

    case 'resume_tour':
      wwt.playTour();
      break;

    case 'pause_tour':
      wwt.stopTour();
      break;

    case 'resume_time':
      wwtlib.SpaceTimeController.set_syncToClock(true);
      wwtlib.SpaceTimeController.set_timeRate(msg['rate']);
      break;

    case 'pause_time':
      wwtlib.SpaceTimeController.set_syncToClock(false);
      break;

    case 'load_image_collection':
      wwt.loadImageCollection(msg['url']);
      break;

    case 'set_foreground_by_name':
      wwt.setForegroundImageByName(msg['name']);
      break;

    case 'set_background_by_name':
      wwt.setBackgroundImageByName(msg['name']);
      break;

    case 'set_foreground_opacity':
      wwt.setForegroundOpacity(msg['value']);
      break;

    case 'center_on_coordinates':
      wwt.gotoRaDecZoom(msg['ra'], msg['dec'], msg['fov'], msg['instant']);
      break;

    case 'load_fits':
      wwt.loadFits(msg['url']);
      break;

    case 'setting_set':
      var name = msg['setting'];
      wwt.settings["set_" + name](msg['value']);
      break;

    case 'annotation_create':

      switch(msg['shape']) {
        case 'circle':
          // TODO: check if ID already exists
          circle = wwt.createCircle();
          circle.set_id(msg['id']);
          circle.set_skyRelative(true);
          circle.setCenter(wwt.getRA() * 15, wwt.getDec());
          wwt.addAnnotation(circle);
          wwt.annotations[msg['id']] = circle;
          break;

        case 'polygon':
          // same TODO as above
          polygon = wwt.createPolygon();
          polygon.set_id(msg['id']);
          wwt.addAnnotation(polygon);
          wwt.annotations[msg['id']] = polygon;
          break;

        case 'line':
          // same TODO as above
          line = wwt.createPolyLine();
          line.set_id(msg['id']);
          wwt.addAnnotation(line);
          wwt.annotations[msg['id']] = line;
          break;
      }
      break;

    case 'annotation_set':

      var name = msg['setting'];
      // TODO: nice error message if annotation doesn't exist
      annotation = wwt.annotations[msg['id']];
      annotation["set_" + name](msg['value']);
      break;

    case 'remove_annotation':

      var name = msg["setting"];
      // TODO: nice error message if annotation doesn't exist
      shape = wwt.annotations[msg['id']];
      wwt.removeAnnotation(shape);
      break;

    case 'circle_set_center':

      var name = msg["setting"];
      // TODO: nice error message if annotation doesn't exist
      circle = wwt.annotations[msg['id']];
      circle.setCenter(msg['ra'], msg['dec']);
      break;

    case 'polygon_add_point':

      var name = msg["setting"];
      // same TODO as above
      polygon = wwt.annotations[msg['id']];
      polygon.addPoint(msg['ra'], msg['dec']);
      break;

    case 'line_add_point':

      var name = msg["setting"];
      // same TODO as above
      line = wwt.annotations[msg['id']];
      line.addPoint(msg['ra'], msg['dec']);
      break;

    case 'set_datetime':

      var date = new Date(msg['year'], msg['month'], msg['day'],
                          msg['hour'], msg['minute'], msg['second'],
                          msg['millisecond']);

      stc = wwtlib.SpaceTimeController;
      stc.set_timeRate(1);
      stc.set_now(date);
      break;

    case 'set_viewer_mode':
      // We need to set both the backround and foreground layers
      // otherwise when changing to planet view, there are weird
      // artifacts due to the fact one of the layes is the sky.
      wwt.setBackgroundImageByName(msg['mode']);
      wwt.setForegroundImageByName(msg['mode']);
      break;

    case 'track_object':
      wwtlib.WWTControl.singleton.renderContext.set_solarSystemTrack(msg['code']);
      break;

    case 'table_layer_create':

      // Decode table from base64
      csv = atob(msg['table'])

      // Get reference frame
      frame = msg['frame']

      layer = wwtlib.LayerManager.createSpreadsheetLayer(frame, "PyWWT Layer", csv);
      layer.set_referenceFrame(frame);

      // FIXME: for now, this doesn't have any effect because WWT should add a 180
      // degree offset but it doesn't - see
      // https://github.com/WorldWideTelescope/wwt-web-client/pull/182 for a
      // possible fix.
      if (frame == 'Sky') {
        layer.set_astronomical(true);
      }

      layer.set_altUnit(1);

      wwt.layers[msg['id']] = layer;
      break;

    case 'table_layer_update':

      var layer = wwt.layers[msg['id']];

      // Decode table from base64
      csv = atob(msg['table']);

      layer.loadFromString(csv, true, true, true, false)

      break;

    case 'table_layer_set':

      var layer = wwt.layers[msg['id']];
      var name = msg['setting'];

      //if (name.includes('Column')) { // compatability issues?
      if (name.indexOf('Column') >= 0) {
        value = layer.get__table().header.indexOf(msg['value']);
      } else if(name == 'color') {
        value = wwtlib.Color.fromHex(msg['value']);
      } else if(name == 'altUnit') {
        value = wwtlib.AltUnits[msg['value']];
      } else if(name == 'raUnits') {
        value = wwtlib.RAUnits[msg['value']];
      } else if(name == 'altType') {
        value = wwtlib.AltTypes[msg['value']];
      } else {
        value = msg['value']
      }

      layer["set_" + name](value);

      // FIXME: workaround for the fact that at the moment, WWT appears
      // to only refresh if the color is changed. So we change to black then
      // back.
      if (name != 'color') {
        color = layer.get_color();
        layer.set_color(wwtlib.Color.fromHex('#000000'));
        layer.set_color(color);
      }

      break;

    case 'table_layer_remove':

      var layer = wwt.layers[msg['id']];
      wwtlib.LayerManager.deleteLayerByID(layer.id, true, true);
      break;

  }

}

// We need to do this so that wwt_apply_json_message is available as a global
// function in the Jupyter widgets code.
window.wwt_apply_json_message = wwt_apply_json_message;
