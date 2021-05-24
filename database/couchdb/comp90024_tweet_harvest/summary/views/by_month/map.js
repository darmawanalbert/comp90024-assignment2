function (doc) {
  var d = new Date(doc.created_at);
  var date = d.getDate();
  var month = d.getMonth() + 1;
  var year = d.getFullYear();
  
  city_dict = {'Australian Capital Territory': 'Canberra - Queanbeyan (Canberra Part)', 'Western Australia': 'Perth (WA)',
  'Blue Mountains National Park': 'Blue Mountains', 'New South Wales' : 'Sydney', 'Victoria': 'Melbourne', 'South Australia': 'Adelaide',
  'Northern Territory': 'Darwin', 'Tasmania': 'Hobart', 'Queensland': 'Brisbane', 'Canberra': 'Canberra - Queanbeyan (Canberra Part)'
  }
  if (doc.place.name in city_dict)
    place = city_dict[doc.place.name];
  else
    place = doc.place.name
  
  if (doc.truncated === true && doc.AURIN_loc_name)
    emit([year, month, doc.AURIN_loc_name.toLowerCase()], 1);
  else if (doc.truncated === false && doc.AURIN_loc_name)
    emit([year, month, doc.AURIN_loc_name.toLowerCase()], 1);
  else if (doc.truncated === true)
    emit([year, month, place.toLowerCase()], 1);
  else
    emit([year, month, place.toLowerCase()], 1);
}